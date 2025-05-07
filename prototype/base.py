import pygame as p

def set_focus(focus = None):
    global pendingFocus
    pendingFocus = focus
pendingFocus = False

def get_modifier(keys):
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