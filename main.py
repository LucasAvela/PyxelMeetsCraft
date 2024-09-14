import pyxel as pyx

class App:
    def __init__(self):
        pyx.init(128, 128, title="Hello Pyxel", display_scale=6)
        pyx.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyx.run(self.update, self.draw)

    def update(self):
        if pyx.btnp(pyx.KEY_Q):
            pyx.quit()

    def draw(self):
        pyx.cls(0)
        pyx.text(40, 32, "Hello, Pyxel!", pyx.frame_count % 16)
        
App()