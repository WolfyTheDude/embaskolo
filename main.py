
import pygame as pg
from player import *
from camera import *
from constants import *
from platform import *

class Game:

    def __init__(self):
        pg.init()  # Initializes Pygame
        self.font = pg.font.SysFont(None, 21)
        self.player = Player()
        self.camera = Camera()

        # Initializes screen
        self.surface = pg.display.set_mode(RES)
        pg.display.set_caption("Embaskolo")

    def debug_text(self, dictionary, hide, *args):
        """
        Blits debug text to surface that is given line by line.

        Arguments:
        1. A dictionary, each key/value pair will be put on a line.
        Can put lists/tuples as dict value, they will simply be comma separated.
        
        2. Boolean, if true this text will not display

        2+. Aything else will be converted to a string and put on its own line
        Lists and tuples will have all of their elements comma separated in the line.
        """

        if hide: return

        # Position of text
        x = 5
        y = 5

        # Takes list or tuple and combines each element with a comma
        combine = lambda x: ", ".join([str(i) for i in x]) \
            if type(x) is list or type(x) is tuple else str(x)

        # Goes through dict
        for key in list(dictionary.keys()):
            line = key + ": " + combine(dictionary[key])
            rendered_text = self.font.render(str.encode(line), True, WHITE, GRAY)
            self.surface.blit(rendered_text, (x, y))
            y += 15 # 18

        # Any other arguments will be converted to string
        # List/tuples will be comma separated
        for item in args:
            line = combine(item)
            rendered_text = self.font.render(str.encode(line), True, WHITE, GRAY)
            self.surface.blit(rendered_text, (x, y))
            y += 15 # 18


    def generate_level(self, size=(50, 50), freq=0.05):
        platforms = []
        for i in range(size[0]):
            for j in range(size[1]):
                width = 32 # + 32 + 64 # sizes[random.randint(0, len(sizes) - 1)] # random.random() * 128
                height = 32 # sizes[random.randint(0, len(sizes) - 1)] # random.random() * 128
                if random.random() < freq:
                    platforms.append(Block(i * 1, j * 32, width, height))
                    for block in platforms:
                        if platforms[-1].pos.colliderect(block.pos):
                            platforms[-1] = Block(i * 32, j * 32, width, height)
        return platforms

    def main(self):
        fps = 30
        clock = pg.time.Clock()

        blocks = self.generate_level()
        blocks.append(Block(0, 32, 32, 32))
        # blocks.append(Block(100, 300, 200))
        # blocks.append(Block(-1 + -500, 400 + 32, 642 + 1000, 2)) # bottom line
        # blocks.append(Block(500, 200))
        # blocks.append(Block(10, 200))
        # blocks.append(Block(50, 50, 200))
        # blocks.append(Block(400, 75, 100))
        # blocks.append(Block(295, 200, 50))
        # blocks.append(Block(640 - 5, 32, 5, 300)) # wall on far right
        # blocks.append(Block(500, 32 + 43, 5, 300 - 32)) # wall on far right counterpart

        # blocks.append(Block(608, 400, up=True))
        # blocks.append(Block(500, 400, 200, moves=True))
        # for i in range(1, 10):
            # blocks.append(Block(i * 32, 200))

        world_size = 50
        block_freq = .05
        hide_debug = False
        # Mainloop
        playing = True
        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False
                key = pg.key.get_pressed()
                if key[pg.K_q]:
                    playing = False
                if key[pg.K_f]:
                    blocks = self.generate_level((world_size, world_size), block_freq)
                if key[pg.K_u]:
                    world_size -= 10
                if key[pg.K_i]:
                    world_size += 10
                if key[pg.K_j]:
                    block_freq -= .05
                if key[pg.K_k]:
                    block_freq += .05
                if key[pg.K_l]:
                    hide_debug = 1 ^ hide_debug

                if key[pg.K_g]:
                    self.camera.zoom = 2
                    for i, block in enumerate(blocks):
                        blocks[i].pos.w *= self.camera.zoom
                        blocks[i].pos.h *= self.camera.zoom
                    self.player.pos.w *= self.camera.zoom
                    self.player.pos.h *= self.camera.zoom
                if key[pg.K_h]:
                    self.camera.zoom = .5
                    for i, block in enumerate(blocks):
                        blocks[i].pos.w *= self.camera.zoom
                        blocks[i].pos.h *= self.camera.zoom
                    self.player.pos.w *= self.camera.zoom
                    self.player.pos.h *= self.camera.zoom

            self.player.update(blocks, self.camera)

            self.surface.fill(WHITE)
            for i, block in enumerate(blocks):
                # blocks[i].draw(self.surface)
                # pg.draw.rect(self.surface, blocks[i].color, blocks[i].pos)
                self.camera.draw_rect(self.surface, blocks[i])
                block.update()

            # pg.draw.line(self.surface, BLACK, (0, 300 + 32), (RES[0], 300 + 32))

            # self.player.draw(self.surface)
            self.camera.draw_rect(self.surface, self.player) # Draw player
            # if self.player.pos.left > int(RES[0] / 2)

            # Have camera follow and center on player
            self.camera.pos.x = (self.player.pos.x - (RES[0] / 2)) + (self.player.pos.w / 2)
            # self.camera.pos.y = (self.player.pos.y - (RES[1] / 2)) - (self.player.pos.h / 2)

            # if (self.camera.pos.bottom - 300 < self.player.pos.y < self.camera.pos.top + 300):
            # If player leaves camera then force camera positon to be at player
            if not self.camera.pos.colliderect(self.player.pos):
                self.camera.pos.y = (self.player.pos.y - (RES[1] / 2)) - (self.player.pos.h / 2)
                self.camera.pos.x = (self.player.pos.x - (RES[0] / 2)) + (self.player.pos.w / 2)

            # If player is lower than 175 pixels from the bottom
            elif self.player.pos.centery > self.camera.pos.bottom - 175:
                self.camera.pos.y += self.player.yv + 1

            # If player is highter than 175 pixels from the top
            elif self.player.pos.centery < self.camera.pos.top + 175:
                if self.player.yv < -15:
                    self.camera.pos.y += self.player.yv * .75
                else:
                    self.camera.pos.y += self.player.yv - 1
                # self.camera.pos.y -= 3
                # self.camera.pos.y = (self.player.pos.y - (RES[1] / 2)) - (self.player.pos.h / 2)
                # self.camera.pos.y += (self.player.yv + -1 if self.player.yv > 0 else -1) # * 1.1

            # self.debug_text({"Wall time": self.player.wall_time,
                             # "On Ground": self.player.on_ground,
                             # "POS": self.player.pos,
                             # "PPOS": self.player.pposes,
                             # "Collide Time": self.player.collide_time,
                             # "Y Speed": self.player.yv})
            # self.debug_text({"Player": [self.player.pos.x, self.player.pos.y],
                             # "Camera": [self.camera.pos.x, self.camera.pos.y]})
            self.debug_text({"World Size (U & I to change)": world_size,
                             "Platform Frequency (J & K to change, higher means more platforms)": "%0.3f" % block_freq},
                            hide_debug,
                            ["R to reset position", "F to generate new level with the given world size/platform frequency"],
                            ["Z & X change size", "G & H experimental", "L to toggle this text"])
            pg.display.flip()
            clock.tick(fps)

game = Game()
game.main()
