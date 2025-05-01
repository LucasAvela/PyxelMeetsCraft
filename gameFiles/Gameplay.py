import pyxel

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer
import gameFiles.GameManager as GameManager

class Inputs:
    def CameraMove():
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            GameManager.Camera.Move(0, -GameManager.GameInfo.CameraSpeed)
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            GameManager.Camera.Move(0, GameManager.GameInfo.CameraSpeed)
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            GameManager.Camera.Move(-GameManager.GameInfo.CameraSpeed, 0)
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            GameManager.Camera.Move(GameManager.GameInfo.CameraSpeed, 0)

        pyxel.camera(GameManager.Camera.Position[0], GameManager.Camera.Position[1],)

    def BreakBlock():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
            position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

            for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
                target_x = position_x // GameManager.GameInfo.BlockSize
                target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
                adj_y = target_y + (layer // 2)

                if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                    if ((target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air):
                        WorldGen.World[(target_x, adj_y, layer)]['Block'] = Data.Blocks.Air
                        break
    
    def PlaceBlock():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
            position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

            for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
                target_x = position_x // GameManager.GameInfo.BlockSize
                target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
                adj_y = target_y + (layer // 2)

                if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                    if (target_x, adj_y, layer + 1) not in WorldGen.World:
                        WorldGen.World[(target_x, adj_y, layer + 1)] = {"Block": Data.Blocks.StoneBricks_block, "Solid": True}
                    
                    if WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air:
                        WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] = Data.Blocks.StoneBricks_block
                    
                    break

    def Update():
        Inputs.CameraMove()
        Inputs.BreakBlock()
        Inputs.PlaceBlock()

class Player:
    def DrawArea():
        position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
        position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

        for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
            target_x = position_x // GameManager.GameInfo.BlockSize
            target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                if ((target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air):
                    pyxel.blt(target_x * GameManager.GameInfo.BlockSize, 
                            (target_y * GameManager.GameInfo.BlockSize) - ((layer % 2) * GameManager.GameInfo.BlockHeight), 
                            1, 
                            48,
                            240, 
                            GameManager.GameInfo.BlockSize, 
                            GameManager.GameInfo.BlockSize, 2)
                break

def Update():
    Inputs.Update()
    WorldGen.GenWorld()

def Draw():
    pyxel.cls(0)

    Renderer.WorldRenderer()
    Player.DrawArea()