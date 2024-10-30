import pyxel
import json
import random

# Config Section
SECREEN_SIZE = [128, 128]
WINDOW_TITLE = 'PyxelCraft'
DISPLAY_SCALE = 7
FPS = 60

# Carregar JSON file data
with open('blocks_id.json') as f: block_data = json.load(f)
total_blocks = len(block_data['Blocks'])

# Camera
camera_diff = [0, 0]

# UI
Show_F3 = False

# World Layers
World_layer_0 = {} # Bedrock
World_layer_1 = {} # Stone & Ores
World_layer_2 = {} # Stone & Dirt
World_layer_3 = {} # Grass & Dirt
World_layer_4 = {} # Player Level
World_layer_5 = {} # Above Player Level
World_Layers = []
World_Layers.extend([World_layer_0, World_layer_1, World_layer_2, World_layer_3, World_layer_4, World_layer_5])

# Show Layers Debug
Show_Layer_0 = True
Show_Layer_1 = True
Show_Layer_2 = True
Show_Layer_3 = True
Show_Layer_4 = True
Show_Layer_5 = True

# Gameplay
Selected_block = 0
Selected_Layer = 4

class InputManager:
    def CameraController():
        if pyxel.btn(pyxel.KEY_LEFT):
            camera_diff[0] -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            camera_diff[0] += 1
        if pyxel.btn(pyxel.KEY_UP):
            camera_diff[1] -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            camera_diff[1] += 1
        
        pyxel.camera(camera_diff[0], camera_diff[1])
    
    def MousePosition():
        mouse_x = pyxel.mouse_x + camera_diff[0]
        mouse_y = pyxel.mouse_y + camera_diff[1]
        pyxel.rect(mouse_x, mouse_y, 1, 1, 7)
        
    def PlaceBlock():
        global Selected_block, Selected_Layer
        
        if pyxel.btnp(pyxel.KEY_EQUALS): Selected_block = (Selected_block + 1) % total_blocks
        if pyxel.btnp(pyxel.KEY_MINUS): Selected_block = (Selected_block - 1) % total_blocks
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            World_Layers[Selected_Layer][(pyxel.mouse_x + camera_diff[0]) // 8 * 8, (pyxel.mouse_y + camera_diff[1]) // 8 * 8] = {
                "Pos": [
                    (pyxel.mouse_x + camera_diff[0]) // 8 * 8,
                    (pyxel.mouse_y + camera_diff[1]) // 8 * 8
                ],
                "Block": block_data['Blocks'][Selected_block]['name']
            }
    
    def SelectLayer():
        global Selected_Layer
        
        if pyxel.btnp(pyxel.KEY_0): Selected_Layer = 0
        if pyxel.btnp(pyxel.KEY_1): Selected_Layer = 1
        if pyxel.btnp(pyxel.KEY_2): Selected_Layer = 2
        if pyxel.btnp(pyxel.KEY_3): Selected_Layer = 3
        if pyxel.btnp(pyxel.KEY_4): Selected_Layer = 4
        if pyxel.btnp(pyxel.KEY_5): Selected_Layer = 5
    
    def DebugKeys():
        global Show_Layer_0, Show_Layer_1, Show_Layer_2, Show_Layer_3, Show_Layer_4, Show_Layer_5, Show_F3
        
        if pyxel.btnp(pyxel.KEY_KP_0): Show_Layer_0 = not Show_Layer_0
        if pyxel.btnp(pyxel.KEY_KP_1): Show_Layer_1 = not Show_Layer_1
        if pyxel.btnp(pyxel.KEY_KP_2): Show_Layer_2 = not Show_Layer_2
        if pyxel.btnp(pyxel.KEY_KP_3): Show_Layer_3 = not Show_Layer_3
        if pyxel.btnp(pyxel.KEY_KP_4): Show_Layer_4 = not Show_Layer_4
        if pyxel.btnp(pyxel.KEY_KP_5): Show_Layer_5 = not Show_Layer_5
        
        if pyxel.btnp(pyxel.KEY_F3): Show_F3 = not Show_F3

