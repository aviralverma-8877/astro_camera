class Menu:
    def __init__(self):
        self.current_selected = 0
        self.menu = [
            {
                "head" : "ISO",
                "unit" : "",
                "current-option" : 0,
                "options" : ["100","200","300","400","500","600","700","800"]
            },
            {
                "head" : "Contrast",
                "unit" : "",
                "current-option" : 4,
                "options" : ["10","20","30","40","50","60","70","80","90","100"]
            },
            {
                "head" : "Brightness",
                "unit" : "",
                "current-option" : 4,
                "options" : ["10","20","30","40","50","60","70","80","90","100"]
            },
            {
                "head" : "Image Time",
                "unit" : "sec",
                "current-option" : 0,
                "options" : ["10","20","30"]
            },
            {
                "head" : "Image Count",
                "unit" : "Photos",
                "current-option" : 0,
                "options" : ["10","20","30"]
            },
            {
                "head" : "START",
                "value" : "Start Capture",
                "unit" : "",
                "current-option" : None,
                "options" : []
            }
        ]

    def change_current_option(self, menu_index, option_index):
        self.menu[menu_index]["current-option"] = option_index

    def get_menu_items(self):
        return self.menu
