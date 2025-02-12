import sys
import pygame
import pygame_gui
from pathlib import Path
import json

import ctypes

import program.constants as constants

import program.paint as paint
from program.button import Button
from program.mark_screen import MarkScreen
from program.main_screen import MainScreen

class Program:
    
    def __init__(self):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(constants.ID)
        
        pygame.init()
        self.display = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("Xeno.exe")
        pygame.display.set_icon(pygame.image.load("src/images/icon.png"))
        
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((constants.WIDTH, constants.HEIGHT))
        
        self.running = True
        self.screen = constants.SCREEN_MAIN
        
        self.prepare_data()
        self.load_variables()
        self.load_screens()
    
    def load_variables(self):
        with open(constants.DIR_DATA, "r") as file:
            self.current_power = json.load(file)["power"]
        
    def prepare_data(self):
        # Create data directory if does not exist
        Path("src/data/").mkdir(parents=True, exist_ok=True)
        try:
            with open(constants.DIR_DATA, "x") as file:
                json.dump({"power": 100, "containers": [[], [], []], "integrity": [0]*25}, file)
        except FileExistsError:
            pass
        try:
            with open(constants.DIR_MONSTER_DATA, "x") as file:
                json.dump([], file)
        except FileExistsError:
            pass
        
        
    def load_screens(self):
        self.screens = [
            MainScreen(self),
            MarkScreen(self),
        ]
        
        
        
    def update(self):
        self.screens[self.screen].update()
        self.manager.update(self.clock.tick(constants.FPS)/1000)
        
        self.screens[self.screen].draw()
        self.manager.draw_ui(self.display)
        
        pygame.display.update()
        self.clock.tick(constants.FPS)
        
        
    
    def change_power(self, change: int):
        self.current_power = min(150, max(0, self.current_power + change))
        
        # update data.json
        with open(constants.DIR_DATA, "r") as file:
            data = json.load(file)
        with open(constants.DIR_DATA, "w") as file:
            data["power"] = self.current_power
            json.dump(data, file)
        
        
    def create_backup(self):
        with open(constants.DIR_DATA, "r") as data:
            with open(constants.DIR_BACKUP, "w") as file:
                json.dump(json.load(data), file)
    
    def end(self):
        self.create_backup()
        pygame.quit()
        sys.exit()

