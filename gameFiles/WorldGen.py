import gameFiles.GameManager as GameManager
import gameFiles.Data as Data

class BlocksStr:
    Grass = ""
    Dirt = ""
    Bedrock = ""
    Stone = ""
    Coal_Ore_block = ""
    Iron_Ore_block = ""
    Gold_Ore_block = ""
    Diamond_Ore_block = ""
    Emerald_Ore_block = ""
    Wood_Log_block = ""
    Leabes_block = ""

World = {}

def GetGameData():
    BlocksStr.Grass = Data.Blocks.Grass_block.value
    BlocksStr.Dirt = Data.Blocks.Dirt_block.value
    BlocksStr.Stone = Data.Blocks.Stone_block.value
    BlocksStr.Bedrock = Data.Blocks.Bedrock_block.value
    BlocksStr.Coal_Ore_block = Data.Blocks.Coal_Ore_block.value
    BlocksStr.Iron_Ore_block = Data.Blocks.Iron_Ore_block.value
    BlocksStr.Gold_Ore_block = Data.Blocks.Gold_Ore_block.value
    BlocksStr.Diamond_Ore_block = Data.Blocks.Diamond_Ore_block.value
    BlocksStr.Emerald_Ore_block = Data.Blocks.Emerald_Ore_block.value
    BlocksStr.Wood_Log_block = Data.Blocks.Wood_Log_block.value
    BlocksStr.Leaves_block = Data.Blocks.Leaves_block.value

def GenWorld():
    global World
    start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea()

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            World[(x, y, 0)] = {"Block": BlocksStr.Bedrock, "Solid": True}
            
            for z in range(1, 3):
                if (x, y, z) in World: continue
                modifier = 8
                noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                block = BlocksStr.Stone

                if noise   > 0.95: block = BlocksStr.Emerald_Ore_block
                elif noise > 0.90: block = BlocksStr.Diamond_Ore_block
                elif noise > 0.80: block = BlocksStr.Gold_Ore_block
                elif noise > 0.70: block = BlocksStr.Iron_Ore_block
                elif noise > 0.60: block = BlocksStr.Coal_Ore_block
                
                World[(x, y, z)] = {"Block": block, "Solid": True}

            for z in range(3, 6):
                if (x, y, z) in World: continue
                modifier = 5
                noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                block = BlocksStr.Stone

                if noise > 0.70: block = BlocksStr.Gold_Ore_block
                elif noise > 0.60: block = BlocksStr.Coal_Ore_block
                elif noise > 0.50: block = BlocksStr.Iron_Ore_block
                
                World[(x, y, z)] = {"Block": block, "Solid": True}

            for z in range(6, 9):
                if (x, y, z) in World: continue
                modifier = 2
                noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                block = BlocksStr.Stone

                if noise > 0.70: block = BlocksStr.Iron_Ore_block
                elif noise > 0.50: block = BlocksStr.Coal_Ore_block
                
                World[(x, y, z)] = {"Block": block, "Solid": True}
            

            layer = 9
            if (x, y, layer) in World: continue
            noise = GameManager.PerlinNoise.noise(x / 8, y / 8)
            slope = 0

            if noise >= 0.35:
                slope = 2
            elif noise >= -0.35:
                slope = 1
            
            for i in range(slope):
                World[(x, y, layer + i)] = {"Block": BlocksStr.Dirt, "Solid": True}
            
            World[(x, y, layer + slope)] = {"Block": BlocksStr.Grass, "Solid": True}

            layer = layer + slope + 1
            if (x, y, layer) in World: continue
            noise = GameManager.PerlinNoise.noise(x / 2, y / 2)

            if noise > 0.8:
                World[(x, y, layer)] = {"Block": BlocksStr.Wood_Log_block, "Solid": True}
                World[(x, y, layer + 1)] = {"Block": BlocksStr.Wood_Log_block, "Solid": True}
                World[(x, y, layer + 2)] = {"Block": BlocksStr.Wood_Log_block, "Solid": True}
                World[(x, y, layer + 3)] = {"Block": BlocksStr.Leaves_block, "Solid": True}
                World[(x - 1, y, layer + 3)] = {"Block": BlocksStr.Leaves_block, "Solid": True}
                World[(x + 1, y, layer + 3)] = {"Block": BlocksStr.Leaves_block, "Solid": True}
                World[(x, y, layer + 4)] = {"Block": BlocksStr.Leaves_block, "Solid": True}