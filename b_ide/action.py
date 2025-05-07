import pygame as p
import base

class Action:
    def __init__(self, parent, keyboard, boundary = None):
        self.keyboard = keyboard

        self.parent = parent
        if boundary is None:
            self.boundary = parent.valid_mouse_position
        else:
            self.boundary = boundary

        self.keyPressed = None
        self.keyCooldown = 0
        self.modifier = None
        self.mouseDown = False

    def press(self):
        key = self.keyboard.retrieve(self.keyPressed, self.modifier)
        if key is None:
            return
        if callable(key):
            key(self.parent)
        else:
            self.parent.append(key)

    def update(self, event):
        self.modifier = base.get_modifier(event.keys)

        for e in event.events:
            if e.type == p.KEYDOWN and e.key in self.keyboard.map.keys():
                self.keyPressed = e.key
                self.press()
                self.keyCooldown = 10
            if e.type == p.KEYUP and e.key == self.keyPressed:
                self.keyPressed = None
            if e.type == p.MOUSEBUTTONDOWN:
                if self.boundary(event.mousePos):
                    coord = self.parent.get_mouse_coordinates(event.mousePos)
                    self.mouseDown = True
                    if self.modifier == "shift":
                        if self.parent.highlight.position is None:
                            self.parent.highlight.position = self.parent.cursor.position
                        self.parent.cursor.position = self.parent.get_position(coord)
                    else:
                        self.parent.cursor.position = self.parent.get_position(coord)
                        self.parent.cursor.blink = 0
                        self.parent.highlight.position = None

        if self.keyPressed is not None:
            if not event.keys[self.keyPressed]:
                self.keyPressed = None
            elif self.keyCooldown > 0:
                self.keyCooldown -= 1
            else:
                self.press()
                self.keyCooldown = 1

        if not event.mouse[0]:
            self.mouseDown = False
        if self.mouseDown:
            coord = self.parent.get_mouse_coordinates(event.mousePos)
            position = self.parent.get_position(coord)
            if position != self.parent.cursor.position:
                if position == self.parent.highlight.position:
                    self.parent.highlight.position = None
                elif self.parent.highlight.position is None:
                    self.parent.highlight.position = self.parent.cursor.position
                self.parent.cursor.position = position
                self.parent.cursor.blink = 0