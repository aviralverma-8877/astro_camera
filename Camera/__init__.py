import time
import io
import cv2
import numpy as np
from picamera2.encoders import JpegEncoder
from picamera2 import Picamera2, Preview
from picamera2.outputs import FileOutput
from datetime import datetime
from fractions import Fraction
from threading import Condition
from PIL import Image, ImageDraw


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class Camera:
    def __init__(self, main_dir) -> None:
        self.main_dir = main_dir
        

    def configure(self, menu):
        wait_time = float(menu[3]["options"][menu[3]["current-option"]])
        self.image_type = menu[4]["options"][menu[4]["current-option"]]
        self.camera = Picamera2()
        modes = self.camera.sensor_modes
        if(self.image_type == "RAW"):
            mode = modes[1]
        else:
            mode = modes[0]
        config = self.camera.create_still_configuration(
            main={"size": mode['size']},
            raw={'format': mode['unpacked']},
            lores={"size": mode['size']})
        self.camera.configure(config)
        if(menu[0]["options"][menu[0]["current-option"]] not in ["Auto"]):
            shutter_speed = int(float(menu[1]["options"][menu[1]["current-option"]]) * 1000000)
            iso = int(menu[0]["options"][menu[0]["current-option"]])
            self.camera.set_controls(
                {
                    "AnalogueGain": int(iso)/100,
                    "ExposureTime": int(shutter_speed)
                })
        self.camera.start()
        self.wait_time = wait_time

    def show_preview(self, menu, height, width, disp, func, callback, cross, zoom, stop):
        output = StreamingOutput()
        encoder = JpegEncoder()
        #Uncomment the next line to change your Pi's Camera rotation (in degrees)
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_video_configuration(main={"size": (height, width)}))
        if(menu[0]["options"][menu[0]["current-option"]] not in ["Auto"]):
            iso = int(menu[0]["options"][menu[0]["current-option"]])
            self.camera.set_controls({
                    "AnalogueGain": int(iso)/100
                })
        self.camera.start_recording(encoder, FileOutput(output))
        try:
            zoomed = False
            crossed = False
            (w, h) = self.camera.camera_properties['PixelArraySize']
            x = int((w/2) - 512)
            y = int((h/2) - 512)
            while True:
                with output.condition:
                    output.condition.wait()
                image = Image.open(output.buffer)
                if cross():
                    if not crossed:
                        crossed = True
                    else:
                        crossed = False
                if crossed:
                    d = ImageDraw.Draw(image)
                    d.line((width/2,(height/2-10),width/2,(height/2+10)), fill=128)
                    d.line(((width/2-10),height/2,(width/2+10),height/2), fill=128)
                    crossed = True
                disp.LCD_ShowImage(image,0,0)
                if stop():
                    exit(0)
                if zoom():
                    if not zoomed:
                        self.camera.set_controls({"ScalerCrop": (x, y, 1024, 1024)})
                        zoomed = True
                    else:
                        self.camera.set_controls({"ScalerCrop": (0, 0, w, h)})
                        zoomed = False
                time.sleep(0.01)
        finally:
            self.camera.stop_recording()
            self.camera.close()
            callback([func])

    def capture(self):
        time.sleep(self.wait_time)
        now = datetime.now()
        filename = now.strftime("/mnt/usb_share/%d_%m_%Y_%H_%M_%S.jpg")
        self.camera.capture_file(filename)
    def blank_method(self, param=[]):
        pass
