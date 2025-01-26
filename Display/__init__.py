from Display.LCD_1in44 import LCD, SCAN_DIR_DFT
from PIL import Image,ImageDraw,ImageFont

class Display:
    def __init__(self, main_dir) -> None:
        self.disp = LCD()
        self.Lcd_ScanDir = SCAN_DIR_DFT
        self.disp.LCD_Init(self.Lcd_ScanDir)
        self.width = 128
        self.height = 128
        self.main_dir = main_dir
    
    def clear_display(self):
        self.disp.LCD_Clear()
    
    def draw_image(self, image_path):
        image = Image.open(image_path)
        self.disp.LCD_ShowImage(image,0,0)
    
    def show_menu(self, head, value):
        image = Image.new('RGB', (self.width, self.height), "Black")
        draw = ImageDraw.Draw(image)
        draw.polygon([(0, 9), (18, 0), (18, 20)], outline="RED", fill="RED")
        draw.polygon([(128, 9), (110, 0), (110, 20)], outline="RED", fill="RED")
        draw.polygon([(79, 50), (89, 32), (99, 50)], outline="RED", fill="RED")
        draw.polygon([(79, 94), (89, 112), (99, 94)], outline="RED", fill="RED")
        head_font = ImageFont.truetype(self.main_dir + "/fonts/Anton-Regular.ttf", 15)
        value_font = ImageFont.truetype(self.main_dir + "/fonts/Orbitron-VariableFont_wght.ttf", 15)
        draw.text((25, 0), head, fill = "RED", font=head_font)
        draw.text((3, 60), value, fill = "RED", font=value_font)
        self.disp.LCD_ShowImage(image,0,0)