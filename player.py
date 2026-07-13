from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            # Corrected: subtract speed_cos/sin for backward movement
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_d]:
            # Corrected: subtract from dx, add to dy for strafing left (relative to forward angle)
            dx -= speed_sin
            dy += speed_cos
        if keys[pg.K_a]:
            # Corrected: add to dx, subtract from dy for strafing right
            dx += speed_sin
            dy -= speed_cos

        self.check_wall_collision(dx, dy)

        #if keys[pg.K_LEFT]:
       #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
      #  if keys[pg.K_RIGHT]:
     #       self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau # Use math.tau (2*pi) instead of math.taudef

    def check_wall(self, x, y):
        # Assuming self.game.map.world_map is a set of wall coordinates
        return (x,y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        # Check X movement first
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        # Check Y movement second
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        # Optional debug drawing lines are commented out in original code
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_WIDTH])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()

    @property # Added the missing decorator for the property methods
    def pos(self):
        return self.x, self.y

    @property # Added the missing decorator for the property methods
    def map_pos(self):
        return int(self.x), int(self.y)
