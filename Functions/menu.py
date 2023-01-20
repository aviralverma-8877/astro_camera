from Camera import Camera
import os
import time
import socket
import _thread

class Menu:
    def __init__(self, main_dir):
        self.current_selected = 0
        self.main_dir = main_dir
        self.camera = Camera(self.main_dir)
        self.menu = [
            {
                "head" : "ISO",
                "unit" : "",
                "current-option" : 0,
                "options" : ["100","200","300","400","500","600","700","800"]
            },
            {
                "head" : "Shutter",
                "unit" : "sec",
                "current-option" : 0,
                "options" : ["0.1","0.2","0.3","0.5","1","2","3","4","5","6"]
            },
            {
                "head" : "Resolution",
                "unit" : "",
                "current-option" : 14,
                "options" : [
                    "176 x 120",
                    "352 x 240",
                    "704 x 240",
                    "704 x 480",
                    "720 x 480",
                    "1280 x 720",
                    "1280 x 960",
                    "1280 x 1024",
                    "1600 x 1200",
                    "1920 x 1080",
                    "2048 x 1536",
                    "2688 x 1520",
                    "2592 x 1944",
                    "3072 x 2048",
                    "3280 x 2464"]
            },
            {
                "head" : "Image Time",
                "unit" : "sec",
                "current-option" : 0,
                "options" : ["0.5","1","2","3","4","5","6","7","8","9","10","20","30"]
            },
            {
                "head" : "Output",
                "unit" : "",
                "current-option" : 0,
                "options" : ["RAW","JPEG"]
            },
            {
                "head" : "Image Count",
                "unit" : "Photos",
                "current-option" : 0,
                "options" : ["1","10","20","30","40","50","60","70","80","90","100"]
            },
            {
                "head" : "START",
                "value" : "Start Capture",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.capture_image,
                "param" : []
            },
            {
                "head" : "IP Address",
                "value" : "Show IP",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.get_ip,
                "param" : []
            },
            {
                "head" : "Shutdown",
                "value" : "Shutdown Pi",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.shutdown_pi,
                "param" : []
            },
            {
                "head" : "Restart",
                "value" : "Restart Pi",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.restart_pi,
                "param" : []
            },
            {
                "head" : "Reset",
                "value" : "Soft Reset",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.reset,
                "param" : []
            },
            {
                "head" : "Quit",
                "value" : "Quit Prog",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.quit,
                "param" : []
            },
        ]

    def capture_image(self, param=[]):
        self.menu[7]["action"] = self.blank_method
        _thread.start_new_thread(self.capture, (param,))

    def capture(self, param=[]):
        image_count = int(self.menu[5]["options"][self.menu[5]["current-option"]])
        self.camera.configure(self.menu)
        for i in range(1, image_count+1):
            func = param[0]
            self.menu[6]["value"] = "Capturing " + str(i)
            func.show_menu_screen()
            self.camera.capture()
        self.menu[6]["value"] = "Start Capture"
        func.show_menu_screen()
        self.menu[6]["action"] = self.capture

    def change_current_option(self, menu_index, option_index):
        self.menu[menu_index]["current-option"] = option_index

    def get_menu_items(self):
        return self.menu

    def get_ip(self, param=[]):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            IPAddr = s.getsockname()[0]
            s.close()
        except:
            IPAddr = "Not Available"
        func = param[0]
        self.menu[func.current_menu_index]["value"] = IPAddr
        func.show_menu_screen()


    def shutdown_pi(self, param=[]):
        func = param[0]
        self.menu[func.current_menu_index]["value"] = "Shutting Down..."
        func.show_menu_screen()
        os.system("shutdown -h now")

    def restart_pi(self, param=[]):
        func = param[0]
        self.menu[func.current_menu_index]["value"] = "Restarting..."
        func.show_menu_screen()
        os.system("reboot")
    
    def reset(self, param=[]):
        func = param[0]
        self.menu[func.current_menu_index]["value"] = "Resetting..."
        func.show_menu_screen()
        time.sleep(1)
        os.system("systemctl restart astro_cam.service")
    
    def quit(self, param=[]):
        func = param[0]
        self.menu[func.current_menu_index]["value"] = "Quitting..."
        func.show_menu_screen()
        time.sleep(1)
        func.gpio_cleanup()
        os.system("systemctl stop astro_cam.service")
    
    def blank_method(self, param=[]):
        pass
