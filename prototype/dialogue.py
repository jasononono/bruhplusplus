import pygame as p
from font import Font

class Dialogue:
    def __init__(self, parent, signature, text = "An error occurred.", position = (0, 0)):
        self.signature = signature
        self.text = text
        self.x, self.y = position
        self.font = Font(size = 12)
        self.size = self.font.get_size(text)
        self.width, self.height = self.size[0] + 20, self.size[1] + 20

        self.keybind = {}
        self.bind(p.K_ESCAPE, parent.exit_dialogue)
        self.bind(p.K_RETURN, parent.exit_dialogue)

    def bind(self, key, function):
        self.keybind[key] = function

    def update(self, screen):
        p.draw.rect(screen.surface, (55, 55, 65), (self.x, self.y, self.width, self.height))
        screen.surface.blit(self.font.render(self.text), (self.x + 10, self.y + 10))
        for i, j in self.keybind.items():
            if screen.event.keys[i]:
                return j
        return None

    def valid_mouse_position(self, position):
        if self.x < position[0] < self.x + self.width and self.y < position[1] < self.y + self.height:
            return True
        return False

pendingFocus = False