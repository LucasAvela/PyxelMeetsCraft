import pyxel

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Hello Pyxel")
        pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.images[1].load(0, 0, 'assets/sprites/Sprite_sheet_0.png')
        pyxel.colors[11] = 0xFFFFFF
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        old_colors = pyxel.colors.to_list()
        if pyxel.btnp(pyxel.KEY_SPACE):
            print(old_colors)

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(56, 56, 1, 0, 0, 8, 8)

App()