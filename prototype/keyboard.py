import pygame as p
from editorTemplate import TextEditorTemplate

class Key:
    def __init__(self, base = None, shift = None, ctrl = None, alt = None):
        self.base = base
        self.shift = shift
        self.ctrl = ctrl
        self.alt = alt

    def __repr__(self):
        return self.base

class Keyboard:
    def __init__(self):
        self.map = {}

    def assign(self, key, base = None, shift = None, ctrl = None, alt = None):
        self.map[key] = Key(base, shift, ctrl, alt)

    def retrieve(self, key, modifier = None):
        if modifier == "shift":
            return self.map[key].shift
        if modifier == "ctrl":
            return self.map[key].ctrl
        if modifier == "alt":
            return self.map[key].alt

        return self.map[key].base

keyboard = Keyboard()

keyboard.assign(p.K_LEFT, TextEditorTemplate.cursor_left, TextEditorTemplate.highlight_left)
keyboard.assign(p.K_RIGHT, TextEditorTemplate.cursor_right, TextEditorTemplate.highlight_right)
keyboard.assign(p.K_DOWN, TextEditorTemplate.cursor_down, TextEditorTemplate.highlight_down)
keyboard.assign(p.K_UP, TextEditorTemplate.cursor_up, TextEditorTemplate.highlight_up)
keyboard.assign(p.K_BACKSPACE, TextEditorTemplate.delete)
keyboard.assign(p.K_TAB, TextEditorTemplate.indent)
keyboard.assign(p.K_RETURN, '\n')
keyboard.assign(p.K_SPACE, ' ', ' ')
keyboard.assign(p.K_1, '1', '!')
keyboard.assign(p.K_2, '2', '@')
keyboard.assign(p.K_3, '3', '#')
keyboard.assign(p.K_4, '4', '$')
keyboard.assign(p.K_5, '5', '%')
keyboard.assign(p.K_6, '6', '^')
keyboard.assign(p.K_7, '7', '&')
keyboard.assign(p.K_8, '8', '*')
keyboard.assign(p.K_9, '9', '(')
keyboard.assign(p.K_0, '0', ')')
keyboard.assign(p.K_BACKQUOTE, '`', '~')
keyboard.assign(p.K_MINUS, '-', '_')
keyboard.assign(p.K_EQUALS, '=', '+')
keyboard.assign(p.K_LEFTBRACKET, '[', '{')
keyboard.assign(p.K_RIGHTBRACKET, ']', '}')
keyboard.assign(p.K_BACKSLASH, '\\', '|')
keyboard.assign(p.K_SEMICOLON, ';', ':')
keyboard.assign(p.K_QUOTE, "'", '"')
keyboard.assign(p.K_COMMA, ',', '<')
keyboard.assign(p.K_PERIOD, '.', '>')
keyboard.assign(p.K_SLASH, '/', '?')
keyboard.assign(p.K_q, 'q', 'Q')
keyboard.assign(p.K_w, 'w', 'W')
keyboard.assign(p.K_e, 'e', 'E')
keyboard.assign(p.K_r, 'r', 'R')
keyboard.assign(p.K_t, 't', 'T')
keyboard.assign(p.K_y, 'y', 'Y')
keyboard.assign(p.K_u, 'u', 'U')
keyboard.assign(p.K_i, 'i', 'I')
keyboard.assign(p.K_o, 'o', 'O')
keyboard.assign(p.K_p, 'p', 'P')
keyboard.assign(p.K_a, 'a', 'A')
keyboard.assign(p.K_s, 's', 'S')
keyboard.assign(p.K_d, 'd', 'D')
keyboard.assign(p.K_f, 'f', 'F')
keyboard.assign(p.K_g, 'g', 'G')
keyboard.assign(p.K_h, 'h', 'H')
keyboard.assign(p.K_j, 'j', 'J')
keyboard.assign(p.K_k, 'k', 'K')
keyboard.assign(p.K_l, 'l', 'L')
keyboard.assign(p.K_z, 'z', 'Z')
keyboard.assign(p.K_x, 'x', 'X')
keyboard.assign(p.K_c, 'c', 'C')
keyboard.assign(p.K_v, 'v', 'V')
keyboard.assign(p.K_b, 'b', 'B')
keyboard.assign(p.K_n, 'n', 'N')
keyboard.assign(p.K_m, 'm', 'M')