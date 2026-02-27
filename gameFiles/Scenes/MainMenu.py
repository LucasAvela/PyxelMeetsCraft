import pyxel
import random
import json
import time
import os

import gameFiles.AppManager as AppManager
import gameFiles.GameManager as GameManager
import gameFiles.Data as Data
import gameFiles.GameObjects as GameObjects

class ScreenManager:
    actualScreen = "Menu"

    def ChangeScreen(newScreen):
        MainScreen.End()
        OptionsScreen.End()
        PlayScreen.End()
        NewGameScreen.End()

        ScreenManager.actualScreen = newScreen

class Options:
    def ChangeMusic(value):
        if value == 1:
            GameManager.SoundController.NextMusic()
        elif value == -1:
            GameManager.SoundController.PreviousMusic()

        ScreenManager.ChangeScreen(ScreenManager.actualScreen)
        
class MainScreen:
    Started = False

    ObjectsHierarchy = [
        GameObjects.ButtonText(72, 88, 112, 16, "Play", lambda: ScreenManager.ChangeScreen("Play")),
        GameObjects.ButtonText(72, 112, 112, 16, "Options", lambda: ScreenManager.ChangeScreen("Options")),
        GameObjects.ButtonText(72, 136, 112, 16, "Exit", lambda: pyxel.quit()),
    ]

    DynamicObjects = []

    def Start():
        if not MainScreen.Started:
            MainScreen.Started = True
    
    def End():
        MainScreen.Started = False

    def Update():
        MainScreen.Start()

        for GameObject in MainScreen.ObjectsHierarchy + MainScreen.DynamicObjects:
            GameObject.update()
            

    def Draw():
        pyxel.blt(64, 64, 0, 0, 128, 128, 128, 2, scale=2) # Background
        pyxel.blt(37, 32, 0, 0, 0, 182, 41, 2) # Logo

        for GameObject in MainScreen.ObjectsHierarchy + MainScreen.DynamicObjects:
            GameObject.draw()

class OptionsScreen:
    Started = False

    ObjectsHierarchy = [
        GameObjects.ButtonText(72, 216, 112, 16, "Back", lambda: ScreenManager.ChangeScreen("Menu")),
        GameObjects.RectangleCenter(128, 32, 128, 16, 5, border=7),
        GameObjects.TextCenter(128, 16, "Music", 7, border=0),
        GameObjects.ButtonSprite(46, 24, 16, 16, 240, 64, 2, lambda: Options.ChangeMusic(-1)),
        GameObjects.ButtonSprite(200, 24, 16, 16, 240, 48, 2, lambda: Options.ChangeMusic(1)),
    ]

    DynamicObjects = []

    def Start():
        if not OptionsScreen.Started:
            OptionsScreen.DynamicObjects.append(GameObjects.TextCenter(128, 32, Data.GameData.musics[GameManager.SoundController.currentMusic][0], 7, border=0, font=Data.GameData.spleen6_font, fontWidth=5, fontHeight=12))
            OptionsScreen.Started = True

    def End():
        OptionsScreen.Started = False
        OptionsScreen.DynamicObjects.clear()

    def Update():
        OptionsScreen.Start()
        for GameObject in OptionsScreen.ObjectsHierarchy + OptionsScreen.DynamicObjects:
            GameObject.update()

    def Draw():
        pyxel.blt(64, 64, 0, 128, 128, 128, 128, 2, scale=2) # Background

        for GameObject in OptionsScreen.ObjectsHierarchy + OptionsScreen.DynamicObjects:
            GameObject.draw()

