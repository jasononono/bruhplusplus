import pygame as p
from font import Font

class Dialogue:
    def __init__(self, text = "An error occurred.", position = (0, 0)):
        self.text = text
        self.x, self.y = position
        self.font = Font(size = 15)
        self.size = self.font.get_size(text)
        self.width, self.height = self.size[0] + 20, self.size[1] + 20

    def update(self, surface, mouse = (), mousePos = ()):
        p.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height))
        surface.blit(self.font.render(self.text), (self.x + 10, self.y + 10))
        if mouse[0] and self.x < mousePos[0] < self.x + self.width and self.y < mousePos[1] < self.y + self.height:
            return True
        return False
