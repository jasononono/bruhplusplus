import pygame as p
from editor import TextEditor

class Screen:
    def __init__(self, size = (800, 600), bg = (255, 255, 255)):
        self.width, self.height = size
        self.surface = p.display.set_mode((self.width, self.height))
        self.bg = bg

        self.editor = TextEditor("", (10, 10), (self.width - 20, self.height - 20))

        self.execute = True
        self.focus = self.editor

    def update(self):
        events = p.event.get()
        keys = p.key.get_pressed()
        mouse = p.mouse.get_pressed()
        mouse_pos = p.mouse.get_pos()

        for e in events:
            if e.type == p.QUIT:
                self.execute = False

        self.surface.fill(self.bg)

        if self.focus is self.editor:
            self.editor.update(self.surface, events, keys, mouse, mouse_pos)
        else:
            self.editor.template.update(self.surface, False)

        p.display.flip()

p.init()
scr = Screen(bg = (240, 240, 240))

clock = p.time.Clock()

while scr.execute:
    clock.tick(30)
    scr.update()
p.quit()