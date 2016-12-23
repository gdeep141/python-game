import math
import pygame as pg
from settings import *
import os

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join('img', 'smallball.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT/ 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0) # velocity
        self.acc = vec(0, 0) # acceleration

    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = - PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION   # slows down player movment when key is let go    
        self.vel += self.acc                         # update velocity
        self.pos += self.vel + 0.5 * self.acc        # update position

        # # wrap around side of screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos  # move player


    def bounce(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)  # collision detection
        for platform in hits:
            # triggers gameover if platform is dangerous 
            if platform.dangerous_chance == 1:
                self.game.death_sound.play()
                self.game.playing = False

            else:
                # check player is above platform and falling
                if self.vel.y > 0 and self.rect.bottom < platform.rect.bottom:
                    self.rect.bottom = platform.rect.top    # prevent player from clipping through platform
                    
                    if platform.disappear_chance == 1:
                        self.game.blueplat_sound.play()
                        self.vel.y = -PLAYER_JUMP * MIDDLE_JUMP_FACTOR   # player jumps higher on disappearing platform
                        platform.kill()   # make platform disappear
                        self.game.score += 100  # score bonus
                    
                    # bounce higher if in center of platform
                    elif platform.rect.midtop[0] - MIDDLE_TOLERANCE < self.rect.midbottom[0] < platform.rect.midtop[0] + MIDDLE_TOLERANCE:
                        self.game.jump_sound.play()
                        self.vel.y = -PLAYER_JUMP * MIDDLE_JUMP_FACTOR
                    
                    # normal platform
                    else:
                        self.game.jump_sound.play()
                        self.vel.y = -PLAYER_JUMP


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w=PLATFORM_WIDTH, h=PLATFORM_HEIGHT): # x and y location, width and height
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join('img', 'green_grass_platform.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.moving_odds = 25   # probability of moving platform
        self.moving_chance = random.randint(0, self.moving_odds)
        self.dangerous_odds = 50
        self.dangerous_chance = random.randint(0, self.dangerous_odds)
        self.disappear_odds = 20
        self.disappear_chance = random.randint(0, self.disappear_odds)

        # change image if platform is moving
        if self.dangerous_chance == 1:
            self.image = pg.image.load(os.path.join('img', 'red_grass_platform.png'))

        elif self.disappear_chance == 1:
            self.image = pg.image.load(os.path.join('img', 'gray_grass_platform.png'))

    def update(self):
        
        if self.moving_chance == 1:
            self.rect.x += self.speed

        # reverse speed if platform hits the side of the screen
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed = -self.speed  