import pyxel

import gameFiles.AppManager as AppManager

class App:
    def __init__(self):
        pyxel.init(
            width  = AppManager.Settings.ScreenWidth, 
            height = AppManager.Settings.ScreenHeight, 
            title  = AppManager.Settings.WindowTitle, 
            fps    = AppManager.Settings.Fps
        )

        pyxel.run(self.update, self.draw)
        
    def update(self):
        pass
    
    def draw(self):
        pyxel.cls(0)

App()
