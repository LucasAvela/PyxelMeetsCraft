import random

World = {}
Entities = {}
MaxLayerValue = 0

def GenerateWorldLayers(blocksByLayer, optfine):
    for i in range(0, MaxLayerValue):
        WorldGenLayer(i, blocksByLayer, optfine)

def GetRandomBlock(layer, blocksByLayer):
    blocks = []
    weights = []

    for block, probability in blocksByLayer[layer].items():
        blocks.append(block)
        weights.append(probability)
    
    choice = random.choices(blocks, weights)[0]
    return choice

def WorldGenLayer(layer, blocksByLayer, optfine):
    global World

    start_x, end_x, start_y, end_y = optfine

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if (x, y, layer) not in World:
                blockSelected = GetRandomBlock(layer, blocksByLayer)
                World[(x, y, layer)] = {"Block": blockSelected}

def SetMaxLayerValue(value):
    global MaxLayerValue
    MaxLayerValue = value