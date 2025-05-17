import pyxel
import json

import gameFiles.AppManager as AppManager
import gameFiles.GameManager as GameManager
import gameFiles.Data as Data
import gameFiles.GameObjects as GameObjects

class Game:
    Camera = [0, 0]

    World = {}
    Entities = {}
    Inventory = {}

class SaveData:
    SaveFile = None

    def Save():
        with open(SaveData.SaveFile, 'r') as f:
            data = json.load(f)
        
        data['Camera'] = Game.Camera
        data['World'] = {str(k): v for k, v in Game.World.items()}
        data['Entities'] = Game.Entities
        data['Inventory'] = Game.Inventory

        with open(SaveData.SaveFile, 'w') as f:
            json.dump(data, f, indent=4)

class Input:
    def CameraMove():
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            Game.Camera[1] -= AppManager.GameInfo.CameraSpeed
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            Game.Camera[1] += AppManager.GameInfo.CameraSpeed
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            Game.Camera[0] -= AppManager.GameInfo.CameraSpeed
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            Game.Camera[0] += AppManager.GameInfo.CameraSpeed

        pyxel.camera(Game.Camera[0], Game.Camera[1])
    
    def SelectHotbar():
        if pyxel.btnp(pyxel.KEY_1): Player.SelectHotbarSlot = 0
        if pyxel.btnp(pyxel.KEY_2): Player.SelectHotbarSlot = 1
        if pyxel.btnp(pyxel.KEY_3): Player.SelectHotbarSlot = 2
        if pyxel.btnp(pyxel.KEY_4): Player.SelectHotbarSlot = 3
        if pyxel.btnp(pyxel.KEY_5): Player.SelectHotbarSlot = 4
        if pyxel.btnp(pyxel.KEY_6): Player.SelectHotbarSlot = 5
        if pyxel.btnp(pyxel.KEY_7): Player.SelectHotbarSlot = 6
        if pyxel.btnp(pyxel.KEY_8): Player.SelectHotbarSlot = 7
        if pyxel.btnp(pyxel.KEY_9): Player.SelectHotbarSlot = 8

        if pyxel.mouse_wheel < 0:
            Player.SelectHotbarSlot += 1
            if Player.SelectHotbarSlot > 8: Player.SelectHotbarSlot = 0
        elif pyxel.mouse_wheel > 0:
            Player.SelectHotbarSlot -= 1
            if Player.SelectHotbarSlot < 0: Player.SelectHotbarSlot = 8

    def SelectBlock():
        position_x = pyxel.mouse_x + Game.Camera[0]
        position_y = pyxel.mouse_y + Game.Camera[1]

        for layer in range(AppManager.GameInfo.MaxLayer, -1, -1):
            target_x = position_x // AppManager.GameInfo.BlockSize
            target_y = (position_y + ((layer % 2) * AppManager.GameInfo.BlockHeight)) // AppManager.GameInfo.BlockSize
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in Game.World and Game.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                if ((target_x, adj_y, layer + 1) not in Game.World or Game.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air):
                    if not Player.MineModifier:
                        Player.SelectBlock = [target_x, adj_y, layer]
                        break
                    elif (target_x, adj_y - 1, layer + 1) in Game.World and Game.World[(target_x, adj_y - 1, layer + 1)]['Block'] != Data.Blocks.Air:
                        Player.SelectBlock = [target_x, adj_y - 1, layer + 1]
                        break

        else: Player.SelectBlock = None

    def SelectionModifier():
        if pyxel.btnp(pyxel.KEY_SHIFT):
            Player.MineModifier = True
        
        if pyxel.btnr(pyxel.KEY_SHIFT):
            Player.MineModifier = False
        
    def LeftInputAction():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if Player.SelectBlock is None: return
            Player.BreakBlock(Player.SelectBlock[0], Player.SelectBlock[1], Player.SelectBlock[2])

    def RightInputAction():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            Player.UseItem(Player.SelectHotbarSlot)

    def Update():
        Input.CameraMove()
        Input.SelectHotbar()
        Input.SelectBlock()
        Input.SelectionModifier()
        Input.LeftInputAction()
        Input.RightInputAction()

        if pyxel.btnp(pyxel.KEY_KP_0):
            SaveData.Save()
            print("Saved Successfully")

        if pyxel.btnp(pyxel.KEY_KP_1): Player.AddItem(Data.Items.Bed_item, 1)
        if pyxel.btnp(pyxel.KEY_KP_2): Player.AddItem(Data.Items.Apple, 7)
        if pyxel.btnp(pyxel.KEY_KP_4): Player.RemoveItem(0, 1)
        if pyxel.btnp(pyxel.KEY_KP_5): Player.RemoveItem(0, 3)

