import pyxel
import gameFiles.GameManager as GameManager
import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen

class BlocksStr:
    Air = ""

def GetGameData():
    BlocksStr.Air = Data.Blocks.Air.value

def WorldRenderer():
    start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea()

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            for layer in range(GameManager.GameInfo.MaxLayer):
                tile = WorldGen.World.get((x, y, layer))
                if tile is None or tile['Block'] == BlocksStr.Air: break
                above_tile = WorldGen.World.get((x, y, layer + 1))
                fwrd_tile = WorldGen.World.get((x, y + 1, layer))
                if above_tile is not None and above_tile['Block'] != BlocksStr.Air:
                    if fwrd_tile is not None and fwrd_tile['Block'] != BlocksStr.Air:    
                        continue
                
                block = Data.GameData.block_data[tile['Block']]
                block_x = block['local']['x']
                block_y = block['local']['y']

                world_x = x * GameManager.GameInfo.BlockSize
                world_y = (y * GameManager.GameInfo.BlockSize) - (layer * GameManager.GameInfo.BlockHeight)

                pyxel.blt(world_x, 
                          world_y, 
                          1, 
                          block_x, 
                          block_y, 
                          GameManager.GameInfo.BlockSize, 
                          GameManager.GameInfo.BlockSize + GameManager.GameInfo.BlockHeight, 
                          2)


def DrawOutLine():
    start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea()

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
                tile = WorldGen.World.get((x, y, layer))
                if tile is None or tile['Block'] == BlocksStr.Air: continue

                solid = tile['Solid']

                top          = WorldGen.World.get((x, y - 1, layer))
                above        = WorldGen.World.get((x, y, layer + 1))
                left         = WorldGen.World.get((x - 1, y, layer))
                right        = WorldGen.World.get((x + 1, y, layer))
                bottom       = WorldGen.World.get((x, y + 1, layer))
                bottom_left  = WorldGen.World.get((x - 1, y + 1, layer))
                bottom_right = WorldGen.World.get((x + 1, y + 1, layer))

                is_air = lambda t: t is None or t['Block'] == BlocksStr.Air

                world_x = x * GameManager.GameInfo.BlockSize
                world_y = (y * GameManager.GameInfo.BlockSize) - (layer * GameManager.GameInfo.BlockHeight)

                if solid and is_air(top) and is_air(above):
                    pyxel.rect(world_x, world_y - 1, GameManager.GameInfo.BlockSize, 1, 0)

                if is_air(left):
                    if solid:
                        pyxel.rect(world_x - 1, world_y, 1, GameManager.GameInfo.BlockSize, 0)
                    if is_air(bottom) and is_air(bottom_left):
                        pyxel.rect(world_x - 1, world_y + GameManager.GameInfo.BlockSize, 1, GameManager.GameInfo.BlockHeight, 0)
                    
                if is_air(right):
                    if solid:
                        pyxel.rect(world_x + GameManager.GameInfo.BlockSize, world_y, 1, GameManager.GameInfo.BlockSize, 0)
                    if is_air(bottom) and is_air(bottom_right):
                        pyxel.rect(world_x + GameManager.GameInfo.BlockSize, world_y + GameManager.GameInfo.BlockSize, 1, GameManager.GameInfo.BlockHeight, 0)
                
                nextBottomTile = WorldGen.World.get((x, y + 1, layer - 1))
                if is_air(nextBottomTile):
                    continue
                else:
                    break
