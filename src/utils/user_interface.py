import datetime
import os
import re
from pgu import gui
import config
from src.utils.events import SAVE_FILE, LOAD_FILE, EDIT_COLORS
import pygame

class ErrorDialog(gui.Dialog):
    def __init__(self, *error_messages: str, **params):
        main = gui.Table()
        for error_message in error_messages:
            main.td(gui.Label(error_message))
            main.tr()
        ok_btn = gui.Button("ok")
        ok_btn.connect(gui.CLICK, self.close, None)
        main.td(ok_btn)
        super().__init__(gui.Label("Error"), main, **params)

class ColorPiker(gui.Table):
    def __init__(self, label: str, default_color: pygame.Color = pygame.Color(0, 0, 0), **params):
        super().__init__(**params)
        self.value = list(default_color)

        self.td(gui.Label(label))

        self.tr()

        self.str_color = gui.Input("rgb({}, {}, {})".format(*self.value[:3]))
        self.str_color.connect(gui.CHANGE, self.edit_str_color, self.str_color)
        self.td(self.str_color)

        self.tr()

        self.color = gui.Color(self.value, width=64, height=64)
        self.td(self.color, rowspan=3, colspan=1)

        self.td(gui.Label(' Red: '),1,0)
        r = gui.HSlider(value=self.value[0],min=0,max=255,size=32,width=128,height=16)
        r.connect(gui.CHANGE,self.adjust,(0,r))
        self.td(r,2,0)
        ##

        self.td(gui.Label(' Green: '),1,1)
        g = gui.HSlider(value=self.value[1],min=0,max=255,size=32,width=128,height=16)
        g.connect(gui.CHANGE,self.adjust,(1,g))
        self.td(g,2,1)

        self.td(gui.Label(' Blue: '), 1, 2)
        b = gui.HSlider(value=self.value[2], min=0, max=255, size=32, width=128, height=16)
        b.connect(gui.CHANGE, self.adjust, (2, b))
        self.td(b, 2, 2)

    def adjust(self, value):
        (num, slider) = value
        self.value[num] = slider.value
        self.str_color._value = "rgb({}, {}, {})".format(*self.value[:3])
        self.color.repaint()
        self.send(gui.CHANGE)

    def edit_str_color(self, input: gui.Input):
        color_val = input.value
        if type(color_val) == str:
            match = re.match(r"rgb\((\d{1,3}),\s(\d{1,3}),\s(\d{1,3})\)", color_val)
            if match:
                self.value[0] = int(match.group(1))
                self.value[1] = int(match.group(2))
                self.value[2] = int(match.group(3))
                self.color.repaint()
                self.send(gui.CHANGE)





class ColorDialog(gui.Dialog):
    def __init__(self, value = "#00ffff", **params):
        self.value = list(gui.parse_color(value))
        
        title = gui.Label("Color Picker")

        main = gui.Table()

        self.backgound_colorpiker = ColorPiker("Background: ", default_color=config.BACKGROUND_COLOR)
        main.td(self.backgound_colorpiker)
        main.tr()
        self.grid_colorpiker = ColorPiker("       Grid:      ", default_color=config.GRID_COLOR)
        main.td(self.grid_colorpiker)
        
        main.tr()
        submit_btn = gui.Button("Submit")
        submit_btn.connect(gui.CLICK, self.submit_click, None)
        main.td(submit_btn)

        
        gui.Dialog.__init__(self,title,main)

    def submit_click(self, _):
        background_color = self.backgound_colorpiker.value
        grid_color = self.grid_colorpiker.value

        event = pygame.event.Event(EDIT_COLORS,
                                {
                                    "background_color": background_color,
                                    "grid_color": grid_color
                                })
        
        pygame.event.post(event)
        self.close()

class Main(gui.Container):
    def __init__(self, **params):
        super().__init__(**params)

        main = gui.Table()
        
        title = gui.Label("Menu")

        self.continue_btn = gui.Button("Continue")
        # continue_btn.connect(gui.CLICK, self.load_dialog, None)

        edit_colors = gui.Button("Edit colors")
        edit_colors.connect(gui.CLICK, self.edit_colors_dialog, None)

        load_btn = gui.Button("Load")
        load_btn.connect(gui.CLICK, self.load_dialog, None)

        save_btn = gui.Button("Save")
        save_btn.connect(gui.CLICK, self.save_dialog, None)

        exit_btn = gui.Button("Exit")
        exit_btn.connect(gui.CLICK, self.exit_all, 1)

        main.td(title)
        main.tr()
        main.td(self.continue_btn)
        main.tr()
        main.td(edit_colors)
        main.tr()
        main.td(load_btn)
        main.tr()
        main.td(save_btn)
        main.tr()
        main.td(exit_btn)

        self.add(main, 0,0)
    
    def exit_all(self, code: int):
        return exit(code)
    
    def edit_colors_dialog(self, _):
        color_dialog = ColorDialog()
        color_dialog.open()
    
    def load(self, dialog: gui.FileDialog):
        path: str = dialog.value # type: ignore
        if path and os.path.isfile(path):
            filename, extension = os.path.splitext(path)
            if extension != "pk":
                event = pygame.event.Event(LOAD_FILE, {"file_path": path})
                pygame.event.post(event) # type: ignore
                return
        error = ErrorDialog("Incorect file")
        error.open()

    def load_dialog(self, _):
        file_dialog_load = gui.FileDialog(title_txt="Select file to load",button_txt="Load")
        file_dialog_load.connect(gui.CHANGE, self.load, file_dialog_load)
        file_dialog_load.open()
    
    def save(self, dialog: gui.FileDialog):
        path: str = dialog.value # type: ignore
        if os.path.isdir(path):
            formatted_date = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
            path = os.path.join(path, f"{formatted_date}.pk")
        elif os.path.isfile(path):
            filename, extension = os.path.splitext(path)

        event = pygame.event.Event(SAVE_FILE, {"file_path": path})
        pygame.event.post(event) # type: ignore

    def save_dialog(self, _):
        file_dialog_save = gui.FileDialog(title_txt="Select folder to save",button_txt="Save")
        file_dialog_save.connect(gui.CHANGE, self.save, file_dialog_save)
        file_dialog_save.open()

# screen = pygame.display.set_mode((640,480))
# main = Main(align=0,valign=0)
# app = gui.App()

# app.init(main)

# clock = pygame.time.Clock()
# done = False
# while not done:
#     for e in pygame.event.get():
#         if e.type is pygame.QUIT: 
#             done = True
#         elif e.type is pygame.KEYDOWN and e.key == pygame.K_ESCAPE: 
#             done = True
#         else:
#             app.event(e)
#     # Clear the screen and render the stars
#     dt = clock.tick(60)/1000.0
#     screen.fill((0,0,0))



    # app.paint()
    # pygame.display.update()
