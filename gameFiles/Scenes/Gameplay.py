import pyxel
import json
import time

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
        data['Entities'] = {str(k): v for k, v in Game.Entities.items()}
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

    def AccessInventory():
        if pyxel.btnp(pyxel.KEY_E):
            if Status.InMenu:
                UI.EntitySlots.clear()

            Status.InMenu = not Status.InMenu
            UI.MenuType = "Inventory"
    
    def AccessMenu(Menu, key):
        Status.InMenu = True
        
        if Menu == "Workbench":
            for i in range(9):
                row = i // 3
                col = i % 3
                x = 75 + (col * 18)
                y = 62 + (18 * row)
                UI.EntitySlots.append(GameObjects.ItemSlot(x, y, i, Game.Entities[key]['Inventory'], 13, crafting=True))
            UI.EntitySlots.append(GameObjects.ItemSlot(165, 80, 9, Game.Entities[key]['Inventory'], 13, result=True))
        
        if Menu == "Furnace":
            UI.EntitySlots.append(GameObjects.ItemSlot(94, 62, 0, Game.Entities[key]['Inventory'], 13))
            UI.EntitySlots.append(GameObjects.ItemSlot(94, 98, 1, Game.Entities[key]['Inventory'], 13))
            UI.EntitySlots.append(GameObjects.ItemSlot(147, 80, 2, Game.Entities[key]['Inventory'], 13, result=True))

        if Menu == "Chest":
            for i in range(27):
                row = i // 9
                col = i % 9
                x = 48 + (col * 18)
                y = 62 + (18 * row)
                UI.EntitySlots.append(GameObjects.ItemSlot(x, y, i, Game.Entities[key]['Inventory'], 13))
        
        UI.MenuType = Menu
        UI.EntityKey = key
    
    def HandleMouseInput():
        left = pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        right = pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT)

        if not Status.InMenu:
            if left:
                if Player.SelectBlock is not None:
                    Player.BreakBlock(Player.SelectBlock[0], Player.SelectBlock[1], Player.SelectBlock[2])
            elif right:
                if Player.SelectBlock is not None:
                    key = (Player.SelectBlock[0], Player.SelectBlock[1], Player.SelectBlock[2])
                    if key in Game.Entities:
                        Input.AccessMenu(Game.Entities[key]['Entity'], key)
                    else:
                        Player.UseItem(Player.SelectHotbarSlot)
        else:
            if left:
                Player.MoveItem("left")
            elif right:
                Player.MoveItem("right")

    def Update():
        if not Status.InMenu:
            Input.CameraMove()
            Input.SelectHotbar()
            Input.SelectBlock()
            Input.SelectionModifier()
        
        Input.HandleMouseInput()
        Input.AccessInventory()

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

    def MoveItem(input):
        auxSlots = None
        if UI.MenuType == "Inventory":
            auxSlots = UI.InventoryCraftSlots
        else:
            auxSlots = UI.EntitySlots

        for itemSlot in UI.InventorySlots + auxSlots:
            if itemSlot.clicked() is not None: 
                if input == "left":
                    if Game.MouseItem["Item"] is None and itemSlot.Item is not None:
                        Game.MouseItem = {"Item": itemSlot.Item, "Amount": itemSlot.Amount}
                        itemSlot.Storage[itemSlot.i] = {"Item": None, "Amount": 0}
                        if itemSlot.result:
                            for slot in auxSlots:
                                if slot.crafting:
                                    slot.Storage[slot.i]["Amount"] -= 1
                                    if slot.Storage[slot.i]["Amount"] <= 0:
                                        slot.Storage[slot.i]["Item"] = None
                                        slot.Storage[slot.i]["Amount"] = 0
                        return

                    if itemSlot.result:return 
                    if itemSlot.Item is None:
                        itemSlot.Storage[itemSlot.i] = Game.MouseItem
                        Game.MouseItem = {"Item": None, "Amount": 0}
                        return
                    if itemSlot.Item == Game.MouseItem["Item"]:
                        total = itemSlot.Storage[itemSlot.i]["Amount"] + Game.MouseItem["Amount"]
                        max_stack = Data.GameData.item_data[itemSlot.Item]["stack"]
                        if total > max_stack:
                            itemSlot.Storage[itemSlot.i]["Amount"] = max_stack
                            Game.MouseItem["Amount"] = total - max_stack
                        else:
                            itemSlot.Storage[itemSlot.i]["Amount"] += Game.MouseItem["Amount"]
                            Game.MouseItem = {"Item": None, "Amount": 0}
                        return
                    else:
                        mouseitem = Game.MouseItem
                        Game.MouseItem = {"Item": itemSlot.Item, "Amount": itemSlot.Amount}
                        itemSlot.Storage[itemSlot.i] = mouseitem
                        return

                if input == "right":
                    if Game.MouseItem["Item"] is None and itemSlot.Item is not None:
                        if itemSlot.result:
                            Game.MouseItem = {"Item": itemSlot.Item, "Amount": itemSlot.Amount}
                            itemSlot.Storage[itemSlot.i] = {"Item": None, "Amount": 0}
                            for slot in auxSlots:
                                if slot.crafting:
                                    slot.Storage[slot.i]["Amount"] -= 1
                                    if slot.Storage[slot.i]["Amount"] <= 0:
                                        slot.Storage[slot.i]["Item"] = None
                                        slot.Storage[slot.i]["Amount"] = 0
                            return
                        getAmount = itemSlot.Amount // 2
                        if getAmount < 1: getAmount = 1
                        Game.MouseItem = {"Item": itemSlot.Item, "Amount": getAmount}
                        itemSlot.Storage[itemSlot.i]["Amount"] -= getAmount
                        return

                    if itemSlot.result:return
                    if itemSlot.Item is None:
                        itemSlot.Storage[itemSlot.i] = {"Item": Game.MouseItem["Item"], "Amount": 1}
                        Game.MouseItem["Amount"] -= 1
                        if Game.MouseItem["Amount"] < 1:
                            Game.MouseItem = {"Item": None, "Amount": 0}
                        return
                    else:
                        if itemSlot.Item != Game.MouseItem["Item"]: return
                        if itemSlot.Storage[itemSlot.i]["Amount"] + 1 > Data.GameData.item_data[itemSlot.Item]["stack"]: return
                        itemSlot.Storage[itemSlot.i]["Amount"] += 1
                        Game.MouseItem["Amount"] -= 1
                        if Game.MouseItem["Amount"] < 1: Game.MouseItem = {"Item": None, "Amount": 0}
                        return

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
        if layer <= 0: return
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
        
        if blockData['name'] == "Bed_block_Top":
            Game.World[(x, y, layer)]['Block'] = Data.Blocks.Air
            Game.World[(x, y + 1, layer)]['Block'] = Data.Blocks.Air
            Player.AddItem("Bed_item", 1)
            return
        
        if blockData['name'] == "Workbench_block" or blockData['name'] == "Furnace_block" or blockData['name'] == "Chest_block":
            Game.World[(x, y, layer)]['Block'] = Data.Blocks.Air
            del Game.Entities[(x, y, layer)]
            if blockData['name'] == "Workbench_block": Player.AddItem("Workbench_block_item", 1)
            if blockData['name'] == "Furnace_block": Player.AddItem("Furnace_block_item", 1)
            if blockData['name'] == "Chest_block": Player.AddItem("Chest_block_item", 1)

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

        if itemData['name'] == "Workbench_block_item":
            Game.World[(x, y, layer + 1)] = {"Block": "Workbench_block", "Solid": True}
            Game.Entities[(x, y, layer + 1)] = {"Entity": "Workbench", "Inventory": {}}
            for i in range(10):
                Game.Entities[(x, y, layer + 1)]["Inventory"][i] = {
                    'Item': None,
                    'Amount': 0
                }

        if itemData['name'] == "Furnace_block_item":
            Game.World[(x, y, layer + 1)] = {"Block": "Furnace_block", "Solid": True}
            Game.Entities[(x, y, layer + 1)] = {"Entity": "Furnace", "Inventory": {}}
            for i in range(3):
                Game.Entities[(x, y, layer + 1)]["MaxFuel"] = 0
                Game.Entities[(x, y, layer + 1)]["Fuel"] = 0
                Game.Entities[(x, y, layer + 1)]["Progress"] = 0
                Game.Entities[(x, y, layer + 1)]["Smelting"] = False
                Game.Entities[(x, y, layer + 1)]["Inventory"][i] = {
                    'Item': None,
                    'Amount': 0
                }

        if itemData['name'] == "Chest_block_item":
            Game.World[(x, y, layer + 1)] = {"Block": "Chest_block", "Solid": True}
            Game.Entities[(x, y, layer + 1)] = {"Entity": "Chest", "Inventory": {}}
            for i in range(27):
                Game.Entities[(x, y, layer + 1)]["Inventory"][i] = {
                    'Item': None,
                    'Amount': 0
                }
        
        Player.RemoveItem(Player.SelectHotbarSlot, 1)

