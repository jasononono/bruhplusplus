from font import Font
import pygame as p

class Cursor:
    def __init__(self, position = None):
        self.position = position
        self.blinkRate = 15
        self.blink = 0
        self.colour = (0, 0, 0)

    def update(self, surface, fontSize, coord, spacing, offset):
        self.tick()
        if self.blink < self.blinkRate:
            p.draw.rect(surface, self.colour, (offset[0] + coord[0] * fontSize * spacing[0],
                                                    offset[1] + coord[1] * fontSize * spacing[1], 1, fontSize))

    def tick(self):
        self.blink = (self.blink + 1) % (self.blinkRate * 2)


class TextDisplay:
    def __init__(self, text = "", pos = (0, 0), size = (800, 600), margin = (10, 10), spacing = (0.6, 1.2),
                 font = "Menlo", fontSize = 15, bg = (255, 255, 255)):
        self.text = text
        self.font = Font(font, fontSize)

        self.x, self.y = pos
        self.width, self.height = size
        self.margin = margin
        self.spacing = spacing
        self.bg = bg
        self.grid = []

    def display(self, surface, text, index, position):
        coord = (self.x + self.margin[0] + position[0] * self.font.size * self.spacing[0],
                 self.y + self.margin[1] + position[1] * self.font.size * self.spacing[1])
        if text != '\n':
            surface.blit(self.font.render(text), coord)

    def update(self, surface):
        p.draw.rect(surface, self.bg, [self.x, self.y, self.width, self.height])

        row, column = 0, 0
        self.grid = []

        for n, i in enumerate(self.text):

            self.display(surface, i, n, (column, row))
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
                 font = "Menlo", fontSize = 15, bg = (255, 255, 255)):
        super().__init__(text, pos, size, margin, spacing, font, fontSize, bg)
        self.cursor = Cursor(0)
        self.highlight = Cursor()

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
        pos = sum(self.grid[:coord[0]]) + coord[0] + min(self.grid[coord[0]], coord[1])
        return min(len(self.text), max(0, pos))

    def get_mouse_coordinates(self, coord):
        if (coord[0] < self.x or coord[0] > self.x + self.width or
            coord[1] < self.y or coord[1] > self.y + self.height):
           return None
        column = round((coord[0] - self.x - self.margin[0]) / self.spacing[0] / self.font.size)
        row = min(int((coord[1] - self.y - self.margin[1]) / self.spacing[1] / self.font.size), len(self.grid) - 1)
        return row, column

    def display(self, surface, text, index, position):
        coord = (self.x + self.margin[0] + position[0] * self.font.size * self.spacing[0],
                 self.y + self.margin[1] + position[1] * self.font.size * self.spacing[1])
        highlighted = (self.highlight.position is not None and min(self.cursor.position, self.highlight.position) <=
                       index < max(self.cursor.position, self.highlight.position))

        if text == '\n':
            if highlighted:
                p.draw.rect(surface, (170, 170, 170),
                            (coord[0], coord[1], self.x + self.width - coord[0], self.font.size * self.spacing[1]))
        elif highlighted:
            surface.blit(self.font.render(text, (255, 255, 255), (170, 170, 170)), coord)
        else:
            surface.blit(self.font.render(text), coord)

    def update(self, surface):
        super().update(surface)

        if self.highlight.position is None:
            coord = self.get_coordinates(self.cursor.position)
            self.cursor.update(surface, self.font.size, coord, self.spacing,
                               (self.x + self.margin[0], self.y + self.margin[1]))

    def append(self, txt):
        self.text = self.text[:self.cursor.position] + txt + self.text[self.cursor.position:]
        self.cursor.position += len(txt)

    def delete(self):
        if self.cursor.position > 0:
            self.text = self.text[:self.cursor.position - 1] + self.text[self.cursor.position:]
            self.cursor.position -= 1

    def indent(self):
        self.append("    ")

    def cursor_left(self):
        if self.cursor.position > 0:
            self.cursor.position -= 1
        self.cursor.blink = 0

    def cursor_right(self):
        if self.cursor.position < len(self.text):
            self.cursor.position += 1
        self.cursor.blink = 0

    def cursor_down(self):
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = len(self.text) if row == len(self.grid) - 1 else self.get_position((row + 1, column))
        self.cursor.blink = 0

    def cursor_up(self):
        column, row = self.get_coordinates(self.cursor.position)
        self.cursor.position = 0 if row == 0 else self.get_position((row - 1, column))
        self.cursor.blink = 0