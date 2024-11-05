import pyxel
import json
import random

#-------------------------------- App
SCREEN_SIZE = [128, 128]
WINDOW_TITLE = 'Pyxel Meets Craft'
DISPLAY_SCALE = 7
FPS = 60

#-------------------------------- Game
BLOCK_SIZE = 8
GAME_STATE = 'MainMenu'
GAME_STATE_LIST = ['MainMenu', 'Gameplay', 'Pause']
BLOCKSBYLAYER = [
    {'Bedrock_block': 100},
    {'Cobblestone_block': 90, 'Coal_Ore_block': 5, 'Iron_Ore_block': 2, 'Gold_Ore_block': 1.5, 'Diamond_Ore_block': 1, 'Emerald_Ore_block': 0.5},
    {'Stone_block': 50, 'Dirt_block': 50},
    {'Grass_block': 99, 'Grass_Dirty_block': 1},
    {'Tree_block': 0.5,'Air': 99.5},
    {'Air': 100}
]

class MainMenu:
    Buttons = {
        'Play': {'Pos': [8, 75], 'Font': [129, 1], 'Size': [48, 18]},
        'Load': {'Pos': [72, 75], 'Font': [178, 1], 'Size': [48, 18]}
    }
    
    class Transition:
        Animation_blocks = []
        transition_active = False
        transition_timer = [0, 0]
        
        def UpdateTransition():
            if MainMenu.Transition.transition_active:
                if MainMenu.Transition.transition_timer[0] < SCREEN_SIZE[0] / BLOCK_SIZE:
                    x = MainMenu.Transition.transition_timer[0] * 8
                    y = MainMenu.Transition.transition_timer[1] * 8
                    MainMenu.Transition.Animation_blocks.append([x, y])
                    MainMenu.Transition.transition_timer[0] += 2
                elif MainMenu.Transition.transition_timer[1] < SCREEN_SIZE[1] / BLOCK_SIZE: 
                    MainMenu.Transition.transition_timer[0] = 0
                    MainMenu.Transition.transition_timer[1] += 2
                else:
                    MainMenu.Transition.transition_active = False
                    StateMachine.ChangeGameState(GAME_STATE_LIST[1])

    def MouseDraw():
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 248, 120, 8, 8, 8)
        
    def Canvas():
        pyxel.blt(0, 0, 0, 0, 0, 128, 128)  # Background
        
        for key, button in MainMenu.Buttons.items():
            pos_x, pos_y = button['Pos']
            font_u, font_v = button['Font']
            size_w, size_h = button['Size']
            
            pyxel.blt(pos_x, pos_y, 0, font_u, font_v, size_w, size_h, 8)
        
        for e in MainMenu.Transition.Animation_blocks:
            pyxel.rect(e[0], e[1], BLOCK_SIZE * 2, BLOCK_SIZE * 2, 0)
    
    def ButtonFunc(button):
        if button == "Play":
            MainMenu.Transition.transition_active = True
        elif button == "Load":
            Gameplay.Atlas.SaveLoad.LoadWorld()
            MainMenu.Transition.transition_active = True
    
    def Inputs():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for key, button in MainMenu.Buttons.items():
                dx = pyxel.mouse_x - button['Pos'][0]
                dy = pyxel.mouse_y - button['Pos'][1]
                    
                if 0 <= dx < button['Size'][0] and 0 <= dy < button['Size'][1]:
                    MainMenu.ButtonFunc(key)
                        
    def Update():
        MainMenu.Inputs()
        MainMenu.Transition.UpdateTransition()
    
    def Draw():
        MainMenu.Canvas()
        MainMenu.MouseDraw()