class PlayScreen:
    Started = False

    ObjectsHierarchy = [
        GameObjects.ButtonText(72, 216, 112, 16, "Back", lambda: ScreenManager.ChangeScreen("Menu")),
        ]

    DynamicObjects = []

    class SaveSlot:
        def loadSlots():
            if Data.GameData.save_0 is not None:
                name = Data.GameData.save_0["Name"]
                PlayScreen.DynamicObjects.append(GameObjects.ButtonText(32,  28, 152, 40, name, lambda: PlayScreen.SaveSlot.LoadGameSlot("Save_0")))
                PlayScreen.DynamicObjects.append(GameObjects.ButtonText(188, 28, 32, 32, "Delete", lambda: PlayScreen.SaveSlot.DeleteSlot("Save_0"), 8))
            else: PlayScreen.DynamicObjects.append(GameObjects.ButtonText(32, 28, 192, 40, "New Game", lambda: PlayScreen.SaveSlot.NewGameSlot("Save_0")))

            if Data.GameData.save_1 is not None:
                name = Data.GameData.save_1["Name"]
                PlayScreen.DynamicObjects.append(GameObjects.ButtonText(32,  84, 152, 40, name, lambda: PlayScreen.SaveSlot.LoadGameSlot("Save_1")))
                PlayScreen.DynamicObjects.append(GameObjects.ButtonText(188, 84, 32, 32, "Delete", lambda: PlayScreen.SaveSlot.DeleteSlot("Save_1"), 8))
            else: PlayScreen.DynamicObjects.append(GameObjects.ButtonText(32, 84, 192, 40, "New Game", lambda: PlayScreen.SaveSlot.NewGameSlot("Save_1")))

            if Data.GameData.save_2 is not None:
                name = Data.GameData.save_2["Name"]
                PlayScreen.DynamicObjects.append(GameObjects.ButtonText(32, 140, 152, 40, name, lambda: PlayScreen.SaveSlot.LoadGameSlot("Save_2")))
                PlayScreen.DynamicObjects.append(GameObjects.ButtonText(188, 140, 32, 32, "Delete", lambda: PlayScreen.SaveSlot.DeleteSlot("Save_2"), 8))
            else: PlayScreen.DynamicObjects.append(GameObjects.ButtonText(32, 140, 192, 40, "New Game", lambda: PlayScreen.SaveSlot.NewGameSlot("Save_2")))

        def NewGameSlot(saveSlot):
            NewGameScreen.Settings.SetSaveFIleSlot(saveSlot)
            LoadingScreen.Game = "New"
            ScreenManager.ChangeScreen("New")

        def LoadGameSlot(saveSlot):
            LoadingScreen.SetLoadFile(saveSlot)
            LoadingScreen.Game = "Load"
            ScreenManager.ChangeScreen("Load")
        
        def DeleteSlot(saveSlot):
            data_path = "gameFiles/Saves/" + saveSlot + ".json"
            os.remove(data_path)
            PlayScreen.End()
            PlayScreen.Start()

    def Start():
        if not PlayScreen.Started:
            Data.GameData.SaveFiles()

            PlayScreen.SaveSlot.loadSlots()

            PlayScreen.Started = True
        pass

    def End():
        PlayScreen.Started = False
        PlayScreen.DynamicObjects.clear()

    def Update():
        PlayScreen.Start()
        for GameObject in PlayScreen.ObjectsHierarchy + PlayScreen.DynamicObjects:
            GameObject.update()

    def Draw():
        pyxel.blt(64, 64, 0, 128, 128, 128, 128, 2, scale=2) # Background

        for GameObject in PlayScreen.ObjectsHierarchy + PlayScreen.DynamicObjects:
            GameObject.draw()

