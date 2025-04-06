from keyboard import *

class Cursor:
    def __init__(self, size):
        self.size = size
        self.blinkRate = 40
        self.blink = 0
        self.pos = 0
        self.highlight = None

    def Update(self, scr, row, column, topMargin, sideMargin, lineSpacing, charSpacing):
        self.blink = (self.blink + 1) % self.blinkRate
        if self.blink < (self.blinkRate - 1) / 2 and self.highlight is None:
            pos = [sideMargin + self.size * column * charSpacing, topMargin + row * self.size * lineSpacing]
            p.draw.rect(scr, [0, 0, 0], [pos[0], pos[1], 1, self.size])

class Editor:
    def __init__(self, fontName, fontSize):
        self.text = ''
        self.colour = []
        self.fontSize = fontSize
        self.font = p.font.SysFont(fontName, fontSize)
        self.cursor = Cursor(fontSize)
        self.topMargin = 10
        self.sideMargin = 10
        self.lineSpacing = 1.2
        self.charSpacing = 0.6
        self.msgbox = None
        self.fileName = None
        self.lastSaved = ''
        
    def Update(self, scr):
        row = 0
        column = 0
        for n, i in enumerate(self.text):
            pos = [self.sideMargin + column * self.fontSize * self.charSpacing, self.topMargin + row * self.fontSize * self.lineSpacing]
            highlighted = self.cursor.highlight is not None and min(self.cursor.pos, self.cursor.highlight) <= n < max(self.cursor.pos, self.cursor.highlight)
            if i == '\n':
                column = 0
                row += 1
                if highlighted:
                    p.draw.rect(scr, [150, 150, 150], [pos[0], pos[1], scrWidth, self.fontSize * self.lineSpacing])
            else:
                if highlighted:
                    scr.blit(self.font.render(i, True, [255, 255, 255], [150, 150, 150]), pos)
                else:
                    scr.blit(self.font.render(i, True, self.colour[n]), pos)
                    
                column += 1

        coord = self.PosToCoord(self.cursor.pos)
        self.cursor.Update(scr, coord[0], coord[1], self.topMargin, self.sideMargin, self.lineSpacing, self.charSpacing)

    def PosToCoord(self, pos = 0):
        row = 0
        column = 0
        l = []
        for i in range(pos):
            if self.text[i] == '\n':
                l.append(column)
                column = -1
                row += 1
            column += 1
        resRow, resCol = row, column
        for i in range(pos, len(self.text)):
            if self.text[i] == '\n':
                l.append(column)
                column = -1
                row += 1
            column += 1
        l.append(column)
        return resRow, resCol, l

    def CoordToPos(self, row, column, l = None):
        if l is None:
            l = PosToCoord(self)[2]
        if column > l[row]:
            column = l[row]
        return sum(l[:row]) + row + column

    def RawToCoord(self, pos):
        l = self.PosToCoord()[2]
        row = min(len(l) - 1, max(0, int((pos[1] - self.topMargin) / (self.fontSize * self.lineSpacing))))
        column = max(0, round((pos[0] - self.sideMargin) / (self.fontSize * self.charSpacing)))
        return row, column, l

def Press(editor, key, mod):
    if key in KB.map.keys() and mod != null:
        key = KB.map[key][mod]
        if key is None:
            return
        if callable(key):
            editor = key(editor)
        else:
            if editor.cursor.highlight is None:
                editor.text = editor.text[:editor.cursor.pos] + key + editor.text[editor.cursor.pos:]
                editor.cursor.pos += len(key)
            else:
                editor.text = editor.text[:min(editor.cursor.pos, editor.cursor.highlight)] + key + editor.text[max(editor.cursor.pos, editor.cursor.highlight):]
                editor.cursor.pos = min(editor.cursor.pos, editor.cursor.highlight) + len(key)
            editor.cursor.highlight = None

def GetModifier(keys):
    s = k[p.K_LSHIFT] or k[p.K_RSHIFT]
    c = k[p.K_LCTRL] or k[p.K_RCTRL] or k[p.K_LMETA] or k[p.K_RMETA]
    a = k[p.K_LALT] or k[p.K_RALT]
    
    if s + c + a > 1:
        return null
    if s:
        return shift
    if c:
        return ctrl
    if a:
        return alt
    return None

def Keyword(word, string):
    if word == '':
        return []
    colour = [0, 0, 0]
    
    if string:
        colour = [60, 180, 40]
    elif word in I.functions.keys():
        colour = [110, 50, 180]
        
    return [colour for _ in range(len(word))]