class UI:
    def UIDebugger():
        pyxel.text(5, 5, f"FPS: {pyxel.frame_count}", 7)
        
    def ItemSlot():
        global Selected_block
        
        pyxel.rect(1, 1, 10, 10, 7)
        pyxel.rect(2, 2, 8, 8, 13)
        
        selected_block = block_data['Blocks'][Selected_block]['name']
        
        block = next(block for block in block_data['Blocks'] if block['name'] == selected_block)
        block_x = block['local']['x']
        block_y = block['local']['y']
        block_w = block['size']['w']
        block_h = block['size']['h']

        pyxel.blt(2, 2, 0, block_x, block_y, block_w, block_h, 2)
        pyxel.text(13, 2, f"Layer: {Selected_Layer}" , 7)

class Optife:
    def GetGenerationArea():
        start_x = ((camera_diff[0] // 8 - SECREEN_SIZE[0] // 8) - 4) * 8
        end_x = ((camera_diff[0] // 8 + SECREEN_SIZE[0] // 8) + 4) * 8
        start_y = ((camera_diff[1] // 8 - SECREEN_SIZE[1] // 8) - 4) * 8
        end_y = ((camera_diff[1] // 8 + SECREEN_SIZE[1] // 8) + 4) * 8
        return start_x, end_x, start_y, end_y

class WorldRandomGen:
    def RandomOresDefine():
        rolldice = random.randint(1, 10)
        if rolldice > 9:
            rolldice = random.randint(1, 10)
            if rolldice > 5:
                rolldice = random.randint(1, 10)
                if rolldice <= 5: return "Iron_Ore_block"
                elif rolldice > 5 and rolldice <= 7: return "Gold_Ore_block"
                elif rolldice > 7  and rolldice < 10: return "Diamond_Ore_block"
                elif rolldice == 10: return "Emerald_Ore_block"
            else:
                return "Coal_Ore_block"
        else:
            return "Cobblestone_block"
        
    def RandomStoneDirtDefine():
        rolldice = random.randint(1, 10)
        if rolldice > 5: return "Dirt_block"
        else: return "Stone_block"
    
    def RandomGrassDirtDefine():
        rolldice = random.randint(1, 1000)
        if rolldice > 999:
            return "Water_block"
        else:
            rolldice = random.randint(1, 100)
            if rolldice > 99: return "Dirt_block"
            else: return "Grass_block"
    
    def RandomTreePositionDefine():
        rolldice = random.randint(1, 100)
        if rolldice > 99: return "Wood_Log_block_Bottom"
        else: return "Air"

class WorldGen:
    @staticmethod
    def WorldGenLayer0():
        start_x, end_x, start_y, end_y = Optife.GetGenerationArea()

        for x in range(start_x, end_x, 8):
            for y in range(start_y, end_y, 8):
                if (x, y) not in World_layer_0:
                    World_layer_0[(x, y)] = {
                        "Pos": [x, y],
                        "Block": "Bedrock_block"
                    }
    
    def WorldGenLayer1():
        start_x, end_x, start_y, end_y = Optife.GetGenerationArea()

        for x in range(start_x, end_x, 8):
            for y in range(start_y, end_y, 8):
                if (x, y) not in World_layer_1:
                    
                    blockselection = WorldRandomGen.RandomOresDefine()
                    
                    World_layer_1[(x, y)] = {
                        "Pos": [x, y],
                        "Block": blockselection
                    }
    
    def WorldGenLayer2():
        start_x, end_x, start_y, end_y = Optife.GetGenerationArea()

        for x in range(start_x, end_x, 8):
            for y in range(start_y, end_y, 8):
                if (x, y) not in World_layer_2:
                    
                    blockselection = WorldRandomGen.RandomStoneDirtDefine()
                    
                    World_layer_2[(x, y)] = {
                        "Pos": [x, y],
                        "Block": blockselection
                    }
    
    def WorldGenLayer3():
        start_x, end_x, start_y, end_y = Optife.GetGenerationArea()

        for x in range(start_x, end_x, 8):
            for y in range(start_y, end_y, 8):
                if (x, y) not in World_layer_3:
                    
                    blockselection = WorldRandomGen.RandomGrassDirtDefine()
                    
                    World_layer_3[(x, y)] = {
                        "Pos": [x, y],
                        "Block": blockselection
                    }
    
    def WorldGenLayer4():
        start_x, end_x, start_y, end_y = Optife.GetGenerationArea()

        for x in range(start_x, end_x, 8):
            for y in range(start_y, end_y, 8):
                if (x, y) not in World_layer_4:
                    
                    blockselection = WorldRandomGen.RandomTreePositionDefine()
                    
                    World_layer_4[(x, y)] = {
                        "Pos": [x, y],
                        "Block": blockselection
                    }

                    if blockselection == "Wood_Log_block_Bottom":
                        for dx in range(-4, 5):
                            for dy in range(-4, 5):
                                if dx * dx + dy * dy <= 16:
                                    if (x + dx * 8, y + dy * 8) not in World_layer_4:
                                        World_layer_4[(x + dx * 8, y + dy * 8)] = {
                                            "Pos": [x + dx * 8, y + dy * 8],
                                            "Block": "Air"
                                        }
                        
                        World_layer_4[(x, y - 8)] = {
                            "Pos": [x, y - 8],
                            "Block": "Wood_Log_block_Bottom"
                        }
                        
                        World_layer_4[(x, y - 8 * 2)] = {
                            "Pos": [x, y - 8 * 2],
                            "Block": "Wood_Log_block_Top"
                        }
    
    def WorldGenLayer5():
        start_x, end_x, start_y, end_y = Optife.GetGenerationArea()

        for x in range(start_x, end_x, 8):
            for y in range(start_y, end_y, 8):
                if World_layer_4[(x, y)]["Block"] == "Wood_Log_block_Top" and (x, y) not in World_layer_5:
                    World_layer_5[(x, y)] = {"Pos": [x, y],"Block": "Leaves_block"}
                    World_layer_5[(x + 8, y)] = {"Pos": [x + 8, y],"Block": "Leaves_block"}
                    World_layer_5[(x - 8, y)] = {"Pos": [x - 8, y],"Block": "Leaves_block"}
                    World_layer_5[(x, y - 8)] = {"Pos": [x, y - 8],"Block": "Leaves_block"}

class Renderer:
    def RenderLayers(WorldLayer):
        center_x = (camera_diff[0] // 8) * 8 + 64
        center_y = (camera_diff[1] // 8) * 8 + 64

        half_width = 64
        half_height = 64

        start_x = center_x - half_width
        end_x = center_x + half_width
        start_y = center_y - half_height
        end_y = center_y + half_height
        
        for v in WorldLayer.values():
            if start_x <= v["Pos"][0] <= end_x and start_y <= v["Pos"][1] <= end_y:
                block = next(block for block in block_data['Blocks'] if block['name'] == v["Block"])
        
                block_x = block['local']['x']
                block_y = block['local']['y']
                block_w = block['size']['w']
                block_h = block['size']['h']

                pyxel.blt(v["Pos"][0], v["Pos"][1], 0, block_x, block_y, block_w, block_h, 2)
    

class App:
    def StorageImages():
        pyxel.images[0].load(0, 0, '.\\assets\\sprites\\Sprite_sheet_0.png')
    
    def __init__(self):
        pyxel.init(SECREEN_SIZE[0], SECREEN_SIZE[1], title=WINDOW_TITLE, display_scale=DISPLAY_SCALE, fps=FPS)
        App.StorageImages()
        pyxel.run(self.update, self.draw)
    
    def update(self):
        WorldGen.WorldGenLayer0()
        WorldGen.WorldGenLayer1()
        WorldGen.WorldGenLayer2()
        WorldGen.WorldGenLayer3()
        WorldGen.WorldGenLayer4()
        WorldGen.WorldGenLayer5()
        
        InputManager.CameraController()
        InputManager.DebugKeys()
        InputManager.PlaceBlock()
        InputManager.SelectLayer()
    
    def draw(self):
        pyxel.cls(0)
        
        if Show_Layer_0: Renderer.RenderLayers(World_layer_0)
        if Show_Layer_1: Renderer.RenderLayers(World_layer_1)
        if Show_Layer_2: Renderer.RenderLayers(World_layer_2)
        if Show_Layer_3: Renderer.RenderLayers(World_layer_3)
        if Show_Layer_4: Renderer.RenderLayers(World_layer_4)
        if Show_Layer_5: Renderer.RenderLayers(World_layer_5)
        
        InputManager.MousePosition()
        
        pyxel.camera(0, 0)
        if Show_F3: UI.UIDebugger()
        UI.ItemSlot()
        
App()