import pygame as p

class Font:
    def __init__(self, name = "Menlo", size = 15):
        self.name = name
        self.size = size
        self.template = p.font.SysFont(name, size)

    def rename(self, name = "Menlo"):
        self.name = name
        self.template = p.font.SysFont(name, self.size)

    def render(self, text = '', colour = (0, 0, 0), background = None):
        return self.template.render(text, True, colour, background)