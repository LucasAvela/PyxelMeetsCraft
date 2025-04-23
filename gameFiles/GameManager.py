import random
import numpy as np

class AppInfo:
    ScreenWidth = 256
    ScreenHeight = 256
    WindowTitle = "Pyxel Meets Craft"
    Fps = 60
    Tps = 3

class GameInfo:
    BlockSize = 8
    BlockHeight = 4
    ViewDistance = 32
    MaxLayer = 16

class Camera:
    Position = [0, 0]

    def GetCameraPosition(offset):
        Camera.position = offset

class ChunkCalc:
    def GetGenerationChunkArea():
        start_x = Camera.Position[0] // GameInfo.BlockSize
        end_x = start_x + (GameInfo.ViewDistance) + 1
        start_y = Camera.Position[1] // GameInfo.BlockSize
        end_y = start_y + (GameInfo.ViewDistance) + GameInfo.MaxLayer
 
        return start_x, end_x, start_y, end_y

class PerlinNoise:
    permutation = []

    def init_seed(seed=None):
        if seed is None: seed = random.randint(0, 1000000)
        random.seed(seed)
        np.random.seed(seed)
        p = np.arange(256, dtype=int)
        np.random.shuffle(p)
        PerlinNoise.permutation = np.stack([p, p]).flatten()
    
    def fade(t):
        return t * t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(a, b, t):
        return a + t * (b - a)
    
    def gradient(h, x, y):
        vectors = np.array([[1,1], [-1,1], [1,-1], [-1,-1], [1,0], [-1,0], [0,1], [0,-1]])
        g = vectors[h % 8]
        return g[0] * x + g[1] * y

    def noise(x, y):
        p = PerlinNoise.permutation
        
        x0, y0 = int(np.floor(x)), int(np.floor(y))
        x1, y1 = x0 + 1, y0 + 1
        
        def hash(x, y):
            return p[(p[x % 256] + y) % 256]
        
        g00 = PerlinNoise.gradient(hash(x0, y0), x - x0, y - y0)
        g10 = PerlinNoise.gradient(hash(x1, y0), x - x1, y - y0)
        g01 = PerlinNoise.gradient(hash(x0, y1), x - x0, y - y1)
        g11 = PerlinNoise.gradient(hash(x1, y1), x - x1, y - y1)
        
        u, v = PerlinNoise.fade(x - x0), PerlinNoise.fade(y - y0)
        
        return PerlinNoise.lerp(PerlinNoise.lerp(g00, g10, u), PerlinNoise.lerp(g01, g11, u), v)