class Gameplay:
    class Camera:
        diff = [0, 0]
        speed = 1
        velocities = [1, 4]
        
        def CamController():
            if pyxel.btn(pyxel.KEY_A): Gameplay.Camera.diff[0] -= Gameplay.Camera.speed
            if pyxel.btn(pyxel.KEY_D): Gameplay.Camera.diff[0] += Gameplay.Camera.speed
            if pyxel.btn(pyxel.KEY_W): Gameplay.Camera.diff[1] -= Gameplay.Camera.speed
            if pyxel.btn(pyxel.KEY_S): Gameplay.Camera.diff[1] += Gameplay.Camera.speed
                
            if pyxel.btnp(pyxel.KEY_SHIFT): Gameplay.Camera.speed = Gameplay.Camera.velocities[1]
            if pyxel.btnr(pyxel.KEY_SHIFT): Gameplay.Camera.speed = Gameplay.Camera.velocities[0]
            
            pyxel.camera(Gameplay.Camera.diff[0], Gameplay.Camera.diff[1])
        
        def UICamera():
            pyxel.camera(0, 0)
 
    class UI:
        Show_Debug = False
        Hotbar_Slots_pos = [17, 29, 41, 53, 65, 77, 89, 101]
        Hotbar_Items_pos = [18, 30, 42, 54, 66, 78, 90, 102]
        Hotbar_Selected_slot = 0
        
        def DrawMouse():
            pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 1, 1, 7)
        
        def Inputs():
            if pyxel.btnp(pyxel.KEY_F3): Gameplay.UI.Show_Debug = not Gameplay.UI.Show_Debug
            
            if pyxel.btnp(pyxel.KEY_1): Gameplay.UI.Hotbar_Selected_slot = 0
            if pyxel.btnp(pyxel.KEY_2): Gameplay.UI.Hotbar_Selected_slot = 1
            if pyxel.btnp(pyxel.KEY_3): Gameplay.UI.Hotbar_Selected_slot = 2
            if pyxel.btnp(pyxel.KEY_4): Gameplay.UI.Hotbar_Selected_slot = 3
            if pyxel.btnp(pyxel.KEY_5): Gameplay.UI.Hotbar_Selected_slot = 4
            if pyxel.btnp(pyxel.KEY_6): Gameplay.UI.Hotbar_Selected_slot = 5
            if pyxel.btnp(pyxel.KEY_7): Gameplay.UI.Hotbar_Selected_slot = 6
            if pyxel.btnp(pyxel.KEY_8): Gameplay.UI.Hotbar_Selected_slot = 7
            
            if pyxel.btnv(pyxel.mouse_wheel > 0): Gameplay.UI.Hotbar_Selected_slot = (Gameplay.UI.Hotbar_Selected_slot + 1) & 7
            if pyxel.btnv(pyxel.mouse_wheel < 0): Gameplay.UI.Hotbar_Selected_slot = (Gameplay.UI.Hotbar_Selected_slot - 1) & 7   
                
        def Hotbar():
            pyxel.rect(Gameplay.UI.Hotbar_Slots_pos[Gameplay.UI.Hotbar_Selected_slot] -1, 115, 12, 12, 10)
            
            for i, slot in enumerate(Gameplay.UI.Hotbar_Slots_pos):
                pyxel.rect(slot, 116, 10, 10, 7)
                pyxel.rect(slot + 1, 117, 8, 8, 13)
                pyxel.text(slot + 2, 111, str(i + 1), 1)
                pyxel.text(slot + 1, 111, str(i + 1), 7)
        
        def Debug():
            pyxel.text(2, 1, f'x:{(pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8}\ny:{(pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8}', 7)
        
        def Update():
            Gameplay.UI.Inputs()
        
        def Draw():
            Gameplay.Camera.UICamera()
            Gameplay.UI.DrawMouse()
            Gameplay.UI.Hotbar()
            if Gameplay.UI.Show_Debug: Gameplay.UI.Debug()
        
    class Optfine:
        def GetGenerationArea():
            start_x = (Gameplay.Camera.diff[0] // BLOCK_SIZE) * BLOCK_SIZE - BLOCK_SIZE
            end_x = (Gameplay.Camera.diff[0] // BLOCK_SIZE + SCREEN_SIZE[0] // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE
            start_y = (Gameplay.Camera.diff[1] // BLOCK_SIZE) * BLOCK_SIZE - BLOCK_SIZE
            end_y = (Gameplay.Camera.diff[1] // BLOCK_SIZE + SCREEN_SIZE[1] // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE * 4
            return start_x, end_x, start_y, end_y
        
    class Atlas:
        World = {}
        MaxLayerValue = len(BLOCKSBYLAYER)
        LayerVisibility = MaxLayerValue
        
        def GetRandomBlock(layer):
            blocks = []
            weights = [] 
            
            for block, probability in BLOCKSBYLAYER[layer].items():
                blocks.append(block)
                weights.append(probability)
            
            choice = random.choices(blocks, weights)
            return choice[0]
        
        def GenerateWorldLayers():
            for i in range(0, Gameplay.Atlas.MaxLayerValue):
                Gameplay.Atlas.WorldGenLayer(i)
        
        def WorldGenLayer(layer):
            start_x, end_x, start_y, end_y = Gameplay.Optfine.GetGenerationArea()

            for x in range(start_x, end_x, BLOCK_SIZE):
                for y in range(start_y, end_y, BLOCK_SIZE):
                    if (x, y, layer) not in Gameplay.Atlas.World:
                        blockselected = Gameplay.Atlas.GetRandomBlock(layer)
                        Gameplay.Atlas.World[(x, y, layer)] = {'Block': blockselected}
        
        def RendererLayer():
            start_x, end_x, start_y, end_y = Gameplay.Optfine.GetGenerationArea()
            
            for layer in range(0, Gameplay.Atlas.LayerVisibility):
                for x in range(start_x, end_x, BLOCK_SIZE):
                    for y in range(start_y, end_y, BLOCK_SIZE):
                        if (x, y, layer) in Gameplay.Atlas.World:
                            v = Gameplay.Atlas.World[(x, y, layer)]
                            block = next(block for block in Data.block_data['Blocks'] if block['name'] == v["Block"])
                            block_x = block['local']['x']
                            block_y = block['local']['y']
                            
                            pyxel.blt(x, y, 1, block_x, block_y, BLOCK_SIZE, BLOCK_SIZE, 2)
        
        class Structures:
           def GenerateWorldStructure():
                start_x, end_x, start_y, end_y = Gameplay.Optfine.GetGenerationArea()
                
                for x in range(start_x, end_x, BLOCK_SIZE):
                    for y in range(start_y, end_y, BLOCK_SIZE):
                        if Gameplay.Atlas.World[(x, y, 4)]['Block'] == "Tree_block":
                            Gameplay.Atlas.Structures.CreateTree(x, y, 4)
            
           def CreateTree(x, y, layer):
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': "Wood_Log_block_Bottom"}
                Gameplay.Atlas.World[(x, y - 8, layer)] = {'Block': "Wood_Log_block_Bottom"}
                Gameplay.Atlas.World[(x, y - 16, layer)] = {'Block': "Wood_Log_block_Top"}
                Gameplay.Atlas.World[(x, y - 16, layer + 1)] = {'Block': "Leaves_block"}
                Gameplay.Atlas.World[(x, y - 24, layer + 1)] = {'Block': "Leaves_block"}
                Gameplay.Atlas.World[(x - 8, y - 16, layer + 1)] = {'Block': "Leaves_block"}
                Gameplay.Atlas.World[(x + 8, y - 16, layer + 1)] = {'Block': "Leaves_block"}
        
        class SaveLoad:
            def SaveWorld():
                world_data = {str(key): value for key, value in Gameplay.Atlas.World.items()}
                with open("world_data.json", "w") as file:
                    json.dump(world_data, file)
                print("World saved to world_data.json")
                
            def LoadWorld():
                try:
                    with open("world_data.json", "r") as file:
                        loaded_data = json.load(file)
                        Gameplay.Atlas.World = {eval(key): value for key, value in loaded_data.items()}
                    print("World loaded from world_data.json")
                except FileNotFoundError:
                    print("No saved world file found. Starting with a new world.")
                except json.JSONDecodeError:
                    print("Error decoding the saved world file. Starting with a new world.")

    class Player:
        frame_count = 0
        blint_mouse = False
        
        break_progress = 0
        last_target = [None, None]
        hold_break = False
        
        def SelectionArea():
            mouse_x = (pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8
            mouse_y = (pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8
            
            Gameplay.Player.frame_count += 1
            if Gameplay.Player.frame_count >= 15:
                Gameplay.Player.frame_count = 0
                Gameplay.Player.blint_mouse = not Gameplay.Player.blint_mouse
            
            if Gameplay.Player.blint_mouse: pyxel.blt(mouse_x, mouse_y, 1, 72, 0, 8, 8, 2)
            else: pyxel.blt(mouse_x, mouse_y, 1, 72, 8, 8, 8, 2)

            if 16 > Gameplay.Player.break_progress > 0: pyxel.blt(mouse_x, mouse_y, 1, 64, 0, 8, 8, 2)
            elif 32 > Gameplay.Player.break_progress > 16: pyxel.blt(mouse_x, mouse_y, 1, 64, 8, 8, 8, 2)
            elif 48 > Gameplay.Player.break_progress > 32: pyxel.blt(mouse_x, mouse_y, 1, 64, 16, 8, 8, 2)
            elif 64 > Gameplay.Player.break_progress > 48: pyxel.blt(mouse_x, mouse_y, 1, 64, 24, 8, 8, 2)
        
        def BreakBLock():
            target_x = (pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8
            target_y = (pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8
            layer = Gameplay.Atlas.MaxLayerValue
            
            if Gameplay.Player.last_target != [target_x, target_y]:
                Gameplay.Player.break_progress = 0
                Gameplay.Player.last_target = [target_x, target_y]
            
            while layer > 0:
                if (target_x, target_y, layer) not in Gameplay.Atlas.World or Gameplay.Atlas.World[(target_x, target_y, layer)]['Block'] == 'Air':
                    layer -= 1
                else:
                    if Gameplay.Player.break_progress > 64:
                        Gameplay.Atlas.World[(target_x, target_y, layer)] = {'Block': 'Air'}
                        Gameplay.Player.break_progress = 0
                        Gameplay.Player.hold_break = True
                        return
                    else:
                        Gameplay.Player.break_progress += 1
                        return
        
        def PlaceBlock():
            target_x = (pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8
            target_y = (pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8
            layer = 0
            
            while layer < Gameplay.Atlas.MaxLayerValue:
                if (target_x, target_y, layer) not in Gameplay.Atlas.World or Gameplay.Atlas.World[(target_x, target_y, layer)]['Block'] == 'Air':
                    Gameplay.Atlas.World[(target_x, target_y, layer)] = {'Block': 'Chest_block'}
                else:
                    layer += 1
        
        def Inputs():
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not Gameplay.Player.hold_break: Gameplay.Player.BreakBLock() 
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT): Gameplay.Player.break_progress = 0; Gameplay.Player.hold_break = False
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT): Gameplay.Player.PlaceBlock()
            
            if pyxel.btnp(pyxel.KEY_E): StateMachine.ChangeGameState('Pause')
        
        def Update():
            Gameplay.Player.Inputs()
                
    def Debug():
        if pyxel.btnp(pyxel.KEY_EQUALS) and Gameplay.Atlas.LayerVisibility < Gameplay.Atlas.MaxLayerValue:
            Gameplay.Atlas.LayerVisibility += 1
        
        if pyxel.btnp(pyxel.KEY_MINUS) and Gameplay.Atlas.LayerVisibility > 0:
            Gameplay.Atlas.LayerVisibility -= 1
            
        if pyxel.btnp(pyxel.KEY_0):
            Gameplay.Atlas.SaveLoad.SaveWorld()
    
    def Update():
        Gameplay.Camera.CamController()
        Gameplay.Atlas.GenerateWorldLayers()
        Gameplay.Atlas.Structures.GenerateWorldStructure()
        Gameplay.UI.Update()
        Gameplay.Player.Update()
        
        Gameplay.Debug()
    
    def Draw():
        Gameplay.Atlas.RendererLayer()
        Gameplay.Player.SelectionArea()
        
        Gameplay.UI.Draw()

class Inventory:
    Inventory_items_Position = [
        [18, 66], [30, 66], [42, 66], [54, 66], [66, 66], [78, 66], [90, 66], [102, 66],
        [18, 78], [30, 78], [42, 78], [54, 78], [66, 78], [78, 78], [90, 78], [102, 78],
        [18, 90], [30, 90], [42, 90], [54, 90], [66, 90], [78, 90], [90, 90], [102, 90],
        
        [18, 110], [30, 110], [42, 110], [54, 110], [66, 110], [78, 110], [90, 110], [102, 110]
    ]
    
    def DrawItemsOnInventory():
        for ItemSlot in Inventory.Inventory_items_Position:
            pyxel.blt(ItemSlot[0], ItemSlot[1], 1, 96, 00, 8, 8, 2)
    
    def Update():
        if pyxel.btnp(pyxel.KEY_E): StateMachine.ChangeGameState('Gameplay')
    
    def Draw():
        Gameplay.Atlas.RendererLayer()
        
        Gameplay.Camera.UICamera()
        pyxel.blt(0, 0, 0, 0, 128, 128, 128, 8)
        Inventory.DrawItemsOnInventory()
        pyxel.camera(Gameplay.Camera.diff[0], Gameplay.Camera.diff[1])

class StateMachine:
    def ChangeGameState(newState):
        global GAME_STATE
        GAME_STATE = newState
        
        print('Game state changed to:', GAME_STATE)

class Data:
    def Images():
        pyxel.images[0].load(0, 0, './assets/sprites/Background_MainMenu.png')  # main menu bg
        pyxel.images[1].load(0, 0, './assets/sprites/Sprite_sheet_0.png')       # blocks, items, and player

    with open('blocks_id.json') as f: block_data = json.load(f)

class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title=WINDOW_TITLE, display_scale=DISPLAY_SCALE, fps=FPS, quit_key=None)
        
        Data.Images()

        pyxel.run(self.update, self.draw)
        
    def update(self):
        if GAME_STATE == 'MainMenu': MainMenu.Update()
        elif GAME_STATE == 'Gameplay': Gameplay.Update()
        elif GAME_STATE == 'Pause': Inventory.Update()
    
    def draw(self):
        pyxel.cls(0)
        if GAME_STATE == 'MainMenu': MainMenu.Draw()
        elif GAME_STATE == 'Gameplay': Gameplay.Draw()
        elif GAME_STATE == 'Pause': Inventory.Draw()

App()