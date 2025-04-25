import pyxel
import gameFiles.GameManager as GameManager
import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen

class BlocksStr:
    Air = ""

class GameData:
    block_size = 0
    block_height = 0
    max_layer = 0

def GetGameData():
    BlocksStr.Air = Data.Blocks.Air.value

    GameData.block_size = GameManager.GameInfo.BlockSize
    GameData.block_height = GameManager.GameInfo.BlockHeight
    GameData.max_layer = GameManager.GameInfo.MaxLayer

def ModifyMaxRenderLayer(layervalue):
    GameData.max_layer += layervalue

def WorldRenderer():
    start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea()

    is_air = lambda t: t is None or t['Block'] == BlocksStr.Air

    for layer in range(GameData.max_layer):
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                pos = (x, y, layer)
                tile = WorldGen.World.get(pos)
                if tile is None or tile['Block'] == BlocksStr.Air:
                    continue

                above_tile = WorldGen.World.get((x, y, layer + 1))
                fwrd_tile = WorldGen.World.get((x, y + 1, layer))
                if above_tile is not None and above_tile['Block'] != BlocksStr.Air:
                    if fwrd_tile is not None and fwrd_tile['Block'] != BlocksStr.Air:
                        continue

                block = Data.GameData.block_data[tile['Block']]
                block_x = block['local']['x']
                block_y = block['local']['y']

                world_x = x * GameData.block_size
                world_y = (y * GameData.block_size) - (layer * GameData.block_height)

                pyxel.blt(
                    world_x,
                    world_y,
                    1,
                    block_x,
                    block_y,
                    GameData.block_size,
                    GameData.block_size + GameData.block_height,
                    2
                )

                solid = tile['Solid']
                top          = WorldGen.World.get((x, y - 1, layer))
                above        = above_tile
                left         = WorldGen.World.get((x - 1, y, layer))
                right        = WorldGen.World.get((x + 1, y, layer))
                bottom       = fwrd_tile
                bottom_left  = WorldGen.World.get((x - 1, y + 1, layer))
                bottom_right = WorldGen.World.get((x + 1, y + 1, layer))

                if solid and is_air(top) and is_air(above):
                    pyxel.rect(world_x, world_y - 1, GameData.block_size, 1, 0)

                if is_air(left):
                    if solid:
                        pyxel.rect(world_x - 1, world_y, 1, GameData.block_size, 0)
                    if is_air(bottom) and is_air(bottom_left):
                        pyxel.rect(world_x - 1, world_y + GameData.block_size, 1, GameData.block_height, 0)

                if is_air(right):
                    if solid:
                        pyxel.rect(world_x + GameData.block_size, world_y, 1, GameData.block_size, 0)
                    if is_air(bottom) and is_air(bottom_right):
                        pyxel.rect(world_x + GameData.block_size, world_y + GameData.block_size, 1, GameData.block_height, 0)