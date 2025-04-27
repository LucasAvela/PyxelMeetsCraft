import pyxel

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer
import gameFiles.GameManager as GameManager

class Debug:
    def UpdateDebug():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
            position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

            for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
                target_x = position_x // GameManager.GameInfo.BlockSize
                target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
                adj_y = target_y + (layer // 2)

                if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air.value:
                    if ((target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value):
                        WorldGen.World[(target_x, adj_y, layer)]['Block'] = Data.Blocks.Air.value
                        break
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
            position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

            for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
                target_x = position_x // GameManager.GameInfo.BlockSize
                target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
                adj_y = target_y + (layer // 2)

                if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air.value:
                    if (target_x, adj_y, layer + 1) not in WorldGen.World:
                        WorldGen.World[(target_x, adj_y, layer + 1)] = {"Block": Data.Blocks.Diamond_block.value, "Solid": True}
                    
                    if WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value:
                        WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] = Data.Blocks.Diamond_block.value
                    
                    break
        
        if pyxel.btnp(pyxel.KEY_EQUALS):
            Renderer.ModifyMaxRenderLayer(1)
        
        if pyxel.btnp(pyxel.KEY_MINUS):
            Renderer.ModifyMaxRenderLayer(-1)

    def DrawDebug():
        position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
        position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

        for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
            target_x = position_x // GameManager.GameInfo.BlockSize
            target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air.value:
                if ((target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value):
                    pyxel.blt(target_x * GameManager.GameInfo.BlockSize, 
                            (target_y * GameManager.GameInfo.BlockSize) - ((layer % 2) * GameManager.GameInfo.BlockHeight), 
                            1, 
                            48,
                            240, 
                            GameManager.GameInfo.BlockSize, 
                            GameManager.GameInfo.BlockSize, 2)

                    pyxel.text(2, 2, f"X: {target_x} Y: {adj_y} L: {layer}", 7)
                    pyxel.text(2, 10, f"{WorldGen.World[(target_x, adj_y, layer)]['Block']}", 7)
                break

class Camera:
    speed = 1
    velocities = [1, 2]
    
    def CamController():
        if pyxel.btn(pyxel.KEY_A): GameManager.Camera.Position[0] -= Camera.speed
        if pyxel.btn(pyxel.KEY_D): GameManager.Camera.Position[0] += Camera.speed
        if pyxel.btn(pyxel.KEY_W): GameManager.Camera.Position[1] -= Camera.speed
        if pyxel.btn(pyxel.KEY_S): GameManager.Camera.Position[1] += Camera.speed
            
        if pyxel.btnp(pyxel.KEY_SHIFT): Camera.speed = Camera.velocities[1]
        if pyxel.btnr(pyxel.KEY_SHIFT): Camera.speed = Camera.velocities[0]
        
        pyxel.camera(GameManager.Camera.Position[0], GameManager.Camera.Position[1])

class App:
    def __init__(self):
        pyxel.init(
            width  = GameManager.AppInfo.ScreenWidth, 
            height = GameManager.AppInfo.ScreenHeight, 
            title  = GameManager.AppInfo.WindowTitle, 
            fps    = GameManager.AppInfo.Fps
        )
        
        Data.GameData.Start()
        
        WorldGen.GetGameData()
        Renderer.GetGameData()

        GameManager.PerlinNoise.init_seed(128)

        pyxel.run(self.update, self.draw)
        
    def update(self):
        Camera.CamController()
        WorldGen.GenWorld()
        Debug.UpdateDebug()
    
    def draw(self):
        pyxel.cls(0)

        Renderer.WorldRenderer()

        Debug.DrawDebug()
        pyxel.camera(0, 0)
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 1, 0, 240, 8, 8, 2)

App()
