import pygame as p

class Font:
    def __init__(self, name = "Menlo", size = 15):
        self.name = name
        self.size = size
        self.template = p.font.SysFont(name, size)

    def rename(self, name = "Menlo"):
        self.name = name
        self.template = p.font.SysFont(name, self.size)

    def resize(self, size = 15):
        self.size = size
        self.template = p.font.SysFont(self.name, size)

    def get_size(self, text):
        return self.template.size(text)

    def render(self, text = '', colour = (255, 255, 255), background = None):
        return self.template.render(text, True, colour, background)