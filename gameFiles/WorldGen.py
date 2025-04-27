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
            for z in range(0, 9):
                if (x, y, z) in World: break

                if z == 0: 
                    World[(x, y, z)] = {"Block": BlocksStr.Bedrock, "Solid": True}
                    continue

                if 0 < z < 3:
                    modifier = 8
                    noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                    block = BlocksStr.Stone

                    if noise   > 0.90: block = BlocksStr.Emerald_Ore_block
                    elif noise > 0.75: block = BlocksStr.Diamond_Ore_block
                    elif noise > 0.65: block = BlocksStr.Gold_Ore_block
                    elif noise > 0.55: block = BlocksStr.Iron_Ore_block
                    
                    World[(x, y, z)] = {"Block": block, "Solid": True}
                    continue

                if 3 <= z < 6:
                    modifier = 5
                    noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                    block = BlocksStr.Stone

                    if noise > 0.70: block = BlocksStr.Gold_Ore_block
                    elif noise > 0.60: block = BlocksStr.Coal_Ore_block
                    elif noise > 0.50: block = BlocksStr.Iron_Ore_block
                    
                    World[(x, y, z)] = {"Block": block, "Solid": True}
                    continue

                if 6 <= z < 9:
                    modifier = 2
                    noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                    block = BlocksStr.Stone

                    if noise > 0.70: block = BlocksStr.Iron_Ore_block
                    elif noise > 0.50: block = BlocksStr.Coal_Ore_block
                    
                    World[(x, y, z)] = {"Block": block, "Solid": True}
                    continue
                
            z = 9
            if (x, y, z) in World: continue
            noise = GameManager.PerlinNoise.noise(x / 16, y / 16)
            slope = 0

            if noise >= 0.35: slope = 2
            elif noise >= -0.35: slope = 1

            for i in range(slope):
                World[(x, y, z + i)] = {"Block": BlocksStr.Dirt, "Solid": True}
            
            World[(x, y, z + slope)] = {"Block": BlocksStr.Grass, "Solid": True}

            z = z + slope + 1
            noise = GameManager.PerlinNoise.noise(x / 2, y / 2)

            if noise >= 0.8:
                World[(x, y, z)] = {"Block": BlocksStr.Wood_Log_block, "Solid": True}
                World[(x, y, z + 1)] = {"Block": BlocksStr.Wood_Log_block, "Solid": True}
                World[(x, y, z + 2)] = {"Block": BlocksStr.Wood_Log_block, "Solid": True}
                World[(x, y, z + 3)] = {"Block": BlocksStr.Leaves_block, "Solid": True}
                World[(x - 1, y, z + 3)] = {"Block": BlocksStr.Leaves_block, "Solid": True}
                World[(x + 1, y, z + 3)] = {"Block": BlocksStr.Leaves_block, "Solid": True}
                World[(x, y, z + 4)] = {"Block": BlocksStr.Leaves_block, "Solid": True}