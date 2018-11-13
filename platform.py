
import pygame as pg
import random

class Block:
    def __init__(self, x, y, length=32, height=32, moves=False, up=False):
        # self.sprite = pg.image.load("block.png")
        self.shade = random.randint(50, 200)
        self.shade_up = True
        self.color = (self.shade, self.shade, self.shade)
        # self.x = x
        # self.y = y
        # self.pos = pg.rect.Rect(x, y + random.randint(1, 50), length, height)  # self.sprite.get_rect()
        self.pos = pg.rect.Rect(x, y, length, height)  # self.sprite.get_rect()
        self.xv = 0
        self.moves = moves
        # self.moves = True
        self.up = up
        self.yv = 0

    def update(self):
        # Change shading
        if self.shade >= 180:
            self.shade_up = False
        if self.shade <= 70:
            self.shade_up = True
        rand_int = 1 # random.randint(1, 10)
        self.shade += rand_int if self.shade_up else -rand_int
        self.color = (self.shade, self.shade, self.shade)

        if self.up:
            if self.pos.top >= 400:
                self.yv = -5
            if self.pos.bottom < 50:
                self.yv = 5
        self.pos.y += self.yv
        if self.moves:
            if self.pos.x > 400:
                self.xv = -5
            if self.pos.x < 50:
                self.xv = 5
            self.pos.x += self.xv

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.pos)
        # surface.blit(self.sprite, (self.x, self.y))
