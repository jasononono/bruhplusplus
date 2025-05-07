import pygame as p
import editor as edit
import base

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
    def __init__(self, size = (800, 600), bg = (41, 41, 64)):
        self.x, self.y = 0, 0
        self.width, self.height = size
        self.surface = p.display.set_mode((self.width, self.height))
        self.bg = bg
        self.event = Event()

        self.editor = edit.TextEditor("", (10, 10), (self.width - 20, self.height - 20))

        self.execute = True
        self.focus = self.editor

    def is_focused(self, instance):
        if instance.valid_mouse_position(self.event.mousePos):
            self.focus = instance
            return True
        return False

    def get_focus(self):
        for i in list(self.editor.dialogue.values())[::-1]:
            if i is None:
                continue
            if self.is_focused(i):
                return
        if self.is_focused(self.editor):
            return
        self.focus = None

    def update(self):
        self.event.update()

        for e in self.event.events:
            if e.type == p.QUIT:
                self.execute = False
            if e.type == p.MOUSEBUTTONDOWN:
                self.get_focus()

        if base.pendingFocus is not False:
            self.focus = base.pendingFocus
            base.pendingFocus = False

        self.surface.fill(self.bg)

        self.editor.update(self)

        p.display.flip()

p.init()
scr = Screen()

clock = p.time.Clock()

while scr.execute:
    clock.tick(30)
    scr.update()
p.quit()