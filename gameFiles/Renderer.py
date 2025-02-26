import pyxel
import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen

class BlocksStr:
    Air = ""

def Init():
    BlocksStr.Air = Data.Blocks.Air.value

def WorldRenderer(optfine):
    start_x, end_x, start_y, end_y = optfine

    for layer in range(Data.layers_quantity):
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = WorldGen.World.get((x, y, layer))

                if tile['Block'] == BlocksStr.Air:
                    continue
                
                block = Data.block_data[tile["Block"]]
                block_x = block['local']['x']
                block_y = block['local']['y']

                world_x = x * Data.block_Size
                world_y = (y * Data.block_Size) - (layer * Data.block_Height)

                pyxel.blt(world_x, world_y, 1, block_x, block_y,Data.block_Size, Data.block_Size + Data.block_Height, 2)

                DrawOutLine(x, y, world_x, world_y, layer)

def DrawOutLine(x, y, world_x, world_y, layer):
    key = (x, y, layer)
    tile = WorldGen.World.get(key)
    
    solid = tile['Solid']
        
    top          = WorldGen.World.get((x, y - 1, layer))
    above        = WorldGen.World.get((x, y, layer + 1))
    left         = WorldGen.World.get((x - 1, y, layer))
    right        = WorldGen.World.get((x + 1, y, layer))
    bottom       = WorldGen.World.get((x, y + 1, layer))
    bottom_left  = WorldGen.World.get((x - 1, y + 1, layer))
    bottom_right = WorldGen.World.get((x + 1, y + 1, layer))

    is_air = lambda t: t is None or t['Block'] == BlocksStr.Air

    if solid and is_air(top) and is_air(above):
        pyxel.rect(world_x, world_y - 1, Data.block_Size, 1, 0)

    if is_air(left):
        if solid:
            pyxel.rect(world_x - 1, world_y, 1, Data.block_Size, 0)
        if is_air(bottom) and is_air(bottom_left):
            pyxel.rect(world_x - 1, world_y + Data.block_Size, 1, Data.block_Height, 0)
        
    if is_air(right):
        if solid:
            pyxel.rect(world_x + Data.block_Size, world_y, 1, Data.block_Size, 0)
        if is_air(bottom) and is_air(bottom_right):
            pyxel.rect(world_x + Data.block_Size, world_y + Data.block_Size, 1, Data.block_Height, 0)
