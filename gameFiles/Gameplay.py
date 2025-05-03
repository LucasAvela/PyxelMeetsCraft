import pyxel

import gameFiles.Data as Data
import gameFiles.WorldGen as WorldGen
import gameFiles.Renderer as Renderer
import gameFiles.GameManager as GameManager

class Inputs:
    def CameraMove():
        if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            GameManager.Camera.Move(0, -GameManager.GameInfo.CameraSpeed)
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            GameManager.Camera.Move(0, GameManager.GameInfo.CameraSpeed)
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            GameManager.Camera.Move(-GameManager.GameInfo.CameraSpeed, 0)
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            GameManager.Camera.Move(GameManager.GameInfo.CameraSpeed, 0)

        pyxel.camera(GameManager.Camera.Position[0], GameManager.Camera.Position[1],)
    
    def SelectHotbar():
        if pyxel.btnp(pyxel.KEY_1): Player.hotbar_selected = 0
        if pyxel.btnp(pyxel.KEY_2): Player.hotbar_selected = 1
        if pyxel.btnp(pyxel.KEY_3): Player.hotbar_selected = 2
        if pyxel.btnp(pyxel.KEY_4): Player.hotbar_selected = 3
        if pyxel.btnp(pyxel.KEY_5): Player.hotbar_selected = 4
        if pyxel.btnp(pyxel.KEY_6): Player.hotbar_selected = 5
        if pyxel.btnp(pyxel.KEY_7): Player.hotbar_selected = 6
        if pyxel.btnp(pyxel.KEY_8): Player.hotbar_selected = 7
        if pyxel.btnp(pyxel.KEY_9): Player.hotbar_selected = 8

        if pyxel.mouse_wheel < 0:
            Player.hotbar_selected += 1
            if Player.hotbar_selected > 8: Player.hotbar_selected = 0
        elif pyxel.mouse_wheel > 0:
            Player.hotbar_selected -= 1
            if Player.hotbar_selected < 0: Player.hotbar_selected = 8

    def DebugAddItem():
        if pyxel.btnp(pyxel.KEY_KP_1):
            Player.AddItem(Data.Items.Gold, 48)

    def SelectBlock():
        position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
        position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

        for layer in range(GameManager.GameInfo.MaxLayer, -1, -1):
            target_x = position_x // GameManager.GameInfo.BlockSize
            target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                if ((target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air):
                    if not Player.modifier:
                        Player.selectBlock = [target_x, adj_y, layer]
                        break
                    elif (target_x, adj_y - 1, layer + 1) in WorldGen.World and WorldGen.World[(target_x, adj_y - 1, layer + 1)]['Block'] != Data.Blocks.Air:
                        Player.selectBlock = [target_x, adj_y - 1, layer + 1]
                        break

        else: Player.selectBlock = None

    def SelectionModifier():
        if pyxel.btnp(pyxel.KEY_SHIFT):
            Player.modifier = True
        
        if pyxel.btnr(pyxel.KEY_SHIFT):
            Player.modifier = False

    def AccessMenu():
        if pyxel.btnp(pyxel.KEY_E):
            Status.inMenu = True

    def LeftInputAction():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if Player.selectBlock is None: return
            Player.BreakBlock(Player.selectBlock[0], Player.selectBlock[1], Player.selectBlock[2])

    def RightInputAction():
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            Player.UseItem(Player.hotbar_selected)

    def Update():
        Inputs.CameraMove()
        Inputs.SelectHotbar()
        Inputs.SelectBlock()
        Inputs.SelectionModifier()
        Inputs.AccessMenu()
        Inputs.LeftInputAction()
        Inputs.RightInputAction()

        Inputs.DebugAddItem()

class Player:
    inventory = {}
    hotbar_selected = 0
    hotbar_postions = [48, 66, 84, 102, 120, 138, 156, 174, 192]
    hotbat_amounts_positions = [58, 76, 94, 112, 130, 148, 166, 184, 202]

    selectBlock = None
    modifier = False

    def AddItem(item, amount):
        itemData = Data.GameData.item_data[item]

        for i in range(GameManager.GameInfo.InvetorySize):
            if Player.inventory[i]['Item'] is None:
                Player.inventory[i]['Item'] = item
                if amount <= itemData["stack"]:
                    Player.inventory[i]['Amount'] = amount
                    break
                else:
                    Player.inventory[i]['Amount'] = itemData["stack"]
                    amount -= itemData["stack"]
                    continue
            elif Player.inventory[i]['Item'] == item:
                if Player.inventory[i]['Amount'] + amount <= itemData["stack"]:
                    Player.inventory[i]['Amount'] += amount
                    break
                else:
                    amount -= (itemData["stack"] - Player.inventory[i]['Amount'])
                    Player.inventory[i]['Amount'] = itemData["stack"]
                    continue
    
    def RemoveItem(key, amount):
        if Player.inventory[key]['Amount'] <= amount:
            Player.inventory[key]['Item'] = None
            Player.inventory[key]['Amount'] = 0
        else:
            Player.inventory[key]['Amount'] -= amount

    def UseItem(key):
        item = Player.inventory[key]['Item']

        if item is None:
            return
        
        itemData = Data.GameData.item_data[item]

        if itemData['action'] == "Place":
            if Player.selectBlock is None: return
            Player.PlaceBlock(Player.selectBlock[0], Player.selectBlock[1], Player.selectBlock[2], itemData['block'])
            return
        elif itemData['action'] == "PlaceSpecial":
            if Player.selectBlock is None: return
            Player.PlaceSpecialBlock(Player.selectBlock[0], Player.selectBlock[1], Player.selectBlock[2], itemData)
            return

    def BreakBlock(x, y, layer):
        block = WorldGen.World[(x, y, layer)]
        blockData = Data.GameData.block_data[block['Block']]
        item = blockData['drop']

        if item == "Special": 
            Player.BreakSpecialBlock(x, y, layer, blockData)
            return

        block['Block'] = Data.Blocks.Air
        Player.AddItem(item, 1)
    
    def BreakSpecialBlock(x, y, layer, blockData):
        if blockData['name'] == "Bed_block_Bottom":
            WorldGen.World[(x, y, layer)]['Block'] = Data.Blocks.Air
            WorldGen.World[(x, y - 1, layer)]['Block'] = Data.Blocks.Air
            Player.AddItem("Bed_item", 1)
            return
        elif blockData['name'] == "Bed_block_Top":
            WorldGen.World[(x, y, layer)]['Block'] = Data.Blocks.Air
            WorldGen.World[(x, y + 1, layer)]['Block'] = Data.Blocks.Air
            Player.AddItem("Bed_item", 1)
            return
    
    def PlaceBlock(x, y, layer, block):
        if Player.modifier:
            x = x
            y = y + 1
            layer = layer - 1

        if layer + 1 < GameManager.GameInfo.MaxLayer:
            WorldGen.World[(x, y, layer + 1)] = {"Block": block, "Solid": True}
            Player.RemoveItem(Player.hotbar_selected, 1)
    
    def PlaceSpecialBlock(x, y, layer, itemData):
        if Player.modifier:
            x = x
            y = y + 1
            layer = layer - 1

        if itemData['name'] == "Bed_item":
            if layer + 1 < GameManager.GameInfo.MaxLayer:
                if (x, y - 1, layer + 1) not in WorldGen.World or WorldGen.World[(x, y - 1, layer + 1)]['Block'] == Data.Blocks.Air:
                    WorldGen.World[(x, y, layer + 1)] = {"Block": "Bed_block_Bottom", "Solid": True}
                    WorldGen.World[(x, y - 1, layer + 1)] = {"Block": "Bed_block_Top", "Solid": True}
                    Player.RemoveItem(Player.hotbar_selected, 1)

class UI:
    def DrawArea():
        if Player.selectBlock is None: return
        
        target_x = Player.selectBlock[0]
        adj_y = Player.selectBlock[1]
        layer = Player.selectBlock[2]

        target_y = adj_y - (layer // 2)

        draw_x = target_x * GameManager.GameInfo.BlockSize
        draw_y = (target_y * GameManager.GameInfo.BlockSize) - ((layer % 2) * GameManager.GameInfo.BlockHeight)

        area_local_x = 48
        area_local_y = 240

        if Player.modifier:
            draw_y += 8
            area_local_y = 252

        pyxel.blt(
            draw_x, 
            draw_y, 
            1, 
            area_local_x, 
            area_local_y, 
            GameManager.GameInfo.BlockSize, 
            GameManager.GameInfo.BlockSize, 
            2)

    def DrawHotbar():
        pyxel.camera(0, 0)
        pyxel.blt(46, 228, 2, 46, 228, 164, 20, 2)
        
        pyxel.blt(Player.hotbar_postions[Player.hotbar_selected] - 3, 230 - 3, 2, 0, 234, 22, 22, 2)
        
        for i in range(9):
            item = Player.inventory[i]['Item']
            amount = Player.inventory[i]['Amount']

            if item is None or amount < 1:
                continue

            itemData = Data.GameData.item_data[item]
            item_x = itemData['local']['x']
            item_y = itemData['local']['y']

            pyxel.blt(
                Player.hotbar_postions[i],
                230,
                1,
                item_x,
                item_y,
                GameManager.GameInfo.ItemSize,
                GameManager.GameInfo.ItemSize,
                2
            )
            
            if amount == 1: continue

            pyxel.text(Player.hotbat_amounts_positions[i], 242 + 1, str(amount) if amount >= 10 else " " + str(amount), 0)
            pyxel.text(Player.hotbat_amounts_positions[i] + 1, 242, str(amount) if amount >= 10 else " " + str(amount), 0)

            pyxel.text(Player.hotbat_amounts_positions[i],
                       242,
                       str(amount) if amount >= 10 else " " + str(amount),
                       7)

class Menu:
    inventory_positions = [
        [47, 183], [65, 183], [83, 183], [101, 183], [119, 183], [137, 183], [155, 183], [173, 183], [191, 183], 
        [47, 127], [65, 127], [83, 127], [101, 127], [119, 127], [137, 127], [155, 127], [173, 127], [191, 127], 
        [47, 145], [65, 145], [83, 145], [101, 145], [119, 145], [137, 145], [155, 145], [173, 145], [191, 145], 
        [47, 163], [65, 163], [83, 163], [101, 163], [119, 163], [137, 163], [155, 163], [173, 163], [191, 163], 
    ]

    def Update():
        if pyxel.btnp(pyxel.KEY_E): Status.inMenu = False

    def Draw():
        pyxel.camera(0, 0)
        pyxel.blt(42, 48 , 2, 42, 48, 172, 158, 2)
        pyxel.blt(222, 218 , 2, 222, 218, 29, 33, 2)

        for i in range(GameManager.GameInfo.InvetorySize):
            item = Player.inventory[i]['Item']
            amount = Player.inventory[i]['Amount']

            if item is None or amount < 1:
                continue

            itemData = Data.GameData.item_data[item]
            item_x = itemData['local']['x']
            item_y = itemData['local']['y']

            pyxel.blt(
                Menu.inventory_positions[i][0],
                Menu.inventory_positions[i][1],
                1,
                item_x,
                item_y,
                GameManager.GameInfo.ItemSize,
                GameManager.GameInfo.ItemSize,
                2
            )

            if amount == 1: continue

            pyxel.text(Menu.inventory_positions[i][0] + 10, Menu.inventory_positions[i][1] + 11, str(amount) if amount >= 10 else " " + str(amount), 0)
            pyxel.text(Menu.inventory_positions[i][0] + 10, Menu.inventory_positions[i][1] + 12, str(amount) if amount >= 10 else " " + str(amount), 0)
            pyxel.text(Menu.inventory_positions[i][0] +  9, Menu.inventory_positions[i][1] + 12, str(amount) if amount >= 10 else " " + str(amount), 0)

            pyxel.text(
                Menu.inventory_positions[i][0] + 9,
                Menu.inventory_positions[i][1] + 11,
                str(amount) if amount >= 10 else " " + str(amount),
                7
            )

class Status:
    Started = False
    inMenu = False

def Start():
    if not Status.Started:
        print("Started Gameplay")

        GameManager.Properties.InitPlayerInventory(Player.inventory)

        Status.Started = True

def Update():
    Start()

    if not Status.Started: return

    WorldGen.GenWorld()

    if not Status.inMenu:
        Inputs.Update()
    else:
        Menu.Update()

def Draw():
    pyxel.cls(0)

    if not Status.Started: return
    
    Renderer.WorldRenderer()

    if not Status.inMenu:
        UI.DrawArea()
        UI.DrawHotbar()
    else:
        Menu.Draw()