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
    InventoryCraft = {}
    MouseItem = None

class SaveData:
    SaveFile = None

    def Save():
        with open(SaveData.SaveFile, 'r') as f:
            data = json.load(f)
        
        data['Camera'] = Game.Camera
        data['World'] = {str(k): v for k, v in Game.World.items()}
        data['Entities'] = Game.Entities
        data['Inventory'] = Game.Inventory
        data['InventoryCraft'] = Game.InventoryCraft
        data['MouseItem'] = Game.MouseItem

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

    def MenuState():
        if pyxel.btnp(pyxel.KEY_E):
            Status.InMenu = not Status.InMenu
        
    def LeftInputAction():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if not Status.InMenu:
                if Player.SelectBlock is not None: Player.BreakBlock(Player.SelectBlock[0], Player.SelectBlock[1], Player.SelectBlock[2])
            else:
                Player.MoveItem("left")

    def RightInputAction():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            if not Status.InMenu:
                Player.UseItem(Player.SelectHotbarSlot)
            else:
                Player.MoveItem("right")


    def Update():
        if not Status.InMenu:
            Input.CameraMove()
            Input.SelectHotbar()
            Input.SelectBlock()
            Input.SelectionModifier()
        
        Input.LeftInputAction()
        Input.RightInputAction()
        
        Input.MenuState()

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

    def MoveItem(input):
        for itemSlot in UI.InventorySlots + UI.InventoryCraftSlots:
            if itemSlot.clicked() is not None: 
                if input == "left":
                    if Game.MouseItem["Item"] is None:
                        Game.MouseItem = {"Item": itemSlot.Item, "Amount": itemSlot.Amount}
                        itemSlot.Storage[itemSlot.i] = {"Item": None, "Amount": 0}
                    else:
                        if itemSlot.result: return
                        if itemSlot.Item is None:
                            itemSlot.Storage[itemSlot.i] = Game.MouseItem
                            Game.MouseItem = {"Item": None, "Amount": 0}
                        else:
                            if itemSlot.Item == Game.MouseItem["Item"]:
                                total = itemSlot.Storage[itemSlot.i]["Amount"] + Game.MouseItem["Amount"]
                                if total > Data.GameData.item_data[itemSlot.Item]["stack"]:
                                    itemSlot.Storage[itemSlot.i]["Amount"] = Data.GameData.item_data[itemSlot.Item]["stack"]
                                    Game.MouseItem["Amount"] = total - Data.GameData.item_data[itemSlot.Item]["stack"]
                                else:
                                    itemSlot.Storage[itemSlot.i]["Amount"] += Game.MouseItem["Amount"]
                                    Game.MouseItem = {"Item": None, "Amount": 0}
                            else:
                                mouseitem = Game.MouseItem
                                Game.MouseItem = {"Item": itemSlot.Item, "Amount": itemSlot.Amount}
                                itemSlot.Storage[itemSlot.i] = mouseitem
        
                if input == "right":
                    if Game.MouseItem["Item"] is None:
                        getAmout = itemSlot.Amount // 2
                        if getAmout < 1: getAmout = 1
                        Game.MouseItem = {"Item": itemSlot.Item, "Amount": getAmout}
                        itemSlot.Storage[itemSlot.i]["Amount"] -= getAmout
                    else:
                        if itemSlot.Item is None:
                            itemSlot.Storage[itemSlot.i] = {"Item": Game.MouseItem["Item"], "Amount": 1}
                            Game.MouseItem["Amount"] -= 1
                            if Game.MouseItem["Amount"] < 1: Game.MouseItem = {"Item": None, "Amount": 0}
                        else:
                            if itemSlot.Item != Game.MouseItem["Item"] or itemSlot.Storage[itemSlot.i]["Amount"] + 1 > Data.GameData.item_data[itemSlot.Item]["stack"]: return
                            itemSlot.Storage[itemSlot.i]["Amount"] += 1
                            Game.MouseItem["Amount"] -= 1
                            if Game.MouseItem["Amount"] < 1: Game.MouseItem = {"Item": None, "Amount": 0}

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
    InventorySlots = []
    InventoryCraftSlots = []
    InventoryButtons = []

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

        pyxel.blt(draw_x, draw_y, 2, area_local_x, area_local_y, AppManager.GameInfo.BlockSize, AppManager.GameInfo.BlockSize, 2)
        
    def DrawHotbar():
        pyxel.camera(0, 0)
        x = (AppManager.Settings.ScreenWidth - 164) / 2
        y = 228

        pyxel.blt(x, y, 2, 0, 160, 164, 20, 2)

        for itemSlot in UI.HotbarSlots:
            itemSlot.draw()

        pyxel.blt(48 - 3 + (Player.SelectHotbarSlot * 18), 227, 2, 176, 0, 22, 22, 2)

    def DrawMenu():
        pyxel.camera(0, 0)
        x = 43
        y = 48

        pyxel.blt(x, y, 2, 0, 0, 172, 158, 2)
        pyxel.blt(165, 80, 2, 64, 224, 16, 16, 2)
        pyxel.text(48, 118, "Inventory", 5, Data.GameData.spleen5_font)
        pyxel.text(126, 58, "Crafting", 5, Data.GameData.spleen5_font)

        for itemSlot in UI.InventorySlots + UI.InventoryCraftSlots + UI.InventoryButtons:
            itemSlot.draw()

    def DrawMouseItem():
        pyxel.camera(0, 0)
        if Game.MouseItem["Item"] is None: return
        x = pyxel.mouse_x
        y = pyxel.mouse_y

        itemData = Data.GameData.item_data[Game.MouseItem["Item"]]
        amount = Game.MouseItem["Amount"]

        item_x = itemData['local']['x']
        item_y = itemData['local']['y']

        pyxel.blt(x+2, y+2, 1, item_x, item_y, 16, 16, 2)
        if amount <= 1: return
        pyxel.text(x + 12, y + 13, str(amount) if amount >= 10 else " " + str(amount), 0)
        pyxel.text(x + 12, y + 14, str(amount) if amount >= 10 else " " + str(amount), 0)
        pyxel.text(x + 11, y + 14, str(amount) if amount >= 10 else " " + str(amount), 0)
        pyxel.text(x + 11, y + 13, str(amount) if amount >= 10 else " " + str(amount), 7)

    def DeleteMouseItem():
        Game.MouseItem = {
                'Item': None,
                'Amount': 0
            }
    
    def Draw():
        if not Status.InMenu:
            UI.DrawArea()
            UI.DrawHotbar()
        else:
            UI.DrawMenu()
            UI.DrawMouseItem()

    def Update():
        if not Status.InMenu:
            for itemSlot in UI.HotbarSlots: 
                itemSlot.update()
        else:
            for itemSlot in UI.InventorySlots + UI.InventoryCraftSlots + UI.InventoryButtons:
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
    InMenu = False

