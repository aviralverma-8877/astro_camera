import RPi.GPIO as GPIO
import time
KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

class Buttons:
    def __init__(self, func) -> None:
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.func = func
        self.key_mapper = {
            "up":False,
            "left":False,
            "right":False,
            "down":False,
            "center":False,
            "key1":False,
            "key2":False,
            "key3":False
        }

    def gpio_cleanup(self):
        GPIO.cleanup()
        
    def up_released(self):
        self.func.action("up-r")
    def up_pressed(self):
        self.func.action("up")

    def left_released(self):
        self.func.action("left-r")
    def left_pressed(self):
        self.func.action("left")
        
    def right_released(self):
        self.func.action("right-r")
    def right_pressed(self):
        self.func.action("right")
    
    def down_released(self):
        self.func.action("down-r")
    def down_pressed(self):
        self.func.action("down")
        
    def center_released(self):
        self.func.action("center-r")
    def center_pressed(self):
        self.func.action("center")

    def key1_released(self):
        self.func.action("key1-r")
    def key1_pressed(self):
        self.func.action("key1")
        
    def key2_released(self):
        self.func.action("key2-r")
    def key2_pressed(self):
        self.func.action("key2")

    def key3_released(self):
        self.func.action("key3-r")
    def key3_pressed(self):
        self.func.action("key3")
        
    def listen(self):
        while True:
            if GPIO.input(KEY_UP_PIN) == 0:
                if not self.key_mapper["up"]:
                    self.key_mapper["up"] = True
                    self.up_pressed()
            else:
                if self.key_mapper["up"]:
                    self.key_mapper["up"] = False
                    self.up_released()

            if GPIO.input(KEY_LEFT_PIN) == 0:
                if not self.key_mapper["left"]:
                    self.key_mapper["left"] = True
                    self.left_pressed() 
            else:
                if self.key_mapper["left"]:
                    self.key_mapper["left"] = False
                    self.left_released()

            if GPIO.input(KEY_RIGHT_PIN) == 0:
                if not self.key_mapper["right"]:
                    self.key_mapper["right"] = True
                    self.right_pressed()
            else:
                if self.key_mapper["right"]:
                    self.key_mapper["right"] = False
                    self.right_released()
                
            if GPIO.input(KEY_DOWN_PIN) == 0:
                if not self.key_mapper["down"]:
                    self.key_mapper["down"] = True
                    self.down_pressed()
            else:
                if self.key_mapper["down"]:
                    self.key_mapper["down"] = False
                    self.down_released()

            if GPIO.input(KEY_PRESS_PIN) == 0:
                if not self.key_mapper["center"]:
                    self.key_mapper["center"] = True
                    self.center_pressed()
            else: 
                if self.key_mapper["center"]:
                    self.key_mapper["center"] = False
                    self.center_released()

            if GPIO.input(KEY1_PIN) == 0:
                if not self.key_mapper["key1"]:
                    self.key_mapper["key1"] = True
                    self.key1_pressed()
            else: 
                if self.key_mapper["key1"]:
                    self.key_mapper["key1"] = False
                    self.key1_released()

            if GPIO.input(KEY2_PIN) == 0:
                if not self.key_mapper["key2"]:
                    self.key_mapper["key2"] = True
                    self.key2_pressed()
            else: 
                if self.key_mapper["key2"]:
                    self.key_mapper["key2"] = False
                    self.key2_released()

            if GPIO.input(KEY3_PIN) == 0:
                if not self.key_mapper["key3"]:
                    self.key_mapper["key3"] = True
                    self.key3_pressed()
            else: 
                if self.key_mapper["key3"]:
                    self.key_mapper["key3"] = False
                    self.key3_released()
            time.sleep(0.01)
