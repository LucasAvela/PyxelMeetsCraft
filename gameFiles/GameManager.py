import pyxel
import random
import numpy
import json

import gameFiles.AppManager as AppManager
import gameFiles.Data as Data

class SceneController:
    actualScene = "MainMenu"

    def ChangeScene(newScene):
        SceneController.actualScene = newScene

class SoundController:
    currentMusic = 0

    def PlayMusic(musicIndex):
        pyxel.stop()
        pyxel.sounds[0].set(Data.GameData.musics[musicIndex][1], tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[1].set(Data.GameData.musics[musicIndex][2], tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[2].set(Data.GameData.musics[musicIndex][3], tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[3].set(Data.GameData.musics[musicIndex][4], tones='t', volumes='4', effects='n', speed=45)
        pyxel.musics[1].set([0], [1], [2], [3])

        SoundController.currentMusic = musicIndex
        pyxel.playm(1, loop=True)

    def NextMusic():
        SoundController.currentMusic = (SoundController.currentMusic + 1) % len(Data.GameData.musics)
        SoundController.PlayMusic(SoundController.currentMusic)
    
    def PreviousMusic():
        SoundController.currentMusic = (SoundController.currentMusic - 1) % len(Data.GameData.musics)
        SoundController.PlayMusic(SoundController.currentMusic)

class Load:
    Camera = []
    World = {}
    Entities = {}
    Inventory = {}
    InventoryCraft = {}
    MouseItem = None

    SaveFile = None

    def NewWorld(saveFile, worldName, Seed):
        data = {
            "Name": worldName,
            "Seed": Seed,
            'Camera': [0, 0],
            "World": {},
            "Entities": {},
            "Inventory": {},
            "InventoryCraft": {},
            "MouseItem": None
        }

        data_path = "gameFiles/Saves/" + saveFile + ".json"

        with open(data_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        Load.LoadWorld(saveFile)
    
    def LoadWorld(saveFile):
        data_path = "gameFiles/Saves/" + saveFile + ".json"

        with open(data_path, 'r') as json_file:
            data = json.load(json_file)

        Load.Camera = data["Camera"]
        Load.World = {eval(k): v for k, v in data["World"].items()}
        Load.Entities = {eval(k): {**v, "Inventory": {int(ik): iv for ik, iv in v["Inventory"].items()}} for k, v in data["Entities"].items()}
        Load.Inventory = {int(k): v for k, v in data["Inventory"].items()}
        Load.InventoryCraft = {int(k): v for k, v in data["InventoryCraft"].items()}
        Load.MouseItem = data["MouseItem"]
        Load.SaveFile = data_path

        PerlinNoise.init_seed(seed=data["Seed"])
        SceneController.ChangeScene("Gameplay")

class ChunkCalc:
    def GetGenerationChunkArea(camera_x, camera_y):
        start_x = (camera_x // AppManager.GameInfo.BlockSize) - 2
        end_x = start_x + AppManager.GameInfo.ViewDistance + 4
        start_y = camera_y // AppManager.GameInfo.BlockSize + 4
        end_y = start_y + (AppManager.GameInfo.ViewDistance) + 4
 
        return start_x, end_x, start_y, end_y
    
class Crafting:
    def Check(Matrix):
        if all(cell is None for row in Matrix for cell in row): return None, 0
        Craft = []
        
        rowCount = len(Matrix)
        colCount = len(Matrix[0])

        min_row = rowCount
        min_col = colCount
        max_row = -1
        max_col = -1

        for i in range(rowCount):
            for j in range(colCount):
                if Matrix[i][j]:
                    if i < min_row: min_row = i
                    if j < min_col: min_col = j
                    if i > max_row: max_row = i
                    if j > max_col: max_col = j

        for i in range(min_row, max_row + 1):
            new_row = []
            for j in range(min_col, max_col + 1):
                new_row.append(Matrix[i][j])
            Craft.append(new_row)

        CraftSize = [len(Craft[0]), len(Craft)]

        for recipe in Data.GameData.crafting_data["Crafts"]:
            if recipe['size'] != CraftSize: continue

            if recipe['craft'] == Craft:
                return recipe['result'], recipe['amount']
           
        return None, 0
    
class PerlinNoise:
    permutation = []

    def init_seed(seed=None):
        if seed is None: seed = random.randint(0, 1000000)
        random.seed(seed)
        numpy.random.seed(seed)
        p = numpy.arange(256, dtype=int)
        numpy.random.shuffle(p)
        PerlinNoise.permutation = numpy.stack([p, p]).flatten()
    
    def fade(t):
        return t * t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(a, b, t):
        return a + t * (b - a)
    
    def gradient(h, x, y):
        vectors = numpy.array([[1,1], [-1,1], [1,-1], [-1,-1], [1,0], [-1,0], [0,1], [0,-1]])
        g = vectors[h % 8]
        return g[0] * x + g[1] * y

    def noise(x, y):
        p = PerlinNoise.permutation
        
        x0, y0 = int(numpy.floor(x)), int(numpy.floor(y))
        x1, y1 = x0 + 1, y0 + 1
        
        def hash(x, y):
            return p[(p[x % 256] + y) % 256]
        
        g00 = PerlinNoise.gradient(hash(x0, y0), x - x0, y - y0)
        g10 = PerlinNoise.gradient(hash(x1, y0), x - x1, y - y0)
        g01 = PerlinNoise.gradient(hash(x0, y1), x - x0, y - y1)
        g11 = PerlinNoise.gradient(hash(x1, y1), x - x1, y - y1)
        
        u, v = PerlinNoise.fade(x - x0), PerlinNoise.fade(y - y0)
        
        return PerlinNoise.lerp(PerlinNoise.lerp(g00, g10, u), PerlinNoise.lerp(g01, g11, u), v)