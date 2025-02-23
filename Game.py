import pyxel

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer

#-------------------------------- App
SCREEN_SIZE = [256, 256]
WINDOW_TITLE = 'Pyxel Meets Craft'
FPS = 60
TPS = FPS // 3

#-------------------------------- Game
BLOCK_SIZE = 8
BLOCK_HEIGHT = 4
VIEW_DISTANCE = 12
GAME_STATE = 'MainMenu'
GAME_STATE_LIST = ['MainMenu', 'Gameplay', 'Menu']
BLOCKSBYLAYER = [
    {Data.Blocks.Bedrock_block.value: 100},
    {Data.Blocks.Cobblestone_block.value: 90, Data.Blocks.Coal_Ore_block.value: 5, Data.Blocks.Iron_Ore_block.value: 2, Data.Blocks.Gold_Ore_block.value: 1.5, Data.Blocks.Diamond_Ore_block.value: 1, Data.Blocks.Emerald_Ore_block.value: 0.5},
    {Data.Blocks.Stone_block.value: 95, Data.Blocks.Coal_Ore_block.value: 3.5, Data.Blocks.Iron_Ore_block.value: 1, Data.Blocks.Gold_Ore_block.value: 0.5},
    {Data.Blocks.Stone_block.value: 50, Data.Blocks.Dirt_block.value: 50},
    {Data.Blocks.Dirt_block.value: 100},
    {Data.Blocks.Grass_block.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
    {Data.Blocks.Air.value: 100},
]

class Debug:
    frame_count = 0
    blink_mouse = False

    blocks_list = [item.value for item in Data.Blocks]
    selected_block = 0

    def UpdateDebug():
        Debug.frame_count += 1
        if Debug.frame_count >= 15:
            Debug.frame_count = 0
            Debug.blink_mouse = True
        
        if pyxel.btnp(pyxel.KEY_EQUALS):
            for key, item in WorldGen.World.items():
                if item['Block'] != 'Air':
                    print(key, item['Block'])
        
        if pyxel.btnp(pyxel.KEY_1):
            if Debug.selected_block < len(Debug.blocks_list) - 1:
                Debug.selected_block += 1
            
        if pyxel.btnp(pyxel.KEY_2):
            if Debug.selected_block > 0:
                Debug.selected_block -= 1
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            position_x = (pyxel.mouse_x + Camera.diff[0])
            position_y = (pyxel.mouse_y + Camera.diff[1])
            layer = len(BLOCKSBYLAYER) - 1

            while layer > 1:
                target_x = position_x // BLOCK_SIZE
                target_y = (position_y + ((layer % 2) * BLOCK_HEIGHT)) // BLOCK_SIZE
                adj_y = target_y + (layer // 2)

                if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air.value:
                    break

                layer -= 1
            
            if (target_x, adj_y, layer) in WorldGen.World:
                if (target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value:
                    WorldGen.World[(target_x, adj_y, layer)]['Block'] = Data.Blocks.Air.value
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            position_x = (pyxel.mouse_x + Camera.diff[0])
            position_y = (pyxel.mouse_y + Camera.diff[1])
            layer = len(BLOCKSBYLAYER) - 1

            while layer > 0:
                target_x = position_x // BLOCK_SIZE
                target_y = (position_y + ((layer % 2) * BLOCK_HEIGHT)) // BLOCK_SIZE
                adj_y = target_y + (layer // 2)

                if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air.value:
                    break

                layer -= 1
            
            if (target_x, adj_y, layer) in WorldGen.World:
                if (target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value:
                    if (layer + 1) < len(BLOCKSBYLAYER):
                        WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] = Debug.blocks_list[Debug.selected_block]

    
    def DrawDebug():
        position_x = (pyxel.mouse_x + Camera.diff[0])
        position_y = (pyxel.mouse_y + Camera.diff[1])
        layer = len(BLOCKSBYLAYER) - 1

        while layer > 0:
            target_x = position_x // BLOCK_SIZE
            target_y = (position_y + ((layer % 2) * BLOCK_HEIGHT)) // BLOCK_SIZE
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air.value:
                break

            layer -= 1

        if (target_x, adj_y, layer) in WorldGen.World:
            if (target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value:
                pyxel.blt(target_x * BLOCK_SIZE, (target_y * BLOCK_SIZE) - ((layer % 2) * BLOCK_HEIGHT), 1, 48, 240, BLOCK_SIZE, BLOCK_SIZE, 2)
        
        pyxel.camera(0, 0)
        # pyxel.text(4, 4, f'mx: {pyxel.mouse_x + Camera.diff[0]} | my: {pyxel.mouse_y + Camera.diff[1]}', 7)
        # pyxel.text(4, 12, f'x: {target_x} | y: {target_y} | z: {layer}', 7)
        pyxel.text(4, 4, f'x: {target_x} | y: {adj_y} | z: {layer}', 7)
        if (target_x, adj_y, layer) in WorldGen.World:
            if (target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air.value:
                pyxel.text(4, 12, f'{WorldGen.World[(target_x, adj_y, layer)]['Block']}', 7)
        pyxel.text(4, SCREEN_SIZE[1] - 12, f'{Debug.blocks_list[Debug.selected_block]}', 7)
        
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 1, 0, 240, 8, 8, 2)

class Camera:
        diff = [0, 0]
        speed = 1
        velocities = [1, 2]
        
        def CamController():
            if pyxel.btn(pyxel.KEY_A): Camera.diff[0] -= Camera.speed
            if pyxel.btn(pyxel.KEY_D): Camera.diff[0] += Camera.speed
            if pyxel.btn(pyxel.KEY_W): Camera.diff[1] -= Camera.speed
            if pyxel.btn(pyxel.KEY_S): Camera.diff[1] += Camera.speed
                
            if pyxel.btnp(pyxel.KEY_SHIFT): Camera.speed = Camera.velocities[1]
            if pyxel.btnr(pyxel.KEY_SHIFT): Camera.speed = Camera.velocities[0]
            
            pyxel.camera(Camera.diff[0], Camera.diff[1])

class Optfine:
    def GetGenerationArea():
        screen_center_x = SCREEN_SIZE[0] // 2 // BLOCK_SIZE
        screen_center_y = SCREEN_SIZE[1] // 2 // BLOCK_SIZE

        start_x = (Camera.diff[0] // BLOCK_SIZE) + (screen_center_x - VIEW_DISTANCE)
        end_x = start_x + (SCREEN_SIZE[0] // BLOCK_SIZE) - ((screen_center_x - VIEW_DISTANCE) * 2)
        start_y = (Camera.diff[1] // BLOCK_SIZE) + (screen_center_y - VIEW_DISTANCE)
        end_y = start_y + (SCREEN_SIZE[1] // BLOCK_SIZE) - ((screen_center_y - VIEW_DISTANCE) * 2)

        return start_x, end_x, start_y, end_y

class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title=WINDOW_TITLE, fps=FPS, quit_key=None)
        
        Data.GameData()
        Data.Images()
        Data.Colors()

        WorldGen.SetMaxLayerValue(len(BLOCKSBYLAYER))

        pyxel.run(self.update, self.draw)
        
    def update(self):
        Debug.UpdateDebug()
        Camera.CamController()
        WorldGen.GenerateWorldLayers(BLOCKSBYLAYER, Optfine.GetGenerationArea())
    
    def draw(self):
        pyxel.cls(0)
        Renderer.WorldRenderer(Optfine.GetGenerationArea(), BLOCK_SIZE, BLOCK_HEIGHT, len(BLOCKSBYLAYER))
        
        Debug.DrawDebug()

App()