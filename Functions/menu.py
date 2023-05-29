from Camera import Camera
from PIL import Image
import os
import time
import socket
import threading

class Menu:
    def __init__(self, main_dir):
        self.previewing = False
        self.k1 = False
        self.k3 = False
        self.k2 = False
        self.capture_thread = None
        self.preview_thread = None
        self.gallery_thread = None
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
                "current-option" : 1,
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
            {
                "head" : "Gallery",
                "value" : "Open Gallery",
                "unit" : "",
                "current-option" : None,
                "options" : [],
                "action" : self.gallery,
                "param" : []
            },
        ]
    
    def reset_gallery(self, param=[]):
        self.previewing = False
        self.k3 = False
        self.k1 = False
        func = param[0]
        self.menu[15]["value"] = "Open Gallery"
        self.menu[15]["action"] = self.gallery
        func.show_menu_screen()

    def open_gallery(self, func, callback, next, prev, stop):
        dir_list = os.listdir("/mnt/usb_share/")
        total_images = len(dir_list)
        index = 0
        p_index = 1
        try:
            while(True):
                if stop():
                    exit(0)
                if next():
                    self.k3 = False
                    index += 1
                    if index >= total_images:
                        index = 0
                if prev():
                    self.k1 = False
                    index -= 1
                    if index < 0:
                        index = total_images-1
                if p_index != index:
                    if dir_list[index].lower().endswith(('.png', '.jpg', '.jpeg')):
                        img = Image.open(f"/mnt/usb_share/{dir_list[index]}")
                        new_img = img.resize((128,128))
                        img.close()
                        func.display.disp.LCD_ShowImage(new_img,0,0)
                    p_index = index
        finally:
            callback([func])

    def gallery(self, param=[]):
        dir_list = os.listdir("/mnt/usb_share/")
        if len(dir_list) > 0:
            total_images = len(dir_list)
            func = param[0]
            self.menu[15]["value"] = f"{str(total_images)} Images"
            self.menu[15]["action"] = self.blank_method
            func.show_menu_screen()

            self.previewing = True
            self.k2 = False
            self.k3 = False
            self.k1 = False
            self.gallery_thread = threading.Thread(target=self.open_gallery, args=(
                func,
                self.reset_gallery,
                lambda: self.k3,
                lambda: self.k1,
                lambda: self.k2))
            self.gallery_thread.start()
        else:
            func = param[0]
            self.menu[15]["value"] = "No Image"
            self.menu[15]["action"] = self.gallery
            func.show_menu_screen()

    def show_preview(self, param=[]):
        func = param[0]
        self.menu[14]["value"] = "Previewing..."
        self.menu[14]["action"] = self.blank_method
        func.show_menu_screen()

        height = func.display.height
        width = func.display.width
        disp = func.display.disp
        self.k2 = False
        self.previewing = True
        self.k3 = False
        self.k1 = False
        self.preview_thread = threading.Thread(target=self.camera.show_preview, args=(
            height,
            width,
            disp,
            func,
            self.reset_preview,
            lambda: self.k1,
            lambda: self.k3,
            lambda: self.k2))
        self.preview_thread.start()

    def reset_preview(self, param=[]):
        func = param[0]
        self.previewing = False
        self.k3 = False
        self.k1 = False
        self.menu[14]["value"] = "Show Preview"
        self.menu[14]["action"] = self.show_preview
        func.show_menu_screen()

    def stop_preview(self, param=[]):
        func = param[0]
        if self.k2 == False:
                self.k2 = True
                func.show_menu_screen()

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
        self.k2 = False
        self.capture_thread = threading.Thread(target=self.capture, args=(lambda: self.k2,param,))
        self.capture_thread.start()

    def capture(self, stop, param=[]):
        image_count = int(self.menu[5]["options"][self.menu[5]["current-option"]])
        self.camera.configure(self.menu)
        try:
            for i in range(1, image_count+1):
                func = param[0]
                self.menu[6]["value"] = "Capturing " + str(i)
                func.show_menu_screen()
                self.camera.capture()
                if stop():
                    self.menu[6]["value"] = "Start Capture"
                    func.show_menu_screen()
                    self.menu[6]["action"] = self.capture_image
                    exit(0)
        finally:
            self.camera.camera.close()
        self.menu[6]["value"] = "Start Capture"
        func.show_menu_screen()
        self.menu[6]["action"] = self.capture_image

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
