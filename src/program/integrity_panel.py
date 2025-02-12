import pygame

import program.constants as constants
from program.part import Part
import json

class IntegrityPanel:
    
    WIDTH = 200
    HEIGHT = 200
    
    def __init__(self, data_dir: str, rect: tuple[int, int, int, int]):
        self.data_dir = data_dir
        self.rect = (rect[0] + rect[2]//2 - IntegrityPanel.WIDTH//2,
                     rect[1] + rect[3]//2 - IntegrityPanel.HEIGHT//2,
                     IntegrityPanel.WIDTH, IntegrityPanel.HEIGHT)
        self.surf = pygame.Surface((IntegrityPanel.WIDTH, IntegrityPanel.HEIGHT), pygame.SRCALPHA)
        
        self.parts = [
            Part((123, 62), pygame.image.load("src/images/integrity/damaged/left_forearm.png")), # left forearm
            Part((112, 18), pygame.image.load("src/images/integrity/damaged/left_arm.png")), # left arm
            
            Part((66, 62), pygame.image.load("src/images/integrity/damaged/right_forearm.png")), # right forearm
            Part((69, 18), pygame.image.load("src/images/integrity/damaged/right_arm.png")), # right arm
            
            Part((104, 115), pygame.image.load("src/images/integrity/damaged/left_knee.png")), # left knee
            Part((102, 66), pygame.image.load("src/images/integrity/damaged/left_leg.png")), # left leg
            Part((103, 141), pygame.image.load("src/images/integrity/damaged/left_shin.png")), # left shin
            
            Part((86, 115), pygame.image.load("src/images/integrity/damaged/right_knee.png")), # right knee
            Part((86, 66), pygame.image.load("src/images/integrity/damaged/right_leg.png")), # right leg
            Part((85, 141), pygame.image.load("src/images/integrity/damaged/right_shin.png")), # right shin
            
            Part((87, 8), pygame.image.load("src/images/integrity/damaged/head.png")), # head
            Part((81, 36), pygame.image.load("src/images/integrity/damaged/body.png")), # body
            
            Part((19, 84), pygame.image.load("src/images/integrity/damaged/right_wing.png"), pygame.image.load("src/images/integrity/damaged/right_wing_lost.png")), # wing 1
            Part((33, 55), pygame.image.load("src/images/integrity/damaged/right_wing.png"), pygame.image.load("src/images/integrity/damaged/right_wing_lost.png")), # wing 2
            Part((47, 26), pygame.image.load("src/images/integrity/damaged/right_wing.png"), pygame.image.load("src/images/integrity/damaged/right_wing_lost.png")), # wing 3
            
            Part((139, 26), pygame.image.load("src/images/integrity/damaged/left_wing.png"), pygame.image.load("src/images/integrity/damaged/left_wing_lost.png")), # wing 4
            Part((153, 55), pygame.image.load("src/images/integrity/damaged/left_wing.png"), pygame.image.load("src/images/integrity/damaged/left_wing_lost.png")), # wing 5
            Part((167, 84), pygame.image.load("src/images/integrity/damaged/left_wing.png"), pygame.image.load("src/images/integrity/damaged/left_wing_lost.png")), # wing 6
        ]
        
        self.image = pygame.image.load("src/images/integrity/base.png")
        
        self.load_data()
        
    def load_data(self):
        with open(self.data_dir, "r") as file:
            data = json.load(file)["integrity"]
            for i, part in enumerate(self.parts):
                part.status = data[i]
    
    def update(self):
        self.surf.blit(self.image, (0, 0))
        
        for part in self.parts:
            part.draw(self.surf)
            
        self.store_integrity_data()
        
    def store_integrity_data(self):
        with open(self.data_dir, "r") as file:
            data = json.load(file)
        with open(self.data_dir, "w") as file:
            entry = []
            for part in self.parts:
                entry.append(part.status)
            data["integrity"] = entry
            json.dump(data, file)
        
        
    def interact(self):
        mx, my = pygame.mouse.get_pos()
        if 0 < mx - self.rect[0] < IntegrityPanel.WIDTH and 0 < my - self.rect[1] < IntegrityPanel.HEIGHT:
            for part in self.parts:
                if part.hovered(mx - self.rect[0], my - self.rect[1]):
                    part.toggle()
                    break
                
            self.update()
        
    
    def draw(self, surf):
        surf.blit(self.surf, (self.rect[0], self.rect[1]))