class UI:
    HotbarSlots = []

    MenuType = None
    EntityKey = None

    InventorySlots = []
    InventoryCraftSlots = []
    InventoryButtons = []

    EntitySlots = []

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
        pyxel.text(48, 117, "Inventory", 5, Data.GameData.spleen5_font)

        for itemSlot in UI.InventorySlots:
            itemSlot.draw()

        if UI.MenuType == "Inventory":
            pyxel.blt(165, 80, 2, 64, 224, 16, 16, 2)
            pyxel.text(127, 60, "Crafting", 5, Data.GameData.spleen5_font)
            for itemSlot in UI.InventoryCraftSlots + UI.InventoryButtons:
                itemSlot.draw()
        else:
            for itemSlot in UI.EntitySlots:
                itemSlot.draw()
        
        if UI.MenuType == "Workbench":
            pyxel.blt(138, 81, 2, 64, 224, 16, 16, 2)
            pyxel.text(80, 52, "Crafting", 5, Data.GameData.spleen5_font)

        if UI.MenuType == "Furnace":
            progressValue = Game.Entities[UI.EntityKey]["Progress"]
            fuelValue = (Game.Entities[UI.EntityKey]["Fuel"] / Game.Entities[UI.EntityKey]["MaxFuel"]) if Game.Entities[UI.EntityKey]["MaxFuel"] > 0 else 0
            fuelValue = 0.1 if 0 < fuelValue < 0.1 else fuelValue
            pyxel.blt(120, 80, 2, 64, 224, 16, 16, 2)
            pyxel.blt(120, 80, 2, 64, 240, 16 * progressValue, 16, 2)
            pyxel.blt(94, 80, 2, 32, 240, 16, 16, 2)
            pyxel.blt(94, 80, 2, 32, 224, 16, (16 - fuelValue * 16), 2)
            pyxel.text(110, 52, "Furnace", 5, Data.GameData.spleen5_font)

        if UI.MenuType == "Chest":
            pyxel.text(48, 52, "Chest", 5, Data.GameData.spleen5_font)

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

    def InventoryCraft():
        matrix = [[Game.InventoryCraft[0]['Item'], Game.InventoryCraft[1]['Item']],
                  [Game.InventoryCraft[2]['Item'], Game.InventoryCraft[3]['Item']]]
        
        Game.InventoryCraft[4]['Item'], Game.InventoryCraft[4]['Amount'] = GameManager.Crafting.Check(matrix)

    def WorkbenchCraft(Inventory):
        matrix = [[Inventory[0]['Item'], Inventory[1]['Item'], Inventory[2]['Item']], 
                  [Inventory[3]['Item'], Inventory[4]['Item'], Inventory[5]['Item']], 
                  [Inventory[6]['Item'], Inventory[7]['Item'], Inventory[8]['Item']]]
        
        Inventory[9]['Item'], Inventory[9]['Amount'] = GameManager.Crafting.Check(matrix)

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
            for itemSlot in UI.InventorySlots:
                itemSlot.update()
            
            if UI.MenuType == "Inventory":
                UI.InventoryCraft()
                for itemSlot in UI.InventoryCraftSlots + UI.InventoryButtons:
                    itemSlot.update()
            else:
                if UI.MenuType == "Workbench": UI.WorkbenchCraft(Game.Entities[UI.EntityKey]['Inventory'])
                for itemSlot in UI.EntitySlots:
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

