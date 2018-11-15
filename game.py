
import pygame as pg
from player import *
from camera import *
from constants import *
from platform import *
from stopwatch import *
from goal import *
from level import *
from menu import Menu

class Game:

    def __init__(self):
        pg.init()  # Initializes Pygame
        self.font = pg.font.SysFont(None, 21)
        self.player = Player()
        self.camera = Camera()
        self.stopwatch = StopWatch()
        self.level = Level()
        self.playing = True
        self.main_menu = Menu()

        # Initializes screen
        self.surface = pg.display.set_mode(RES)
        pg.display.set_caption("Embaskolo")

    def exit_to_main(self):
        self.level.exit()

        self.main_menu.open()

    def debug_text(self, dictionary, hide=False, *args):
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

    def events(self):
        world_size = 50
        block_freq = .05
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            key = pg.key.get_pressed()
            if key[pg.K_q]:
                self.playing = False
            if key[pg.K_f]:
                self.level.generate_level((world_size, world_size), block_freq)
            if key[pg.K_u]:
                world_size -= 10
            if key[pg.K_i]:
                world_size += 10
            if key[pg.K_j]:
                block_freq -= .05
            if key[pg.K_k]:
                block_freq += .05
            if key[pg.K_l]:
                hide_debug ^= 1
            if key[pg.K_p]:
                dark_mode ^= 1
            if key[pg.K_r]:
                self.stopwatch.start()
                self.level.goal.reset()
                self.player.pos.x = self.level.player_start_pos.x
                self.player.pos.y = self.level.player_start_pos.y
                self.player.xv = 0
                self.player.yv = 0

            if key[pg.K_1]:
                self.level.read_level_basic(self.player, "original1")
                self.player.pos.x = self.level.player_start_pos.x
                self.player.pos.y = self.level.player_start_pos.y
            if key[pg.K_2]:
                self.level.read_level_basic(self.player, "original2")
                self.player.pos.x = self.level.player_start_pos.x
                self.player.pos.y = self.level.player_start_pos.y
            if key[pg.K_3]:
                self.level.read_level_basic(self.player, "level1")
                self.player.pos.x = self.level.player_start_pos.x
                self.player.pos.y = self.level.player_start_pos.y
            if key[pg.K_4]:
                self.level.read_level_basic(self.player, "level2")
                self.player.pos.x = self.level.player_start_pos.x
                self.player.pos.y = self.level.player_start_pos.y
            # if key[pg.K_y]:

            # if key[pg.K_g]:
                # self.camera.zoom = 2
                # for i, block in enumerate(self.level):
                    # self.level[i].pos.w *= self.camera.zoom
                    # self.level[i].pos.h *= self.camera.zoom
                # self.player.pos.w *= self.camera.zoom
                # self.player.pos.h *= self.camera.zoom
            # if key[pg.K_h]:
                # self.camera.zoom = .5
                # for i, block in enumerate(self.level):
                    # self.level[i].pos.w *= self.camera.zoom
                    # self.level[i].pos.h *= self.camera.zoom
                # self.player.pos.w *= self.camera.zoom
                # self.player.pos.h *= self.camera.zoom

    def main(self):
        clock = pg.time.Clock()
        light = pg.Rect(0, 0, 256, 256)
        dark_mode = False

        # self.level = self.generate_level()
        # self.level = self.level.read_level_basic("level1")
        # self.level.append(Block(0, 32, 32, 32))
        self.level.generate_level()

        hide_debug = False
        # Mainloop
        while self.playing:
            self.events()
            self.player.update(self.level, self.camera)
            light.centerx = self.player.pos.centerx
            light.centery = self.player.pos.centery

            if dark_mode:
                self.surface.fill(BLACK)
            else:
                self.surface.fill(WHITE)
            for i, block in enumerate(self.level):
                # self.level[i].draw(self.surface)
                # pg.draw.rect(self.surface, self.level[i].color, self.level[i].pos)
                if dark_mode:
                    if block.pos.colliderect(light):
                        self.camera.draw_rect(self.surface, self.level[i].color, self.level[i].pos)
                else:
                    self.camera.draw_rect(self.surface, self.level[i].color, self.level[i].pos)
                block.update()
            self.camera.draw_rect(self.surface, self.level.goal.color, self.level.goal.pos)
            self.level.goal.update(self.stopwatch, self.player)

            # pg.draw.line(self.surface, BLACK, (0, 300 + 32), (RES[0], 300 + 32))
            # self.camera.draw_line(self.surface,
                                  # (RES[0] * .564, 50), # RES[1] * 1.364),
                                  # (RES[0] / 2, RES[1] / 2))
                                  # (RES[0] * 1.564, RES[1] * .364))

            # self.player.draw(self.surface)
            self.camera.draw_rect(self.surface, self.player.color, self.player.pos) # Draw player
            self.camera.update(self.player)

            self.debug_text({"Timer": self.stopwatch.get_time()})
            # self.debug_text({"World Size (U & I to change)": world_size,
                             # "Platform Frequency (J & K to change, higher means more platforms)": "%0.3f" % block_freq},
                            # hide_debug,
                            # ["R to reset position", "F to generate new level with the given world size/platform frequency"],
                            # ["Z & X change size", "G & H experimental", "L to toggle this text"])
            pg.display.flip()
            clock.tick(FPS)

game = Game()
game.main()
