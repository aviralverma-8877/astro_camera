import time
import io
from picamera import PiCamera
from datetime import datetime
from fractions import Fraction
from threading import Condition
from PIL import Image


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
        framerate = 60
        self.camera = PiCamera(
            framerate = framerate
        )

    def configure(self, menu):
        resolution = (
            int(menu[2]["options"][menu[2]["current-option"]].split(" x ")[0]),
            int(menu[2]["options"][menu[2]["current-option"]].split(" x ")[1])
        )
        shutter_speed = int(float(menu[1]["options"][menu[1]["current-option"]]) * 1000000)
        iso = int(menu[0]["options"][menu[0]["current-option"]])
        wait_time = float(menu[3]["options"][menu[3]["current-option"]])
        self.image_type = menu[4]["options"][menu[4]["current-option"]]


        print("resulution",resolution)
        print("shutter_speed",shutter_speed)
        print("wait_time",wait_time)
        print("Image Type", self.image_type)

        self.camera.resolution = resolution
        self.camera.shutter_speed = shutter_speed
        self.camera.iso = iso
        self.wait_time = wait_time

    def show_preview(self, height, width, disp, stop):
        output = StreamingOutput()
        #Uncomment the next line to change your Pi's Camera rotation (in degrees)
        self.camera.rotation = 90
        self.camera.resolution = str(height)+"x"+str(width)
        self.camera.start_recording(output, format='mjpeg')
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                image = Image.open(output.buffer)
                disp.LCD_ShowImage(image,0,0)
                if stop():
                    self.camera.stop_recording()
                    exit(0)
        finally:
            self.camera.stop_recording()

    def capture(self):
        time.sleep(self.wait_time)
        now = datetime.now()
        filename = now.strftime("/mnt/usb_share/%d_%m_%Y_%H_%M_%S.jpeg")
        if(self.image_type == "RAW"):
            self.camera.capture(filename, format='jpeg', bayer=True)
        else:
            self.camera.capture(filename, format='jpeg')