import pygame as p
from editor import TextEditor

class Event:
    def __init__(self):
        self.events = ()
        self.keys = ()
        self.mouse = ()
        self.mousePos = ()

    def update(self):
        self.events = p.event.get()
        self.keys = p.key.get_pressed()
        self.mouse = p.mouse.get_pressed()
        self.mousePos = p.mouse.get_pos()

class Screen:
    def __init__(self, size = (800, 600), bg = (255, 255, 255)):
        self.width, self.height = size
        self.surface = p.display.set_mode((self.width, self.height))
        self.bg = bg
        self.event = Event()

        self.editor = TextEditor("", (10, 10), (self.width - 20, self.height - 20))

        self.execute = True
        self.focus = self.editor

    def update(self):
        self.event.update()

        for e in self.event.events:
            if e.type == p.QUIT:
                self.execute = False

        self.surface.fill(self.bg)

        self.editor.update(self.surface, self.event, self.focus is self.editor)

        p.display.flip()

p.init()
scr = Screen(bg = (240, 240, 240))
p.display.set_caption("EDITOR PROTOTYPE 5")

clock = p.time.Clock()

while scr.execute:
    clock.tick(30)
    scr.update()
p.quit()