class NewGameScreen:
    Started = False

    ObjectsHierarchy = [
        GameObjects.TextInputField(46, 32, 164, 16, 32, " World Name", lambda text: NewGameScreen.Settings.ChangeWorldName(text), "NEW WORLD"),
        GameObjects.TextInputField(46, 64, 164, 16, 32, " Seed", lambda text: NewGameScreen.Settings.ChangeSeed(text), ""),
        GameObjects.ButtonText(72, 192, 112, 16, "Create", lambda: NewGameScreen.LoadNewWorld()),
        GameObjects.ButtonText(72, 216, 112, 16, "Back", lambda: ScreenManager.ChangeScreen("Play")),
    ]

    DynamicObjects = []

    SaveFile = None
    WorldName = None
    Seed = None
    GameMode = 0

    class Settings:
        def SetSaveFIleSlot(slot):
            NewGameScreen.SaveFile = slot

        def ChangeWorldName(name):
            NewGameScreen.WorldName = name

        def ChangeSeed(newSeed):
            seed = ""

            for char in newSeed:
                if char.isdigit():
                    seed += char
                elif char.isalpha():
                    value = ord(char.upper()) - ord('A') + 10
                    seed += str(value)
                else:
                    seed += "0"
            
            if seed != '':
                NewGameScreen.Seed = int(seed) % (2**32)

        def ChangeGameMode(value):
            NewGameScreen.GameMode = (NewGameScreen.GameMode + value + len(AppManager.GameInfo.GameModes)) % len(AppManager.GameInfo.GameModes)
        
        def PrintSettings():
            print(f"SaveFile: {NewGameScreen.SaveFile}")
            print(f"WorldName: {NewGameScreen.WorldName}")
            print(f"Seed: {NewGameScreen.Seed}")
            print(f"GameMode: {NewGameScreen.GameMode}")
    
    def LoadNewWorld():
        LoadingScreen.SetNewWorld(NewGameScreen.SaveFile, NewGameScreen.WorldName, NewGameScreen.Seed)
        ScreenManager.ChangeScreen("Load")

    def Start():
        if not NewGameScreen.Started:
            NewGameScreen.WorldName = "NEW WORLD"
            NewGameScreen.Seed = random.randint(1, 99999999)
            NewGameScreen.GameMode = 0

            NewGameScreen.Started = True

    def End():
        NewGameScreen.WorldName = None
        NewGameScreen.Seed = None
        NewGameScreen.GameMode = 0
        NewGameScreen.Started = False

        NewGameScreen.DynamicObjects.clear()

    def Update():
        NewGameScreen.Start()
        for GameObject in NewGameScreen.ObjectsHierarchy + NewGameScreen.DynamicObjects:
            GameObject.update()

    def Draw():
        pyxel.blt(64, 64, 0, 128, 128, 128, 128, 2, scale=2) # Background

        for GameObject in NewGameScreen.ObjectsHierarchy + NewGameScreen.DynamicObjects:
            GameObject.draw()

class LoadingScreen:
    Started = False
    Finish = False
    dither = 0

    SaveFile = None
    WorldName = None
    Seed = None
    GameMode = 0

    Game = None

    def SetNewWorld(saveFile, worldName, Seed):
        LoadingScreen.SaveFile = saveFile
        LoadingScreen.WorldName = worldName
        LoadingScreen.Seed = Seed
        LoadingScreen.GameMode = 0

    def SetLoadFile(saveFile):
        LoadingScreen.SaveFile = saveFile

    def CreateNewWorld():
        GameManager.Load.NewWorld(LoadingScreen.SaveFile, LoadingScreen.WorldName, LoadingScreen.Seed)

    def LoadGameWorld():
        GameManager.Load.LoadWorld(LoadingScreen.SaveFile)

    def Start():
        if not LoadingScreen.Started:
            LoadingScreen.dither = 1.0
            LoadingScreen.Started = True

    def Update():
        LoadingScreen.Start()

        if not LoadingScreen.Finish:
            if LoadingScreen.dither > 0:
                LoadingScreen.dither -= 0.02
            else:
                LoadingScreen.dither = 0
                LoadingScreen.Finish = True

        pyxel.dither(LoadingScreen.dither)

        if LoadingScreen.Finish:
            time.sleep(0.5)
            ScreenManager.ChangeScreen("Menu")
            LoadingScreen.Started = False
            LoadingScreen.Finish = False
            Status.Started = False
            Status.dither = 0
            if LoadingScreen.Game == "New":
                LoadingScreen.CreateNewWorld()
            elif LoadingScreen.Game == "Load":
                LoadingScreen.LoadGameWorld()
            

    def Draw():
        pyxel.blt(64, 64, 0, 128, 128, 128, 128, 2, scale=2) # Background

class Status:
    Started = False
    dither = 0

def Start():
    if not Status.Started:
        if Status.dither < 1:
            Status.dither += 0.02
            pyxel.dither(Status.dither)
            return
        Status.Started = True

def Update():
    Start()
    if   ScreenManager.actualScreen == "Menu": MainScreen.Update()
    elif ScreenManager.actualScreen == "Options": OptionsScreen.Update()
    elif ScreenManager.actualScreen == "Play": PlayScreen.Update()
    elif ScreenManager.actualScreen == "New": NewGameScreen.Update()
    elif ScreenManager.actualScreen == "Load": LoadingScreen.Update()

def Draw():
    if   ScreenManager.actualScreen == "Menu": MainScreen.Draw()
    elif ScreenManager.actualScreen == "Options": OptionsScreen.Draw()
    elif ScreenManager.actualScreen == "Play": PlayScreen.Draw()
    elif ScreenManager.actualScreen == "New": NewGameScreen.Draw()
    elif ScreenManager.actualScreen == "Load": LoadingScreen.Draw()