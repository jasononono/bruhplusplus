import pygame as p
import base
from font import Font


class ButtonTemplate:
    def __init__(self, parent, command, position = (0, 0), size = (19, 19)):
        self.parent = parent
        self.command = command
        self.x, self.y = position
        self.width, self.height = size

    def update(self, screen):
        origin = self.parent.get_absolute_position()
        if screen.focus is self.parent and self.valid_mouse_position(screen.event.mousePos):
            p.draw.rect(screen.surface, (55, 55, 65),
                        (origin[0] + self.x, origin[1] + self.y, self.width, self.height))
            if screen.event.mouse[0] and self.valid_mouse_position(screen.event.mousePos):
                return self.command
        else:
            p.draw.rect(screen.surface, (45, 45, 55),
                        (origin[0] + self.x, origin[1] + self.y, self.width, self.height))
        return None

    def valid_mouse_position(self, position):
        origin = self.parent.get_absolute_position()
        if (origin[0] + self.x < position[0] < origin[0] + self.x + self.width and
            origin[1] + self.y < position[1] < origin[1] + self.y + self.height):
            return True
        return False


class IconButton(ButtonTemplate):
    def __init__(self, parent, command, position = (0, 0), size = (19, 19), icon = "x"):
        super().__init__(parent, command, position, size)


class Dialogue:
    def __init__(self, parent, signature, text = "Something went wrong.", position = (0, 0), title = "Notice",
                 life = 100, initial_focus = False):
        self.parent = parent
        self.signature = signature
        self.text = text
        self.x, self.y = position
        self.title = title
        self.life = life
        self.age = 0

        self.font = Font(size = 12)
        self.titleFont = Font(size = 14, bold = True)
        self.size = self.font.get_size(text)
        self.titleSize = self.titleFont.get_size(title)
        self.width, self.height = max(self.titleSize[0] + 40, self.size[0]) + 20, self.titleSize[1] + self.size[1] + 26

        self.close = ButtonTemplate(self, parent.exit_dialogue, (2, 2))

        self.keybind = {}
        self.bind(p.K_ESCAPE, parent.exit_dialogue)

        if initial_focus:
            base.set_focus(self)

    def bind(self, key, function):
        self.keybind[key] = function

    def get_absolute_position(self):
        return self.parent.x + self.x, self.parent.y + self.y

    def update(self, screen):
        self.age += 1
        if self.age > self.life:
            return self.parent.exit_dialogue
        if screen.focus is self:
            self.age = 0
            p.draw.rect(screen.surface, (142, 142, 209),
                        (self.parent.x + self.x - 1, self.parent.y + self.y - 1,
                         self.width + 2, self.height + 2))

        p.draw.rect(screen.surface, (55, 55, 65),
                    (self.parent.x + self.x, self.parent.y + self.y, self.width, self.height))
        p.draw.rect(screen.surface, (69, 69, 79),
                    (self.parent.x + self.x, self.parent.y + self.y, self.width, self.titleSize[1] + 6))

        screen.surface.blit(self.font.render(self.text),
                            (self.parent.x + self.x + 10, self.parent.y + self.y + self.titleSize[1] + 16))
        screen.surface.blit(self.titleFont.render(self.title),
                            (self.parent.x + self.x + 30, self.parent.y + self.y + 3))

        action = self.close.update(screen)
        if action is not None:
            return action

        if screen.focus is self:
            for i, j in self.keybind.items():
                if screen.event.keys[i]:
                    return j
        return None

    def valid_mouse_position(self, position):
        if (self.parent.x + self.x < position[0] < self.parent.x + self.x + self.width and
            self.parent.y + self.y < position[1] < self.parent.y + self.y + self.height):
            return True
        return False