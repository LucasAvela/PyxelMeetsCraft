import pyxel

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer
import gameFiles.GameManager as GameManager

import gameFiles.MainMenu as MainMenu
import gameFiles.Gameplay as Gameplay

class Mouse:
    actual_cursor = "Default"

    cursors = {
        "Default": {"local_x": 0, "local_y": 240, "offset_x": 0, "offset_y": 0},
        "Hand":    {"local_x": 0, "local_y": 248, "offset_x": -3, "offset_y": 0},
        "Sword":   {"local_x": 8, "local_y": 240, "offset_x": 0, "offset_y": 0},
    }

    def DrawMouse():
        x = pyxel.mouse_x
        y = pyxel.mouse_y

        local_x = Mouse.cursors[Mouse.actual_cursor]["local_x"]
        local_y = Mouse.cursors[Mouse.actual_cursor]["local_y"]

        offset_x = Mouse.cursors[Mouse.actual_cursor]["offset_x"]
        offset_y = Mouse.cursors[Mouse.actual_cursor]["offset_y"]

        pyxel.camera(0, 0)
        pyxel.blt(x + offset_x, y + offset_y, 1, local_x, local_y, 8, 8, 2)

class App:
    def __init__(self):
        pyxel.init(
            width  = GameManager.AppInfo.ScreenWidth, 
            height = GameManager.AppInfo.ScreenHeight, 
            title  = GameManager.AppInfo.WindowTitle, 
            fps    = GameManager.AppInfo.Fps
        )
        
        Data.GameData.Start()
        
        Renderer.GetGameData()
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if   GameManager.GameState.current == Data.GameStates.MainMenu.value: MainMenu.Update()
        elif GameManager.GameState.current == Data.GameStates.Gameplay.value: Gameplay.Update()
    
    def draw(self):
        if   GameManager.GameState.current == Data.GameStates.MainMenu.value: MainMenu.Draw()
        elif GameManager.GameState.current == Data.GameStates.Gameplay.value: Gameplay.Draw()
        Mouse.DrawMouse()

App()
