import os
from pgu import gui
from src.utils.other import SAVE_FILE, LOAD_FILE
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

class Main(gui.Container):
    def __init__(self, **params):
        super().__init__(**params)

        main = gui.Table()
        
        title = gui.Label("Menu")

        self.continue_btn = gui.Button("Continue")
        # continue_btn.connect(gui.CLICK, self.load_dialog, None)

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
        main.td(load_btn)
        main.tr()
        main.td(save_btn)
        main.tr()
        main.td(exit_btn)

        self.add(main, 0,0)
    
    def exit_all(self, code: int):
        return exit(code)
    
    def load(self, dialog: gui.FileDialog):
        path: str = dialog.value # type: ignore
        if path and os.path.isfile(path):
            filename, extension = os.path.splitext(path)
            if extension != "pk":
                event = pygame.event.Event(LOAD_FILE, {"file_path": path})
                pygame.event.post(event) # type: ignore
                # self.continue_btn.event(gui.CLICK)
                print(dialog.value)
                return
        error = ErrorDialog("Incorect file")
        error.open()

    def load_dialog(self, _):
        file_dialog_load = gui.FileDialog(title_txt="Select file to load",button_txt="Load")
        file_dialog_load.connect(gui.CHANGE, self.load, file_dialog_load)
        file_dialog_load.open()
    
    def save(self, dialog: gui.FileDialog):
        path: str = dialog.value # type: ignore
        event = pygame.event.Event(SAVE_FILE, {"file_path": path})
        pygame.event.post(event) # type: ignore
        # self.continue_btn.event(gui.CLICK)

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
