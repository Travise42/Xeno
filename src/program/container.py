import program.constants as constants

import json

import pygame
import pygame_gui

class Container:
    
    count = 0
    
    def __init__(self, data_dir: str, rect: tuple[int, int, int, int], font: pygame.font.Font, capacity: int, max_characters: int):
        self.id = Container.count
        Container.count += 1
        self.data_dir = data_dir
        
        self.rect = rect
        self.font = font
        self.capacity = capacity
        self.max_characters = max_characters
        self.drag_y = 0
        self.grabbed = None
        
        self.load_widgets()
        
    def load_widgets(self):
        self.widgets = []
        with open(self.data_dir, "r") as file:
            data = json.load(file)
            for widget in data["containers"][self.id]:
                self.widgets.append(Widget(self, widget))
        
    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, constants.PALETTE_SHADOW, self.rect, 0, 12)
        
        mx, my = pygame.mouse.get_pos()
        
        for i, widget in enumerate(self.widgets):
            x = self.rect[0] + Widget.PADDING
            y = self.calc_y(i)
            width = self.rect[2] - 2*Widget.PADDING
            widget.draw(surf, x, y, width, 0 < mx - x  < width and 0 < my - y < Widget.SIZE, to_delete=mx > x + width - Widget.SIZE)
        
    def grab(self):
        mx, my = pygame.mouse.get_pos()
        self.drag_y = my
        for i, widget in enumerate(self.widgets):
            x = self.rect[0] + Widget.PADDING
            y = self.calc_y(i)
            width = self.rect[2] - 2*Widget.PADDING
            if 0 < mx - x  < width and 0 < my - y < Widget.SIZE:
                self.grabbed = widget.grab((mx - x, my - y))
                return
        self.grabbed = None
        
    def drag(self):
        my = pygame.mouse.get_pos()[1]
        new_level = (my - self.rect[1] - Widget.PADDING/2)//(Widget.PADDING + Widget.SIZE)
        old_level = (self.drag_y - self.rect[1] - Widget.PADDING/2)//(Widget.PADDING + Widget.SIZE)
        if self.grabbed != None:
            if new_level > old_level:
                self.widgets.remove(self.grabbed)
                self.widgets.insert(int(min(self.capacity - 1, max(0, (my - self.rect[1] + Widget.SIZE/2)//(Widget.PADDING + Widget.SIZE) - 1))), self.grabbed)
            elif new_level < old_level:
                self.widgets.remove(self.grabbed)
                self.widgets.insert(int(min(self.capacity - 1, max(0, (my - self.rect[1] + Widget.SIZE/2)//(Widget.PADDING + Widget.SIZE)))), self.grabbed)
            
    def interact(self, screen):
        mx, my = pygame.mouse.get_pos()
        new_level = (my - self.rect[1] - Widget.PADDING/2)//(Widget.PADDING + Widget.SIZE)
        old_level = (self.drag_y - self.rect[1] - Widget.PADDING/2)//(Widget.PADDING + Widget.SIZE)
        if self.grabbed != None and new_level != old_level:
            self.store_container_data()
            self.grabbed.grabbed = False
            self.grabbed = None
            return
        for i, widget in enumerate(self.widgets):
            x = self.rect[0] + Widget.PADDING
            y = self.calc_y(i)
            width = self.rect[2] - 2*Widget.PADDING
            if 0 < mx - x  < width and 0 < my - y < Widget.SIZE:
                if not (0 < self.drag_y - y < Widget.SIZE):
                    return
                if mx > x + width - Widget.SIZE:
                    self.widgets.pop(i)
                    self.store_container_data()
                else:
                    widget.interact(screen)
                if self.grabbed != None:
                    self.grabbed.grabbed = False
                    self.grabbed = None
                return
        
        if self.grabbed == None:
            if len(self.widgets) < self.capacity and 0 < mx - self.rect[0] < self.rect[2] and 0 < my - self.rect[1] < self.rect[3]:
                self.widgets.append(Widget(self, "").interact(screen))
        else:
            self.grabbed.grabbed = False
            self.grabbed = None
            
    
    def draw_grabbed(self, surf: pygame.Surface):
        self.grabbed.draw(surf, 0, 0, self.rect[2] - 2*Widget.PADDING, True)
                
            
    def calc_y(self, i: int):
        return self.rect[1] + Widget.PADDING + i*(Widget.SIZE + Widget.PADDING)
    
    def store_container_data(self):
        with open(self.data_dir, "r") as file:
            data = json.load(file)
        with open(self.data_dir, "w") as file:
            entry = []
            for widget in self.widgets:
                entry.append(widget.text)
            data["containers"][self.id] = entry
            json.dump(data, file)
            
class Widget:
    
    PADDING = 12
    SIZE = 50
    
    def __init__(self, container: Container, text: str):
        self.text = text
        self.container = container
        self.surf_text = self.container.font.render(text, 1, constants.PALETTE_HIGHLIGHT)
        self.grabbed = False
        
    def rename(self, text: str):
        self.text = text
        m = self.container.max_characters
        self.surf_text = self.container.font.render(text[:m - 3].rstrip() + "..." if m < len(text) else text, 1, constants.PALETTE_HIGHLIGHT)
        
    def grab(self, delta):
        self.grabbed = delta
        return self
        
    def release(self):
        self.grabbed = False
    
    def interact(self, screen):
        screen.open_entry_widget(self)
        return self
    
    def draw(self, surf: pygame.Surface, x: int, y: int, width: int, hovered: bool = False, to_delete: bool = False):
        if self.grabbed:
            x = pygame.mouse.get_pos()[0] - self.grabbed[0]
            y = pygame.mouse.get_pos()[1] - self.grabbed[1]
        pygame.draw.rect(surf, constants.PALETTE_BACKGROUND, (x, y, width, Widget.SIZE), 0, 12)
        if hovered:
            pygame.draw.rect(surf, constants.PALETTE_ERROR if to_delete else constants.PALETTE_HIGHLIGHT, (x, y, width, Widget.SIZE), 2, 12)
        surf.blit(self.surf_text, (x + width//2 - self.surf_text.get_width()//2 - Widget.SIZE/2, y + Widget.SIZE//2 - self.surf_text.get_height()//2))
        pygame.draw.line(surf, constants.PALETTE_ERROR if hovered and to_delete else constants.PALETTE_SHADOW,
                         (x + width - Widget.SIZE/2 + Widget.SIZE/4, y + Widget.SIZE/2 + Widget.SIZE/4),
                         (x + width - Widget.SIZE/2 - Widget.SIZE/4, y + Widget.SIZE/2 - Widget.SIZE/4), 5)
        pygame.draw.line(surf, constants.PALETTE_ERROR if hovered and to_delete else constants.PALETTE_SHADOW,
                         (x + width - Widget.SIZE/2 + Widget.SIZE/4, y + Widget.SIZE/2 - Widget.SIZE/4),
                         (x + width - Widget.SIZE/2 - Widget.SIZE/4, y + Widget.SIZE/2 + Widget.SIZE/4), 5)