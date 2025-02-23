import pyxel
import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen

def WorldRenderer(optfine):
    start_x, end_x, start_y, end_y = optfine

    for layer in range(0, Data.layers_quantity):
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if (x, y, layer) in WorldGen.World and WorldGen.World[(x, y, layer)]['Block'] != Data.Blocks.Air.value:
                    v = WorldGen.World[(x, y, layer)]

                    block = next(block for block in Data.block_data['Blocks'] if block['name'] == v["Block"])
                    block_x = block['local']['x']
                    block_y = block['local']['y']

                    world_x = x * Data.block_Size
                    world_y = (y * Data.block_Size) - (layer * Data.block_Height)

                    pyxel.blt(world_x, world_y, 1, block_x, block_y, Data.block_Size, Data.block_Size + Data.block_Height, 2)
        
        DrawOutLine(layer, optfine)

def DrawOutLine(layer, optfine):
    start_x, end_x, start_y, end_y = optfine
    
    for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if (x, y, layer) in WorldGen.World and WorldGen.World[(x, y, layer)]['Block'] != Data.Blocks.Air.value:
                    
                    world_x = x * Data.block_Size
                    world_y = (y * Data.block_Size) - (layer * Data.block_Height)

                    if (x, y - 1, layer) in WorldGen.World and WorldGen.World[(x, y - 1, layer)]['Block'] == Data.Blocks.Air.value:
                        if (x, y, layer + 1) not in WorldGen.World or WorldGen.World[(x, y, layer + 1)]['Block'] == Data.Blocks.Air.value:
                            if (x, y, layer) in WorldGen.World and WorldGen.World[(x, y, layer)]['Block'] == Data.Blocks.Door_block_Top.value:
                                continue
                            pyxel.rect(world_x, world_y - 1, Data.block_Size, 1, 0)
                    
                    if (x - 1, y, layer) in WorldGen.World and WorldGen.World[(x - 1, y, layer)]['Block'] == Data.Blocks.Air.value:
                        pyxel.rect(world_x - 1, world_y, 1, Data.block_Size, 0)
                        if (x, y + 1, layer) in WorldGen.World and WorldGen.World[(x, y + 1, layer)]['Block'] == Data.Blocks.Air.value:
                            if (x - 1, y + 1, layer) in WorldGen.World and WorldGen.World[(x - 1, y + 1, layer)]['Block'] == Data.Blocks.Air.value:
                                pyxel.rect(world_x - 1, world_y + Data.block_Size, 1, Data.block_Height, 0)
                    
                    if (x + 1, y, layer) in WorldGen.World and WorldGen.World[(x + 1, y, layer)]['Block'] == Data.Blocks.Air.value:
                        pyxel.rect(world_x + Data.block_Size, world_y, 1, Data.block_Size, 0)
                        if (x, y + 1, layer) in WorldGen.World and WorldGen.World[(x, y + 1, layer)]['Block'] == Data.Blocks.Air.value:
                            if (x + 1, y + 1, layer) in WorldGen.World and WorldGen.World[(x + 1, y + 1, layer)]['Block'] == Data.Blocks.Air.value:
                                pyxel.rect(world_x + Data.block_Size, world_y + Data.block_Size, 1, Data.block_Height, 0)