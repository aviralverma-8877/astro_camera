from Display import Display
from Buttons import Buttons
from Functions.menu import Menu
import time
import _thread

class Functions:
    def init_system(self):
        self.menu_obj = Menu()
        self.menu = self.menu_obj.get_menu_items()
        self.total_menu_items = len(self.menu)
        self.current_menu_index = 0
        self.buttons = Buttons(self)
        self.display = Display()
        self.display.clear_display()
        self.display.draw_image('./images/logo.jpg')
        time.sleep(2)
        self.show_menu_screen()
        
    def show_menu_screen(self):
        self.menu_obj.current_selected = self.current_menu_index % self.total_menu_items
        head = self.menu[self.menu_obj.current_selected]["head"]
        current_option = self.menu[self.menu_obj.current_selected]["current-option"]
        if current_option != None:
            body = self.menu[self.menu_obj.current_selected]["options"][current_option] + " " + self.menu[self.menu_obj.current_selected]["unit"]
        else:
            body = self.menu[self.menu_obj.current_selected]["value"]
        self.display.show_menu(head, body)

    def setup_buttons(self):
        _thread.start_new_thread(self.buttons.listen,())

    def action(self, key):
        if (key == "left"):
            self.current_menu_index -= 1
            self.show_menu_screen()

        if (key == "right"):
            self.current_menu_index += 1
            self.show_menu_screen()

        if (key == "up"):
            option_length = len(self.menu[self.menu_obj.current_selected]["options"])
            current_option = self.menu[self.menu_obj.current_selected]["current-option"]
            current_option -= 1
            self.menu_obj.change_current_option(self.current_menu_index, current_option % option_length)
            self.show_menu_screen()
        
        if (key == "down"):
            option_length = len(self.menu[self.menu_obj.current_selected]["options"])
            current_option = self.menu[self.menu_obj.current_selected]["current-option"]
            current_option += 1
            self.menu_obj.change_current_option(self.current_menu_index, current_option % option_length)
            self.show_menu_screen()
