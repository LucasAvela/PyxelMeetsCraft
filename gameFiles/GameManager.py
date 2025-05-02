import pyxel
import random
import numpy as np

import gameFiles.Data as Data

class AppInfo:
    ScreenWidth = 256
    ScreenHeight = 256
    WindowTitle = "Pyxel Meets Craft"
    Fps = 64
    Tps = 3

class GameInfo:
    BlockSize = 8
    BlockHeight = 4
    ItemSize = 16
    ViewDistance = 32
    MaxLayer = 24
    CameraSpeed = 1
    InvetorySize = 36

class GameState:
    current = Data.GameStates.MainMenu.value

    def Set(state):
        GameState.current = state

class Camera:
    Position = [0, 0]

    def Move(x, y):
        Camera.Position[0] += x
        Camera.Position[1] += y

    def GetCameraPosition():
        return Camera.Position

    def SetCameraPosition(offset):
        Camera.position = offset

class Properties:
    def InitPlayerInventory(dictionary):
        for i in range(4 * 9):
            dictionary[i] = {
                'Item': None, 
                'Amount': 0
            }

class ChunkCalc:
    def GetGenerationChunkArea():
        start_x = Camera.Position[0] // GameInfo.BlockSize
        end_x = start_x + (GameInfo.ViewDistance) + 2
        start_y = Camera.Position[1] // GameInfo.BlockSize + 4
        end_y = start_y + (GameInfo.ViewDistance) + 4
 
        return start_x, end_x, start_y, end_y

class PerlinNoise:
    permutation = []

    def init_seed(seed=None):
        if seed is None: seed = random.randint(0, 1000000)
        random.seed(seed)
        np.random.seed(seed)
        p = np.arange(256, dtype=int)
        np.random.shuffle(p)
        PerlinNoise.permutation = np.stack([p, p]).flatten()
    
    def fade(t):
        return t * t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(a, b, t):
        return a + t * (b - a)
    
    def gradient(h, x, y):
        vectors = np.array([[1,1], [-1,1], [1,-1], [-1,-1], [1,0], [-1,0], [0,1], [0,-1]])
        g = vectors[h % 8]
        return g[0] * x + g[1] * y

    def noise(x, y):
        p = PerlinNoise.permutation
        
        x0, y0 = int(np.floor(x)), int(np.floor(y))
        x1, y1 = x0 + 1, y0 + 1
        
        def hash(x, y):
            return p[(p[x % 256] + y) % 256]
        
        g00 = PerlinNoise.gradient(hash(x0, y0), x - x0, y - y0)
        g10 = PerlinNoise.gradient(hash(x1, y0), x - x1, y - y0)
        g01 = PerlinNoise.gradient(hash(x0, y1), x - x0, y - y1)
        g11 = PerlinNoise.gradient(hash(x1, y1), x - x1, y - y1)
        
        u, v = PerlinNoise.fade(x - x0), PerlinNoise.fade(y - y0)
        
        return PerlinNoise.lerp(PerlinNoise.lerp(g00, g10, u), PerlinNoise.lerp(g01, g11, u), v)

class Button:
    def __init__(self, x, y, w, h, text, callback, color=5, text_color=7):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.text = text
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def is_hovered(self):
        return self.x <= pyxel.mouse_x <= self.x + self.w and self.y <= pyxel.mouse_y <= self.y + self.h

    def update(self):
        self.hovered = self.is_hovered()
        if self.hovered and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.callback()

    def draw(self):
        color = self.color
        border_color = 7 if self.hovered else 0
        text_color = self.text_color

        pyxel.rect(self.x - 1, self.y - 1, self.w + 2, self.h + 2, border_color)
        pyxel.rect(self.x, self.y, self.w, self.h, color)

        text_x = self.x + (self.w - len(self.text)*5) // 2
        text_y = self.y + (self.h - 8) // 2
        pyxel.text(text_x, text_y, self.text, text_color, font=Data.GameData.spleen5_font)

class TextInputField:
    def __init__(self, x, y, w, h, max, title, callback, placeHolder="", color=0, text_color=7):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.max = max
        self.title = title
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.writing = False
        self.text = placeHolder

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