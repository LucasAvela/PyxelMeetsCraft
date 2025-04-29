import pyxel
import json
from enum import Enum

class Blocks(Enum):
    Air = "Air"
    Grass_block = "Grass_block"
    Dirt_block = "Dirt_block"
    Stone_block = "Stone_block"
    Cobblestone_block = "Cobblestone_block"
    Bedrock_block = "Bedrock_block"
    Coal_Ore_block = "Coal_Ore_block"
    Iron_Ore_block = "Iron_Ore_block"
    Gold_Ore_block = "Gold_Ore_block"
    Diamond_Ore_block = "Diamond_Ore_block"
    Emerald_Ore_block = "Emerald_Ore_block"
    Stone_Bricks_block = "StoneBricks_block"
    Iron_block = "Iron_block"
    Gold_block = "Gold_block"
    Diamond_block = "Diamond_block"
    Emerald_block = "Emerald_block"
    Wood_Log_block = "Wood_Log_block"
    Wood_plank_block = "Wood_Plank_block"
    Leaves_block = "Leaves_block"
    Workbench_block = "Workbench_block"
    Chest_block = "Chest_block"
    Furnace_block = "Furnace_block"
    Bed_block_Top = "Bed_block_Top"
    Bed_block_Bottom = "Bed_block_Bottom"
    Door_block_Top = "Door_block_Top"
    Door_block_Bottom = "Door_block_Bottom"
    Glass_block = "Glass_block"

class GameStates(Enum):
    MainMenu = 0
    Gameplay = 1
    Menu = 2

class GameData():
    block_data = None
    item_data = None
    crafting_data = None
    smelting_data = None

    def GameData():
        with open('D:/Projects/Avela/Pyxel/PyxelMeetsCraft/assets/data/blocks_id.json', 'r') as f:
            blocks_list = json.load(f)
            GameData.block_data = { block["name"]: block for block in blocks_list["Blocks"] }

        with open('D:/Projects/Avela/Pyxel/PyxelMeetsCraft/assets/data/items_id.json', 'r') as g:
            item_list = json.load(g)
            GameData.item_data = { item["name"]: item for item in item_list["Items"] }

        with open('D:/Projects/Avela/Pyxel/PyxelMeetsCraft/assets/data/craftings_recipes.json', 'r') as h:
            GameData.crafting_data = json.load(h)

        with open('D:/Projects/Avela/Pyxel/PyxelMeetsCraft/assets/data/smelting_recipes.json', 'r') as i:
            GameData.smelting_data = json.load(i)

    def Images():
        pyxel.images[0].load(0, 0, 'assets/sprites/Sprite_sheet_Menu.png')
        pyxel.images[1].load(0, 0, 'assets/sprites/Sprite_sheet.png')
        pyxel.images[2].load(0, 0, 'assets/sprites/Sprite_sheet_UI.png')

    def Colors():
        pyxel.colors[5] = 0x545454

    def Start():
        GameData.GameData()
        GameData.Images()
        GameData.Colors()