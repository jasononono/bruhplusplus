import pygame as p
from keyboard import keyboard

class EditorAction:
    def __init__(self, parent):
        self.keyboard = keyboard

        self.editor = parent

        self.keyPressed = None
        self.keyCooldown = 0
        self.modifier = None
        self.mouseDown = False

    def get_modifier(self, keys):
        shift = keys[p.K_LSHIFT] or keys[p.K_RSHIFT]
        ctrl = keys[p.K_LCTRL] or keys[p.K_RCTRL] or keys[p.K_LMETA] or keys[p.K_RMETA]
        alt = keys[p.K_LALT] or keys[p.K_RALT]

        if shift + ctrl + alt > 1:
            return None
        if shift:
            return "shift"
        if ctrl:
            return "ctrl"
        if alt:
            return "alt"
        return None

    def press(self):
        key = self.keyboard.retrieve(self.keyPressed, self.modifier)
        if key is None:
            return
        if callable(key):
            key(self.editor)
        else:
            self.editor.append(key)

    def update(self, event):
        self.modifier = self.get_modifier(event.keys)

        for e in event.events:
            if e.type == p.KEYDOWN and e.key in self.keyboard.map.keys():
                self.keyPressed = e.key
                self.press()
                self.keyCooldown = 10
            if e.type == p.KEYUP and e.key == self.keyPressed:
                self.keyPressed = None
            if e.type == p.MOUSEBUTTONDOWN:
                coord = self.editor.get_mouse_coordinates(event.mousePos)
                if self.editor.valid_mouse_position(event.mousePos):
                    self.mouseDown = True
                    if self.modifier == "shift":
                        if self.editor.highlight.position is None:
                            self.editor.highlight.position = self.editor.cursor.position
                        self.editor.cursor.position = self.editor.get_position(coord)
                    else:
                        self.editor.cursor.position = self.editor.get_position(coord)
                        self.editor.cursor.blink = 0
                        self.editor.highlight.position = None

        if self.keyPressed is not None:
            if self.keyCooldown > 0:
                self.keyCooldown -= 1
            else:
                self.press()
                self.keyCooldown = 1

        if not event.mouse[0]:
            self.mouseDown = False
        if self.mouseDown:
            coord = self.editor.get_mouse_coordinates(event.mousePos)
            position = self.editor.get_position(coord)
            if position != self.editor.cursor.position:
                if position == self.editor.highlight.position:
                    self.editor.highlight.position = None
                elif self.editor.highlight.position is None:
                    self.editor.highlight.position = self.editor.cursor.position
                self.editor.cursor.position = position
                self.editor.cursor.blink = 0