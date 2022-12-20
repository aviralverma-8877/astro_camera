from Display import Display
import time

class Functions:
    def __init__(self) -> None:
        action_queue = []
    
    def init_system(self):
        self.display = Display()
        self.display.clear_display()
        self.display.draw_image('./images/logo.jpg')
        time.sleep(2)
        self.display.show_menu("Test","Hello World")