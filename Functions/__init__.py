from Display import Display
from Buttons import Buttons
from Functions.menu import Menu
import time
import threading

class Functions:
    def init_system(self, main_dir):
        self.main_dir = main_dir
        self.menu_obj = Menu(self.main_dir)
        self.menu = self.menu_obj.get_menu_items()
        self.total_menu_items = len(self.menu)
        self.current_menu_index = 0
        self.buttons = Buttons(self)
        self.display = Display(self.main_dir)
        self.display.clear_display()
        self.display.draw_image(self.main_dir+'/images/logo.jpg')
        time.sleep(2)
        self.show_menu_screen()
        
    def show_menu_screen(self):
        self.menu_obj.current_selected = self.current_menu_index
        head = self.menu[self.current_menu_index]["head"]
        current_option = self.menu[self.current_menu_index]["current-option"]
        if current_option != None:
            body = self.menu[self.current_menu_index]["options"][current_option] + " " + self.menu[self.current_menu_index]["unit"]
        else:
            body = self.menu[self.current_menu_index]["value"]
        self.display.show_menu(head, body)

    def setup_buttons(self):
        setup_buttons_thread = threading.Thread(target=self.buttons.listen, args=())
        setup_buttons_thread.start()

    def gpio_cleanup(self):
        self.buttons.gpio_cleanup()

    def action(self, key):
        if not self.menu_obj.previewing:
            if (key == "left"):
                self.current_menu_index -= 1
                
            if (key == "right"):
                self.current_menu_index += 1
                
            if self.current_menu_index == -1:
                self.current_menu_index = self.total_menu_items - 1
            if self.current_menu_index == self.total_menu_items:
                self.current_menu_index = 0
            
            option_length = len(self.menu[self.current_menu_index]["options"])
            current_option = self.menu[self.current_menu_index]["current-option"]

            if (key == "up"):            
                if current_option != None:
                    current_option -= 1
            
            if (key == "down"):
                if current_option != None:
                    current_option += 1
            if (key == "key2"):
                if current_option == None:
                    action = self.menu[self.current_menu_index]["action"]
                    param = self.menu[self.current_menu_index]["param"]
                    param.append(self)
                    action(param = param)

            if current_option == -1:
                current_option = option_length - 1
            elif current_option == option_length:
                current_option = 0

            self.menu_obj.change_current_option(self.current_menu_index, current_option)
            self.show_menu_screen()

        if (key == "key1"):
            if self.menu_obj.stop_threads == False:
                self.menu_obj.stop_threads = True
                self.show_menu_screen()

