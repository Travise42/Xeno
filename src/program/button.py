import pygame

import program.constants as constants

class Button:
    
    STATE_IDLE = 0
    STATE_HOVERED = 1
    STATE_PRESSED = 2
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str = "", font: pygame.font.Font = None, image_path: str = "", rounded_factor: float = 1, justify: bool = False):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = Button.STATE_IDLE
        self.font = font
        self.text = text
        self.image_path = image_path
        self.rounded_factor = rounded_factor
        self.justify = justify
        
        self.init_draw()
        
    def init_draw(self):
        self.surf_idle = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surf_idle, constants.PALETTE_SHADOW, (4, 4, self.width-8, self.height-8), 0, int(12*self.rounded_factor))
        pygame.draw.rect(self.surf_idle, constants.PALETTE_HIGHLIGHT + (50,), (2, 2, self.width-4, self.height-4), 3, int(13*self.rounded_factor))
        pygame.draw.rect(self.surf_idle, constants.PALETTE_HIGHLIGHT + (100,), (3, 3, self.width-6, self.height-6), 3, int(12*self.rounded_factor))
        pygame.draw.rect(self.surf_idle, constants.PALETTE_HIGHLIGHT, (4, 4, self.width-8, self.height-8), 3, int(12*self.rounded_factor))
        text_surf = self.create_text_surf(constants.PALETTE_HIGHLIGHT, self.text, self.font, self.image_path)
        if self.justify:
            self.surf_idle.blit(text_surf, (self.width // 10, self.width // 10))
        else:
            self.surf_idle.blit(text_surf, (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - text_surf.get_height() // 2))
        
        self.surf_hovered = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surf_hovered, constants.PALETTE_BACKGROUND, (4, 4, self.width-8, self.height-8), 0, int(12*self.rounded_factor))
        pygame.draw.rect(self.surf_hovered, constants.PALETTE_HIGHLIGHT + (50,), (0, 0, self.width, self.height), 3, int(15*self.rounded_factor))
        pygame.draw.rect(self.surf_hovered, constants.PALETTE_HIGHLIGHT + (100,), (1, 1, self.width-2, self.height-2), 3, int(14*self.rounded_factor))
        pygame.draw.rect(self.surf_hovered, constants.PALETTE_HIGHLIGHT + (150,), (2, 2, self.width-4, self.height-4), 3, int(13*self.rounded_factor))
        pygame.draw.rect(self.surf_hovered, constants.PALETTE_HIGHLIGHT + (200,), (3, 3, self.width-6, self.height-6), 3, int(12*self.rounded_factor))
        pygame.draw.rect(self.surf_hovered, constants.PALETTE_HIGHLIGHT, (4, 4, self.width-8, self.height-8), 3, int(12*self.rounded_factor))
        text_surf = self.create_text_surf(constants.PALETTE_HIGHLIGHT, self.text, self.font, self.image_path, True)
        if self.justify:
            self.surf_hovered.blit(text_surf, (self.width // 10, self.width // 10))
        else:
            self.surf_hovered.blit(text_surf, (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - text_surf.get_height() // 2))
        
        self.surf_pressed = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surf_pressed, constants.PALETTE_SHADOW, (4, 4, self.width-8, self.height-8), 0, int(12*self.rounded_factor))
        pygame.draw.rect(self.surf_pressed, constants.PALETTE_CONTRAST, (4, 4, self.width-8, self.height-8), 3, int(12*self.rounded_factor))
        text_surf = self.create_text_surf(constants.PALETTE_CONTRAST, self.text, self.font, self.image_path)
        if self.justify:
            self.surf_pressed.blit(text_surf, (self.width // 10, self.width // 10))
        else:
            self.surf_pressed.blit(text_surf, (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - text_surf.get_height() // 2))
        
    def change_text(self, new_text):
        self.text = new_text
        self.init_draw()
        
    def create_text_surf(self, color: tuple[int, int, int], text: str = "", font: pygame.font.Font = None, image_path: str = "", blur: bool = False):
        if font == None:
            text_surf = pygame.image.load(image_path)
            text_surf.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            text_surf = font.render(text, 1, constants.PALETTE_HIGHLIGHT)
        if blur:
            glow = pygame.transform.smoothscale_by(text_surf, 1/3)
            glow = pygame.transform.smoothscale_by(glow, 3)
            glow.blit(text_surf, (text_surf.get_width()//30, 0))
            return glow
        return text_surf
        
    def update(self):
        self.state = self.get_state()
    
    def draw(self, surf):
        surf.blit([self.surf_idle, self.surf_hovered, self.surf_pressed][self.state], (self.x, self.y))

    def hovered(self) -> bool:
        mx, my = pygame.mouse.get_pos()
        return 0 < mx - self.x < self.width and 0 < my - self.y < self.height

    def get_state(self) -> int:
        if self.hovered():
            if pygame.mouse.get_pressed()[0]:
                return 2
            return 1
        return 0
    