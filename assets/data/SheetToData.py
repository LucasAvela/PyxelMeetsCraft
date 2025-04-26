import pandas as pd
import json

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