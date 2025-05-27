import pyxel
import os
import json

class Blocks:
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
    StoneBricks_block = "StoneBricks_block"
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

class Items:
    Stick = "Stick"
    Coal = "Coal"
    Raw_Iron = "Raw_Iron"
    Iron = "Iron"
    Raw_Gold = "Raw_Gold"
    Gold = "Gold"
    Diamond = "Diamond"
    Emerald = "Emerald"
    Apple = "Apple"
    Golden_Apple = "Golden_Apple"
    Raw_Steak = "Raw_Steak"
    Cooked_Steak = "Cooked_Steak"
    Wooden_Pickaxe = "Wooden_Pickaxe"
    Wooden_Axe = "Wooden_Axe"
    Wooden_Shovel = "Wooden_Shovel"
    Wooden_Hoe = "Wooden_Hoe"
    Wooden_Sword = "Wooden_Sword"
    Stone_Pickaxe = "Stone_Pickaxe"
    Stone_Axe = "Stone_Axe"
    Stone_Shovel = "Stone_Shovel"
    Stone_Hoe = "Stone_Hoe"
    Stone_Sword = "Stone_Sword"
    Iron_Pickaxe = "Iron_Pickaxe"
    Iron_Axe = "Iron_Axe"
    Iron_Shovel = "Iron_Shovel"
    Iron_Hoe = "Iron_Hoe"
    Iron_Sword = "Iron_Sword"
    Golden_Pickaxe = "Golden_Pickaxe"
    Golden_Axe = "Golden_Axe"
    Golden_Shovel = "Golden_Shovel"
    Golden_Hoe = "Golden_Hoe"
    Golden_Sword = "Golden_Sword"
    Diamond_Pickaxe = "Diamond_Pickaxe"
    Diamond_Axe = "Diamond_Axe"
    Diamond_Shovel = "Diamond_Shovel"
    Diamond_Hoe = "Diamond_Hoe"
    Diamond_Sword = "Diamond_Sword"
    Scissors = "Scissors"
    Grass_block_item = "Grass_block_item"
    Dirt_block_item = "Dirt_block_item"
    Stone_block_item = "Stone_block_item"
    Cobblestone_block_item = "Cobblestone_block_item"
    Bedrock_block_item = "Bedrock_block_item"
    Farmland_block_item = "Farmland_block_item"
    StoneBricks_block_item = "StoneBricks_block_item"
    Coal_Ore_block_item = "Coal_Ore_block_item"
    Iron_Ore_block_item = "Iron_Ore_block_item"
    Gold_Ore_block_item = "Gold_Ore_block_item"
    Diamond_Ore_block_item = "Diamond_Ore_block_item"
    Emerald_Ore_block_item = "Emerald_Ore_block_item"
    Iron_block_item = "Iron_block_item"
    Gold_block_item = "Gold_block_item"
    Diamond_block_item = "Diamond_block_item"
    Emerald_block_item = "Emerald_block_item"
    Wood_Planks_block_item = "Wood_Planks_block_item"
    Wood_Log_block_item = "Wood_Log_block_item"
    Leaves_block_item = "Leaves_block_item"
    Workbench_block_item = "Workbench_block_item"
    Furnace_block_item = "Furnace_block_item"
    Chest_block_item = "Chest_block_item"
    Glass_block_item = "Glass_block_item"
    Wool_White_block_item = "Wool_White_block_item"
    Wool_Black_block_item = "Wool_Black_block_item"
    Wool_Red_block_item = "Wool_Red_block_item"
    Wool_Yellow_block_item = "Wool_Yellow_block_item"
    Wool_Blue_block_item = "Wool_Blue_block_item"
    Wool_Green_block_item = "Wool_Green_block_item"
    Bed_item = "Bed_item"
    Door_item = "Door_item"

class GameData:
    block_data = None
    item_data = None
    crafting_data = None
    smelting_data = None

    save_0 = None
    save_1 = None
    save_2 = None

    spleen5_font = pyxel.Font('assets/fonts/spleen-5x8.bdf')
    spleen6_font = pyxel.Font('assets/fonts/spleen-6x12.bdf')

    def GameData():
        with open('assets/data/blocks_id.json', 'r') as f:
            blocks_list = json.load(f)
            GameData.block_data = { block["name"]: block for block in blocks_list["Blocks"] }

        with open('assets/data/items_id.json', 'r') as g:
            item_list = json.load(g)
            GameData.item_data = { item["name"]: item for item in item_list["Items"] }

        with open('assets/data/crafts_recipes.json', 'r') as h:
            GameData.crafting_data = json.load(h)

        with open('assets/data/smelts_recipes.json', 'r') as i:
            smelt_list = json.load(i)
            GameData.smelting_data = { smelt["item"]: smelt for smelt in smelt_list["Recipes"] }

    def SaveFiles():
        try:
            with open('gameFiles/Saves/save_0.json', 'r') as f: GameData.save_0 = json.load(f)
        except FileNotFoundError: GameData.save_0 = None

        try:
            with open('gameFiles/Saves/save_1.json', 'r') as f: GameData.save_1 = json.load(f)
        except FileNotFoundError: GameData.save_1 = None

        try:
            with open('gameFiles/Saves/save_2.json', 'r') as f: GameData.save_2 = json.load(f)
        except FileNotFoundError: GameData.save_2 = None

    def Images():
        pyxel.images[0].load(0, 0, 'assets/sprites/Sprite_sheet_Menu.png')
        pyxel.images[1].load(0, 0, 'assets/sprites/Sprite_sheet.png')
        pyxel.images[2].load(0, 0, 'assets/sprites/Sprite_sheet_UI.png')

    def Colors():
        pyxel.colors[0]  = 0x000000  # Black
        pyxel.colors[1]  = 0x25335f  # Dark Blue
        pyxel.colors[2]  = 0x7e2072  # Dark Purple
        pyxel.colors[3]  = 0x19959c  # Dark Green
        pyxel.colors[4]  = 0x8b4852  # Brown
        pyxel.colors[5]  = 0x545454  # Dark Gray
        pyxel.colors[6]  = 0xa9c1ff  # Light Blue
        pyxel.colors[7]  = 0xeeeeee  # White
        pyxel.colors[8]  = 0xd41844  # Red
        pyxel.colors[9]  = 0xd38441  # Orange
        pyxel.colors[10] = 0xe9c35b  # Yellow
        pyxel.colors[11] = 0x70c6a9  # Green
        pyxel.colors[12] = 0x7696de  # Blue
        pyxel.colors[13] = 0xa3a3a3  # Indigo
        pyxel.colors[14] = 0xff9798  # Pink
        pyxel.colors[15] = 0xedc7b0  # Peach

    def Start():
        GameData.GameData()
        GameData.SaveFiles()
        GameData.Images()
        GameData.Colors()