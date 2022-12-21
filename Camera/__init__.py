import time
import gc
from picamera import PiCamera
from datetime import datetime
from fractions import Fraction

class Camera:
    def __init__(self) -> None:
        framerate = Fraction(1, 6)
        resolution = (1024, 768)
        sensor_mode = 3
        self.camera = PiCamera(
            resolution =resolution,
            framerate = framerate,
            sensor_mode = sensor_mode
        )

    def configure(self, menu):
        self.camera.shutter_speed = int(float(menu[1]["options"][menu[1]["current-option"]]) * 1000000)
        self.camera.iso = int(menu[0]["options"][menu[0]["current-option"]])
        self.wait_time = float(menu[4]["options"][menu[4]["current-option"]])

    def capture(self):
        time.sleep(self.wait_time)
        now = datetime.now()
        filename = now.strftime("/tmp/%d_%m_%Y_%H_%M_%S.jpeg")
        self.camera.capture(filename)