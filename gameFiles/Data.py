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
    Door_block_Top = "Door_block_Top"
    Door_block_Bottom = "Door_block_Bottom"
    Glass_block = "Glass_block"

class GameStates(Enum):
    MainMenu = 0
    Gameplay = 1
    Menu = 2

blocks_by_layer = [
    {Blocks.Bedrock_block.value: 100},
    {Blocks.Cobblestone_block.value: 90, Blocks.Coal_Ore_block.value: 5, Blocks.Iron_Ore_block.value: 2, Blocks.Gold_Ore_block.value: 1.5, Blocks.Diamond_Ore_block.value: 1, Blocks.Emerald_Ore_block.value: 0.5},
    {Blocks.Stone_block.value: 95, Blocks.Coal_Ore_block.value: 3.5, Blocks.Iron_Ore_block.value: 1, Blocks.Gold_Ore_block.value: 0.5},
    {Blocks.Stone_block.value: 50, Blocks.Dirt_block.value: 50},
    {Blocks.Dirt_block.value: 100},
    {Blocks.Grass_block.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
    {Blocks.Air.value: 100},
]

block_Size = 8
block_Height = 4
chunk_size = 8
view_Distance = 2

layers_quantity = len(blocks_by_layer)
top_layer = layers_quantity - 1
bot_layer = 0

def Images():
    pyxel.images[1].load(0, 0, 'assets/sprites/Sprite_sheet.png')

def Colors():
    pyxel.colors[5] = 0x545454

block_data = None
item_data = None
crafting_data = None
smelting_data = None
def GameData():
    global block_data, item_data, crafting_data, smelting_data

    with open('assets/data/blocks_id.json', 'r') as f:
        blocks_list = json.load(f)
        block_data = { block["name"]: block for block in blocks_list["Blocks"] }

    with open('assets/data/Items_id.json', 'r') as g:
        item_list = json.load(g)
        item_data = { item["name"]: item for item in item_list["Items"] }

    with open('assets/data/craftings_recipes.json', 'r') as h:
        crafting_data = json.load(h)

    with open('assets/data/smelting_recipes.json', 'r') as i:
        smelting_data = json.load(i)