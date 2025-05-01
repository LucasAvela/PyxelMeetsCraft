import pyxel
import random

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer
import gameFiles.GameManager as GameManager

import gameFiles.Gameplay as Gameplay

class MainScreen:
    Started = False
    Buttons = [
        GameManager.Button(72, 88, 112, 16, "Play", lambda: Manager.ChangeScreen("Play")),
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
    splash_x = 176 - (len(splash_text) * 6 // 2)

    def Start():
        if not MainScreen.Started:
            print("Started Main")
            pyxel.camera(0, 0)
            MainScreen.Started = True
    
    def Update():
        MainScreen.Start()

        for button in MainScreen.Buttons:
            button.update()

    def Draw():
        pyxel.cls(0)
    
        pyxel.blt(64, 64, 0, 0, 128, 128, 128, 2, scale=2)
        pyxel.blt(37, 32, 0, 0, 0, 182, 41, 2)

        pyxel.text(MainScreen.splash_x, 60 + 1, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x, 60 - 1, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x + 1, 60, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x - 1, 60, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x + 1, 60 + 1, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x - 1, 60 - 1, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x + 1, 60 - 1, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x - 1, 60 + 1, MainScreen.splash_text, 0, font=Data.GameData.spleen6_font)
        pyxel.text(MainScreen.splash_x, 60, MainScreen.splash_text, 10, font=Data.GameData.spleen6_font)

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
            pyxel.camera(0, 0)
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

class PlayScreen:
    Started = False
    Buttons = [
        GameManager.Button(32,  28, 192, 40, "New Game", lambda: Manager.ChangeScreen("NewGame")),
        GameManager.Button(32,  84, 192, 40, "New Game", lambda: Manager.ChangeScreen("NewGame")),
        GameManager.Button(32, 140, 192, 40, "New Game", lambda: Manager.ChangeScreen("NewGame")),
        GameManager.Button(72, 216, 112, 16, "Back", lambda: Manager.ChangeScreen("Main"))
    ]

    def Start():
        if not PlayScreen.Started:
            print("Started Play")
            pyxel.camera(0, 0)
            PlayScreen.Started = True

    def Update():
        PlayScreen.Start()

        for button in PlayScreen.Buttons:
            button.update()

    def Draw():
        pyxel.cls(0)

        pyxel.blt(64, 64, 0, 128, 128, 128, 128, 2, scale=2)

        for button in PlayScreen.Buttons:
            button.draw()

class NewGameScreen:
    Started = False
    Buttons = [
        GameManager.Button(72, 192, 112, 16, "Create", lambda: Manager.NewGame()),
        GameManager.Button(72, 216, 112, 16, "Back", lambda: Manager.ChangeScreen("Play"))
    ]

    seed = 128

    def Start():
        if not NewGameScreen.Started:
            print("Started New Game")
            pyxel.camera(0, 0)
            NewGameScreen.Started = True

    def Update():
        NewGameScreen.Start()

        for button in NewGameScreen.Buttons:
            button.update()

    def Draw():
        pyxel.cls(0)

        pyxel.blt(64, 64, 0, 128, 128, 128, 128, 2, scale=2)

        for button in NewGameScreen.Buttons:
            button.draw()

class Animation:
    dither = 0

class Manager:
    ActualScreen = "Main"

    def ChangeScreen(screen):
        MainScreen.Started = False
        OptionsScreen.Started = False
            
        Manager.ActualScreen = screen

    def NewGame():
        Manager.ChangeScreen("Main")
        GameManager.PerlinNoise.init_seed(seed=NewGameScreen.seed)
        GameManager.GameState.Set(Data.GameStates.Gameplay.value)

def Update():
    if   (Manager.ActualScreen == "Main"): MainScreen.Update()
    elif (Manager.ActualScreen == "Play"): PlayScreen.Update()
    elif (Manager.ActualScreen == "Options"): OptionsScreen.Update()
    elif (Manager.ActualScreen == "NewGame"): NewGameScreen.Update()

def Draw():
    if   (Manager.ActualScreen == "Main"): MainScreen.Draw()
    elif (Manager.ActualScreen == "Play"): PlayScreen.Draw()
    elif (Manager.ActualScreen == "Options"): OptionsScreen.Draw()
    elif (Manager.ActualScreen == "NewGame"): NewGameScreen.Draw()