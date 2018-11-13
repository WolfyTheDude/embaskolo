
import pygame as pg
from constants import *

class Camera:
    def __init__(self):
        self.pos = pg.Rect(0, 0, RES[0], RES[1])
        self.zoom = 1

    def draw(self, surface, obj):
        surface.blit(pg.Rect(obj.pos.x + self.pos.x,
                             obj.pos.y + self.pos.y,
                             obj.width, obj.height))

    def draw_rect(self, surface, obj):
        if self.pos.colliderect(obj.pos):
            pg.draw.rect(surface, obj.color,
                        pg.Rect(obj.pos.x - self.pos.x,
                        obj.pos.y - self.pos.y,
                        obj.pos.width,
                        obj.pos.height))
        

    def draw_line(self, surface, start_pos, end_pos):
        # if self.pos.colliderect(obj.pos):
        pg.draw.line(surface, BLACK, start_pos, end_pos)
        # pg.draw.line(surface, BLACK, (self.pos.x, self.pos.y),
                    # (self.pos.x + 640, self.pos.y + 480))
        # pg.draw.line(surface, BLACK, (self.pos.midleft[0], self.pos.midleft[1]),
                    # (self.pos.midright[0], self.pos.midright[1]))
