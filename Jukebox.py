import pyxel

class App:
    def __init__(self):
        pyxel.init(
            width  = 256, 
            height = 256, 
            title  = "Jukebox",
            fps    = 60
        )

        with open("assets/music/2_ariamath.txt", "r") as musicFile:
            lines = musicFile.readlines()

        n0 = lines[1]
        n1 = lines[2]
        n2 = lines[3]
        n3 = lines[4]

        pyxel.sounds[0].set(n0, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[1].set(n1, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[2].set(n2, tones='t', volumes='4', effects='n', speed=45)
        pyxel.sounds[3].set(n3, tones='t', volumes='4', effects='n', speed=45)
        pyxel.musics[1].set([0], [1], [2], [3])
        
        pyxel.playm(1, loop=False)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

App()