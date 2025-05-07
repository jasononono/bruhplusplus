from font import Font
import dialogue
import base
import pygame as p
import os.path
from cursor import Cursor

class TextDisplay:
    def __init__(self, text = "", pos = (0, 0), size = (800, 600), margin = (10, 10), spacing = (0.6, 1.2),
                 font = "Menlo", fontSize = 14, bg = (33, 33, 43)):
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
        p.draw.rect(screen.surface, ((138, 138, 188) if screen.focus is self else (127, 127, 143)),
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
                 font = "Menlo", fontSize = 14, bg = (28, 28, 43)):
        super().__init__(text, pos, size, margin, spacing, font, fontSize, bg)

        from action import Action
        from keyboard import keyboard
        self.action = Action(self, keyboard)
        self.cursor = Cursor(0)
        self.highlight = Cursor()

        self.dialogue = {}

        self.fileName = None
        self.temporaryFileName = None
        self.fileContent = ""

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
            p.draw.rect(screen.surface, ((67, 67, 156) if screen.focus is self else (70, 70, 70)),
                        (coord[0], coord[1],
                         (int(self.font.size * self.spacing[0]) + 1 if text != '\n' else
                          self.x + self.width - coord[0] - self.margin[0]), int(self.font.size * self.spacing[1]) + 1))
        if text != '\n':
            screen.surface.blit(self.font.render(text), coord)

    def update(self, screen):
        super().update(screen)

        if screen.focus is self:
            if self.highlight.position is None:
                coord = self.get_coordinates(self.cursor.position)
                self.cursor.update(screen.surface, self.font, coord,
                                   (self.x + self.margin[0], self.y + self.margin[1]), self.spacing)

            self.action.update(screen.event)

        items = list(self.dialogue.items())
        for i, j in items:
            if j is not None:
                command = j.update(screen)
                if command is not None:
                    self.end_dialogue(i, j, command)

        if self.fileName is None:
            p.display.set_caption("Bruh++ Editor 3.0" if self.fileContent == self.text else "*Bruh++ Editor 3.0*")
        else:
            p.display.set_caption(self.fileName if self.fileContent == self.text else f"*{self.fileName}*")

    def end_dialogue(self, signature, instance, command):
        base.set_focus(self)

        if command is not False:
            if signature == "open_file":
                if os.path.exists(instance.textInput):
                    if self.fileContent != self.text:
                        self.dialogue["unsaved_file"] = dialogue.ConfirmDialogue(self, f"File contents unsaved. Save before exiting?",
                                                                                     (5, 5), "Warning")
                        self.temporaryFileName = instance.textInput
                    else:
                        self.read_file(instance.textInput)
                else:
                    self.dialogue["file_not_found"] = dialogue.Dialogue(self,f"File '{instance.textInput}' not found.",
                                                                        (5, 5), "Error", initial_focus = True)

            elif signature == "save_file":
                if os.path.exists(instance.textInput):
                    self.dialogue["conflicted_file_name"] = dialogue.ConfirmDialogue(self, f"File '{instance.textInput}' already exists. Replace?",
                                                                                     (5, 5), "Warning")
                    self.temporaryFileName = instance.textInput
                else:
                    self.write_file(instance.textInput)

            elif signature == "conflicted_file_name":
                self.write_file(self.temporaryFileName)

            elif signature == "unsaved_file":
                if self.fileName is None:
                    self.dialogue["save_file"] = dialogue.InputDialogue(self, "Save file as:",
                                                                        (5, 5), "Save File", ".bpp")
                else:
                    with open(self.fileName, 'w') as file:
                        file.write(self.text)
                        self.fileContent = self.text
                    self.read_file(self.temporaryFileName)

        self.dialogue[signature] = None

    def unfocus(self):
        base.set_focus()

    def write_file(self, name):
        with open(name, 'w') as file:
            file.write(self.text)
            self.fileContent = self.text
            self.fileName = name

    def read_file(self, name):
        if name is None:
            self.fileName = None
            self.fileContent = ""
            self.text = ""
            self.cursor.position = 0
        else:
            with open(name, 'r') as file:
                self.text = file.read()
                self.cursor.position = len(self.text)
                self.fileName = name
                self.fileContent = self.text
        self.highlight.position = None

    def open_file(self):
        self.dialogue["open_file"] = dialogue.InputDialogue(self, "Enter file name:",
                                                            (5, 5), "Open File", ".bpp")

    def save_file(self):
        if self.fileName is None:
            self.dialogue["save_file"] = dialogue.InputDialogue(self, "Save file as:",
                                                                (5, 5), "Save File", ".bpp")
        else:
            with open(self.fileName, 'w') as file:
                file.write(self.text)
                self.fileContent = self.text

    def new_file(self):
        if self.fileContent != self.text:
            self.dialogue["unsaved_file"] = dialogue.ConfirmDialogue(self,
                                                                     f"File contents unsaved. Save before exiting?",
                                                                     (5, 5), "Warning")
            self.temporaryFileName = None
        else:
            self.read_file(None)


    def unsaved_file(self):
        self.dialogue["unsaved_file"] = dialogue.ConfirmDialogue(self, f"File not saved. Save before exiting?",
                                                                                     (5, 5), "Warning")

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