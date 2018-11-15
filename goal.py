# 11.29

from constants import *
import pygame as pg

class Goal:
    def __init__(self, x=90, y=90, width=16, height=16):
        self.color = BLACK
        self.pos = pg.Rect(x, y, width, height)
        self.hit = False

    def update(self, stopwatch, player):
        if not self.hit and self.pos.colliderect(player.pos):
            self.hit = True
            stopwatch.stop()

    def reset(self):
        self.hit = False
