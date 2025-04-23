import random
import gameFiles.GameManager as GameManager
import gameFiles.Data as Data

class BlocksStr:
    Grass = ""
    Dirt = ""
    Bedrock = ""
    Stone = ""

World = {}

def GetGameData():
    BlocksStr.Grass = Data.Blocks.Grass_block.value
    BlocksStr.Dirt = Data.Blocks.Dirt_block.value
    BlocksStr.Stone = Data.Blocks.Stone_block.value
    BlocksStr.Bedrock = Data.Blocks.Bedrock_block.value

def GenWorld():
    start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea()

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            BedrockGeneration(x, y, layer=0)
            UnderGroundGeneration(x, y, layer=1)
            TopographyGeneration(x, y, layer=9)

def BedrockGeneration(x, y, layer):
    global World
    if (x, y, layer) in World: return

    World[(x, y, layer)] = {"Block": BlocksStr.Bedrock, "Solid": True}

def UnderGroundGeneration(x, y, layer):
    global World
    if (x, y, layer) in World: return

    for i in range(8):
        World[(x, y, layer + i)] = {"Block": BlocksStr.Stone, "Solid": True}

def TopographyGeneration(x, y, layer):
    global World
    if (x, y, layer) in World: return

    noise = GameManager.PerlinNoise.noise(x / 8, y / 8)
    slope = 0

    if noise >= 0.35:
        slope = 2
    elif noise >= -0.35:
        slope = 1
    
    for i in range(slope):
        World[(x, y, layer + i)] = {"Block": BlocksStr.Dirt, "Solid": True}
    
    World[(x, y, layer + slope)] = {"Block": BlocksStr.Grass, "Solid": True}