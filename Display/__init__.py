from . import LCD_1in44
from . import LCD_Config
from PIL import Image,ImageDraw,ImageFont,ImageColor

class Display:
    def __init__(self) -> None:
        self.disp = LCD_1in44.LCD()
        self.Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
        self.disp.LCD_Init(self.Lcd_ScanDir)
        self.width = 128
        self.height = 128
    
    def clear_display(self):
        self.disp.LCD_Clear()
    
    def draw_image(self, image_path):
        image = Image.open(image_path)
        self.disp.LCD_ShowImage(image,0,0)
    
    def show_menu(self, head, value):
        image = Image.new('RGB', (self.width, self.height), "WHITE")
        draw = ImageDraw.Draw(image)
        draw.polygon([(79, 50), (89, 32), (99, 50)], outline=0xffffff, fill=0x5c5c5c)
        draw.polygon([(79, 94), (89, 112), (99, 94)], outline=0xffffff, fill=0x5c5c5c)
        head_font = ImageFont.truetype("fonts/Anton-Regular.ttf", 15)
        value_font = ImageFont.truetype("fonts/Orbitron-VariableFont_wght.ttf", 10)
        draw.text((3, 3), head, fill = "BLACK", font=head_font)
        draw.text((3, 64), value, fill = "GREEN", font=value_font)
        self.disp.LCD_ShowImage(image,0,0)