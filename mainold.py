import pyxel
import json

# Config Section
screen_size = [128, 128]
window_title = 'PyxelCraft'
display_scale = 7
frames_per_second = 60

# Camera
camera_diff = [0, 0]

# World Gen
World = {}

# Blocks
SelectedBlock = 0
Blocks = ["Grass_block", "Dirt_block", "Stone_block", "Bedrock_block", "Coal_Ore_block", "Iron_Ore_block", "Gold_Ore_block", "Diamond_Ore_block", "Emerald_Ore_block",
          "Wood_Log_block_Bottom", "Wood_Log_block_Top", "Wood_Plank_block", "Leaves_block", "Chest_block", "Furnace_block", "Bed_block_Top", "Bed_block_Bottom"]

# Carregar dados do arquivo JSON
with open('blocks_id.json') as f:
    block_data = json.load(f)

class Inputs:
    def MousePosition():
        mouse_x = pyxel.mouse_x + camera_diff[0]
        mouse_y = pyxel.mouse_y + camera_diff[1]
        pyxel.rect(mouse_x, mouse_y, 1, 1, 7)
        
    def ShowMouseCoordinates():
        pyxel.text(5, 5, f"Mouse: {pyxel.mouse_x + camera_diff[0]}, {pyxel.mouse_y + camera_diff[1]}", 7)
        pyxel.text(5, 13, Blocks[SelectedBlock], 7)

class WorldGen:
    @staticmethod
    def initialize_grass_blocks():
        # Preenche a tela inicial com blocos de grama
        for x in range(0, screen_size[0], 8):  # Cada bloco assume uma largura de 8 pixels
            for y in range(0, screen_size[1], 8):  # Cada bloco assume uma altura de 8 pixels
                World[(x, y)] = {
                    "Pos": [x, y],
                    "Block": "Grass_block"
                }

    @staticmethod
    def generate_nearby_grass_blocks():
        # Definir a área ao redor da câmera para gerar blocos adicionais
        start_x = (camera_diff[0] // 8 - screen_size[0] // 8) * 8
        end_x = (camera_diff[0] // 8 + screen_size[0] // 8) * 8
        start_y = (camera_diff[1] // 8 - screen_size[1] // 8) * 8
        end_y = (camera_diff[1] // 8 + screen_size[1] // 8) * 8

        for x in range(start_x, end_x + 1, 8):
            for y in range(start_y, end_y + 1, 8):
                if (x, y) not in World:
                    World[(x, y)] = {
                        "Pos": [x, y],
                        "Block": "Grass_block"
                    }

class Renderer:
    def RenderBlocks():
        for v in World.values():
            block = next(block for block in block_data['Blocks'] if block['name'] == v["Block"])
    
            block_x = block['local']['x']
            block_y = block['local']['y']
            block_w = block['size']['w']
            block_h = block['size']['h']

            pyxel.blt(v["Pos"][0], v["Pos"][1], 0, block_x, block_y, block_w, block_h, 2)

class App:
    def StorageImages():
        pyxel.images[0].load(0, 0, '.\\assets\\sprites\\Sprite_sheet_0.png')
        
    def __init__(self):
        pyxel.init(screen_size[0], screen_size[1], title=window_title, display_scale=display_scale, fps=frames_per_second)
        App.StorageImages()

        # Gera blocos de grama na tela inicial
        WorldGen.initialize_grass_blocks()

        pyxel.run(self.update, self.draw)

    def update(self):
        global SelectedBlock
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            World[(pyxel.mouse_x + camera_diff[0]) // 8 * 8, (pyxel.mouse_y + camera_diff[1]) // 8 * 8] = {
                "Pos": [
                    (pyxel.mouse_x + camera_diff[0]) // 8 * 8,
                    (pyxel.mouse_y + camera_diff[1]) // 8 * 8
                ],
                "Block": Blocks[SelectedBlock]
            }

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            SelectedBlock = (SelectedBlock + 1) % len(Blocks)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_MIDDLE):
            print(World)

        # Movendo o jogador com as teclas de seta
        if pyxel.btn(pyxel.KEY_LEFT):
            camera_diff[0] -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            camera_diff[0] += 1
        if pyxel.btn(pyxel.KEY_UP):
            camera_diff[1] -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            camera_diff[1] += 1

        # Gerar blocos de grama nas áreas próximas ao jogador
        WorldGen.generate_nearby_grass_blocks()

        # Fazendo a câmera seguir o jogador
        pyxel.camera(camera_diff[0], camera_diff[1])

    def draw(self):
        pyxel.cls(0)

        Renderer.RenderBlocks()
            
        Inputs.MousePosition()
        pyxel.camera(0, 0)
        Inputs.ShowMouseCoordinates()
        
App()
