
from platform import *
from goal import *
import pygame as pg

class Level:
    def __init__(self, type="Goal"):
        self.goal = Goal()
        self.platforms = []
        self.player_start_pos = pg.Rect(0, 0, 32, 32)

    def __getitem__(self, index):
        return self.platforms[index]
    
    def exit(self):
        self.platforms = []

    def generate_level(self, size=(50, 50), freq=0.05):
        self.platforms = []
        for i in range(size[0]):
            for j in range(size[1]):
                width = 32 # + 32 + 64 # sizes[random.randint(0, len(sizes) - 1)] # random.random() * 128
                height = 32 # sizes[random.randint(0, len(sizes) - 1)] # random.random() * 128
                if random.random() < freq:
                    self.platforms.append(Block(i * 1, j * 32, width, height))
                    for block in self.platforms:
                        if self.platforms[-1].pos.colliderect(block.pos):
                            self.platforms[-1] = Block(i * 32, j * 32, width, height)

    def read_level_basic(self, player, name):
        self.platforms = []
        # Width and height for platforms/blocks
        width = 32
        height = 32
        if name == "original1":
            # First level ever
            self.platforms = [Block(i * 32, 200) for i in range(1, 10)]
        if name == "original2":
            # Second level ever
            self.platforms.append(Block(100, 300, 200))
            self.platforms.append(Block(-1 + -500, 400 + 32, 642 + 1000, 2)) # bottom line
            self.platforms.append(Block(500, 200))
            self.platforms.append(Block(10, 200))
            self.platforms.append(Block(50, 50, 200))
            self.platforms.append(Block(400, 75, 100))
            self.platforms.append(Block(295, 200, 50))
            self.platforms.append(Block(640 - 5, 32, 5, 300)) # wall on far right
            self.platforms.append(Block(500, 32 + 43, 5, 300 - 32)) # wall on far right counterpart

            self.platforms.append(Block(608, 400, up=True))
            self.platforms.append(Block(500, 400, 200, moves=True))
            return self.platforms

        try:
            self.platforms_file = open(name, "r")
        except FileNotFoundError:
            return

        up = True
        color = 50
        for i, line in enumerate(self.platforms_file):
            for j, char in enumerate(line):
                if char == "b": # B for block
                    self.platforms.append(Block(j * width, i * height, width, height, color))
                elif char == "g":
                    self.goal = Goal((j * width) + width / 4,
                                      (i * height) + height / 4,
                                      width / 2, height / 2)
                elif char == "p": # P for platform
                    self.player_start_pos = pg.Rect(j * width, i * height, 32, 32)
                    # player.pos.x = j * width
                    # player.pos.y = i * height
                    # self.platforms.append(Block(j * width, i * height, width * 3, height))

            if color > 200:
                up = False
            if color < 50:
                up = True
            color += 10 if up else -10

