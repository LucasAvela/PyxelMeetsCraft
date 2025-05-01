import gameFiles.GameManager as GameManager
import gameFiles.Data as Data

World = {}

def GenWorld():
    global World
    start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea()

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            for z in range(0, 9):
                if (x, y, z) in World: break

                if z == 0: 
                    World[(x, y, z)] = {"Block": Data.Blocks.Bedrock_block, "Solid": True}
                    continue

                if 0 < z < 3:
                    modifier = 8
                    noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                    block = Data.Blocks.Stone_block

                    if noise   > 0.90: block = Data.Blocks.Emerald_Ore_block
                    elif noise > 0.75: block = Data.Blocks.Diamond_Ore_block
                    elif noise > 0.65: block = Data.Blocks.Gold_Ore_block
                    elif noise > 0.55: block = Data.Blocks.Iron_Ore_block
                    
                    World[(x, y, z)] = {"Block": block, "Solid": True}
                    continue

                if 3 <= z < 6:
                    modifier = 5
                    noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                    block = Data.Blocks.Stone_block

                    if noise > 0.70: block = Data.Blocks.Gold_Ore_block
                    elif noise > 0.60: block = Data.Blocks.Coal_Ore_block
                    elif noise > 0.50: block = Data.Blocks.Iron_Ore_block
                    
                    World[(x, y, z)] = {"Block": block, "Solid": True}
                    continue

                if 6 <= z < 9:
                    modifier = 2
                    noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                    block = Data.Blocks.Stone_block

                    if noise > 0.70: block = Data.Blocks.Iron_Ore_block
                    elif noise > 0.50: block = Data.Blocks.Coal_Ore_block
                    
                    World[(x, y, z)] = {"Block": block, "Solid": True}
                    continue
                
            z = 9
            if (x, y, z) in World: continue
            noise = GameManager.PerlinNoise.noise(x / 16, y / 16)
            slope = 0

            if noise >= 0.35: slope = 2
            elif noise >= -0.35: slope = 1

            for i in range(slope):
                World[(x, y, z + i)] = {"Block": Data.Blocks.Dirt_block, "Solid": True}
            
            World[(x, y, z + slope)] = {"Block": Data.Blocks.Grass_block, "Solid": True}

            z = z + slope + 1
            noise = GameManager.PerlinNoise.noise(x / 2, y / 2)

            if noise >= 0.8:
                World[(x, y, z)] = {"Block": Data.Blocks.Wood_Log_block, "Solid": True}
                World[(x, y, z + 1)] = {"Block": Data.Blocks.Wood_Log_block, "Solid": True}
                World[(x, y, z + 2)] = {"Block": Data.Blocks.Wood_Log_block, "Solid": True}
                World[(x, y, z + 3)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}
                World[(x - 1, y, z + 3)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}
                World[(x + 1, y, z + 3)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}
                World[(x, y, z + 4)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}