def Colour():
    result = []
    word = ''
    string = False
    for i in editor.text:
        if i == "'":
            if string:
                result.extend(Keyword(word + i, string))
                word = ''
            else:
                result.extend(Keyword(word, string))
                word = "'"
            string = not string
            continue

        if i == ' ' or i == '\n':
            result.extend(Keyword(word, string))
            result.append([0, 0, 0])
            word = ''
            if i == '\n':
                string = False
        else:
            word += i
            
    result.extend(Keyword(word, string))
    return result
    
def read(name):
    try:
        f = open(name, 'r')
    except:
        return FileNotFoundError
    txt = f.read()
    f.close()
    return txt

p.init()

scrWidth, scrHeight = 800, 600
scr = p.display.set_mode([scrWidth, scrHeight])

overlay = p.Surface([scrWidth, scrHeight], p.SRCALPHA)
overlay.fill([0, 0, 0, 100])

editor = Editor('Menlo', 15)

keyPressed = None
keyCooldown = 0
modifier = None

cursorPos = 0
cursorBlink = 0

clock = p.time.Clock()
run = True

while run:
    clock.tick(30)

    if editor.msgbox is not None:
        keyPressed = None
        scr.fill([255, 255, 255])
        editor.Update(scr)
        scr.blit(overlay, [0, 0])
        editor.msgbox.Update(scr)
        p.display.flip()
        
        for e in p.event.get():
            if e.type == p.QUIT:
                editor = halt(editor)
            if e.type == p.KEYDOWN:
                editor.msgbox = editor.msgbox.KeyPressed(e)
                if type(editor.msgbox) == list:
                    if editor.msgbox[1] == 'r':
                        result = read(editor.msgbox[0] + '.bpp')
                        if result is FileNotFoundError:
                            editor.msgbox = Msgbox(f"File '{editor.msgbox[0] + '.bpp'}' does not exist.", [350 + (len(editor.msgbox[0]) + 4) * 10, 50], msgOffset = 25)
                            break
                        else:
                            editor.text = result
                            editor.cursor.pos = len(editor.text)
                            editor.fileName = editor.msgbox[0]
                            editor.lastSaved = result
                    elif editor.msgbox[1] == 'w':
                        with open(editor.msgbox[0] + '.bpp', 'w') as f:
                            f.write(editor.text)
                        editor.lastSaved = editor.text
                        editor.fileName = editor.msgbox[0]
                    elif editor.msgbox[1] == 'q':
                        run = False
                    editor.msgbox = None
                elif editor.msgbox is None:
                    break
        continue

    # INPUTS
    k = p.key.get_pressed()
    m = p.mouse.get_pressed()
    mp = p.mouse.get_pos()
    modifier = GetModifier(k)

    # EVENTS
    for e in p.event.get():
        if e.type == p.QUIT:
            editor = halt(editor)
        if e.type == p.KEYDOWN:
            keyPressed = e.key
            Press(editor, keyPressed, modifier)
            keyCooldown = 10
        if e.type == p.KEYUP and e.key == keyPressed:
            keyPressed = None
        if e.type == p.MOUSEBUTTONDOWN:
            row, column, l = editor.RawToCoord(mp)
            pos = editor.CoordToPos(row, column, l)
            if modifier == shift:
                editor.cursor.highlight = pos
            else:
                editor.cursor.pos = pos
                editor.cursor.blink = 0
                editor.cursor.highlight = None
                
    # RELAY INPUT TO EDITOR
    if keyPressed is not None:
        if keyCooldown > 0:
            keyCooldown -= 1
        else:
            Press(editor, keyPressed, modifier)
            keyCooldown = 1
    if m[0]:
        r, c, l = editor.RawToCoord(mp)
        m = editor.CoordToPos(r, c, l)
        if m != editor.cursor.pos:
            editor.cursor.highlight = m
        else:
            editor.cursor.highlight = None
            
    # UPDATE
    scr.fill([255, 255, 255])
    editor.colour = Colour()
    editor.Update(scr)
    p.display.flip()

    if editor.lastSaved == editor.text:
        p.display.set_caption('untitled' if editor.fileName is None else f'{editor.fileName}.bpp')
    else:
        p.display.set_caption('*untitled*' if editor.fileName is None else f'*{editor.fileName}.bpp*')

p.quit()
sys.exit()
