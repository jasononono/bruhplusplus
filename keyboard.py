########## IMPORT ##########

import pygame as p
import sys
from tkinter.filedialog import asksaveasfile

########## MODIFIER KEYS ##########

class null:
    pass

class shift:
    pass

class ctrl:
    pass

class alt:
    pass

class Msgbox:
    def __init__(self, msg, size, font, fontSize, msgOffset = 16):
        self.msg = msg
        self.width, self.height = size
        self.scrWidth , self.scrHeight = p.display.get_window_size()
        self.text = p.font.SysFont(font, fontSize).render(self.msg, True, [0, 0, 0])
        self.textRect = self.text.get_rect(center = [self.scrWidth / 2, (self.scrHeight - size[1]) / 2 + msgOffset])
        self.font = font
        self.fontSize = fontSize

    def Update(self, scr):
        p.draw.rect(scr, [255, 255, 255], [(self.scrWidth - self.width) / 2, (self.scrHeight - self.height) / 2, self.width, self.height])
        scr.blit(self.text, self.textRect)

    def KeyPressed(self, event):
        if event.key == p.K_ESCAPE or event.key == p.K_RETURN:
            return None
        return self

class FileInput(Msgbox):
    def __init__(self, msg, intent, size, font, fontSize, msgOffset = 25, inputOffset = 40):
        super().__init__(msg, size, font, fontSize, msgOffset)
        self.inputTxt = ''
        self.inputOffset = inputOffset
        self.intent = intent

    def Update(self, scr):
        super().Update(scr)
        inputText = p.font.SysFont(self.font, self.fontSize).render(self.inputTxt + '.bpp', True, [0, 0, 0])
        p.draw.rect(scr, [0, 0, 0], [(self.scrWidth - self.width) / 2 + 10, (self.scrHeight + self.height) / 2 - self.inputOffset, self.width - 20, self.fontSize * 1.6], 2)
        scr.blit(inputText, [(self.scrWidth - self.width) / 2 + 15, (self.scrHeight + self.height) / 2 - self.inputOffset + 5])

    def KeyPressed(self, event):
        if event.unicode.lower() in '1234567890qwertyuiopasdfghjklzxcvbnm-_':
            self.inputTxt += event.unicode
        elif event.key == p.K_BACKSPACE:
            self.inputTxt = self.inputTxt[:-1]
        elif event.key == p.K_RETURN:
            return [self.inputTxt, self.intent]
        return super().KeyPressed(event)
        

########## FUNCTIONS ##########

def delete(editor):
    if editor.cursor.highlight is not None:
        editor.text = editor.text[:min(editor.cursor.pos, editor.cursor.highlight)] + editor.text[max(editor.cursor.pos, editor.cursor.highlight):]
        editor.cursor.pos = min(editor.cursor.pos, editor.cursor.highlight)
    elif editor.cursor.pos > 0:
        editor.text = editor.text[:editor.cursor.pos - 1] + editor.text[editor.cursor.pos:]
        editor.cursor.pos -= 1
    editor.cursor.highlight = None
    return editor

def quickdel(editor):
    if editor.cursor.highlight is not None:
        return delete(editor)
    for i in range(editor.cursor.pos - 2, -1, -1):
        if editor.text[i] == ' ' or editor.text[i] == '\n':
            editor.text = editor.text[:i + 1] + editor.text[editor.cursor.pos:]
            editor.cursor.pos = i + 1
            return editor
    editor.text = editor.text[editor.cursor.pos:]
    editor.cursor.pos = 0
    return editor
        
def indent(editor):
    if editor.cursor.highlight is None:
        editor.text = editor.text[:editor.cursor.pos] + '   ' + editor.text[editor.cursor.pos:]
        editor.cursor.pos += 3
    else:
        editor.text = editor.text[:min(editor.cursor.pos, editor.cursor.highlight)] + '   ' + editor.text[max(editor.cursor.pos, editor.cursor.highlight):]
        editor.cursor.pos = min(editor.cursor.pos, editor.cursor.highlight) + 3
    editor.cursor.highlight = None
    return editor

def dedent(editor):
    return editor

def highlightAll(editor):
    editor.cursor.highlight = 0
    editor.cursor.pos = len(editor.text)
    return editor

def cursorLeft(editor):
    if editor.cursor.highlight is not None:
        editor.cursor.highlight = None
    elif editor.cursor.pos > 0:
        editor.cursor.pos -= 1
    editor.cursor.blink = 0
    return editor

def cursorRight(editor):
    if editor.cursor.highlight is not None:
        editor.cursor.highlight = None
    elif editor.cursor.pos < len(editor.text):
        editor.cursor.pos += 1
    editor.cursor.blink = 0
    return editor

