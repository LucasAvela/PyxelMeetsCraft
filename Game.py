import pyxel

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer
import gameFiles.GameManager as GameManager

import gameFiles.MainMenu as MainMenu
import gameFiles.Gameplay as Gameplay

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
                        WorldGen.World[(target_x, adj_y, layer + 1)] = {"Block": Data.Blocks.Stone_Bricks_block.value, "Solid": True}
                    
                    if WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value:
                        WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] = Data.Blocks.Stone_Bricks_block.value
                    
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

                    pyxel.camera(0, 0)
                    pyxel.text(2, 2, f"X: {target_x} Y: {adj_y} L: {layer}", 7)
                    pyxel.text(2, 10, f"{WorldGen.World[(target_x, adj_y, layer)]['Block']}", 7)
                break

class Mouse:
    actual_cursor = "Default"

    cursors = {
        "Default": {"local_x": 0, "local_y": 240, "offset_x": 0, "offset_y": 0},
        "Hand":    {"local_x": 0, "local_y": 248, "offset_x": -3, "offset_y": 0},
        "Sword":   {"local_x": 8, "local_y": 240, "offset_x": 0, "offset_y": 0},
    }

    def DrawMouse():
        x = pyxel.mouse_x
        y = pyxel.mouse_y

        local_x = Mouse.cursors[Mouse.actual_cursor]["local_x"]
        local_y = Mouse.cursors[Mouse.actual_cursor]["local_y"]

        offset_x = Mouse.cursors[Mouse.actual_cursor]["offset_x"]
        offset_y = Mouse.cursors[Mouse.actual_cursor]["offset_y"]

        pyxel.camera(0, 0)
        pyxel.blt(x + offset_x, y + offset_y, 1, local_x, local_y, 8, 8, 2)


class App:
    def __init__(self):
        pyxel.init(
            width  = GameManager.AppInfo.ScreenWidth, 
            height = GameManager.AppInfo.ScreenHeight, 
            title  = GameManager.AppInfo.WindowTitle, 
            fps    = GameManager.AppInfo.Fps
        )
        
        Data.GameData.Start()
        
        Renderer.GetGameData()
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if   GameManager.GameState.current == Data.GameStates.MainMenu.value: MainMenu.Update()
        elif GameManager.GameState.current == Data.GameStates.Gameplay.value: Gameplay.Update()
    
    def draw(self):
        if   GameManager.GameState.current == Data.GameStates.MainMenu.value: MainMenu.Draw()
        elif GameManager.GameState.current == Data.GameStates.Gameplay.value: Gameplay.Draw()
        Mouse.DrawMouse()

App()
