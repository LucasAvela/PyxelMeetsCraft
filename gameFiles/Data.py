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
    Stone_Bricks_block = "Stone_Bricks_block"
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
    Door_block = "Door_block"

block_data = None
item_data = None
crafting_data = None
smelting_data = None

def Images():
    pyxel.images[1].load(0, 0, 'assets/sprites/Sprite_sheet.png')

def Colors():
    pyxel.colors[5] = 0x545454

def GameData():
    global block_data, item_data, crafting_data, smelting_data
    with open('assets/data/blocks_id.json') as f: block_data = json.load(f)
    with open('assets/data/Items_id.json') as g: item_data = json.load(g)
    with open('assets/data/craftings_recipes.json') as h: crafting_data = json.load(h)
    with open('assets/data/smelting_recipes.json') as i: smelting_data = json.load(i)