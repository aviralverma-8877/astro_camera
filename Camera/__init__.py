import time
import gc
from picamera import PiCamera
from datetime import datetime
from fractions import Fraction

class Camera:
    def __init__(self, main_dir) -> None:
        self.main_dir = main_dir
        framerate = Fraction(1, 6)
        sensor_mode = 3
        self.camera = PiCamera(
            framerate = framerate,
            sensor_mode = sensor_mode
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

    def capture(self):
        time.sleep(self.wait_time)
        now = datetime.now()
        filename = now.strftime("/mnt/usb_share/%d_%m_%Y_%H_%M_%S.jpeg")
        if(self.image_type == "RAW"):
            self.camera.capture(filename, format='jpeg', bayer=True)
        else:
            self.camera.capture(filename, format='jpeg')