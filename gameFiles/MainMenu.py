import pyxel

class Status:
    Started = False

class Hierarchy:
    buttons = []

class Button:
    def __init__(self, x, y, w, h, text, callback, color_idle=5, color_hover=13, color_text_idle=7, color_text_hover=10):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.text = text
        self.callback = callback
        self.color_idle = color_idle
        self.color_hover = color_hover
        self.color_text_idle = color_text_idle
        self.color_text_hover = color_text_hover
        self.hovered = False

    def is_hovered(self):
        return self.x <= pyxel.mouse_x <= self.x + self.w and self.y <= pyxel.mouse_y <= self.y + self.h

    def drawVisual(self):
        pyxel.rect(self.x, self.y -1, self.w, 1, 0)
        pyxel.rect(self.x, self.y + self.h, self.w, 1, 0)
        pyxel.rect(self.x - 1, self.y, 1, self.h, 0)
        pyxel.rect(self.x + self.w, self.y, 1, self.h, 0)

    def update(self):
        self.hovered = self.is_hovered()
        if self.hovered and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.callback()

    def draw(self):
        color = self.color_hover if self.hovered else self.color_idle
        text_color = self.color_text_hover if self.hovered else self.color_text_idle
        pyxel.rect(self.x, self.y, self.w, self.h, color)
        self.drawVisual()
        text_x = self.x + (self.w - len(self.text)*4) // 2
        text_y = self.y + (self.h - 6) // 2
        pyxel.text(text_x, text_y, self.text, text_color)

def Start():
    if not Status.Started:
        Hierarchy.buttons.append(Button(52, 148, 152, 16, "Play", lambda: print("Play clicked")))
        Status.Started = True

def Update():
    Start()
    for button in Hierarchy.buttons:
        button.update()

def Draw():
    pyxel.cls(0)
    
    pyxel.blt(64, 64, 0, 0, 128, 128, 128, 2, scale=2)
    pyxel.blt(37, 32, 0, 0, 0, 182, 41, 2)

    for button in Hierarchy.buttons:
        button.draw()