def End():
    Status.Started = False
    Status.dither = 0
    Status.InMenu = False
    Player.SelectHotbarSlot = 0
    UI.HotbarSlots.clear()
    UI.InventorySlots.clear()
    UI.InventoryCraftSlots.clear()
    UI.InventoryButtons.clear()
    GameManager.SceneController.ChangeScene("MainMenu")

def Start():
    if not Status.Started:
        Game.Camera = GameManager.Load.Camera
        Game.World = GameManager.Load.World
        Game.Entities = GameManager.Load.Entities
        Game.Inventory = GameManager.Load.Inventory
        Game.InventoryCraft = GameManager.Load.InventoryCraft
        Game.MouseItem = GameManager.Load.MouseItem
        SaveData.SaveFile = GameManager.Load.SaveFile

        if not Game.Inventory:
            for i in range(AppManager.GameInfo.InvetorySize):
                Game.Inventory[i] = {
                    'Item': None,
                    'Amount': 0
                }
        if not Game.InventoryCraft:
            for i in range(5):
                Game.InventoryCraft[i] = {
                    'Item': None,
                    'Amount': 0
                }
        
        if not Game.MouseItem:
            Game.MouseItem = {
                'Item': None,
                'Amount': 0
            }

        for i in range(9):
            UI.HotbarSlots.append(GameObjects.ItemSlot(48 + (i * 18), 230, i, Game.Inventory, 5, hotbar=True))
            UI.InventorySlots.append(GameObjects.ItemSlot(48 + (i * 18), 183, i, Game.Inventory, 13))

        for i in range(9, AppManager.GameInfo.InvetorySize):
            row = (i // 9) - 1
            col = i % 9
            x = 48 + (col * 18)
            y = 127 + (18 * row)
            UI.InventorySlots.append(GameObjects.ItemSlot(x, y, i, Game.Inventory, 13))

        UI.InventoryButtons.append(GameObjects.ButtonText(57, 71, 56, 16, "Save", lambda: SaveData.Save(), 13, 7, 7, 5))
        UI.InventoryButtons.append(GameObjects.ButtonText(57, 89, 56, 16, "Main Menu", lambda: End(), 13, 7, 7, 5))
        UI.InventoryButtons.append(GameObjects.ButtonSprite(224, 176, 32, 32, 0, 224, 2, lambda: UI.DeleteMouseItem()))

        for i in range(4):
            row = i // 2
            col = i % 2
            x = 129 + (col * 18)
            y = 71 + (18 * row)
            UI.InventoryCraftSlots.append(GameObjects.ItemSlot(x, y, i, Game.InventoryCraft, 13))
        UI.InventoryCraftSlots.append(GameObjects.ItemSlot(183, 80, 4, Game.InventoryCraft, 13, result=True))

        print("Start")
        Status.Started = True

    if Status.dither < 1:
        Status.dither += 0.02
        pyxel.dither(Status.dither)
        return

def Update():
    Start()
    Input.Update()
    World.Generation()
    UI.Update()

def Draw():
    World.Renderer()
    UI.Draw()