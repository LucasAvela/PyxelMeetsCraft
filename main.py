import pyxel
import json
import random
import copy

#-------------------------------- App
SCREEN_SIZE = [128, 128]
WINDOW_TITLE = 'Pyxel Meets Craft'
FPS = 60
TPS = FPS // 3

#-------------------------------- Game
BLOCK_SIZE = 8
GAME_STATE = 'MainMenu'
GAME_STATE_LIST = ['MainMenu', 'Gameplay', 'Menu']
BLOCKSBYLAYER = [
    {'Bedrock_block': 100},
    {'Cobblestone_block': 90, 'Coal_Ore_block': 5, 'Iron_Ore_block': 2, 'Gold_Ore_block': 1.5, 'Diamond_Ore_block': 1, 'Emerald_Ore_block': 0.5},
    {'Stone_block': 95, 'Coal_Ore_block': 3.5, 'Iron_Ore_block': 1, 'Gold_Ore_block': 0.5},
    {'Stone_block': 50, 'Dirt_block': 50},
    {'Grass_block': 99, 'Grass_Dirty_block': 1},
    {'Tree_block': 0.5,'Air': 99.5},
    {'Air': 100}
]

class MainMenu:
    Menus = ['Main', "Options", 'Controls']
    current_Menu = 'Main'
    
    Buttons = {
        'Play':     {'Pos': [17, 61], 'Font': [129, 56], 'Size': [94, 11]},
        'Load':     {'Pos': [17, 74], 'Font': [129, 68], 'Size': [94, 11]},
        'Options':  {'Pos': [17, 87], 'Font': [129, 80], 'Size': [46, 11]},
        'Controls': {'Pos': [65, 87], 'Font': [177, 80], 'Size': [46, 11]}
    }
    
    Options_Buttons = {
        'CloseOptions': {'Pos': [98, 30], 'Size': [7, 7]},
        'NXMusic':      {'Pos': [93, 98], 'Size': [3, 5]},
        'PVMusic':      {'Pos': [32, 98], 'Size': [3, 5]},
    }
    
    Controls_Buttons = {
        'CloseOptions': {'Pos': [98, 30], 'Size': [7, 7]}
    }
    
    PyxelCraft_txt = [20, 5]
    
    Panels = {
        'Options':   {'Pos': [24, 30], 'Font': [129, 92], 'Size': [83, 83]},
        'Controls':  {'Pos': [24, 30], 'Font': [1,  129], 'Size': [83, 83]}
    }
    
    class Transition:
        dither = -0.5
        intro_active = True
        transition_active = False
        
        def UpdateIntro():
            if MainMenu.Transition.intro_active:
                    if MainMenu.Transition.dither < 1: 
                        MainMenu.Transition.dither += 0.02
                        pyxel.dither(MainMenu.Transition.dither)
                    else:
                        MainMenu.Transition.intro_active = False
                    
        def UpdateTransition():
            if MainMenu.Transition.transition_active:
                if MainMenu.Transition.dither > 0:
                    MainMenu.Transition.dither -= 0.02
                    pyxel.dither(MainMenu.Transition.dither)
                else:
                    StateMachine.ChangeGameState(GAME_STATE_LIST[1])
                    MainMenu.Transition.transition_active = False

    def MouseDraw():
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 248, 0, 8, 8, 2)
        
    def Canvas():
        pyxel.blt(0, 0, 0, 0, 0, 128, 128)  # Background
        
        pyxel.blt(MainMenu.PyxelCraft_txt[0], MainMenu.PyxelCraft_txt[1], 0, 129, 1, 88, 54, 2) # Text
        
        for key, button in MainMenu.Buttons.items():
            pos_x, pos_y = button['Pos']
            font_u, font_v = button['Font']
            size_w, size_h = button['Size']
            pyxel.blt(pos_x, pos_y, 0, font_u, font_v, size_w, size_h, 2)
        
        for key, panel in MainMenu.Panels.items():
            if key == MainMenu.current_Menu:
                pos_x, pos_y = panel['Pos']
                font_u, font_v = panel['Font']
                size_w, size_h = panel['Size']
                pyxel.blt(pos_x, pos_y, 0, font_u, font_v, size_w, size_h, 2)

            if MainMenu.current_Menu == "Options":
                MusicText = Sound.musics[Sound.currentMusic]
                MusicTextW = len(MusicText) * 4
                pyxel.text(((83 - MusicTextW) // 2) + 24, 98, Sound.musics[Sound.currentMusic], 7)
    
    def ButtonFunc(button):
        if button == "Play":
            MainMenu.Transition.transition_active = True
        elif button == "Load":
            Data.SaveLoad.LoadWorld()
            MainMenu.Transition.transition_active = True
        elif button == "Options":
            MainMenu.current_Menu = 'Options'
        elif button == "Controls":
            MainMenu.current_Menu = 'Controls'
        elif button == "CloseOptions":
            MainMenu.current_Menu = 'Main'
        elif button == "NXMusic":
            if Sound.currentMusic < len(Sound.musics) - 1: Sound.MusicSelection(Sound.currentMusic + 1)
            else: Sound.MusicSelection(0)
        elif button == "PVMusic":
            if Sound.currentMusic > 0: Sound.MusicSelection(Sound.currentMusic - 1)
            else: Sound.MusicSelection(len(Sound.musics) - 1)
    
    def Inputs():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if MainMenu.current_Menu == "Main":
                for key, button in MainMenu.Buttons.items():
                    dx = pyxel.mouse_x - button['Pos'][0]
                    dy = pyxel.mouse_y - button['Pos'][1]
                        
                    if 0 <= dx < button['Size'][0] and 0 <= dy < button['Size'][1]:
                        MainMenu.ButtonFunc(key)
                        
            elif MainMenu.current_Menu == "Options":
                for key, button in MainMenu.Options_Buttons.items():
                    dx = pyxel.mouse_x - button['Pos'][0]
                    dy = pyxel.mouse_y - button['Pos'][1]
                        
                    if 0 <= dx < button['Size'][0] and 0 <= dy < button['Size'][1]:
                        MainMenu.ButtonFunc(key)
            
            elif MainMenu.current_Menu == "Controls":
                for key, button in MainMenu.Controls_Buttons.items():
                    dx = pyxel.mouse_x - button['Pos'][0]
                    dy = pyxel.mouse_y - button['Pos'][1]
                        
                    if 0 <= dx < button['Size'][0] and 0 <= dy < button['Size'][1]:
                        MainMenu.ButtonFunc(key)
    def Update():
        MainMenu.Transition.UpdateIntro()
        MainMenu.Transition.UpdateTransition()
        if not MainMenu.Transition.intro_active and not MainMenu.Transition.transition_active: MainMenu.Inputs()
    
    def Draw():
        MainMenu.Canvas()
        MainMenu.MouseDraw()

class Gameplay:
    class Camera:
        diff = [0, 0]
        speed = 1
        velocities = [1, 2]
        
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
        Horbar_ItemsAmount_pos = [23, 35, 47, 59, 71, 83, 95, 107]
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
            pyxel.rect(Gameplay.UI.Hotbar_Slots_pos[Gameplay.UI.Hotbar_Selected_slot] -1, 114, 12, 12, 10)
            
            for i, slot in enumerate(Gameplay.UI.Hotbar_Slots_pos):
                pyxel.rect(slot, 115, 10, 10, 7)
                pyxel.rect(slot + 1, 116, 8, 8, 13)
                pyxel.text(slot + 2, 110, str(i + 1), 1)
                pyxel.text(slot + 1, 110, str(i + 1), 7)
                
                if Menu.Inventory[i]['Item'] != None:
                    j = next(j for j in Data.item_data['Items'] if j['name'] == Menu.Inventory[i]['Item'])
                    pyxel.blt(Gameplay.UI.Hotbar_Items_pos[i], 116, 1, j['local']['x'], j['local']['y'], 8, 8, 2)
                    if Menu.Inventory[i]['amount'] > 1:
                        pyxel.rect(Gameplay.UI.Horbar_ItemsAmount_pos[i], 122, 4, 5, 7)
                        pyxel.text(Gameplay.UI.Horbar_ItemsAmount_pos[i] + 1, 122, f'{Menu.Inventory[i]['amount']}', 0)
                            
        def Debug():
            pyxel.text(2, SCREEN_SIZE[0] - 25, f'Tick: {Gameplay.tick}', 7)
            
            selectarea_x = (pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8
            selectarea_y = (pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8
            
            pyxel.text(2, 1, f'x:{selectarea_x // 8}\ny:{selectarea_y // 8}', 7)
            
            for i in range(0, Gameplay.Atlas.MaxLayerValue):
                pyxel.text(2, 15 + i * 7, f'{Gameplay.Atlas.World[selectarea_x, selectarea_y, i]['Block']}', 7)
        
        def Update():
            Gameplay.UI.Inputs()
        
        def Draw():
            Gameplay.Camera.UICamera()
            Gameplay.UI.DrawMouse()
            Gameplay.UI.Hotbar()
            if Gameplay.UI.Show_Debug: Gameplay.UI.Debug()

    class Transition:
            transition_active = True
            dither = -1
            
            def UpdateTransition():
                if Gameplay.Transition.transition_active:
                    if Gameplay.Transition.dither < 1:
                        Gameplay.Transition.dither += 0.02
                        pyxel.dither(Gameplay.Transition.dither)
                    else:
                        Gameplay.Transition.transition_active = False
        
    class Optfine:
        def GetGenerationArea():
            start_x = (Gameplay.Camera.diff[0] // BLOCK_SIZE) * BLOCK_SIZE - BLOCK_SIZE
            end_x = (Gameplay.Camera.diff[0] // BLOCK_SIZE + SCREEN_SIZE[0] // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE * 4
            start_y = (Gameplay.Camera.diff[1] // BLOCK_SIZE) * BLOCK_SIZE - BLOCK_SIZE
            end_y = (Gameplay.Camera.diff[1] // BLOCK_SIZE + SCREEN_SIZE[1] // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE * 4
            return start_x, end_x, start_y, end_y
        
    class Atlas:
        World = {}
        Entities = {}
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
                        for z in range(0, Gameplay.Atlas.MaxLayerValue):
                            if Gameplay.Atlas.World[(x, y, z)]['Block'] == "Tree_block":
                                Gameplay.Atlas.Structures.CreateTree(x, y, z)
            
           def CreateTree(x, y, layer):
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': "Wood_Log_block_Bottom"}
                Gameplay.Atlas.World[(x, y - 8, layer)] = {'Block': "Wood_Log_block_Bottom"}
                Gameplay.Atlas.World[(x, y - 16, layer)] = {'Block': "Wood_Log_block_Top"}
                Gameplay.Atlas.World[(x, y - 16, layer + 1)] = {'Block': "Leaves_block"}
                Gameplay.Atlas.World[(x, y - 24, layer + 1)] = {'Block': "Leaves_block"}
                Gameplay.Atlas.World[(x - 8, y - 16, layer + 1)] = {'Block': "Leaves_block"}
                Gameplay.Atlas.World[(x + 8, y - 16, layer + 1)] = {'Block': "Leaves_block"}

    class Player:
        frame_count = 0
        blint_mouse = False
        
        break_progress = 0
        tick_time = None
        last_target = [None, None]
        hold_break = False
        
        def SelectionArea():
            mouse_x = (pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8
            mouse_y = (pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8
            
            Gameplay.Player.frame_count += 1
            if Gameplay.Player.frame_count >= 15:
                Gameplay.Player.frame_count = 0
                Gameplay.Player.blint_mouse = not Gameplay.Player.blint_mouse
            
            if Gameplay.Player.blint_mouse: pyxel.blt(mouse_x, mouse_y, 1, 104, 56, 8, 8, 2)
            else:                           pyxel.blt(mouse_x, mouse_y, 1, 104, 64, 8, 8, 2)

            if   16 > Gameplay.Player.break_progress >  0: pyxel.blt(mouse_x, mouse_y, 1, 120, 56, 8, 8, 2)
            elif 32 > Gameplay.Player.break_progress > 16: pyxel.blt(mouse_x, mouse_y, 1, 120, 64, 8, 8, 2)
            elif 48 > Gameplay.Player.break_progress > 32: pyxel.blt(mouse_x, mouse_y, 1, 120, 72, 8, 8, 2)
            elif 64 > Gameplay.Player.break_progress > 48: pyxel.blt(mouse_x, mouse_y, 1, 120, 80, 8, 8, 2)
        
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
                        block = next(block for block in Data.item_data['Items'] if block['name'] == Gameplay.Atlas.World[(target_x, target_y, layer)]['Block'])
                        Menu.AddItem(block['drop'], 1, None)
                        Gameplay.Atlas.World[(target_x, target_y, layer)] = {'Block': 'Air'}
                        if block['placeSpecial'] == True: Gameplay.Special.Break(block['name'], target_x, target_y, layer)
                        Gameplay.Player.break_progress = 0
                        Gameplay.Player.tick_time = None
                        Gameplay.Player.hold_break = True
                        return
                    else:
                        Gameplay.Player.break_progress += 1
                        return
        
        def PlaceBlock():
            target_x = (pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8
            target_y = (pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8
            layer = 0
            selected_block = Menu.Inventory[Gameplay.UI.Hotbar_Selected_slot]['Item']
            block = next((block for block in Data.item_data['Items'] if block['name'] == selected_block), None)
            
            if selected_block == None or block['type'] != "Block":
                return
            
            while layer < Gameplay.Atlas.MaxLayerValue:
                if (target_x, target_y, layer) not in Gameplay.Atlas.World or Gameplay.Atlas.World[(target_x, target_y, layer)]['Block'] == 'Air':
                    if block['placeSpecial'] == True:
                        Gameplay.Special.Place(selected_block, target_x, target_y, layer)
                    else:
                        Gameplay.Atlas.World[(target_x, target_y, layer)] = {'Block': selected_block}
                        Menu.RemoveItem(Gameplay.UI.Hotbar_Selected_slot, 1)
                    return
                else:
                    layer += 1
        
        def AccessMenu():
            target_x = (pyxel.mouse_x + Gameplay.Camera.diff[0]) // 8 * 8
            target_y = (pyxel.mouse_y + Gameplay.Camera.diff[1]) // 8 * 8
            layer = 0
            selected_block = Menu.Inventory[Gameplay.UI.Hotbar_Selected_slot]['Item']
            #block = next((block for block in Data.item_data['Items'] if block['name'] == selected_block), None)
            
            if selected_block != None:
                return

            while layer < Gameplay.Atlas.MaxLayerValue:
                if Gameplay.Atlas.World[(target_x, target_y, layer)]['Block'] == 'Workbench_block':
                    Menu.Actual_Menu = "Workbench"
                    StateMachine.ChangeGameState("Menu")
                    return
                elif Gameplay.Atlas.World[(target_x, target_y, layer)]['Block'] == 'Chest_block':
                    Menu.inChest.actual_inventory = Gameplay.Atlas.Entities[(target_x, target_y, layer)]['Inventory']
                    Menu.inChest.actual_chest = [target_x, target_y, layer]
                    Menu.Actual_Menu = "Chest"
                    StateMachine.ChangeGameState("Menu")
                    return
                elif Gameplay.Atlas.World[(target_x, target_y, layer)]['Block'] == 'Furnace_block':
                    Menu.inFurnace.actual_inventory = Gameplay.Atlas.Entities[(target_x, target_y, layer)]['Inventory']
                    Menu.inFurnace.progress = Gameplay.Atlas.Entities[(target_x, target_y, layer)]['Progress']
                    Menu.inFurnace.inProgress = Gameplay.Atlas.Entities[(target_x, target_y, layer)]['inProgress']
                    Menu.inFurnace.consumed_fuel = Gameplay.Atlas.Entities[(target_x, target_y, layer)]['consumed_fuel']
                    Menu.inFurnace.actual_furnace = [target_x, target_y, layer]
                    Menu.Actual_Menu = "Furnace"
                    StateMachine.ChangeGameState("Menu")
                    return
                else:
                    layer += 1
            
            
        def Inputs():
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not Gameplay.Player.hold_break: Gameplay.Player.BreakBLock() 
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT): Gameplay.Player.break_progress = 0; Gameplay.Player.hold_break = False
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                Gameplay.Player.AccessMenu()
                Gameplay.Player.PlaceBlock()
            
            if pyxel.btnp(pyxel.KEY_E): StateMachine.ChangeGameState('Menu')
        
        def Update():
            Gameplay.Player.Inputs()

    class Special:
        def Place(block, x, y, layer):
            if block == 'Bed':
                if Gameplay.Atlas.World[(x, y - BLOCK_SIZE, layer)]['Block'] == "Air":
                    Gameplay.Atlas.World[(x, y, layer)] = {'Block': "Bed_block_Bottom"}
                    Gameplay.Atlas.World[(x, y - BLOCK_SIZE, layer)] = {'Block': "Bed_block_Top"}
                else: return
                    
            elif block == 'Chest_block':
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': "Chest_block"}
                Gameplay.Atlas.Entities[(x, y, layer)] = {'Inventory': copy.deepcopy(Menu.chest_inventory)}
                
            elif block == 'Furnace_block':
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': "Furnace_block"}
                Gameplay.Atlas.Entities[(x, y, layer)] = {'Inventory': copy.deepcopy(Menu.furnace_inventory),
                                                          'Progress': 0,
                                                          'inProgress': False,
                                                          'consumed_fuel': 0}
            
            Menu.RemoveItem(Gameplay.UI.Hotbar_Selected_slot, 1)
        
        def Break(block, x, y, layer):
            if block == 'Bed_block_Bottom':
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': 'Air'}
                Gameplay.Atlas.World[(x, y - BLOCK_SIZE, layer)] = {'Block': 'Air'}
            elif block == 'Bed_block_Top':
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': 'Air'}
                Gameplay.Atlas.World[(x, y + BLOCK_SIZE, layer)] = {'Block': 'Air'}     
              
            elif block == "Chest_block":
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': "Air"}
                Gameplay.Atlas.Entities[(x, y, layer)] = {'Inventory': None}
                del Gameplay.Atlas.Entities[(x, y, layer)]
                
            elif block == "Furnace_block":
                Gameplay.Atlas.World[(x, y, layer)] = {'Block': "Air"}
                Gameplay.Atlas.Entities[(x, y, layer)] = {'Inventory': None}
                del Gameplay.Atlas.Entities[(x, y, layer)]
    
    tick = 0
    frame_count = 0
    
    def TickUpdate():
        Gameplay.frame_count += 1
        
        if Gameplay.frame_count >= TPS:
            Gameplay.tick += 1
            Gameplay.frame_count = 0
    
    def Debug():
        if pyxel.btnp(pyxel.KEY_EQUALS) and Gameplay.Atlas.LayerVisibility < Gameplay.Atlas.MaxLayerValue:
            Gameplay.Atlas.LayerVisibility += 1
        
        if pyxel.btnp(pyxel.KEY_MINUS) and Gameplay.Atlas.LayerVisibility > 0:
            Gameplay.Atlas.LayerVisibility -= 1
    
    def Update():
        Gameplay.TickUpdate()
        Gameplay.Camera.CamController()
        Gameplay.Atlas.GenerateWorldLayers()
        Gameplay.Atlas.Structures.GenerateWorldStructure()
        Gameplay.UI.Update()
        Gameplay.Player.Update()
        
        Gameplay.Transition.UpdateTransition()
        Gameplay.Debug()
    
    def Draw():
        Gameplay.Atlas.RendererLayer()
        Gameplay.Player.SelectionArea()
        
        Gameplay.UI.Draw()

class Menu:
    Inventory = {
        0:  {'Pos': [18 , 110], 'Item': None, 'amount': 0},
        1:  {'Pos': [30 , 110], 'Item': None, 'amount': 0},
        2:  {'Pos': [42 , 110], 'Item': None, 'amount': 0},
        3:  {'Pos': [54 , 110], 'Item': None, 'amount': 0},
        4:  {'Pos': [66 , 110], 'Item': None, 'amount': 0},
        5:  {'Pos': [78 , 110], 'Item': None, 'amount': 0},
        6:  {'Pos': [90 , 110], 'Item': None, 'amount': 0},
        7:  {'Pos': [102, 110], 'Item': None, 'amount': 0},
        8:  {'Pos': [18 , 66 ], 'Item': None, 'amount': 0},
        9:  {'Pos': [30 , 66 ], 'Item': None, 'amount': 0},
        10: {'Pos': [42 , 66 ], 'Item': None, 'amount': 0},
        11: {'Pos': [54 , 66 ], 'Item': None, 'amount': 0},
        12: {'Pos': [66 , 66 ], 'Item': None, 'amount': 0},
        13: {'Pos': [78 , 66 ], 'Item': None, 'amount': 0},
        14: {'Pos': [90 , 66 ], 'Item': None, 'amount': 0},
        15: {'Pos': [102, 66 ], 'Item': None, 'amount': 0},
        16: {'Pos': [18 , 78 ], 'Item': None, 'amount': 0},
        17: {'Pos': [30 , 78 ], 'Item': None, 'amount': 0},
        18: {'Pos': [42 , 78 ], 'Item': None, 'amount': 0},
        19: {'Pos': [54 , 78 ], 'Item': None, 'amount': 0},
        20: {'Pos': [66 , 78 ], 'Item': None, 'amount': 0},
        21: {'Pos': [78 , 78 ], 'Item': None, 'amount': 0},
        22: {'Pos': [90 , 78 ], 'Item': None, 'amount': 0},
        23: {'Pos': [102, 78 ], 'Item': None, 'amount': 0},
        24: {'Pos': [18 , 90 ], 'Item': None, 'amount': 0},
        25: {'Pos': [30 , 90 ], 'Item': None, 'amount': 0},
        26: {'Pos': [42 , 90 ], 'Item': None, 'amount': 0},
        27: {'Pos': [54 , 90 ], 'Item': None, 'amount': 0},
        28: {'Pos': [66 , 90 ], 'Item': None, 'amount': 0},
        29: {'Pos': [78 , 90 ], 'Item': None, 'amount': 0},
        30: {'Pos': [90 , 90 ], 'Item': None, 'amount': 0},
        31: {'Pos': [102, 90 ], 'Item': None, 'amount': 0}
    }
    
    chest_inventory = {
        0: {'Pos': [18, 18], 'Item': None, 'amount': 0},
        1: {'Pos': [30, 18], 'Item': None, 'amount': 0},
        2: {'Pos': [42, 18], 'Item': None, 'amount': 0},
        3: {'Pos': [54, 18], 'Item': None, 'amount': 0},
        4: {'Pos': [66, 18], 'Item': None, 'amount': 0},
        5: {'Pos': [78, 18], 'Item': None, 'amount': 0},
        6: {'Pos': [90, 18], 'Item': None, 'amount': 0},
        7: {'Pos': [102, 18], 'Item': None, 'amount': 0},
        8: {'Pos': [18, 30], 'Item': None, 'amount': 0},
        9: {'Pos': [30, 30], 'Item': None, 'amount': 0},
        10: {'Pos': [42, 30], 'Item': None, 'amount': 0},
        11: {'Pos': [54, 30], 'Item': None, 'amount': 0},
        12: {'Pos': [66, 30], 'Item': None, 'amount': 0},
        13: {'Pos': [78, 30], 'Item': None, 'amount': 0},
        14: {'Pos': [90, 30], 'Item': None, 'amount': 0},
        15: {'Pos': [102, 30], 'Item': None, 'amount': 0},
        16: {'Pos': [18, 42], 'Item': None, 'amount': 0},
        17: {'Pos': [30, 42], 'Item': None, 'amount': 0},
        18: {'Pos': [42, 42], 'Item': None, 'amount': 0},
        19: {'Pos': [54, 42], 'Item': None, 'amount': 0},
        20: {'Pos': [66, 42], 'Item': None, 'amount': 0},
        21: {'Pos': [78, 42], 'Item': None, 'amount': 0},
        22: {'Pos': [90, 42], 'Item': None, 'amount': 0},
        23: {'Pos': [102, 42], 'Item': None, 'amount': 0}
    }

    furnace_inventory = {
        0: {'Pos': [42, 18], 'Slot': 'Material', 'Item': None, 'amount': 0},
        1: {'Pos': [42, 42], 'Slot': 'Fuel'    , 'Item': None, 'amount': 0},
        2: {'Pos': [90, 30], 'Slot': 'Result'  , 'Item': None, 'amount': 0}
    }
    
    Holding_Item = False
    Holding_item_name = None
    Holding_item_amount = 0
    
    Menus_names = ['Inventory', 'Workbench', 'Chest', 'Furnace']
    Actual_Menu = 'Inventory'
    
    class inInventory:
        grid_pos = {
            (0, 0): {'grid': [0, 0], 'x': 18, 'y': 10},
            (0, 1): {'grid': [0, 1], 'x': 30, 'y': 10},
            (1, 0): {'grid': [1, 0], 'x': 18, 'y': 22},
            (1, 1): {'grid': [1, 1], 'x': 30, 'y': 22},
        }
        
        grid = [
            [None, None],
            [None, None]
        ]
        
        ItemOnCraft = None
        CraftSlot = [30, 46]
        
        def DeleteItem(Amount):
            if Menu.Holding_Item:
                dx = pyxel.mouse_x - 101
                dy = pyxel.mouse_y - 46
                if 0 <= dx < 7 and 0 <= dy < 9:
                    if Amount >= Menu.Holding_item_amount:
                        Menu.Holding_Item = False
                        Menu.Holding_item_name = None
                        Menu.Holding_item_amount = 0
                    else:
                        Menu.Holding_item_amount -= Amount
        
        def Save():
            dx = pyxel.mouse_x - 96
            dy = pyxel.mouse_y - 6
            
            if 0 <= dx < 20 and 0 <= dy < 11:
                Data.SaveLoad.SaveWorld()
        
        def Update():
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                Menu.CraftingFunction.MoveItemToCraft(Menu.inInventory.grid_pos, Menu.inInventory.grid)
                Menu.CraftingFunction.ExecuteCraft(Menu.inInventory.ItemOnCraft, Menu.inInventory.CraftSlot)
                Menu.inInventory.DeleteItem(Menu.Holding_item_amount)
                Menu.inInventory.Save()
        
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                Menu.inInventory.DeleteItem(1)
            
            Menu.inInventory.ItemOnCraft = Menu.CraftingFunction.CheckCrafting(Menu.inInventory.grid)
            
        def Draw():
            for i, x in enumerate(Menu.inInventory.grid):
                for j, y in enumerate(x):
                    if Menu.inInventory.grid[i][j] == None: continue
                    
                    item = next(item for item in Data.item_data['Items'] if item['name'] == Menu.inInventory.grid[i][j])
                    pyxel.blt(Menu.inInventory.grid_pos[(i, j)]['x'], 
                              Menu.inInventory.grid_pos[(i, j)]['y'], 1, item['local']['x'], item['local']['y'], 8, 8, 2)
            
            if Menu.inInventory.ItemOnCraft != None:
                item = next(item for item in Data.item_data['Items'] if item['name'] == Menu.inInventory.ItemOnCraft['item'])
                pyxel.blt(Menu.inInventory.CraftSlot[0], Menu.inInventory.CraftSlot[1], 1, item['local']['x'], item['local']['y'], 8, 8, 2)
                pyxel.rect(Menu.inInventory.CraftSlot[0] + 6, Menu.inInventory.CraftSlot[1] + 4, 5, 7, 7)
                pyxel.text(Menu.inInventory.CraftSlot[0] + 7, Menu.inInventory.CraftSlot[1] + 5, f'{Menu.inInventory.ItemOnCraft['amount']}', 0)
   
    class inWorkbench:
        grid_pos = {
            (0, 0): {'grid': [0, 0], 'x': 30, 'y': 18},
            (0, 1): {'grid': [0, 1], 'x': 42, 'y': 18},
            (0, 2): {'grid': [0, 2], 'x': 54, 'y': 18},
            (1, 0): {'grid': [1, 0], 'x': 30, 'y': 30},
            (1, 1): {'grid': [1, 1], 'x': 42, 'y': 30},
            (1, 2): {'grid': [1, 2], 'x': 54, 'y': 30},
            (2, 0): {'grid': [2, 0], 'x': 30, 'y': 42},
            (2, 1): {'grid': [2, 1], 'x': 42, 'y': 42},
            (2, 2): {'grid': [2, 2], 'x': 54, 'y': 42},
        }
        
        grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        
        ItemOnCraft = None
        CraftSlot = [90, 30]
        
        def Update():
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                Menu.CraftingFunction.MoveItemToCraft(Menu.inWorkbench.grid_pos, Menu.inWorkbench.grid)
                Menu.CraftingFunction.ExecuteCraft(Menu.inWorkbench.ItemOnCraft, Menu.inWorkbench.CraftSlot)
            
            Menu.inWorkbench.ItemOnCraft = Menu.CraftingFunction.CheckCrafting(Menu.inWorkbench.grid)
        
        def Draw():
            for i, x in enumerate(Menu.inWorkbench.grid):
                for j, y in enumerate(x):
                    if Menu.inWorkbench.grid[i][j] == None: continue
                    
                    item = next(item for item in Data.item_data['Items'] if item['name'] == Menu.inWorkbench.grid[i][j])
                    pyxel.blt(Menu.inWorkbench.grid_pos[(i, j)]['x'], 
                              Menu.inWorkbench.grid_pos[(i, j)]['y'], 1, item['local']['x'], item['local']['y'], 8, 8, 2)
            
            if Menu.inWorkbench.ItemOnCraft != None:
                item = next(item for item in Data.item_data['Items'] if item['name'] == Menu.inWorkbench.ItemOnCraft['item'])
                pyxel.blt(Menu.inWorkbench.CraftSlot[0], Menu.inWorkbench.CraftSlot[1], 1, item['local']['x'], item['local']['y'], 8, 8, 2)
                pyxel.rect(Menu.inWorkbench.CraftSlot[0] + 6, Menu.inWorkbench.CraftSlot[1] + 4, 5, 7, 7)
                pyxel.text(Menu.inWorkbench.CraftSlot[0] + 7, Menu.inWorkbench.CraftSlot[1] + 5, f'{Menu.inWorkbench.ItemOnCraft['amount']}', 0)

    class inChest:
        actual_inventory = None
        actual_chest = None
        
        def CloseChest():
            Gameplay.Atlas.Entities[Menu.inChest.actual_chest[0], Menu.inChest.actual_chest[1], Menu.inChest.actual_chest[2]]['Inventory'] = Menu.inChest.actual_inventory
            Menu.inChest.actual_inventory = None
            Menu.inChest.actual_chest = None
        
        def RemoveItemInChest(Key, amount):
            if Menu.inChest.actual_inventory[Key]['amount'] > 0:
                Menu.inChest.actual_inventory[Key]['amount'] -= amount
                if Menu.inChest.actual_inventory[Key]['amount'] <= 0:
                    Menu.inChest.actual_inventory[Key]['Item'] = None
        
        def MoveItemInChest(Amount):
            for key, Item in Menu.inChest.actual_inventory.items():
                    dx = pyxel.mouse_x - Menu.inChest.actual_inventory[key]['Pos'][0]
                    dy = pyxel.mouse_y - Menu.inChest.actual_inventory[key]['Pos'][1]
                    
                    if 0 <= dx < 8 and 0 <= dy < 8:
                        if not Menu.Holding_Item:
                            if Item['Item'] != None:
                                Menu.Holding_item_name = Item['Item']
                                Menu.Holding_item_amount = Item['amount']
                                Menu.Holding_Item = True
                                Menu.inChest.RemoveItemInChest(key, Item['amount'])
                                return
                        else:
                            if Item['Item'] == None:
                                Menu.inChest.actual_inventory[key]["Item"] = Menu.Holding_item_name
                                Menu.inChest.actual_inventory[key]["amount"] = Amount
                                Menu.Holding_item_amount -= Amount
                                if Menu.Holding_item_amount <= 0: Menu.Holding_Item = False; Menu.Holding_item_name = None
                                return
                            elif Item['Item'] == Menu.Holding_item_name:
                                i = next(i for i in Data.item_data['Items'] if i['name'] == Item['Item'])
                                if Item['amount'] + Amount <= i['stack']:
                                    Menu.inChest.actual_inventory[key]["amount"] += Amount
                                    Menu.Holding_item_amount -= Amount
                                    if Menu.Holding_item_amount <= 0: Menu.Holding_Item = False; Menu.Holding_item_name = None
                                    return
                                else:
                                    quant = i['stack'] - Item['amount']
                                    if quant < 0: quant = quant * -1
                                    while quant > 0:
                                        Menu.inChest.actual_inventory[key]["amount"] += 1
                                        Menu.Holding_item_amount -= 1
                                        quant -= 1
        
        def Update():
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): Menu.inChest.MoveItemInChest(Menu.Holding_item_amount)
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT): Menu.inChest.MoveItemInChest(1)
        
        def Draw():
            for key, Item in Menu.inChest.actual_inventory.items():
                if Item['Item'] != None:
                    i = next(i for i in Data.item_data['Items'] if i['name'] == Item['Item'])
                    pos = Menu.inChest.actual_inventory[key]['Pos']
                    pyxel.blt(pos[0], pos[1], 1, i['local']['x'], i['local']['y'], 8, 8, 2)
                    if Item['amount'] > 1:
                        pyxel.rect(pos[0] + 6, pos[1] + 4, 5, 7, 7)
                        pyxel.text(pos[0] + 7, pos[1] + 5, f'{Item['amount']}', 0)
           
    class inFurnace:
        actual_inventory = None
        actual_furnace = None
        
        frame_count = 0
        progress = 0
        inProgress = False
        consumed_fuel = 0
        
        def CloseFurnace():
            Gameplay.Atlas.Entities[Menu.inFurnace.actual_furnace[0], Menu.inFurnace.actual_furnace[1], Menu.inFurnace.actual_furnace[2]]['Inventory'] = Menu.inFurnace.actual_inventory
            Gameplay.Atlas.Entities[Menu.inFurnace.actual_furnace[0], Menu.inFurnace.actual_furnace[1], Menu.inFurnace.actual_furnace[2]]['Progress'] = Menu.inFurnace.progress
            Gameplay.Atlas.Entities[Menu.inFurnace.actual_furnace[0], Menu.inFurnace.actual_furnace[1], Menu.inFurnace.actual_furnace[2]]['inProgress'] = Menu.inFurnace.inProgress
            Gameplay.Atlas.Entities[Menu.inFurnace.actual_furnace[0], Menu.inFurnace.actual_furnace[1], Menu.inFurnace.actual_furnace[2]]['consumed_fuel'] = Menu.inFurnace.consumed_fuel
            Menu.inFurnace.actual_inventory = None
            Menu.inFurnace.progress = 0
            Menu.inFurnace.inProgress = False
            Menu.inFurnace.consumed_fuel = 0
            Menu.inFurnace.actual_furnace = None
        
        def RemoveItemInFurnace(Key, amount):
            if Menu.inFurnace.actual_inventory[Key]['amount'] > 0:
                Menu.inFurnace.actual_inventory[Key]['amount'] -= amount
                if Menu.inFurnace.actual_inventory[Key]['amount'] <= 0:
                    Menu.inFurnace.actual_inventory[Key]['Item'] = None
        
        def MoveItemInFurnace(Amount):
            for key, Item in Menu.inFurnace.actual_inventory.items():
                    dx = pyxel.mouse_x - Menu.inFurnace.actual_inventory[key]['Pos'][0]
                    dy = pyxel.mouse_y - Menu.inFurnace.actual_inventory[key]['Pos'][1]
                    
                    if 0 <= dx < 8 and 0 <= dy < 8:
                        if not Menu.Holding_Item:
                            if Item['Item'] != None:
                                Menu.Holding_item_name = Item['Item']
                                Menu.Holding_item_amount = Item['amount']
                                Menu.Holding_Item = True
                                Menu.inFurnace.RemoveItemInFurnace(key, Item['amount'])
                                return
                        else:
                            if Item['Item'] == None:
                                if Menu.inFurnace.actual_inventory[key]["Slot"] == 'Fuel':
                                    i = next(i for i in Data.item_data['Items'] if i['name'] == Menu.Holding_item_name)
                                    if i['fuelValue'] <= 0: return
                                elif Menu.inFurnace.actual_inventory[key]["Slot"] == 'Result': return
                                    
                                Menu.inFurnace.actual_inventory[key]["Item"] = Menu.Holding_item_name
                                Menu.inFurnace.actual_inventory[key]["amount"] = Amount
                                Menu.Holding_item_amount -= Amount
                                if Menu.Holding_item_amount <= 0: Menu.Holding_Item = False; Menu.Holding_item_name = None
                                return
                            elif Item['Item'] == Menu.Holding_item_name:
                                i = next(i for i in Data.item_data['Items'] if i['name'] == Item['Item'])
                                if Item['amount'] + Amount <= i['stack']:
                                    Menu.inFurnace.actual_inventory[key]["amount"] += Amount
                                    Menu.Holding_item_amount -= Amount
                                    if Menu.Holding_item_amount <= 0: Menu.Holding_Item = False; Menu.Holding_item_name = None
                                    return
                                else:
                                    quant = i['stack'] - Item['amount']
                                    if quant < 0: quant = quant * -1
                                    while quant > 0:
                                        Menu.inFurnace.actual_inventory[key]["amount"] += 1
                                        Menu.Holding_item_amount -= 1
                                        quant -= 1
        
        def FurnaceEngine():
            if Menu.inFurnace.inProgress == False:
                if Menu.inFurnace.actual_inventory[0]["Item"] != None and Menu.inFurnace.actual_inventory[1]["Item"] != None:
                    i = next(i for i in Data.item_data['Items'] if i['name'] == Menu.inFurnace.actual_inventory[1]["Item"])
                    Menu.inFurnace.consumed_fuel = i['fuelValue']
                    Menu.inFurnace.RemoveItemInFurnace(1, 1)
                    Menu.inFurnace.inProgress = True
                else:
                    Menu.inFurnace.inProgress = False
                    
        def FurnaceUpdate():
            if Menu.inFurnace.inProgress == True:
                if Menu.inFurnace.consumed_fuel > 0:
                    
                    Menu.inFurnace.frame_count += 1
            
                    if Menu.inFurnace.frame_count >= TPS:
                        Menu.inFurnace.progress += 1
                        Menu.inFurnace.frame_count = 0
                
                    if Menu.inFurnace.progress >= 24:
                        Menu.inFurnace.MeltItem()
                        Menu.inFurnace.progress = 0
                        Menu.inFurnace.consumed_fuel -= 1
                        
                    if Menu.inFurnace.actual_inventory[0]["Item"] == None:
                        Menu.inFurnace.inProgress = False
                        
                else:
                    Menu.inFurnace.inProgress = False
        
        def MeltItem():
            i = next(i for i in Data.smelting_data['recipes'] if i['Item'] == Menu.inFurnace.actual_inventory[0]["Item"])
            j = next(j for j in Data.item_data['Items'] if j['name'] == i["Result"])
            
            if Menu.inFurnace.actual_inventory[2]["Item"] == None:
                Menu.inFurnace.actual_inventory[2]["Item"] = i["Result"]
                Menu.inFurnace.actual_inventory[2]['amount'] = 1
            elif Menu.inFurnace.actual_inventory[2]["Item"] == i["Result"] and Menu.inFurnace.actual_inventory[2]['amount'] < j['stack']:
                Menu.inFurnace.actual_inventory[2]['amount'] += 1
            else:
                return
                
            Menu.inFurnace.RemoveItemInFurnace(0, 1)
                        
        def Update():
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): Menu.inFurnace.MoveItemInFurnace(Menu.Holding_item_amount)
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT): Menu.inFurnace.MoveItemInFurnace(1)
            Menu.inFurnace.FurnaceEngine()
            Menu.inFurnace.FurnaceUpdate()
        
        def Draw():
            pyxel.rect(60, 30, 24, 8, 0)
            pyxel.rect(60, 30, Menu.inFurnace.progress, 8, 8)
            pyxel.blt(60, 30, 2, 188, 158, 24, 8, 2)
            
            for key, Item in Menu.inFurnace.actual_inventory.items():
                if Item['Item'] != None:
                    i = next(i for i in Data.item_data['Items'] if i['name'] == Item['Item'])
                    pos = Menu.inFurnace.actual_inventory[key]['Pos']
                    pyxel.blt(pos[0], pos[1], 1, i['local']['x'], i['local']['y'], 8, 8, 2)
                    if Item['amount'] > 1:
                        pyxel.rect(pos[0] + 6, pos[1] + 4, 5, 7, 7)
                        pyxel.text(pos[0] + 7, pos[1] + 5, f'{Item['amount']}', 0)
                       
    class CraftingFunction:
        def MoveItemToCraft(matriz_pos, matriz):
            for key, slot in matriz_pos.items():
                dx = pyxel.mouse_x - slot['x']
                dy = pyxel.mouse_y - slot['y']
                
                if 0 <= dx < 8 and 0 <= dy < 8:
                    if Menu.Holding_Item:
                        if matriz[slot['grid'][0]][slot['grid'][1]] == None:
                            matriz[slot['grid'][0]][slot['grid'][1]] = Menu.Holding_item_name
                            Menu.Holding_item_amount -= 1
                            if Menu.Holding_item_amount <= 0: Menu.Holding_Item = False; Menu.Holding_item_name = None
                    elif matriz[slot['grid'][0]][slot['grid'][1]] != None:
                        Menu.Holding_item_name = matriz[slot['grid'][0]][slot['grid'][1]]
                        matriz[slot['grid'][0]][slot['grid'][1]] = None
                        Menu.Holding_item_amount = 1
                        Menu.Holding_Item = True
        
        def CheckCrafting(matriz):
            CheckGrid = []
            tempGrid = []
            
            min_pos_x = None; max_pos_x = None; min_pos_y = None; max_pos_y = None
            for i, x in enumerate(matriz):
                for j, y in enumerate(x):
                    if y != None:
                        holdX = i + 1
                        holdY = j + 1
                        if min_pos_x == None: min_pos_x = holdX
                        if min_pos_y == None: min_pos_y = holdY
                        if min_pos_y != None and min_pos_y > holdY: min_pos_y = holdY
                        break
            
            max_pos_x = min_pos_x
            max_pos_y = min_pos_y
            
            for i, x in enumerate(matriz):
                for j, y in enumerate(x):
                    if y != None:
                        holdX = i + 1
                        holdY = j + 1
                        max_pos_x = holdX if holdX > max_pos_x else max_pos_x
                        max_pos_y = holdY if holdY > max_pos_y else max_pos_y
                        
            for x in matriz:
                for y in x:
                    if y != None:
                        tempGrid.append(y)
                else:
                    if tempGrid != []:
                        CheckGrid.append(tempGrid)
                        tempGrid = []
            
            if CheckGrid != []:
                grid_size = [(max_pos_x + min_pos_x - 1)// min_pos_x, (max_pos_y + min_pos_y - 1) // min_pos_y]
            
            for recipe in Data.crafting_data['recipes']:
                if recipe['shaped'] == True:
                    if matriz == recipe['craft']:
                        return recipe['result']
                else:
                    if CheckGrid == recipe['craft'] and grid_size == recipe['size']:
                        return recipe['result']
        
        def ExecuteCraft(itemOnCraft, craftSlot):
            if itemOnCraft != None:
                dx = pyxel.mouse_x - craftSlot[0]
                dy = pyxel.mouse_y - craftSlot[1]
                if 0 <= dx < 8 and 0 <= dy < 8:
                    if Menu.Holding_Item == False:
                        Menu.CraftingFunction.CleanGrid()
                        Menu.Holding_item_name = itemOnCraft['item']
                        Menu.Holding_item_amount = itemOnCraft['amount']
                        Menu.Holding_Item = True
                        return
                    else:
                        Menu.CraftingFunction.CleanGrid()
                        Menu.AddItem(itemOnCraft['item'], itemOnCraft['amount'], None)
                        return
        
        def CleanGrid():
            if Menu.Actual_Menu == "Inventory": Menu.inInventory.grid = [[None, None],[None, None]]
            elif Menu.Actual_Menu == "Workbench": Menu.inWorkbench.grid = [[None, None, None],[None, None, None], [None, None, None]]
            #elif Menu.Actual_Menu == "Chest": 
            #elif Menu.Actual_Menu == "Furnace": 
    
    def AddItem(Item, amount, KEY):
        i = next(i for i in Data.item_data['Items'] if i['name'] == Item)
        if KEY == None:
            for key, slot in Menu.Inventory.items():
                if slot['Item'] == None or (slot['Item'] == Item and slot['amount'] < i['stack']):
                    Menu.Inventory[key]['Item'] = Item
                    Menu.Inventory[key]['amount'] += amount
                    return
        else:
            Menu.Inventory[KEY]['Item'] = Item
            Menu.Inventory[KEY]['amount'] += amount
    
    def RemoveItem(Key, amount):
        if Menu.Inventory[Key]['amount'] > 0:
            Menu.Inventory[Key]['amount'] -= amount
            if Menu.Inventory[Key]['amount'] <= 0:
                Menu.Inventory[Key]['Item'] = None
    
    def MoveItem(Amount):
        for key, Item in Menu.Inventory.items():
                dx = pyxel.mouse_x - Menu.Inventory[key]['Pos'][0]
                dy = pyxel.mouse_y - Menu.Inventory[key]['Pos'][1]
                
                if 0 <= dx < 8 and 0 <= dy < 8:
                    if not Menu.Holding_Item:
                        if Item['Item'] != None:
                            Menu.Holding_item_name = Item['Item']
                            Menu.Holding_item_amount = Item['amount']
                            Menu.Holding_Item = True
                            Menu.RemoveItem(key, Item['amount'])
                            return
                    else:
                        if Item['Item'] == None:
                                Menu.Inventory[key]["Item"] = Menu.Holding_item_name
                                Menu.Inventory[key]["amount"] = Amount
                                Menu.Holding_item_amount -= Amount
                                if Menu.Holding_item_amount <= 0: Menu.Holding_Item = False; Menu.Holding_item_name = None
                                return
                        elif Item['Item'] == Menu.Holding_item_name:
                            i = next(i for i in Data.item_data['Items'] if i['name'] == Item['Item'])
                            if Item['amount'] + Amount <= i['stack']:
                                Menu.Inventory[key]["amount"] += Amount
                                Menu.Holding_item_amount -= Amount
                                if Menu.Holding_item_amount <= 0: Menu.Holding_Item = False; Menu.Holding_item_name = None
                                return
                            else:
                                quant = i['stack'] - Item['amount']
                                if quant < 0: quant = quant * -1
                                while quant > 0:
                                    Menu.Inventory[key]["amount"] += 1
                                    Menu.Holding_item_amount -= 1
                                    quant -= 1
    
    def DrawItemsOnInventory():
        for key, Item in Menu.Inventory.items():
            if Item['Item'] != None:
                i = next(i for i in Data.item_data['Items'] if i['name'] == Item['Item'])
                pos = Menu.Inventory[key]['Pos']
                pyxel.blt(pos[0], pos[1], 1, i['local']['x'], i['local']['y'], 8, 8, 2)
                if Item['amount'] > 1:
                    pyxel.rect(pos[0] + 6, pos[1] + 4, 5, 7, 7)
                    pyxel.text(pos[0] + 7, pos[1] + 5, f'{Item['amount']}', 0)
                
    def DrawItemOnMouse():
        i = next(i for i in Data.item_data['Items'] if i['name'] == Menu.Holding_item_name)
        pos = [pyxel.mouse_x + 4, pyxel.mouse_y + 8]
        pyxel.blt(pos[0], pos[1], 1, i['local']['x'], i['local']['y'], 8, 8, 2)
        pyxel.rect(pos[0] + 6, pos[1] + 4, 5, 7, 7)
        pyxel.text(pos[0] + 7, pos[1] + 5, f'{Menu.Holding_item_amount}', 0)
    
    def DrawMenu():
        if Menu.Actual_Menu == "Inventory"  : pyxel.blt(0, 0, 2, 0  , 0  , 128, 128, 2); Menu.inInventory.Draw()
        elif Menu.Actual_Menu == "Workbench": pyxel.blt(0, 0, 2, 128, 0  , 128, 128, 2); Menu.inWorkbench.Draw()
        elif Menu.Actual_Menu == "Chest"    : pyxel.blt(0, 0, 2, 0  , 128, 128, 128, 2); Menu.inChest.Draw()
        elif Menu.Actual_Menu == "Furnace"  : pyxel.blt(0, 0, 2, 128, 128, 128, 128, 2); Menu.inFurnace.Draw()
    
    def Inputs():
        if pyxel.btnp(pyxel.KEY_E):   
            if Menu.Actual_Menu == 'Chest': Menu.inChest.CloseChest()
            if Menu.Actual_Menu == 'Furnace': Menu.inFurnace.CloseFurnace()
            StateMachine.ChangeGameState('Gameplay')
            Menu.Actual_Menu = "Inventory"
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            Menu.MoveItem(Menu.Holding_item_amount)
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            Menu.MoveItem(1)
    
    def Update():
        Menu.Inputs()
        if Menu.Actual_Menu == "Inventory": Menu.inInventory.Update()
        elif Menu.Actual_Menu == "Workbench": Menu.inWorkbench.Update()
        elif Menu.Actual_Menu == "Chest": Menu.inChest.Update()
        elif Menu.Actual_Menu == "Furnace": Menu.inFurnace.Update()
    
    def Draw():
        Gameplay.Atlas.RendererLayer()
        Gameplay.Camera.UICamera()
        
        Menu.DrawMenu() # Draw Actual Menu
        Menu.DrawItemsOnInventory()
        if Menu.Holding_Item: Menu.DrawItemOnMouse()
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, 248, 0, 8, 8, 2) # Draw Mouse
        
        pyxel.camera(Gameplay.Camera.diff[0], Gameplay.Camera.diff[1])

class Sound:
    musics = ['No Music', 'Sweden', 'Wet Hands', 'Subwoofer', 'Mice on Venus']
    currentMusic = 1
    
    def BackgroundMusics():
        sweden_nt0='rrrrE0RRF#0RRG0RRB0RRA0RRG0RRD0RRRRE0RRF#0RRG0RRB0RRA0RRG0RRD0RRRRE0RRF#0RRG0RRB0RRA0RRG0RRD0RRRRE0RRF#0B2G0RRB0D2E2A0RRG0F#2A2D0RRRRE0D3F#0A2G0RRB0D2E2A0RRG0A2F#2D0RRRRE0RRF#0B2G0RRB0D2E2A0RRG0F#2C#3D0RRRRE0RRF#0B2G0RRB0D2E2A0RRG0F#2A2D0RRRRE0RRF#0B2G0RRB0D2E2A0RRG0F#2A2D0RRRRE0RRF#0B2G0RRB0D2E2A0RRG0F#2A2D0RRRRB0RRRRB2A2E0RRE2D2A0RRRRD1E2G0RRRRB0RRRRB0RRRRB2A2E0RRE2D2A0RRD3D2E2D1R'
        sweden_nt1='rrrrE1RRRRRA1RRRRRF#1RRRRRA1RRRRE1RRRRRA1RRRRRF#1RRRRRA1RRRRE1RRRRRA1RRRRRF#1RRRRRA1RRRRE1RRA2RA1RRRRRF#1RRRRRA1RRRRE1RB2RA1RRRRRF#1RRRRRA1RRRRE1RRA2RA1RRRF#3E3F#1RRRD3RA1RRRRE1RRA2RA1RRRRRF#1RRRRRA1RRRRE1RRA2RA1RRRRRF#1RRRRRA1RRRRE1RRA2RA1RRRRRF#1RRF#3RRA1RRRRB1RRRRRRE1RRRRE1RRRRRRD1RRRRB1RRRRB1RRRRRRE1RRRE3E1RRRF#3RG1R'
        sweden_nt2='rrrrG1RRRRRD2RRRRRRRRRRRC#2RRRRG1RRRRRD2RRRRRA1RRRRRC#2RRRRG1RRRRRD2RRRRRA1RRRRRC#2RRRRG1RRRRD2RRRRRA1RRRRRC#2RRRRG1RRRD2RRRRRA1RRRRRC#2RRRRG1RRRRD2RRRRRA1RRRRRC#2RRRRG1RRRRD2RRRRRA1RRRRRC#2RRRRG1RRRRD2RRRRRA1RRRRRC#2RRRRG1RRRRD2RRRRRA1RRRRRC#2RRRRD2RRRRRRG#1RRRRA1RRRRRRG1RRRRD2RRRRD2RRRRRRG#1RRRRA1RRRRRB1R'
        sweden_nt3='rrrrRRRRRRRRRRRRRRRRRRRRRRRB1RRRRRF#2RRRRRC#2RRRRRE2RRRRB1RRRRRF#2RRRRRC#2RRRRRE2RRRRB1RRRRF#2RRRRRC#2RRRRRE2RRRRB1RRRF#2RRRRRC#2RRRRRE2RRRRB1RRRRF#2RRRRRC#2RRRRRE2RRRRB1RRRRF#2RRRRRC#2RRRRRE2RRRRB1RRRRF#2RRRRRC#2RRRRRE2RRRRB1RRRRF#2RRRRRC#2RRRRRE1RRRRF#2RRRRRRB1RRRRC#2RRRRRRB1RRRRF#2RRRRF#2RRRRRRB1RRRRC#2RRRRRRR'
        pyxel.sounds[0].set(sweden_nt0, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[1].set(sweden_nt1, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[2].set(sweden_nt2, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[3].set(sweden_nt3, tones='t', volumes='4', effects='n', speed=45)
        pyxel.musics[1].set([0], [1], [2], [3])
        
        wethands_nt0='rrrrA0E1A1B1C#2B1A1E1D1F#1C#2E2C#2A1RA0E1A1B1C#2B1A1E1D1F#1C#2E2C#2A1RG#2E1A1B1C#2B1RE1F#2F#1C#2E2C#2A1RE2F#2G#2E1A1B1RC#3D1RC#2E2A1RC#3E3RB0D1RRF#1RRG0B0D1F#1A1RRB0F#3F#1RF#1RRG0B0D1F#1A1RA2RE1A1B1C#2B1A1E1A0E1A1B1C#2RE1A2C#3RRD1F#1C#3A2RRB0RF#1A1C#2RA1C#3RB0C#3D3A1F#3C#3RB1A1RRG#0B0E1G#1E1B0G#0RE0G#0B0E1G#1E1A0G0B0D1F#1A1F#1D1B0A0D#1E1A1C#2B1A1E1RE0G#0B0E1G#1E0G#0B0E1G#1R'
        wethands_nt1='rrrrRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA2RRRRRRRRRRRRRRA1RRF#1RRRRRRG3RRF#3A1RD1B0RRRRRRG3RRRA1RD1B0RRRRRRRA0RRRRRRRRRRRRRRRRRB0RRRRE2F#2RD1RRRRRRG0RRRRRRRRRRE0RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'
        wethands_nt2='rrrrRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRA1RRRRRRRRRRRRRRB2RRF#2RRRRRRG0RRF#1D3RA2B2RRRRRRG0RRRD3RA2B2RRRRRRRE2RRRRRRRRRRRRRRRRRD2RRRRE3F#3RD2RRRRRRD3RRRRRRRRRRB1RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'
        pyxel.sounds[4].set(wethands_nt0, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[5].set(wethands_nt1, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[6].set(wethands_nt2, tones='t', volumes='4', effects='n', speed=45)
        pyxel.musics[2].set([4], [5], [6])
        
        subwoofer_nt0='rrrrC2RRRG2RRRC2RRRG2RRRC2RRRG2RRRC2RRRG2RRRC1RC2RC1RC2RC1RC2RC1RC2RC1RC2RC1RC2RC1RC2RC1RC2RC1C3B1E3G1D3B1B2C1RB1G2G1RB1RA0E3C2E3A1G3C2E3A0RC2E3A1G3C2E3A0RC2RA1RC2RF0E3A1C3F1A2A1RG0G2B1E3G1D3B1F2F0E3A1C3F1A2A1RG0RB1D3G1B2RC1RC2RC1RC2RC1B1RC1RB1RC1RC2RC1RC2RC1B1RC1RB1RE1'
        subwoofer_nt1='rrrrRRE2RRRE2RRRE2RRRE2RRRE2RRRE2RRRE2RRRE2RC2RE2RG2RE2RC2RE2RG2RE2RC2RE2RG2RE2RC2RE2RG2RE2RC2RE2RRRE2RC2RE2RRRE2RA1RE2RRRE2RA1RE2RRRE2RA1RE2RRRE2RF1RC2RRRC2RG1RD2RRRD2RF1RC2RRRC2RG1RD2RRRRRRB2RG2RB2RRE2RG2RE2RRRB2RG2RB2RRE2RG2RE2RR'
        subwoofer_nt2='rrrrRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RRRB2RB2RD3RRRRRC3RRRRRRRB2RD3RRRRRRRD3RRRRRRRD3RRRB2RF3RRRRRC3RB2RRRRRE2RF3RRRRRA3RG3RE3RRRRRRG3RE3RG3RRB2RE3RB2RRRG3RE3RG3RRB2RE3RB2RR'
        pyxel.sounds[7].set(subwoofer_nt0, tones='t', volumes='4', effects=('n'), speed=45)
        pyxel.sounds[8].set(subwoofer_nt1, tones='t', volumes='4', effects=('n'), speed=45)
        pyxel.sounds[9].set(subwoofer_nt2, tones='t', volumes='4', effects=('n'), speed=45)
        pyxel.musics[3].set([7], [8], [9])
        
    def MusicSelection(music):
        pyxel.stop()
        pyxel.playm(music, loop=True)
        Sound.currentMusic = music
        
class StateMachine:
    def ChangeGameState(newState):
        global GAME_STATE
        GAME_STATE = newState

class Data:
    def Images():
        pyxel.images[0].load(0, 0, 'assets/sprites/Background_MainMenu.png')       # main menu bg
        pyxel.images[1].load(0, 0, 'assets/sprites/Sprite_sheet_0.png')            # blocks, items, and player
        pyxel.images[2].load(0, 0, 'assets/sprites/Background_Menus_ingame.png')   # menus in game

    with open('assets/data/blocks_id.json') as f: block_data = json.load(f)
    with open('assets/data/Items_id.json') as g: item_data = json.load(g)
    with open('assets/data/craftings_recipes.json') as h: crafting_data = json.load(h)
    with open('assets/data/smelting_recipes.json') as i: smelting_data = json.load(i)
       
    def CollorPallets(n):
        if n ==0:
            pyxel.colors[0] = 0x000000
            pyxel.colors[1] = 0x2B335F
            pyxel.colors[2] = 0x7E2072
            pyxel.colors[3] = 0x19959C
            pyxel.colors[4] = 0x8B4852
            pyxel.colors[5] = 0x395C98
            pyxel.colors[6] = 0xA9C1FF
            pyxel.colors[7] = 0xEEEEEE
            pyxel.colors[8] = 0xD4186C
            pyxel.colors[9] = 0xD38441
            pyxel.colors[10] = 0xE9C35B
            pyxel.colors[11] = 0x70C6A9
            pyxel.colors[12] = 0x7696D3
            pyxel.colors[13] = 0xA3A3A3
            pyxel.colors[14] = 0xFF9798
            pyxel.colors[15] = 0xEDC7B0
            
        elif n == 1:
            pyxel.colors[0] = 0x000000
            pyxel.colors[1] = 0x27275f
            pyxel.colors[2] = 0x511d72
            pyxel.colors[3] = 0x19588b
            pyxel.colors[4] = 0x573152
            pyxel.colors[5] = 0x2e3b89
            pyxel.colors[6] = 0x666ebc
            pyxel.colors[7] = 0x8984b4
            pyxel.colors[8] = 0x7c186c
            pyxel.colors[9] = 0x7b4f41
            pyxel.colors[10] = 0x866f5b
            pyxel.colors[11] = 0x4a7091
            pyxel.colors[12] = 0x4d58ac
            pyxel.colors[13] = 0x635f8e
            pyxel.colors[14] = 0x915989
            pyxel.colors[15] = 0x887195
    
    class SaveLoad:
        def SaveWorld():
            inventory_data = {str(key): value for key, value in Menu.Inventory.items()}
            world_data = {str(key): value for key, value in Gameplay.Atlas.World.items()}
            entities_data = {str(key): value for key, value in Gameplay.Atlas.Entities.items()}  # Incluindo entities
            camera_diff = Gameplay.Camera.diff

            save_data = {
                'inventory': inventory_data,
                'world': world_data,
                'entities': entities_data,
                'camera_diff': camera_diff,
            }

            file_path = 'Save_data.json'

            if file_path: 
                with open(file_path, "w") as file:
                    json.dump(save_data, file)
                print(f"Game saved to {file_path}")

        def LoadWorld():
            try:
                file_path = 'Save_data.json'

                if not file_path:
                    return

                with open(file_path, "r") as file:
                    save_data = json.load(file)

                    inventory_data = save_data.get('inventory', {})
                    Menu.Inventory = {int(key): value for key, value in inventory_data.items()}
                    
                    world_data = save_data.get('world', {})
                    Gameplay.Atlas.World = {eval(key): value for key, value in world_data.items()}

                    entities_data = save_data.get('entities', {})
                    Gameplay.Atlas.Entities = {eval(key): value for key, value in entities_data.items()}

                    camera_diff = save_data.get('camera_diff', [0, 0])
                    Gameplay.Camera.diff = camera_diff

                print("Game loaded from save_data.json")
            except FileNotFoundError:
                print("No saved game file found. Starting with a new game.")
            except json.JSONDecodeError:
                print("Error decoding the saved game file. Starting with a new game.")

class App:
    def __init__(self):
        pyxel.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title=WINDOW_TITLE, fps=FPS, quit_key=None)
        
        Data.Images()
        Sound.BackgroundMusics()
        Sound.MusicSelection(Sound.currentMusic)

        pyxel.run(self.update, self.draw)
        
    def update(self):
        if   GAME_STATE == 'MainMenu': MainMenu.Update()
        elif GAME_STATE == 'Gameplay': Gameplay.Update()
        elif GAME_STATE == 'Menu': Menu.Update()
    
    def draw(self):
        pyxel.cls(0)
        if   GAME_STATE == 'MainMenu': MainMenu.Draw()
        elif GAME_STATE == 'Gameplay': Gameplay.Draw()
        elif GAME_STATE == 'Menu': Menu.Draw()

App()