def cursorDown(editor):
    if editor.cursor.highlight is not None:
        editor.cursor.highlight = None
    else:
        row, column, l = editor.PosToCoord(editor.cursor.pos)
        if row == len(l) - 1:
            editor.cursor.pos = len(editor.text)
        elif editor.cursor.pos < len(editor.text):
            editor.cursor.pos = editor.CoordToPos(row + 1, column, l)
    editor.cursor.blink = 0
    return editor

def cursorUp(editor):
    if editor.cursor.highlight is not None:
        editor.cursor.highlight = None
    else:
        row, column, l = editor.PosToCoord(editor.cursor.pos)
        if row == 0:
            editor.cursor.pos = 0
        elif editor.cursor.pos > 0:
            editor.cursor.pos = editor.CoordToPos(row - 1, column, l)
    editor.cursor.blink = 0
    return editor

def saveFile(editor):
    if editor.fileName is None:
        editor.msgbox = FileInput('Save file as:', 'w', [200, 100], 'Menlo', 20)
    else:
        with open(editor.fileName + '.bpp', 'w') as f:
            f.write(editor.text)
        editor.lastSaved = editor.text
    return editor

def newFile(editor):
    editor.text = ''
    editor.lastSaved = ''
    editor.cursor.pos = 0
    editor.fileName = None

def openFile(editor):
    editor.msgbox = FileInput('Open file named:', 'r', [250, 100], 'Menlo', 20)
    return editor

def halt(editor):
    p.quit()
    sys.exit()
    

########## KEYBOARD ##########

class Keyboard:
    def __init__(self):
        self.map = {}
        
    def Assign(self, key, raw = None, s = None, c = None, a = None):
        self.map[key] = {None: raw, shift: s, ctrl: c, alt: a}

KB = Keyboard()

KB.Assign(p.K_LEFT, cursorLeft)
KB.Assign(p.K_RIGHT, cursorRight)
KB.Assign(p.K_DOWN, cursorDown)
KB.Assign(p.K_UP, cursorUp)
KB.Assign(p.K_BACKSPACE, delete, c = quickdel)
KB.Assign(p.K_TAB, indent)
KB.Assign(p.K_RETURN, '\n', '\n')
KB.Assign(p.K_SPACE, ' ', ' ')
KB.Assign(p.K_1, '1', '!')
KB.Assign(p.K_2, '2', '@')
KB.Assign(p.K_3, '3', '#')
KB.Assign(p.K_4, '4', '$')
KB.Assign(p.K_5, '5', '%')
KB.Assign(p.K_6, '6', '^')
KB.Assign(p.K_7, '7', '&')
KB.Assign(p.K_8, '8', '*')
KB.Assign(p.K_9, '9', '(')
KB.Assign(p.K_0, '0', ')')
KB.Assign(p.K_BACKQUOTE, '`', '~')
KB.Assign(p.K_MINUS, '-', '_')
KB.Assign(p.K_EQUALS, '=', '+')
KB.Assign(p.K_LEFTBRACKET, '[', '{')
KB.Assign(p.K_RIGHTBRACKET, ']', '}')
KB.Assign(p.K_BACKSLASH, '\\', '|')
KB.Assign(p.K_SEMICOLON, ';', ':')
KB.Assign(p.K_QUOTE, "'", '"')
KB.Assign(p.K_COMMA, ',', '<')
KB.Assign(p.K_PERIOD, '.', '>')
KB.Assign(p.K_SLASH, '/', '?')
KB.Assign(p.K_q, 'q', 'Q')
KB.Assign(p.K_w, 'w', 'W', halt)
KB.Assign(p.K_e, 'e', 'E')
KB.Assign(p.K_r, 'r', 'R')
KB.Assign(p.K_t, 't', 'T')
KB.Assign(p.K_y, 'y', 'Y')
KB.Assign(p.K_u, 'u', 'U')
KB.Assign(p.K_i, 'i', 'I')
KB.Assign(p.K_o, 'o', 'O', openFile)
KB.Assign(p.K_p, 'p', 'P')
KB.Assign(p.K_a, 'a', 'A', highlightAll)
KB.Assign(p.K_s, 's', 'S', saveFile)
KB.Assign(p.K_d, 'd', 'D')
KB.Assign(p.K_f, 'f', 'F')
KB.Assign(p.K_g, 'g', 'G')
KB.Assign(p.K_h, 'h', 'H')
KB.Assign(p.K_j, 'j', 'J')
KB.Assign(p.K_k, 'k', 'K')
KB.Assign(p.K_l, 'l', 'L')
KB.Assign(p.K_z, 'z', 'Z')
KB.Assign(p.K_x, 'x', 'X')
KB.Assign(p.K_c, 'c', 'C')
KB.Assign(p.K_v, 'v', 'V')
KB.Assign(p.K_b, 'b', 'B')
KB.Assign(p.K_n, 'n', 'N', newFile)
KB.Assign(p.K_m, 'm', 'M')
