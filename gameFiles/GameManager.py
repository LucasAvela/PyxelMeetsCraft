import random
import numpy

import gameFiles.AppManager as AppManager

class Properties:
    def InitPlayerInventory(dictionary):
        for i in range(AppManager.GameInfo.InvetorySize):
            dictionary[i] = {
                'Item': None, 
                'Amount': 0
            }

class ChunkCalc:
    def GetGenerationChunkArea(camera_x, camera_y):
        start_x = camera_x // AppManager.GameInfo.BlockSize
        end_x = start_x + (AppManager.GameInfo.ViewDistance) + 2
        start_y = camera_y // AppManager.GameInfo.BlockSize + 4
        end_y = start_y + (AppManager.GameInfo.ViewDistance) + 4
 
        return start_x, end_x, start_y, end_y
    
class PerlinNoise:
    permutation = []

    def init_seed(seed=None):
        if seed is None: seed = random.randint(0, 1000000)
        random.seed(seed)
        numpy.random.seed(seed)
        p = numpy.arange(256, dtype=int)
        numpy.random.shuffle(p)
        PerlinNoise.permutation = numpy.stack([p, p]).flatten()
    
    def fade(t):
        return t * t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(a, b, t):
        return a + t * (b - a)
    
    def gradient(h, x, y):
        vectors = numpy.array([[1,1], [-1,1], [1,-1], [-1,-1], [1,0], [-1,0], [0,1], [0,-1]])
        g = vectors[h % 8]
        return g[0] * x + g[1] * y

    def noise(x, y):
        p = PerlinNoise.permutation
        
        x0, y0 = int(numpy.floor(x)), int(numpy.floor(y))
        x1, y1 = x0 + 1, y0 + 1
        
        def hash(x, y):
            return p[(p[x % 256] + y) % 256]
        
        g00 = PerlinNoise.gradient(hash(x0, y0), x - x0, y - y0)
        g10 = PerlinNoise.gradient(hash(x1, y0), x - x1, y - y0)
        g01 = PerlinNoise.gradient(hash(x0, y1), x - x0, y - y1)
        g11 = PerlinNoise.gradient(hash(x1, y1), x - x1, y - y1)
        
        u, v = PerlinNoise.fade(x - x0), PerlinNoise.fade(y - y0)
        
        return PerlinNoise.lerp(PerlinNoise.lerp(g00, g10, u), PerlinNoise.lerp(g01, g11, u), v)