class Player:
    SelectBlock = None
    MineModifier = False

    SelectHotbarSlot = 0

    def AddItem(item, amount):
        itemData = Data.GameData.item_data[item]

        for i in range(AppManager.GameInfo.InvetorySize):
            if Game.Inventory[i]['Item'] is None:
                Game.Inventory[i]['Item'] = item
                if amount <= itemData["stack"]:
                    Game.Inventory[i]['Amount'] = amount
                    break
                else:
                    Game.Inventory[i]['Amount'] = itemData["stack"]
                    amount -= itemData["stack"]
                    continue
            elif Game.Inventory[i]['Item'] == item:
                if Game.Inventory[i]['Amount'] + amount <= itemData["stack"]:
                    Game.Inventory[i]['Amount'] += amount
                    break
                else:
                    amount -= (itemData["stack"] - Game.Inventory[i]['Amount'])
                    Game.Inventory[i]['Amount'] = itemData["stack"]
                    continue

    def RemoveItem(key, amount):
        if Game.Inventory[key]['Amount'] <= amount:
            Game.Inventory[key]['Item'] = None
            Game.Inventory[key]['Amount'] = 0
        else:
            Game.Inventory[key]['Amount'] -= amount

    def UseItem(key):
        item = Game.Inventory[key]['Item']
        if item is None: return
        itemData = Data.GameData.item_data[item]

        if itemData['action'] == "Place": 
            if Player.SelectBlock is None: return
            Player.PlaceBlock(Player.SelectBlock[0], Player.SelectBlock[1], Player.SelectBlock[2], itemData['block'])
            return
        elif itemData['action'] == "PlaceSpecial":
            if Player.SelectBlock is None: return
            Player.PlaceSpecialBlock(Player.SelectBlock[0], Player.SelectBlock[1], Player.SelectBlock[2], itemData)

    def BreakBlock(x, y, layer):
        block = Game.World[(x, y, layer)]
        blockData = Data.GameData.block_data[block['Block']]
        item = blockData['drop']

        if item == "Special": 
            Player.BreakSpecialBlock(x, y, layer, blockData)
            return
        
        block['Block'] = Data.Blocks.Air
        Player.AddItem(item, 1)

    def BreakSpecialBlock(x, y, layer, blockData):
        if blockData['name'] == "Bed_block_Bottom":
            Game.World[(x, y, layer)]['Block'] = Data.Blocks.Air
            Game.World[(x, y - 1, layer)]['Block'] = Data.Blocks.Air
            Player.AddItem("Bed_item", 1)
            return
        elif blockData['name'] == "Bed_block_Top":
            Game.World[(x, y, layer)]['Block'] = Data.Blocks.Air
            Game.World[(x, y + 1, layer)]['Block'] = Data.Blocks.Air
            Player.AddItem("Bed_item", 1)
            return

    def PlaceBlock(x, y, layer, block):
        if Player.MineModifier:
            x = x
            y = y + 1
            layer = layer - 1

        if layer + 1 < AppManager.GameInfo.MaxLayer:
            Game.World[(x, y, layer + 1)] = {"Block": block, "Solid": True}
            Player.RemoveItem(Player.SelectHotbarSlot, 1)
    
    def PlaceSpecialBlock(x, y, layer, itemData):
        if Player.MineModifier:
            x = x
            y = y + 1
            layer = layer - 1
        
        if itemData['name'] == "Bed_item":
            if layer + 1 < AppManager.GameInfo.MaxLayer:
                if (x, y - 1, layer + 1) not in Game.World or Game.World[(x, y - 1, layer + 1)]['Block'] == Data.Blocks.Air:
                    Game.World[(x, y, layer + 1)] = {"Block": "Bed_block_Bottom", "Solid": True}
                    Game.World[(x, y - 1, layer + 1)] = {"Block": "Bed_block_Top", "Solid": True}
                    Player.RemoveItem(Player.SelectHotbarSlot, 1)

