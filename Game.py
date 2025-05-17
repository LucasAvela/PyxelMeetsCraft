import pyxel

import gameFiles.AppManager as AppManager
import gameFiles.GameManager as GameManager
import gameFiles.Data as Data
import gameFiles.GameObjects as GameObjects

import gameFiles.Scenes.MainMenu as sceneMainMenu
import gameFiles.Scenes.Gameplay as sceneGameplay

class Mouse:
    def Draw():
        pyxel.camera(0, 0)
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 2, 240, 0, 8, 8, 2)

class App:
    def __init__(self):
        pyxel.init(
            width  = AppManager.Settings.ScreenWidth, 
            height = AppManager.Settings.ScreenHeight, 
            title  = AppManager.Settings.WindowTitle, 
            fps    = AppManager.Settings.Fps
        )

        Data.GameData.Start()

        pyxel.run(self.update, self.draw)
        
    def update(self):
        if   GameManager.SceneController.actualScene == "MainMenu": sceneMainMenu.Update()
        elif GameManager.SceneController.actualScene == "Gameplay": sceneGameplay.Update()
    
    def draw(self):
        pyxel.cls(0)

        if   GameManager.SceneController.actualScene == "MainMenu": sceneMainMenu.Draw()
        elif GameManager.SceneController.actualScene == "Gameplay": sceneGameplay.Draw()

        Mouse.Draw()

App()
