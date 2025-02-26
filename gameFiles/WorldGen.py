import random
import gameFiles.Data as Data

World = {}
Entities = {}

def GenerateWorldLayers(optfine):
    for i in range(Data.layers_quantity):
        WorldGenLayer(i, optfine)

def GetRandomBlock(layer):
    blocks = []
    weights = []

    for block, probability in Data.blocks_by_layer[layer].items():
        blocks.append(block)
        weights.append(probability)
    
    choice = random.choices(blocks, weights)[0]
    return choice

def WorldGenLayer(layer, optfine):
    global World

    start_x, end_x, start_y, end_y = optfine

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            key = (x, y, layer)
            if key not in World:
                blockSelected = GetRandomBlock(layer)
                block = Data.block_data[blockSelected]
                World[key] = {"Block": blockSelected, "Solid": block['Solid']}
