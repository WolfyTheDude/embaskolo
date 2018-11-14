
import pygame as pg
from constants import *

class Camera:
    def __init__(self):
        self.pos = pg.Rect(0, 0, RES[0], RES[1])
        self.zoom = 1
        self.freeze = False

    def update(self, player):
            # Have camera follow and center on player
            self.pos.x = (player.pos.x - (RES[0] / 2)) + (player.pos.w / 2)
            # self.pos.y = (player.pos.y - (RES[1] / 2)) - (player.pos.h / 2)

            # if (self.pos.bottom - 300 < player.pos.y < self.pos.top + 300):
            # If player leaves camera then force camera positon to be at player
            if not self.pos.colliderect(player.pos):
                self.pos.y = (player.pos.y - (RES[1] / 2)) - (player.pos.h / 2)
                self.pos.x = (player.pos.x - (RES[0] / 2)) + (player.pos.w / 2)

            # If player is lower than 36.4% pixels from the bottom
            elif player.pos.centery > self.pos.bottom - RES[1] * .364: # 175
                self.pos.y += player.yv + 1

            # If player is highter than 36.4% pixels from the top
            elif player.pos.centery < self.pos.top + RES[1] * .364: # 175
                if player.yv < -15:
                    self.pos.y += player.yv * .75
                else:
                    self.pos.y += player.yv - 1
                # self.pos.y = (player.pos.y - (RES[1] / 2)) - (player.pos.h / 2)
                # self.pos.y += (player.yv + -1 if player.yv > 0 else -1) # * 1.1

    def draw(self, surface, obj):
        surface.blit(obj.sprite)
        surface.blit(pg.Rect(obj.pos.x + self.pos.x,
                             obj.pos.y + self.pos.y,
                             obj.width, obj.height))

    def apply_offset(self, rect):
                return pg.Rect(
                    rect.x - self.pos.x, rect.y - self.pos.y,
                    rect.width, rect.height)

    def draw_rect(self, surface, color, rect):
        """Draw RECT on SURFACE"""
        if self.pos.colliderect(rect):
            pg.draw.rect(surface, color, self.apply_offset(rect))
            # pg.draw.rect(surface, color,
                        # pg.Rect(rect.x - self.pos.x,
                        # rect.y - self.pos.y,
                        # rect.width,
                        # rect.height))

    def draw_line(self, surface, start_pos, end_pos):
        # if self.pos.colliderect(obj.pos):
        pg.draw.line(surface, BLACK, start_pos, end_pos)
        # pg.draw.line(surface, BLACK, (self.pos.x, self.pos.y),
                    # (self.pos.x + 640, self.pos.y + 480))
        # pg.draw.line(surface, BLACK, (self.pos.midleft[0], self.pos.midleft[1]),
                    # (self.pos.midright[0], self.pos.midright[1]))