class Entities:
    def FurnaceEntity(key):
        entity = Game.Entities[key]
        materialSlot = entity["Inventory"][0]
        fuelSlot = entity["Inventory"][1]
        resultSlot = entity["Inventory"][2]

        if not entity["Smelting"]:
            if materialSlot["Item"] is not None and fuelSlot["Item"] is not None:
                try: 
                    materialData = Data.GameData.smelting_data[materialSlot["Item"]]
                    fuelData = Data.GameData.item_data[fuelSlot["Item"]]
                except KeyError: return

                if resultSlot["Item"] is None or resultSlot["Item"] == materialData["result"]:
                    entity["MaxFuel"] = fuelData["fuel"]
                    entity["Fuel"] = fuelData["fuel"]
                    
                    fuelSlot["Amount"] -= 1
                    if fuelSlot["Amount"] <= 0:
                        fuelSlot["Item"] = None
                        fuelSlot["Amount"] = 0
                    
                    entity["Smelting"] = True

        if entity["Smelting"]:
            try: 
                materialData = Data.GameData.smelting_data[materialSlot["Item"]]
                if resultSlot["Item"] is not None and materialData["result"] != resultSlot["Item"] or resultSlot["Amount"] >= Data.GameData.item_data[materialData["result"]]["stack"]:
                    entity["Progress"] = 0
            except KeyError:
                entity["Progress"] = 0

            if entity['Fuel'] > 0:
                entity['Fuel'] -= 0.04
                if materialSlot["Item"] is not None:
                    entity["Progress"] += 0.04
                    if entity["Progress"] >= 1:
                        entity["Progress"] = 0
                        if resultSlot["Item"] is None:
                            resultSlot["Item"] = materialData["result"]
                            resultSlot["Amount"] = 1
                        elif resultSlot["Item"] == materialData["result"]:
                            resultSlot["Amount"] += 1
                        materialSlot["Amount"] -= 1
                        if materialSlot["Amount"] <= 0:
                            materialSlot["Item"] = None
                            materialSlot["Amount"] = 0
            else:
                if fuelSlot["Item"] is not None:
                    try: fuelData = Data.GameData.item_data[fuelSlot["Item"]]
                    except KeyError:
                        entity["Smelting"] = False
                        entity["Progress"] = 0
                        entity["Fuel"] = 0
                        entity["MaxFuel"] = 0
                        return

                    if materialSlot["Item"] is None:
                        if entity["Fuel"] <= 0:
                            entity["Smelting"] = False
                            entity["Progress"] = 0
                            entity["Fuel"] = 0
                            entity["MaxFuel"] = 0
                            return
                        
                    if materialData is not None and materialData["result"] != resultSlot["Item"]:
                        entity["Smelting"] = False
                        entity["Progress"] = 0
                        entity["Fuel"] = 0
                        entity["MaxFuel"] = 0
                        return

                    entity["MaxFuel"] = fuelData["fuel"]
                    entity["Fuel"] = fuelData["fuel"]
                    fuelSlot["Amount"] -= 1
                    if fuelSlot["Amount"] <= 0:
                        fuelSlot["Item"] = None
                        fuelSlot["Amount"] = 0
    
                else:
                    entity["Smelting"] = False
                    entity["Progress"] = 0
                    entity["Fuel"] = 0
                    entity["MaxFuel"] = 0
                    return
                

    def Update():
        for key, entity in Game.Entities.items():
            if entity["Entity"] == "Furnace": Entities.FurnaceEntity(key)

