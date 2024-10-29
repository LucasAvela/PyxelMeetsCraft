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

class WorldGen():
    def WorldGenerations(x, y):
        print(x)
        
class Renderer:
    def RenderBlocks():
        for i, v in World.items():
            block = next(block for block in block_data['Blocks'] if block['name'] == v["Block"])
    
            block_x = block['local']['x']
            block_y = block['local']['y']
            block_w = block['size']['w']
            block_h = block['size']['h']

            pyxel.blt(v["Pos"][0], v["Pos"][1], 0, block_x, block_y, block_w, block_h)

class App:
    def StorageImages():
        pyxel.images[0].load(0, 0, '.\\assets\\sprites\\Sprite_sheet_0.png')
        
    def __init__(self):
        pyxel.init(screen_size[0], screen_size[1], title=window_title, display_scale=display_scale, fps=frames_per_second)
        App.StorageImages()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            World[len(World)] = {"Pos": [pyxel.mouse_x - (pyxel.mouse_x % 8) + camera_diff[0], pyxel.mouse_y - (pyxel.mouse_y % 8) + camera_diff[1]], "Block": "Grass_block"}
            
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            World[len(World)] = {"Pos": [pyxel.mouse_x - (pyxel.mouse_x % 8) + camera_diff[0], pyxel.mouse_y - (pyxel.mouse_y % 8) + camera_diff[1]], "Block": "Stone_block"}

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

        # Fazendo a câmera seguir o jogador
        pyxel.camera(camera_diff[0], camera_diff[1])

    def draw(self):
        pyxel.cls(0)

        Renderer.RenderBlocks()
            
        Inputs.MousePosition()
        pyxel.camera(0, 0)
        Inputs.ShowMouseCoordinates()
        
App()
