import pygame as p
from editorTemplate import TextEditorTemplate
from keyboard import keyboard

class TextEditor:
    def __init__(self, text = "", pos = (0, 0), size = (800, 600), margin = (10, 10), spacing = (0.6, 1.2),
                 font = "Menlo", fontSize = 15, bg = (255, 255, 255)):
        self.template = TextEditorTemplate(text, pos, size, margin, spacing, font, fontSize, bg)
        self.keyboard = keyboard

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
            key(self.template)
        else:
            self.template.append(key)

    def update(self, surface, events, keys, mouse, mouse_pos):
        self.modifier = self.get_modifier(keys)

        for e in events:
            if e.type == p.KEYDOWN and e.key in self.keyboard.map.keys():
                self.keyPressed = e.key
                self.press()
                self.keyCooldown = 10
            if e.type == p.KEYUP and e.key == self.keyPressed:
                self.keyPressed = None
            if e.type == p.MOUSEBUTTONDOWN:
                coord = self.template.get_mouse_coordinates(mouse_pos)
                if self.template.valid_mouse_position(mouse_pos):
                    self.mouseDown = True
                    if self.modifier == "shift":
                        if self.template.highlight.position is None:
                            self.template.highlight.position = self.template.cursor.position
                        self.template.cursor.position = self.template.get_position(coord)
                    else:
                        self.template.cursor.position = self.template.get_position(coord)
                        self.template.cursor.blink = 0
                        self.template.highlight.position = None

        if self.keyPressed is not None:
            if self.keyCooldown > 0:
                self.keyCooldown -= 1
            else:
                self.press()
                self.keyCooldown = 1

        if not mouse[0]:
            self.mouseDown = False
        if self.mouseDown:
            coord = self.template.get_mouse_coordinates(mouse_pos)
            position = self.template.get_position(coord)
            if position != self.template.cursor.position:
                if position == self.template.highlight.position:
                    self.template.highlight.position = None
                elif self.template.highlight.position is None:
                    self.template.highlight.position = self.template.cursor.position
                self.template.cursor.position = position
                self.template.cursor.blink = 0

        self.template.update(surface)