import pyxel
import random

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer
import gameFiles.GameManager as GameManager

class MainScreen:
    Started = False
    Buttons = [
        GameManager.Button(72, 88, 112, 16, "Play", lambda: print("Play")),
        GameManager.Button(72, 112, 112, 16, "Options", lambda: Manager.ChangeScreen("Options")),
        GameManager.Button(72, 136, 112, 16, "Exit", lambda: pyxel.quit())
    ]

    splash_texts = [
        "Awesome!",
        "Limited edition!",
        "Made with pyxel",
        "Indev!",
        "It's a game!",
        "Made in Brazil!",
        "1337"
    ]

    splash_text = random.choice(splash_texts)

    def Start():
        if not MainScreen.Started:
            print("Started Main")
            MainScreen.Started = True
    
    def Update():
        MainScreen.Start()

        for button in MainScreen.Buttons:
            button.update()

    def Draw():
        pyxel.cls(0)
    
        pyxel.blt(64, 64, 0, 0, 128, 128, 128, 2, scale=2)
        pyxel.blt(37, 32, 0, 0, 0, 182, 41, 2)

        pyxel.text(152, 65, MainScreen.splash_text, 9, font=Data.GameData.spleen5_font)
        pyxel.text(152, 64, MainScreen.splash_text, 10, font=Data.GameData.spleen5_font)

        for button in MainScreen.Buttons:
            button.draw()

class OptionsScreen:
    Started = False
    Buttons = [
        GameManager.Button(72, 216, 112, 16, "Back", lambda: Manager.ChangeScreen("Main"))
    ]

    def Start():
        if not OptionsScreen.Started:
            print("Started Options")
            OptionsScreen.Started = True

    def Update():
        OptionsScreen.Start()

        for button in OptionsScreen.Buttons:
            button.update()

    def Draw():
        pyxel.cls(0)

        pyxel.blt(64, 64, 0, 128, 128, 128, 128, 2, scale=2)

        for button in OptionsScreen.Buttons:
            button.draw()

class Manager:
    ActualScreen = "Main"

    def ChangeScreen(screen):
        MainScreen.Started = False
        OptionsScreen.Started = False
            
        Manager.ActualScreen = screen

def Update():
    if   (Manager.ActualScreen == "Main"): MainScreen.Update()
    elif (Manager.ActualScreen == "Options"): OptionsScreen.Update()

def Draw():
    if   (Manager.ActualScreen == "Main"): MainScreen.Draw()
    elif (Manager.ActualScreen == "Options"): OptionsScreen.Draw()