class UI:
    HotbarSlots = []

    def DrawArea():
        if Player.SelectBlock is None: return
        
        target_x = Player.SelectBlock[0]
        adj_y = Player.SelectBlock[1]
        layer = Player.SelectBlock[2]

        target_y = adj_y - (layer // 2)

        draw_x = target_x * AppManager.GameInfo.BlockSize
        draw_y = (target_y * AppManager.GameInfo.BlockSize) - ((layer % 2) * AppManager.GameInfo.BlockHeight)

        area_local_x = 240
        area_local_y = 16

        if Player.MineModifier:
            draw_y += 8
            area_local_y = 28

        pyxel.blt(
            draw_x, 
            draw_y, 
            2, 
            area_local_x, 
            area_local_y, 
            AppManager.GameInfo.BlockSize, 
            AppManager.GameInfo.BlockSize, 
            2)
        
    def DrawHotbar():
        pyxel.camera(0, 0)
        x = (AppManager.Settings.ScreenWidth - 164) / 2
        y = 228

        pyxel.blt(x, y, 2, 0, 160, 164, 20, 2)
    
    def Draw():
        UI.DrawArea()
        UI.DrawHotbar()

        for itemSlot in UI.HotbarSlots:
            itemSlot.draw()

        pyxel.blt(48 - 3 + (Player.SelectHotbarSlot * 18), 227, 2, 176, 0, 22, 22, 2)

    def Update():
        for itemSlot in UI.HotbarSlots:
            itemSlot.update()

class World:
    def Generation():
        start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea(Game.Camera[0], Game.Camera[1])

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                for z in range(0, 9):
                    if (x, y, z) in Game.World: break

                    if z == 0: 
                        Game.World[(x, y, z)] = {"Block": Data.Blocks.Bedrock_block, "Solid": True}
                        continue

                    if 0 < z < 3:
                        modifier = 8
                        noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                        block = Data.Blocks.Stone_block

                        if noise   > 0.90: block = Data.Blocks.Emerald_Ore_block
                        elif noise > 0.75: block = Data.Blocks.Diamond_Ore_block
                        elif noise > 0.65: block = Data.Blocks.Gold_Ore_block
                        elif noise > 0.55: block = Data.Blocks.Iron_Ore_block
                        
                        Game.World[(x, y, z)] = {"Block": block, "Solid": True}
                        continue

                    if 3 <= z < 6:
                        modifier = 5
                        noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                        block = Data.Blocks.Stone_block

                        if noise > 0.70: block = Data.Blocks.Gold_Ore_block
                        elif noise > 0.60: block = Data.Blocks.Coal_Ore_block
                        elif noise > 0.50: block = Data.Blocks.Iron_Ore_block
                        
                        Game.World[(x, y, z)] = {"Block": block, "Solid": True}
                        continue

                    if 6 <= z < 9:
                        modifier = 2
                        noise = GameManager.PerlinNoise.noise((x + modifier * 100) / 2, (y + z * modifier * 10) / 2)
                        block = Data.Blocks.Stone_block

                        if noise > 0.70: block = Data.Blocks.Iron_Ore_block
                        elif noise > 0.50: block = Data.Blocks.Coal_Ore_block
                        
                        Game.World[(x, y, z)] = {"Block": block, "Solid": True}
                        continue
                    
                z = 9
                if (x, y, z) in Game.World: continue
                noise = GameManager.PerlinNoise.noise(x / 16, y / 16)
                slope = 0

                if noise >= 0.35: slope = 2
                elif noise >= -0.35: slope = 1

                for i in range(slope):
                    Game.World[(x, y, z + i)] = {"Block": Data.Blocks.Dirt_block, "Solid": True}
                
                Game.World[(x, y, z + slope)] = {"Block": Data.Blocks.Grass_block, "Solid": True}

                z = z + slope + 1
                noise = GameManager.PerlinNoise.noise(x / 2, y / 2)

                if noise >= 0.8:
                    Game.World[(x, y, z)] = {"Block": Data.Blocks.Wood_Log_block, "Solid": True}
                    Game.World[(x, y, z + 1)] = {"Block": Data.Blocks.Wood_Log_block, "Solid": True}
                    Game.World[(x, y, z + 2)] = {"Block": Data.Blocks.Wood_Log_block, "Solid": True}
                    Game.World[(x, y, z + 3)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}
                    Game.World[(x - 1, y, z + 3)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}
                    Game.World[(x + 1, y, z + 3)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}
                    Game.World[(x, y, z + 4)] = {"Block": Data.Blocks.Leaves_block, "Solid": True}

    def Renderer():
        pyxel.camera(Game.Camera[0], Game.Camera[1])
        start_x, end_x, start_y, end_y = GameManager.ChunkCalc.GetGenerationChunkArea(Game.Camera[0], Game.Camera[1])

        is_air = lambda t: t is None or t['Block'] == Data.Blocks.Air

        for layer in range(AppManager.GameInfo.MaxLayer):
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    pos = (x, y, layer)
                    tile = Game.World.get(pos)
                    if tile is None or tile['Block'] == Data.Blocks.Air:
                        continue

                    above_tile = Game.World.get((x, y, layer + 1))
                    fwrd_tile = Game.World.get((x, y + 1, layer))
                    if above_tile is not None and above_tile['Block'] != Data.Blocks.Air:
                        if fwrd_tile is not None and fwrd_tile['Block'] != Data.Blocks.Air:
                            continue

                    block = Data.GameData.block_data[tile['Block']]
                    block_x = block['local']['x']
                    block_y = block['local']['y']

                    world_x = x * AppManager.GameInfo.BlockSize
                    world_y = (y * AppManager.GameInfo.BlockSize) - (layer * AppManager.GameInfo.BlockHeight)

                    pyxel.blt(
                        world_x,
                        world_y,
                        1,
                        block_x,
                        block_y,
                        AppManager.GameInfo.BlockSize,
                        AppManager.GameInfo.BlockSize + AppManager.GameInfo.BlockHeight,
                        2
                    )

                    solid = tile['Solid']
                    above        = above_tile
                    bellow       = Game.World.get((x, y , layer - 1))
                    top          = Game.World.get((x, y - 1, layer))
                    bottom       = fwrd_tile
                    left         = Game.World.get((x - 1, y, layer))
                    right        = Game.World.get((x + 1, y, layer))
                    bottom_left  = Game.World.get((x - 1, y + 1, layer))
                    bottom_right = Game.World.get((x + 1, y + 1, layer))

                    if solid and is_air(top) and is_air(above):
                        pyxel.rect(world_x, world_y - 1, AppManager.GameInfo.BlockSize, 1, 0)
                    
                    if solid and is_air(bellow) and is_air(bottom):
                        pyxel.rect(world_x, world_y + AppManager.GameInfo.BlockSize + AppManager.GameInfo.BlockHeight, AppManager.GameInfo.BlockSize, 1, 0)

                    if is_air(left):
                        if solid:
                            pyxel.rect(world_x - 1, world_y, 1, AppManager.GameInfo.BlockSize, 0)
                        if is_air(bottom) and is_air(bottom_left):
                            pyxel.rect(world_x - 1, world_y + AppManager.GameInfo.BlockSize, 1, AppManager.GameInfo.BlockHeight, 0)

                    if is_air(right):
                        if solid:
                            pyxel.rect(world_x + AppManager.GameInfo.BlockSize, world_y, 1, AppManager.GameInfo.BlockSize, 0)
                        if is_air(bottom) and is_air(bottom_right):
                            pyxel.rect(world_x + AppManager.GameInfo.BlockSize, world_y + AppManager.GameInfo.BlockSize, 1, AppManager.GameInfo.BlockHeight, 0)

class Status:
    Started = False
    dither = 0

def End():
    Status.Started = False
    UI.HotbarSlots.clear()

def Start():
    if not Status.Started:
        if Status.dither < 1:
            Status.dither += 0.02
            pyxel.dither(Status.dither)
            return

        Game.Camera = GameManager.Load.Camera
        Game.World = GameManager.Load.World
        Game.Entities = GameManager.Load.Entities
        Game.Inventory = GameManager.Load.Inventory

        SaveData.SaveFile = GameManager.Load.SaveFile

        if not Game.Inventory:
            for i in range(AppManager.GameInfo.InvetorySize):
                Game.Inventory[i] = {
                    'Item': None,
                    'Amount': 0
                }

        for i in range(9):
            UI.HotbarSlots.append(GameObjects.ItemSlot(48 + (i * 18), 230, i, Game.Inventory, 5, hotbar=True))

        Status.Started = True

def Update():
    Start()
    if not Status.Started: return
    World.Generation()
    UI.Update()
    Input.Update()

def Draw():
    if not Status.Started: return
    World.Renderer()
    UI.Draw()