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

    def DebugAddItem():
        if pyxel.btnp(pyxel.KEY_KP_1):
            Player.AddItem(Data.Items.Grass_block_item, 1)

    def Update():
        Inputs.CameraMove()
        Inputs.SelectHotbar()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): Player.BreakBlock()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT): Player.UseItem(Player.hotbar_selected)

        Inputs.DebugAddItem()

class Player:
    inventory = {}
    hotbar_selected = 0
    hotbar_postions = [48, 66, 84, 102, 120, 138, 156, 174, 192]
    hotbat_amounts_positions = [58, 76, 94, 112, 130, 148, 166, 184, 202]

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

        if itemData['type'] == "Block":
            Player.RemoveItem(key, 1)
            Player.PlaceBlock(itemData['block'])


    def BreakBlock():
        position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
        position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

        for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
            target_x = position_x // GameManager.GameInfo.BlockSize
            target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                if ((target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air):
                    blockData = Data.GameData.block_data[WorldGen.World[(target_x, adj_y, layer)]['Block']]
                    item = blockData['drop']
                    WorldGen.World[(target_x, adj_y, layer)]['Block'] = Data.Blocks.Air
                    Player.AddItem(item, 1)
                    break
    
    def PlaceBlock(block):
        position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
        position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

        for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
            target_x = position_x // GameManager.GameInfo.BlockSize
            target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                if (target_x, adj_y, layer + 1) not in WorldGen.World:
                    WorldGen.World[(target_x, adj_y, layer + 1)] = {"Block": block, "Solid": True}
                
                if WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air:
                    WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] = block
                
                break

class UI:
    def DrawArea():
        position_x = pyxel.mouse_x + GameManager.Camera.Position[0]
        position_y = pyxel.mouse_y + GameManager.Camera.Position[1]

        for layer in range(GameManager.GameInfo.MaxLayer, 0, -1):
            target_x = position_x // GameManager.GameInfo.BlockSize
            target_y = (position_y + ((layer % 2) * GameManager.GameInfo.BlockHeight)) // GameManager.GameInfo.BlockSize
            adj_y = target_y + (layer // 2)

            if (target_x, adj_y, layer) in WorldGen.World and WorldGen.World[(target_x, adj_y, layer)]['Block'] != Data.Blocks.Air:
                if ((target_x, adj_y, layer + 1) not in WorldGen.World or WorldGen.World[(target_x, adj_y, layer + 1)]['Block'] == Data.Blocks.Air):
                    pyxel.blt(target_x * GameManager.GameInfo.BlockSize, 
                            (target_y * GameManager.GameInfo.BlockSize) - ((layer % 2) * GameManager.GameInfo.BlockHeight), 
                            1, 
                            48,
                            240, 
                            GameManager.GameInfo.BlockSize, 
                            GameManager.GameInfo.BlockSize, 2)
                break

    def DrawHotbar():
        pyxel.camera(0, 0)
        pyxel.blt(46, 228, 2, 46, 228, 164, 20, 2)
        
        pyxel.blt(Player.hotbar_postions[Player.hotbar_selected] - 3,
                230 - 3,
                2,
                0,
                234,
                22,
                22,
                2)
        
        for i in range(9):
            item = Player.inventory[i]['Item']
            amount = Player.inventory[i]['Amount']

            if item is None or amount < 1:
                continue

            itemData = Data.GameData.item_data[item]
            item_x = itemData['local']['x']
            item_y = itemData['local']['y']

            pyxel.blt(Player.hotbar_postions[i],
                    230,
                    1,
                    item_x,
                    item_y,
                    GameManager.GameInfo.ItemSize,
                    GameManager.GameInfo.ItemSize,
                    2)
            
            if amount == 1: continue

            pyxel.text(Player.hotbat_amounts_positions[i], 242 + 1, str(amount) if amount >= 10 else " " + str(amount), 0)
            pyxel.text(Player.hotbat_amounts_positions[i] + 1, 242, str(amount) if amount >= 10 else " " + str(amount), 0)

            pyxel.text(Player.hotbat_amounts_positions[i],
                       242,
                       str(amount) if amount >= 10 else " " + str(amount),
                       7)
        

class Status:
    Started = False

def Start():
    if not Status.Started:
        print("Started Gameplay")

        GameManager.Properties.InitPlayerInventory(Player.inventory)

        Status.Started = True

def Update():
    Start()
    Inputs.Update()
    WorldGen.GenWorld()

def Draw():
    pyxel.cls(0)

    if Status.Started:
        Renderer.WorldRenderer()
        UI.DrawArea()
        UI.DrawHotbar()