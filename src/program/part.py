import pygame

class Part:
    
    STATUS_GOOD = 0
    STATUS_BROKEN = 1
    STATUS_LOST = 2
    
    def __init__(self, pos: tuple[int, int], broken_image: pygame.Surface, lost_image: pygame.Surface = None):
        self.pos = pos
        self.broken_image = broken_image
        self.lost_image = lost_image
        self.status = Part.STATUS_GOOD
        
        self.statuses = 2 if lost_image == None else 3
        
    def draw(self, surf):
        if self.status == Part.STATUS_BROKEN:
            surf.blit(self.broken_image, (self.pos[0], self.pos[1]))
        elif self.status == Part.STATUS_LOST:
            surf.blit(self.lost_image, (self.pos[0], self.pos[1]))
        
    def hovered(self, mx: int, my: int):
        return 0 < mx - self.pos[0] < self.broken_image.get_width() and 0 < my - self.pos[1] < self.broken_image.get_height()
    
    def toggle(self):
        self.status = (self.status + 1) % self.statuses