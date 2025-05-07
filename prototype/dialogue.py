import pygame as p
import base
import icon
from font import Font
from cursor import Cursor


class ButtonTemplate:
    def __init__(self, parent, command, position = (0, 0), size = (19, 19),
                 colour = (55, 55, 65), highlight_colour = (45, 45, 55)):
        self.parent = parent
        self.command = command
        self.x, self.y = position
        self.absX, self.absY = self.x + parent.absX, self.y + parent.absY
        self.width, self.height = size
        self.colour = colour
        self.highlightColour = highlight_colour

    def update(self, screen):
        if screen.focus is self.parent and self.valid_mouse_position(screen.event.mousePos):
            p.draw.rect(screen.surface, self.highlightColour,
                        (self.absX, self.absY, self.width, self.height))
            if screen.event.mouse[0] and self.valid_mouse_position(screen.event.mousePos):
                return self.command
        else:
            p.draw.rect(screen.surface, self.colour,
                        (self.absX, self.absY, self.width, self.height))
        return None

    def valid_mouse_position(self, position):
        if (self.absX < position[0] < self.absX + self.width and
            self.absY < position[1] < self.absY + self.height):
            return True
        return False


class IconButton(ButtonTemplate):
    def __init__(self, parent, command, position = (0, 0), size = (19, 19), instruction = icon.x,
                 colour = (45, 45, 55), highlight_colour = (55, 55, 65)):
        super().__init__(parent, command, position, size, colour, highlight_colour)
        self.icon = icon.Icon(instruction)

    def update(self, screen):
        action = super().update(screen)
        self.icon.display(screen, (self.absX, self.absY))
        return action


class TextButton(ButtonTemplate):
    def __init__(self, parent, command, position = (0, 0), text = "Ok", fontSize = 13,
                 colour = (55, 55, 65), highlight_colour = (45, 45, 55)):
        self.text = text
        self.font = Font(size = fontSize, bold = True)
        super().__init__(parent, command, position, self.get_size(), colour, highlight_colour)

    def get_size(self):
        return [i + 10 for i in self.font.get_size(self.text)]

    def update(self, screen):
        action = super().update(screen)
        screen.surface.blit(self.font.render(self.text), (self.absX + 5, self.absY + 5))
        return action


class Dialogue:
    def __init__(self, parent, text = "Something went wrong.", position = (0, 0), title = "Notice",
                 life = 100, initial_focus = False):
        self.parent = parent
        self.text = text
        self.x, self.y = position
        self.absX, self.absY = self.parent.x + self.x, self.parent.y + self.y
        self.width, self.height = 0, 0
        self.title = title
        self.life = life
        self.age = 0

        self.font = Font(size = 12)
        self.titleFont = Font(size = 14, bold = True)
        self.size = self.font.get_size(text)
        self.titleSize = self.titleFont.get_size(title)
        self.set_size()

        self.close = IconButton(self, False, (2, 2))

        self.keybind = {}
        self.bind(p.K_ESCAPE, False)

        if initial_focus:
            base.set_focus(self)

    def bind(self, key, function):
        self.keybind[key] = function

    def set_size(self):
        self.width, self.height = self.get_size()

    def get_size(self):
        return max(self.titleSize[0] + 40, self.size[0]) + 20, self.titleSize[1] + self.size[1] + 26

    def update(self, screen):
        self.age += 1
        if self.age > self.life:
            return False
        if screen.focus is self:
            self.age = 0
        p.draw.rect(screen.surface, ((138, 138, 188) if screen.focus is self else (127, 127, 143)),
                    (self.absX - 1, self.absY - 1,
                     self.width + 2, self.height + 2))

        p.draw.rect(screen.surface, (55, 55, 65),
                    (self.absX, self.absY, self.width, self.height))
        p.draw.rect(screen.surface, (69, 69, 79),
                    (self.absX, self.absY, self.width, self.titleSize[1] + 6))

        screen.surface.blit(self.font.render(self.text),
                            (self.absX + 10, self.absY + self.titleSize[1] + 16))
        screen.surface.blit(self.titleFont.render(self.title),
                            (self.absX + 30, self.absY + 3))

        action = self.close.update(screen)
        if action is not None:
            return action

        if screen.focus is self:
            for i, j in self.keybind.items():
                if screen.event.keys[i]:
                    return j
        return None

    def valid_mouse_position(self, position):
        if (self.absX < position[0] < self.absX + self.width and
            self.absY < position[1] < self.absY + self.height):
            return True
        return False

class ButtonDialogue(Dialogue):
    def __init__(self, parent, text = "Confirm action?", options = None, position = (0, 0), title = "Notice",
                 life = float('inf'), initial_focus = True, option_offset = 0):
        if options is None:
            self.options = {"Confirm": True, "Cancel": False}
        else:
            self.options = options
        self.buttons = []
        self.buttonPosition = ()
        self.optionOffset = option_offset
        super().__init__(parent, text, position, title, life, initial_focus)

    def set_size(self):
        location = 10
        y_position = self.titleSize[1] + self.size[1] + self.optionOffset + 26
        for i, j in self.options.items():
            self.buttons.append(TextButton(self, j, (location, y_position), i))
            location += self.buttons[-1].get_size()[0] + 10
        self.buttonPosition = (location - 10, y_position)
        self.width, self.height = self.get_size()

    def get_size(self):
        return (max(self.titleSize[0] + 40, self.size[0], self.buttonPosition[0] - 10) + 20,
                self.buttonPosition[1] + self.buttons[-1].get_size()[1] + 10)

    def update(self, screen):
        action = super().update(screen)
        if action is not None:
            return action
        for i in self.buttons:
            button_action = i.update(screen)
            if button_action is not None:
                return button_action
        return None