class Status:
    Started = False
    dither = 0
    InMenu = False
    Enter = False
    Exit = False
    
    def ExitAction():
        Status.Exit = True

    def ExitAnimation():
        if Status.Exit:
            if Status.dither > 0:
                Status.dither -= 0.02
                pyxel.dither(Status.dither)
                return
            else:
                End()

    def Update():
        Status.ExitAnimation()

def End():
    Status.Started = False
    Status.dither = 0
    Status.InMenu = False
    Status.Enter = False
    Status.Exit = False
    Player.SelectHotbarSlot = 0
    UI.HotbarSlots.clear()
    UI.InventorySlots.clear()
    UI.InventoryCraftSlots.clear()
    UI.InventoryButtons.clear()
    time.sleep(0.5)
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
            x = 48 + (i * 18)
            UI.HotbarSlots.append(GameObjects.ItemSlot(x, 230, i, Game.Inventory, 5, hotbar=True))
            UI.InventorySlots.append(GameObjects.ItemSlot(x, 183, i, Game.Inventory, 13))
        
        for i in range(9, AppManager.GameInfo.InvetorySize):
            row = (i // 9) - 1
            col = i % 9
            x = 48 + (col * 18)
            y = 127 + (18 * row)
            UI.InventorySlots.append(GameObjects.ItemSlot(x, y, i, Game.Inventory, 13))
        
        UI.InventoryButtons += [
            GameObjects.ButtonText(57, 71, 56, 16, "Save", lambda: SaveData.Save(), 13, 7, 7, 5),
            GameObjects.ButtonText(57, 89, 56, 16, "Main Menu", lambda: Status.ExitAction(), 13, 7, 7, 5),
            GameObjects.ButtonSprite(224, 176, 32, 32, 0, 224, 2, lambda: UI.DeleteMouseItem())
        ]

        for i in range(4):
            x = 129 + (i % 2) * 18
            y = 71 + (i // 2) * 18
            UI.InventoryCraftSlots.append(GameObjects.ItemSlot(x, y, i, Game.InventoryCraft, 13, crafting=True))
        UI.InventoryCraftSlots.append(GameObjects.ItemSlot(183, 80, 4, Game.InventoryCraft, 13, result=True))

        Status.Started = True

    if Status.dither < 1 and not Status.Enter:
        Status.dither += 0.02
        pyxel.dither(Status.dither)
        return

    Status.Enter = True

def TickUpdate():
    if pyxel.frame_count % (AppManager.Settings.Fps // AppManager.Settings.Tps) == 0:
        Entities.Update()

def Update():
    Start()
    TickUpdate()
    Input.Update()
    World.Generation()
    UI.Update()
    Status.Update()

def Draw():
    World.Renderer()
    UI.Draw()