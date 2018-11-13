
from constants import *
import pygame as pg
import random
import os

class Player():
    def __init__(self): # , sprite):
        # self.sprite = sprite
        self.color = (100, 100, 200)
        self.air_time = 0
        self.wall_time = 0
        self.pos = pg.rect.Rect(0, 0, 32, 32)
        self.ppos = pg.rect.Rect(0, 0, 32, 32)
        self.pposes = [pg.rect.Rect(0, 0, 32, 32)]
        self.yv = 0
        self.xv = 0
        self.on_ground = False
        self.on_left_wall = False
        self.on_right_wall = False
        self.can_jump = False
        self.collide_time = 0

    def update(self, obj, cam):

        # percent_y = (self.pos.center[1] / RES[1])
        # col = percent_y * 255
        # if col < 0:
            # col = 0
        # self.color = (col, col, col)

        key = pg.key.get_pressed()

        if key[pg.K_w]:
            if self.on_ground:
                self.yv -= 3.5
            else:
                self.yv -= 1.5
        if key[pg.K_a] or key[pg.K_LEFT]:
            if self.on_ground:
                self.xv -= GROUND_SPEED
            else:
                self.xv -= AIR_SPEED
        if key[pg.K_s]:
            if self.on_ground:
                self.yv += 2.5
            else:
                self.yv += 0.5
        if key[pg.K_d] or key[pg.K_RIGHT]:
            if self.on_ground:
                self.xv += GROUND_SPEED
            else:
                self.xv += AIR_SPEED
        if key[pg.K_r]:
            self.pos.y = 0
            self.pos.x = 0 # 200
            self.xv = 0
            self.yv = 0
        if key[pg.K_t]:
            self.pos.y = 300
            self.pos.x = 200
            self.xv = 0
            self.yv = 0
        if key[pg.K_e]:
            self.xv = 40
            self.yv = -20
        if key[pg.K_z]:
            # self.xv = -.1
            self.pos.w += 1
        if key[pg.K_x]:
            # self.xv = .1
            self.pos.w -= 1


        # if key[pg.K_SPACE] and not self.in_air(obj):
        if key[pg.K_SPACE] or key[pg.K_UP]:
            # if self.pos.y == self.ppos.y:
            if self.on_ground and self.can_jump:
                jump = (abs(self.xv) - abs(self.xv) * 3) * .2
                self.yv = jump - 30  # * (jump / 10)
                # self.yv -= 29
            elif self.wall_time > 5:
                if self.on_left_wall and not self.on_ground:
                    self.yv = -20
                    self.xv = 30
                elif self.on_right_wall and not self.on_ground:
                    self.yv = -20
                    self.xv = -30

        # Previous position
        self.pposes = [pg.Rect(self.pos.x, self.pos.y, self.pos.w, self.pos.h)]
        self.ppos.x = self.pos.x
        self.ppos.y = self.pos.y

        # Gravity
        self.yv += GRAVITATIONAL_PULL #.6 # abs(self.yv + 1 * 1.05) # gravity # FIX

        # Make velocity 0 if greater than -1 and less than 1
        if -1 < self.xv < 1: self.xv = 0 
        if -1 < self.yv < 1: self.yv = 0

        # Movement
        # if not (self.pos.x > -1 and self.pos.x < 0):
        # if not -1 < self.pos.x < 0:
        self.pos.x += self.xv
        self.pos.y += self.yv

        # Friction
        if self.on_ground:
            self.xv *= GROUND_FRICTION
            self.yv *= GROUND_FRICTION
        else:
            self.xv *= AIR_FRICTION
            self.yv *= AIR_FRICTION

        # Maximum speed
        if self.xv > MAX_X_VELOCITY: self.xv = MAX_X_VELOCITY
        if self.xv < -MAX_X_VELOCITY: self.xv = -MAX_X_VELOCITY
        if self.yv > MAX_Y_VELOCITY: self.yv = MAX_Y_VELOCITY

        # If player goes off screen, they will appear on other side
        # if self.pos.left > RES[0]: self.pos.right = 0
        # if self.pos.right < 0: self.pos.left = RES[0]

        # if self.pos.y == self.ppos.y: self.yv = 0 # Del?

        self.on_right_wall = False
        self.on_left_wall = False
        self.on_ground = False

        self.check_collision(obj, cam)

        if self.on_ground:
            self.can_jump = True

        if not self.on_ground:
            self.air_time += 1
        else:
            self.air_time = 0

        if self.on_right_wall or self.on_left_wall and \
           self.air_time > 5 and not self.on_ground:
            self.wall_time += 1
        else:
            self.wall_time = 0

    def check_collision(self, obj, cam):
        has_collided = False
        for objects in obj:
            xlt = self.ppos.bottomright[0] < objects.pos.topleft[0]
            ylt = self.ppos.bottomright[1] < objects.pos.topleft[1]
            tl_up = True if xlt and ylt else False
            if cam.pos.colliderect(objects.pos):
                if self.pos.colliderect(objects.pos):
                    has_collided = True
                    self.pposes.append(pg.Rect(self.pos.x, self.pos.y, self.pos.w, self.pos.h))
                    if len(self.pposes) > 9:
                        self.pos.x = self.pposes[0].x
                        self.pos.y = self.pposes[0].y
                        self.pposes = [self.pposes[0]]


                    # if player came from bottom left
                    if self.pos.topright[0] == objects.pos.bottomleft[0] and \
                    self.pos.topright[1] == objects.pos.bottomleft[1]:
                        self.pos.y -= self.pos.top - objects.pos.bottom
                        self.pos.x += 1

                    # if player came from bottom right
                    elif self.pos.topleft[0] == objects.pos.bottomright[0] and \
                    self.pos.topleft[1] == objects.pos.bottomright[1]:
                        self.pos.y -= self.pos.top - objects.pos.bottom
                        self.pos.x -= 1

                    # if player came from top right
                    elif self.pos.bottomleft[0] == objects.pos.topright[0] and \
                    self.pos.bottomleft[1] == objects.pos.topright[1]:
                        # self.pos.y -= self.pos.top - objects.pos.bottom
                        self.pos.x -= 1

                    # if player came from top left
                    elif self.pos.bottomright[0] == objects.pos.topleft[0] and \
                    self.pos.bottomright[1] == objects.pos.topleft[1]:
                        # self.pos.y -= self.pos.top - objects.pos.bottom
                        self.pos.x += 1

                    elif self.ppos.bottom <= objects.pos.top - objects.yv: # if player came from above
                    # if self.yv > 0:
                        # self.pos.y -= self.pos.bottom - objects.pos.top
                        # if objects.yv != 0:

                        # objects.color = BLUE
                        if objects.yv < 0:
                            self.pos.bottom = objects.pos.top
                        elif objects.yv > 0:
                            self.pos.bottom = objects.pos.top
                            # self.pos.y += objects.yv
                            self.yv += objects.yv
                        elif objects.yv == 0:
                            self.pos.bottom = objects.pos.top
                            self.yv = 0

                        self.on_ground = True
                        # elif objects.moves:
                            # self.pos.x += objects.xv # objects.xv # + ((objects.xv * .99) / .99) # + 5

                    elif self.ppos.top >= objects.pos.bottom: # if player came from below
                    # elif self.yv < 0:
                        # self.pos.y -= self.pos.top - objects.pos.bottom
                        self.pos.top = objects.pos.bottom
                        self.yv = 0
                        # Bumping your head at a high speed will slow you down
                        if self.xv > 10:
                            self.xv /= 2
                        self.can_jump = False

                    elif self.ppos.right <= objects.pos.left: # if player came from left
                    # elif self.xv > 0:
                        # self.pos.x -= self.pos.right - objects.pos.left
                        self.pos.right = objects.pos.left
                        self.xv = 0
                        self.on_right_wall = True
                        # if objects.moves:

                    elif self.ppos.left >= objects.pos.right: # if player came from right
                    # elif self.xv < 0:
                        # self.pos.x -= self.pos.left - objects.pos.right
                        self.pos.left = objects.pos.right
                        self.xv = 0
                        self.on_left_wall = True
                        # if objects.moves:
                            # self.xv = objects.xv
                    # if abs(objects.xv) > abs(self.xv):
                    # if -3 < self.xv < 3:
                    # if self.xv == 0:
                        # self.pos.x += objects.xv * .50
                        # self.xv += objects.xv

                    # if objects.xv != 0:
                        # self.pos.x += objects.xv

        if has_collided:
            self.collide_time += 1
        else:
            self.collide_time = 0

            """
            while self.pos.colliderect(objects.pos):
                if self.ppos.bottom <= objects.pos.top: # if player came from above
                    self.pos.y -= 1
                    self.yv = 0
                if self.ppos.top >= objects.pos.bottom: # if player came from below
                    self.pos.y += 1
                    self.yv = 0
                if self.ppos.right <= objects.pos.left: # if player came from left
                    self.pos.x -= 1
                    self.xv = 0
                if self.ppos.left >= objects.pos.right: # if plaxer came from right
                    self.pos.x += 1
                    self.xv = 0
            """

    def draw(self, surface):
        # Shadow
        # pg.draw.rect(surface, DGRAY, pg.Rect(self.pos.x - 3,
                                             # self.pos.y + 3,
                                             # self.pos.width,
                                             # self.pos.height))
        pg.draw.rect(surface, self.color, self.pos)
        # surface.blit(self.sprite, self.pos)

    def closer(*args):
        for check in args[1:]:
            for check2 in args[-1:]:
                if check:
                    pass

    def is_on_ground(self, obj):
        for i in obj:
            if self.pos.colliderect(i):
                if self.pos.bottom >= i.pos.top:
                    return True
        return False

    def in_air(self, obj):
        ray = pg.Rect(self.pos.x, self.pos.y, 32, 32)
        # ray = self.pos
        ray.y += 1

        for i in obj:
            if ray.colliderect(i.pos):
                return False
        else:
            return True