class InputDialogue(ButtonDialogue):
    def __init__(self, parent, text = "Confirm action?", position = (0, 0),title = "Notice",
                 text_input = ""):
        self.inputFont = Font(size = 15)
        self.textInput = text_input
        super().__init__(parent, text, None, position, title,
                         option_offset = self.inputFont.get_size()[1] + 15)
        from action import Action
        from keyboard import inputKeyboard
        self.action = Action(self, inputKeyboard, self.valid_input_position)
        self.cursor = Cursor(0)
        self.highlight = Cursor()

        self.bind(p.K_RETURN, True)

    def get_size(self):
        return (max(self.titleSize[0] + 40, self.size[0],
                    max(200, self.inputFont.get_size(self.textInput)[0] + 10), self.buttonPosition[0] - 10) + 20,
                self.buttonPosition[1] + self.buttons[-1].get_size()[1] + 10)

    def valid_input_position(self, position):
        size = self.inputFont.get_size(self.textInput)
        y_position = self.absY + self.titleSize[1] + self.size[1] + 26
        if (self.absX + 10 < position[0] < self.absX + 10 + max(200, size[0] + 10) and
            y_position < position[1] < y_position + size[1] + 10):
            return True
        return False

    def get_mouse_coordinates(self, coord):
        previous = 0
        for i in range(1, len(self.textInput) + 1):
            result = self.absX + 10 + self.inputFont.get_size(self.text[:i])[0]
            if result > coord[0]:
                if result - coord[0] > coord[0] - previous:
                    return i - 2, 0
                return i - 1, 0
        return len(self.textInput), 0

    def get_position(self, coord):
        return coord[0]

    def update(self, screen):
        action = super().update(screen)
        size = self.inputFont.get_size(self.textInput)

        p.draw.rect(screen.surface, (45, 45, 55),
                    (self.absX + 10, self.absY + self.titleSize[1] + self.size[1] + 26,
                     max(200, size[0] + 10), size[1] + 10))

        if self.highlight.position is not None:
            minimum, maximum = (min(self.cursor.position, self.highlight.position),
                                max(self.cursor.position, self.highlight.position))
            p.draw.rect(screen.surface, ((67, 67, 156) if screen.focus is self else (70, 70, 70)),
                        (self.absX + 15 +
                         self.inputFont.get_size(self.textInput[:minimum])[0],
                         self.absY + self.titleSize[1] + self.size[1] + 31,
                         self.inputFont.get_size(self.textInput[minimum:maximum])[0],
                         size[1]))

        screen.surface.blit(self.inputFont.render(self.textInput),
                            (self.absX + 15, self.absY + self.titleSize[1] + self.size[1] + 31))
        self.width, self.height = self.get_size()

        if screen.focus is self:
            self.cursor.oneline_update(screen.surface, self.inputFont, self.textInput[:self.cursor.position],
                                       (self.absX + 15, self.absY + self.titleSize[1] + self.size[1] + 31))
            self.action.update(screen.event)

        return action

    def append(self, txt):
        if self.highlight.position is None:
            self.textInput = self.textInput[:self.cursor.position] + txt + self.textInput[self.cursor.position:]
            self.cursor.position += len(txt)
        else:
            self.textInput = (self.textInput[:min(self.cursor.position, self.highlight.position)] + txt +
                         self.textInput[max(self.cursor.position, self.highlight.position):])
            self.cursor.position = min(self.cursor.position, self.highlight.position) + len(txt)
        self.highlight.position = None

    def delete(self):
        if self.highlight.position is not None:
            self.textInput = (self.textInput[:min(self.cursor.position, self.highlight.position)] +
                         self.textInput[max(self.cursor.position, self.highlight.position):])
            self.cursor.position = min(self.cursor.position, self.highlight.position)
        elif self.cursor.position > 0:
            self.textInput = self.textInput[:self.cursor.position - 1] + self.textInput[self.cursor.position:]
            self.cursor.position -= 1
        self.highlight.position = None

    def cursor_left(self):
        if self.highlight.position is not None:
            self.cursor.position = min(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        elif self.cursor.position > 0:
            self.cursor.position -= 1
        self.cursor.blink = 0

    def cursor_right(self):
        if self.highlight.position is not None:
            self.cursor.position = max(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        elif self.cursor.position < len(self.textInput):
            self.cursor.position += 1
        self.cursor.blink = 0

    def cursor_down(self):
        self.cursor.position = 0
        self.highlight.position = 0
        self.cursor.blink = 0

    def cursor_up(self):
        self.cursor.position = len(self.textInput)
        self.highlight.position = len(self.textInput)
        self.cursor.blink = 0

    def highlight_left(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        if self.cursor.position > 0:
            self.cursor.position -= 1
        self.cursor.blink = 0

    def highlight_right(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        if self.cursor.position < len(self.textInput):
            self.cursor.position += 1
        self.cursor.blink = 0

    def highlight_down(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        self.cursor.position = len(self.textInput)
        self.cursor.blink = 0

    def highlight_up(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        self.cursor.position = 0
        self.cursor.blink = 0

    def select_all(self):
        self.highlight.position = 0
        self.cursor.position = len(self.textInput)