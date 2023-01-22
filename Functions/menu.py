from Camera import Camera
import os
import time
import socket
import threading

class Menu:
    def __init__(self, main_dir):
        self.stop_threads = False
        self.capture_thread = None
        self.preview_thread = None
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
                "current-option" : 9,
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
                    "1920 x 1080"]
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
            {
                "head" : "Mass Storage",
                "value" : "Start",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.start_mass_storage,
                "param" : []
            },
            {
                "head" : "Erase",
                "value" : "Erase Images",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.erase_storage,
                "param" : []
            },
            {
                "head" : "Preview",
                "value" : "Show Preview",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.show_preview,
                "param" : []
            },
        ]        
    def show_preview(self, param=[]):
        func = param[0]
        height = func.display.height
        width = func.display.width
        disp = func.display.disp
        self.stop_threads = False
        self.preview_thread = threading.Thread(target=self.camera.show_preview, args=(height, width, disp, lambda: self.stop_threads))
        self.preview_thread.start()

    def erase_storage(self, param=[]):
        func = param[0]
        self.menu[13]["value"] = "Erasing..."
        self.menu[13]["action"] = self.blank_method

        self.menu[12]["value"] = "Start"
        self.menu[12]["action"] = self.start_mass_storage
        func.show_menu_screen()
        os.system("sudo modprobe g_mass_storage -r")
        time.sleep(1)
        os.system("sudo rm -r /mnt/usb_share/*")
        self.menu[13]["value"] = "Erase Images"
        self.menu[13]["action"] = self.erase_storage
        func.show_menu_screen()

    def start_mass_storage(self, param=[]):
        func = param[0]
        self.menu[12]["value"] = "Stop"
        self.menu[12]["action"] = self.stop_mass_storage
        func.show_menu_screen()
        os.system("sudo modprobe g_mass_storage file=/piusb.bin removable=y ro=1 stall=0")
    
    def stop_mass_storage(self, param=[]):
        func = param[0]
        self.menu[12]["value"] = "Start"
        self.menu[12]["action"] = self.start_mass_storage
        func.show_menu_screen()
        os.system("sudo modprobe g_mass_storage -r")     

    def capture_image(self, param=[]):
        func = param[0]
        self.menu[6]["value"] = "Starting..."
        self.menu[6]["action"] = self.blank_method

        self.menu[12]["value"] = "Start"
        self.menu[12]["action"] = self.start_mass_storage
        func.show_menu_screen()
        os.system("sudo modprobe g_mass_storage -r")
        time.sleep(1)
        self.stop_threads = False
        self.capture_thread = threading.Thread(target=self.capture, args=(lambda: self.stop_threads,param,))
        self.capture_thread.start()

    def capture(self, stop, param=[]):
        image_count = int(self.menu[5]["options"][self.menu[5]["current-option"]])
        self.camera.configure(self.menu)
        for i in range(1, image_count+1):
            func = param[0]
            self.menu[6]["value"] = "Capturing " + str(i)
            func.show_menu_screen()
            self.camera.capture()
            if stop():
                self.menu[6]["value"] = "Start Capture"
                func.show_menu_screen()
                self.menu[6]["action"] = self.capture
                exit(0)
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
        print(IPAddr)
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
