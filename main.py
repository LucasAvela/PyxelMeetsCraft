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
Hotbar_Slots_pos = [17, 29, 41, 53, 65, 77, 89, 101]
Hotbar_Items_pos = [18, 30, 42, 54, 66, 78, 90, 102]
Hotbar_Items = [
    ["Grass_block", "Dirt_block", "Grass_Dirty_block", "Stone_block", "Cobblestone_block", "Wood_Log_block_Top", "Wood_Log_block_Bottom", "Wood_Plank_block"],
    ["Bedrock_block", "Coal_Ore_block", "Iron_Ore_block", "Gold_Ore_block", "Diamond_Ore_block", "Emerald_Ore_block", "Leaves_block", "Empty"],
    ["Workbench_block", "Chest_block", "Furnace_block", "Bed_block_Top", "Bed_block_Bottom", "Water_block_0", "Water_block_1", "Empty"]
]
Actual_Hotbar = 0
Hotbar_Selected_slot = 0
Selected_Item = Hotbar_Items[Actual_Hotbar][Hotbar_Selected_slot]

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

class InputManager:
    def CameraController():
        if pyxel.btn(pyxel.KEY_A):
            camera_diff[0] -= 1
        if pyxel.btn(pyxel.KEY_D):
            camera_diff[0] += 1
        if pyxel.btn(pyxel.KEY_W):
            camera_diff[1] -= 1
        if pyxel.btn(pyxel.KEY_S):
            camera_diff[1] += 1
        
        pyxel.camera(camera_diff[0], camera_diff[1])
    
    def MousePosition():
        mouse_x = pyxel.mouse_x + camera_diff[0]
        mouse_y = pyxel.mouse_y + camera_diff[1]
        pyxel.rect(mouse_x, mouse_y, 1, 1, 7)
        
    def BreakBlock():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            BlockPosition = [(pyxel.mouse_x + camera_diff[0]) // 8 * 8, (pyxel.mouse_y + camera_diff[1]) // 8 * 8]
            LastLayer = len(World_Layers) - 1
            ActualLayer = LastLayer
            
            while ActualLayer > 0:
                if (BlockPosition[0], BlockPosition[1]) not in World_Layers[ActualLayer] or World_Layers[ActualLayer][(BlockPosition[0], BlockPosition[1])]["Block"] == "Air":
                    ActualLayer -= 1
                else: 
                    World_Layers[ActualLayer][BlockPosition[0],BlockPosition[1]] = {
                        "Pos": [BlockPosition[0],BlockPosition[1]],
                        "Block": "Air"
                    }
                    return
        
    def PlaceBlock():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            BlockPosition = [(pyxel.mouse_x + camera_diff[0]) // 8 * 8, (pyxel.mouse_y + camera_diff[1]) // 8 * 8]
            LastLayer = len(World_Layers)
            ActualLayer = 1
            
            while ActualLayer < LastLayer:
                if (BlockPosition[0], BlockPosition[1]) in World_Layers[ActualLayer] and World_Layers[ActualLayer][(BlockPosition[0], BlockPosition[1])]["Block"] != "Air":
                    ActualLayer += 1
                else:
                    World_Layers[ActualLayer][BlockPosition[0],BlockPosition[1]] = {
                        "Pos": [BlockPosition[0],BlockPosition[1]],
                        "Block": Selected_Item
                    }
                    return
    
    def ChangeHotbar():
        global Actual_Hotbar, Selected_Item, Hotbar_Selected_slot
        
        if pyxel.btnp(pyxel.KEY_Q): Actual_Hotbar = (Actual_Hotbar + 1) % (len(Hotbar_Items))
        
        if pyxel.btnp(pyxel.KEY_1): Hotbar_Selected_slot = 0
        if pyxel.btnp(pyxel.KEY_2): Hotbar_Selected_slot = 1
        if pyxel.btnp(pyxel.KEY_3): Hotbar_Selected_slot = 2
        if pyxel.btnp(pyxel.KEY_4): Hotbar_Selected_slot = 3
        if pyxel.btnp(pyxel.KEY_5): Hotbar_Selected_slot = 4
        if pyxel.btnp(pyxel.KEY_6): Hotbar_Selected_slot = 5
        if pyxel.btnp(pyxel.KEY_7): Hotbar_Selected_slot = 6
        if pyxel.btnp(pyxel.KEY_8): Hotbar_Selected_slot = 7
        
        if pyxel.btnp(pyxel.KEY_RIGHT): Hotbar_Selected_slot = (Hotbar_Selected_slot + 1) & 7
        if pyxel.btnp(pyxel.KEY_LEFT): Hotbar_Selected_slot = (Hotbar_Selected_slot - 1) & 7
        
        Selected_Item = Hotbar_Items[Actual_Hotbar][Hotbar_Selected_slot]
    
    def DebugKeys():
        global Show_Layer_0, Show_Layer_1, Show_Layer_2, Show_Layer_3, Show_Layer_4, Show_Layer_5
        
        if pyxel.btnp(pyxel.KEY_KP_0): Show_Layer_0 = not Show_Layer_0
        if pyxel.btnp(pyxel.KEY_KP_1): Show_Layer_1 = not Show_Layer_1
        if pyxel.btnp(pyxel.KEY_KP_2): Show_Layer_2 = not Show_Layer_2
        if pyxel.btnp(pyxel.KEY_KP_3): Show_Layer_3 = not Show_Layer_3
        if pyxel.btnp(pyxel.KEY_KP_4): Show_Layer_4 = not Show_Layer_4
        if pyxel.btnp(pyxel.KEY_KP_5): Show_Layer_5 = not Show_Layer_5

class UI:
    def UIDebugger():
        pyxel.text(5, 5, f"FPS: {pyxel.frame_count}", 7)
        
    def ItemHotbar():
        global Hotbar_Selected_slot
        pyxel.rect(Hotbar_Slots_pos[Hotbar_Selected_slot] - 1, 115, 12, 12, 10)
        
        for i, slot in enumerate(Hotbar_Slots_pos):
            pyxel.rect(slot, 116, 10, 10, 7)
            pyxel.rect(slot + 1, 117, 8, 8, 13)
            pyxel.text(slot + 2, 111, str(i + 1), 1)
            pyxel.text(slot + 1, 111, str(i + 1), 7)
        
        for i, item in enumerate(Hotbar_Items[Actual_Hotbar]):
            block = next(block for block in block_data['Blocks'] if block['name'] == item)
            block_x = block['local']['x']
            block_y = block['local']['y']
            block_w = block['size']['w']
            block_h = block['size']['h']
            pyxel.blt(Hotbar_Items_pos[i], 117, 0, block_x, block_y, block_w, block_h, 2)
            
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
        rolldice = random.randint(1, 100)
        if rolldice > 99: return "Grass_Dirty_block"
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
        InputManager.ChangeHotbar()
        InputManager.PlaceBlock()
        InputManager.BreakBlock()
    
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
        UI.ItemHotbar()
        
App()