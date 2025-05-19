import pandas as pd
import json

def Blocks():
    df = pd.read_excel('assets\\data\\SheetTable.xlsx', sheet_name='Blocks')

    blocks = []

    for _, row in df.iterrows():
        name = row['Name']
        drop = row['Drop']
        tool = row['Tool']
        level = row['Level']
        local_x = row['Local_x']
        local_y = row['Local_y']
        solid = bool(row['Solid'])
        collision = bool(row['Collision'])

        local = {
            "x": int(local_x),
            "y": int(local_y)
        }

        block = {
            "name": name,
            "drop": drop,
            "tool": tool,
            "level": int(level),
            "local": local,
            "Colision": collision,
            "Solid": solid
        }

        blocks.append(block)

    data = {
        "Blocks": blocks
    }

    with open('assets\\data\\blocks_id.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("blocks_id.json created successfully!")

def Items():
    df = pd.read_excel('assets\\data\\SheetTable.xlsx', sheet_name='Items')

    items = []

    for _, row in df.iterrows():
        name = row['Name']
        type = row['Type']
        level = row['Level']
        stack = row['Stack']
        fuel = row['Fuel']
        action = row['Action']
        block = row['Block']
        local_x = row['Local_x']
        local_y = row['Local_y']

        action = None if pd.isna(action) else action
        block = None if pd.isna(block) else block

        local = {
            "x": int(local_x),
            "y": int(local_y)
        }

        item = {
            "name": name,
            "type": type,
            "level": int(level),
            "stack": int(stack),
            "fuel": int(fuel),
            "action": action,
            "block": block,
            "local": local,
        }

        items.append(item)

    data = {
        "Items": items
    }

    with open('assets\\data\\items_id.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("items_id.json created successfully!")

def Craft():
    df = pd.read_excel('assets\\data\\SheetTable.xlsx', sheet_name='Craft')

    crafts = []

    for _, row in df.iterrows():
        result = row['Result']
        amount = row['Amount']
        size_x = int(row['Size_X'])
        size_y = int(row['Size_Y'])
        Shaped = bool(row['Shaped'])
        craft_0 = str(row['Craft_0'])
        craft_1 = str(row['Craft_1'])
        craft_2 = str(row['Craft_2'])

        size = [size_x, size_y]

        craft_line_0 = craft_0.split(',')
        craft_line_1 = craft_1.split(',')
        craft_line_2 = craft_2.split(',')

        for i in craft_line_0:
            if i == 'null': craft_line_0[craft_line_0.index(i)] = None

        for i in craft_line_1:
            if i == 'null': craft_line_1[craft_line_1.index(i)] = None

        for i in craft_line_2:
            if i == 'null': craft_line_2[craft_line_2.index(i)] = None

        empty = ["nan"]
        mold = []
        if craft_line_0 != empty: mold.append(craft_line_0)
        if craft_line_1 != empty: mold.append(craft_line_1)
        if craft_line_2 != empty: mold.append(craft_line_2)

        craft = {
            "result": result,
            "amount": int(amount),
            "size": size,
            "shaped": Shaped,
            "craft": mold
        }

        crafts.append(craft)

    data = {
        "Crafts": crafts
    }

    with open('assets\\data\\crafts_recipes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("craft_id.json created successfully!")

def Smelt():
    df = pd.read_excel('assets\\data\\SheetTable.xlsx', sheet_name='Smelt')

    recipes = []

    for _, row in df.iterrows():
        result = row['Result']
        item = row['Item']

        recipe = {
            "result": result,
            "item": item
        }

        recipes.append(recipe)
    
    data = {
        "Recipes": recipes
    }

    with open('assets\\data\\smelts_recipes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("smelt_id.json created successfully!")

Blocks()
Items()
Craft()
Smelt()