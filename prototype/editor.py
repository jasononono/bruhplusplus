from font import Font
import dialogue
import base
import pygame as p

class Cursor:
    def __init__(self, position = None):
        self.position = position
        self.blinkRate = 15
        self.blink = 0
        self.colour = (255, 255, 255)

    def update(self, surface, fontSize, coord, spacing, offset):
        self.tick()
        if self.blink < self.blinkRate:
            p.draw.rect(surface, self.colour, (offset[0] + coord[0] * fontSize * spacing[0],
                                                    offset[1] + coord[1] * fontSize * spacing[1], 1, fontSize))

    def tick(self):
        self.blink = (self.blink + 1) % (self.blinkRate * 2)


class TextDisplay:
    def __init__(self, text = "", pos = (0, 0), size = (800, 600), margin = (10, 10), spacing = (0.6, 1.2),
                 font = "Menlo", fontSize = 15, bg = (33, 33, 43)):
        self.text = text
        self.font = Font(font, fontSize)

        self.x, self.y = pos
        self.width, self.height = size
        self.margin = margin
        self.spacing = spacing
        self.bg = bg
        self.grid = []

    def valid_mouse_position(self, position):
        if (position[0] < self.x or position[0] > self.x + self.width or
                position[1] < self.y or position[1] > self.y + self.height):
            return False
        return True

    def display(self, screen, text, index, position):
        coord = (self.x + self.margin[0] + position[0] * self.font.size * self.spacing[0],
                 self.y + self.margin[1] + position[1] * self.font.size * self.spacing[1])
        if text != '\n':
            screen.surface.blit(self.font.render(text), coord)

    def get_grid(self):
        row, column = 0, 0
        self.grid = []
        for n, i in enumerate(self.text):
            if i == '\n':
                self.grid.append(column)
                column = 0
                row += 1
            else:
                column += 1
        self.grid.append(column)
        return self.grid

    def update(self, screen):
        if screen.focus is self:
            p.draw.rect(screen.surface, (142, 142, 209),
                        (self.x - 1, self.y - 1, self.width + 2, self.height + 2))
        p.draw.rect(screen.surface, self.bg, (self.x, self.y, self.width, self.height))

        row, column = 0, 0
        self.grid = []

        for n, i in enumerate(self.text):
            self.display(screen, i, n, (column, row))
            if i == '\n':
                self.grid.append(column)
                column = 0
                row += 1
            else:
                column += 1
        self.grid.append(column)

    def set_pos(self, pos = None):
        self.x, self.y = pos

    def resize(self, size = None):
        self.width, self.height = size

class TextEditor(TextDisplay):
    def __init__(self, text = "", pos = (0, 0), size = (800, 600), margin = (10, 10), spacing = (0.6, 1.2),
                 font = "Menlo", fontSize = 15, bg = (28, 28, 43)):
        super().__init__(text, pos, size, margin, spacing, font, fontSize, bg)

        from editorAction import EditorAction
        self.action = EditorAction(self)
        self.cursor = Cursor(0)
        self.highlight = Cursor()

        self.dialogue = {}

        self.fileName = None
        self.fileContents = None

    def get_coordinates(self, pos):
        if pos < 0:
            return 0, 0
        total = 0
        for i, j in enumerate(self.grid):
            total += j + 1
            if pos < total:
                return pos - total + j + 1, i
        return self.get_coordinates(len(self.text))

    def get_position(self, coord):
        column = max(coord[0], 0)
        row = max(coord[1], 0)
        pos = sum(self.grid[:row]) + row + min(self.grid[row], column)
        return min(len(self.text), max(0, pos))

    def get_mouse_coordinates(self, coord):
        column = round((coord[0] - self.x - self.margin[0]) / self.spacing[0] / self.font.size)
        row = min(int((coord[1] - self.y - self.margin[1]) / self.spacing[1] / self.font.size), len(self.grid) - 1)
        return column, row

    def display(self, screen, text, index, position):
        coord = (self.x + self.margin[0] + position[0] * self.font.size * self.spacing[0],
                 self.y + self.margin[1] + position[1] * self.font.size * self.spacing[1])
        highlighted = (self.highlight.position is not None and min(self.cursor.position, self.highlight.position) <=
                       index < max(self.cursor.position, self.highlight.position))

        if highlighted:
            rect = (coord[0], coord[1],
                    (self.font.size * self.spacing[0] if text != '\n' else
                     self.x + self.width - coord[0] - self.margin[0]), self.font.size * self.spacing[1])
            p.draw.rect(screen.surface, ((67, 67, 156) if screen.focus is self else (70, 70, 70)), rect)
        if text != '\n':
            screen.surface.blit(self.font.render(text), coord)

    def update(self, screen):
        super().update(screen)

        if screen.focus is self:
            if self.highlight.position is None:
                coord = self.get_coordinates(self.cursor.position)
                self.cursor.update(screen.surface, self.font.size, coord, self.spacing,
                                   (self.x + self.margin[0], self.y + self.margin[1]))
            self.action.update(screen.event)

        for i in self.dialogue.values():
            if i is not None:
                command = i.update(screen)
                if command is not None:
                    command(i)
        p.display.set_caption("untitled")

    def exit_dialogue(self, instance):
        self.dialogue[instance.signature] = None
        base.set_focus(self)

    def unfocus(self):
        base.set_focus()

    def open_file(self):
        self.dialogue["open_file"] = dialogue.Dialogue(self, "open_file",
                                                       "This feature is yet to be implemented.", (5, 5))

    def append(self, txt):
        if self.highlight.position is None:
            self.text = self.text[:self.cursor.position] + txt + self.text[self.cursor.position:]
            self.cursor.position += len(txt)
        else:
            self.text = (self.text[:min(self.cursor.position, self.highlight.position)] + txt +
                         self.text[max(self.cursor.position, self.highlight.position):])
            self.cursor.position = min(self.cursor.position, self.highlight.position) + len(txt)
        self.highlight.position = None

    def delete(self):
        if self.highlight.position is not None:
            self.text = (self.text[:min(self.cursor.position, self.highlight.position)] +
                         self.text[max(self.cursor.position, self.highlight.position):])
            self.cursor.position = min(self.cursor.position, self.highlight.position)
        elif self.cursor.position > 0:
            self.text = self.text[:self.cursor.position - 1] + self.text[self.cursor.position:]
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
        elif self.cursor.position < len(self.text):
            self.cursor.position += 1
        self.cursor.blink = 0

    def cursor_down(self):
        if self.highlight.position is not None:
            self.cursor.position = max(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = len(self.text) if row == len(self.grid) - 1 else self.get_position((row + 1, column))
        self.cursor.blink = 0

    def cursor_up(self):
        if self.highlight.position is not None:
            self.cursor.position = min(self.cursor.position, self.highlight.position)
            self.highlight.position = None
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = 0 if row == 0 else self.get_position((row - 1, column))
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
        if self.cursor.position < len(self.text):
            self.cursor.position += 1
        self.cursor.blink = 0

    def highlight_down(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = len(self.text) if row == len(self.grid) - 1 else self.get_position((row + 1, column))
        self.cursor.blink = 0

    def highlight_up(self):
        if self.highlight.position is None:
            self.highlight.position = self.cursor.position
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = 0 if row == 0 else self.get_position((row - 1, column))
        self.cursor.blink = 0

    def select_all(self):
        self.highlight.position = 0
        self.cursor.position = len(self.text)

    def indent(self):
        self.append("    ")