import time
import io
<<<<<<< HEAD
import cv2
import numpy as np
=======
>>>>>>> a19c7c96449840610dbd5a6d0c5c0f4912f5fafb
from picamera import PiCamera
from datetime import datetime
from fractions import Fraction
from threading import Condition
from PIL import Image, ImageDraw


class StreamingOutput(object):
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
        resolution = (
            int(menu[2]["options"][menu[2]["current-option"]].split(" x ")[0]),
            int(menu[2]["options"][menu[2]["current-option"]].split(" x ")[1])
        )
        shutter_speed = int(float(menu[1]["options"][menu[1]["current-option"]]) * 1000000)
        iso = int(menu[0]["options"][menu[0]["current-option"]])
        wait_time = float(menu[3]["options"][menu[3]["current-option"]])
        self.image_type = menu[4]["options"][menu[4]["current-option"]]
        framerate = Fraction(1,6)
        sensor_mode = 3
        self.camera = PiCamera()
        self.camera.framerate = framerate
        self.camera.sensor_mode = sensor_mode
        self.camera.resolution = resolution
        self.camera.shutter_speed = shutter_speed
        self.camera.iso = iso
        self.camera.exposure_mode = 'off'
        self.wait_time = wait_time

    def show_preview(self, height, width, disp, func, callback, cross, zoom, stop):
        output = StreamingOutput()
        #Uncomment the next line to change your Pi's Camera rotation (in degrees)
        framerate = 24
        self.camera = PiCamera()
        self.camera.framerate = framerate
        self.camera.rotation = 90
        self.camera.resolution = str(height)+"x"+str(width)
        self.camera.start_recording(output, format='mjpeg')
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                image = Image.open(output.buffer)
                if cross():
                    d = ImageDraw.Draw(image)
                    d.line((width/2,(height/2-10),width/2,(height/2+10)), fill=128)
                    d.line(((width/2-10),height/2,(width/2+10),height/2), fill=128)

                disp.LCD_ShowImage(image,0,0)
                if stop():
                    exit(0)
                if zoom():
                    self.camera.zoom = (0.4,0.4,0.2,0.2)
                else:
                    self.camera.zoom = (0,0,width,height)
        finally:
            self.camera.stop_recording()
            self.camera.close()
            callback([func])

    def capture(self):
        time.sleep(self.wait_time)
        now = datetime.now()
        filename = now.strftime("/mnt/usb_share/%d_%m_%Y_%H_%M_%S.jpg")
        if(self.image_type == "RAW"):
            self.camera.capture(filename, format='jpeg', bayer=True)
            with open(filename, "rb") as f:
                image_data = f.read()
            image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)
            raw_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            cv2.imwrite(filename.replace(".jpg","-b.jpg"), raw_image)
        else:
            self.camera.capture(filename, format='jpeg')
    def blank_method(self, param=[]):
        pass
