import pyxel

import gameFiles.Data as Data

class TextCenter:
    def __init__(self, x, y, text, color, border=None, font=Data.GameData.spleen5_font, fontWidth=5, fontHeight=8):
        self.x, self.y = x, y
        self.text = text
        self.color = color
        self.border = border

        self.font = font

        self.w = len(self.text) * fontWidth
        self.h = fontHeight

    def update(self):
        pass

    def draw(self):
        text_x = self.x - (self.w // 2)
        text_y = self.y - (self.h // 2)

        if self.border is not None:
            #pyxel.text(text_x-1, text_y, self.text, self.border, self.font)
            pyxel.text(text_x+1, text_y, self.text, self.border, self.font)
            #pyxel.text(text_x, text_y-1, self.text, self.border, self.font)
            pyxel.text(text_x, text_y+1, self.text, self.border, self.font)
            #pyxel.text(text_x-1, text_y-1, self.text, self.border, self.font)
            pyxel.text(text_x+1, text_y+1, self.text, self.border, self.font)
            #pyxel.text(text_x+1, text_y-1, self.text, self.border, self.font)
            #pyxel.text(text_x-1, text_y+1, self.text, self.border, self.font)

        pyxel.text(text_x, text_y, self.text, self.color, self.font)


class ButtonText:
    def __init__(self, x, y, w, h, text, callback, color=5, text_color=7, border_color=0, highlight_color=7):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.text = text
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.border_color = border_color
        self.highlight_color = highlight_color
        self.hovered = False

    def is_hovered(self):
        return self.x <= pyxel.mouse_x <= self.x + self.w and self.y <= pyxel.mouse_y <= self.y + self.h

    def update(self):
        self.hovered = self.is_hovered()
        if self.hovered and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.callback()

    def draw(self):
        color = self.color
        border_color = self.highlight_color if self.hovered else self.border_color
        text_color = self.text_color

        pyxel.rect(self.x - 1, self.y - 1, self.w + 2, self.h + 2, border_color)
        pyxel.rect(self.x, self.y, self.w, self.h, color)

        text_x = self.x + (self.w - len(self.text)*5) // 2
        text_y = self.y + (self.h - 8) // 2
        pyxel.text(text_x, text_y, self.text, text_color, font=Data.GameData.spleen5_font)

class ButtonSprite:
    def __init__(self, x, y, w, h, u, v, colorKey, callback):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.u, self.v = u, v
        self.colorKey = colorKey
        self.callback = callback

    def is_hovered(self):
        return self.x <= pyxel.mouse_x <= self.x + self.w and self.y <= pyxel.mouse_y <= self.y + self.h
    
    def update(self):
        self.hovered = self.is_hovered()
        if self.hovered and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.callback()
    
    def draw(self):
        pyxel.blt(self.x, self.y, 2, self.u, self.v, self.w, self.h, self.colorKey)

class TextInputField:
    def __init__(self, x, y, w, h, max, title, callback, placeHolder="", color=0, text_color=7):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.max = max
        self.title = title
        self.callback = callback
        self.text = placeHolder
        self.color = color
        self.text_color = text_color
        self.writing = False

    def Select(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.x <= pyxel.mouse_x <= self.x + self.w and self.y <= pyxel.mouse_y <= self.y + self.h:
                self.writing = True
            elif self.writing:
                self.callback(self.text)
                self.writing = False

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_RETURN2):
            if self.writing:
                self.callback(self.text)
                self.writing = False

    def Write(self):
        if self.writing:
            for i in range(32, 127):
                if pyxel.btnp(i) and len(self.text) < self.max:
                    self.text += chr(i).upper()

            if pyxel.btnp(pyxel.KEY_BACKSPACE):
                self.text = self.text[:-1]

    def update(self):
        self.Select()
        self.Write()

    def draw(self):
        color = self.color
        text_color = self.text_color
        title = self.title

        pyxel.text(self.x, self.y - 10 + 1, title, 0, font=Data.GameData.spleen5_font)
        pyxel.text(self.x + 1, self.y - 10, title, 0, font=Data.GameData.spleen5_font)
        pyxel.text(self.x, self.y - 10, title, text_color, font=Data.GameData.spleen5_font)

        pyxel.rect(self.x - 1, self.y - 1, self.w + 2, self.h + 2, text_color)
        pyxel.rect(self.x, self.y, self.w, self.h, color)

        text_x = self.x + 2
        text_y = self.y + (self.h - 8) // 2

        pyxel.text(text_x, text_y, self.text, text_color, font=Data.GameData.spleen5_font)

        if self.writing:
            text_width = len(self.text) * 5
            
            if (pyxel.frame_count // 30) % 2 == 0:
                cursor_x = text_x + text_width
                pyxel.text(cursor_x, text_y, "|", text_color, font=Data.GameData.spleen5_font)

class ItemSlot:
    def __init__(self, x, y, i, storage, color, hotbar=False):
        self.x, self.y = x, y
        self.i = i
        self.Storage = storage
        self.color = color
        self.Item = None
        self.Amount = 0
        self.ItemData = None
        self.hotbar = hotbar
    
    def update(self):
        self.Item = self.Storage[self.i]["Item"]
        self.Amount = self.Storage[self.i]["Amount"]

        if self.Item is not None: self.ItemData = Data.GameData.item_data[self.Item]
        else: self.ItemData = None

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not self.hotbar:
            if self.x <= pyxel.mouse_x <= self.x + 16 and self.y <= pyxel.mouse_y <= self.y + 16:
                print(f"slot: {self.i}")
                return self.i

    def draw(self):
        pyxel.rect(self.x, self.y, 16, 16, self.color)

        if self.ItemData is None: return
        
        pyxel.blt(self.x, self.y, 1, self.ItemData['local']['x'], self.ItemData['local']['y'], 16, 16, 2)

        if self.Amount <= 1: return

        pyxel.text(self.x + 10, self.y + 11, str(self.Amount) if self.Amount >= 10 else " " + str(self.Amount), 0)
        pyxel.text(self.x + 10, self.y + 12, str(self.Amount) if self.Amount >= 10 else " " + str(self.Amount), 0)
        pyxel.text(self.x +  9, self.y + 12, str(self.Amount) if self.Amount >= 10 else " " + str(self.Amount), 0)
        pyxel.text(self.x +  9, self.y + 11, str(self.Amount) if self.Amount >= 10 else " " + str(self.Amount), 7)