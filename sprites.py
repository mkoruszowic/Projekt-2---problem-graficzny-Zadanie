import pygame as pg
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(400, 0, 50, 50)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 4, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mask = pg.mask.from_surface(self.image)

    def load_images(self):
        self.jumping_frames = [self.game.spritesheet.get_image(206, 120, 62, 62),
                               self.game.spritesheet.get_image(0, 50, 62, 62),
                               self.game.spritesheet.get_image(62, 50, 68, 68),
                               self.game.spritesheet.get_image(130, 50, 70, 70),
                               self.game.spritesheet.get_image(200, 50, 68, 68),
                               self.game.spritesheet.get_image(268, 50, 62, 62),
                               self.game.spritesheet.get_image(330, 50, 50, 50),
                               self.game.spritesheet.get_image(380, 50, 62, 62),
                               self.game.spritesheet.get_image(0, 120, 68, 68),
                               self.game.spritesheet.get_image(68, 120, 70, 70),
                               self.game.spritesheet.get_image(138, 120, 68, 68)]
        for frame in self.jumping_frames:
            frame.set_colorkey(BLACK)

    def jump(self):
        plathits = pg.sprite.spritecollide(self, self.game.platforms, False)
        orbhits = pg.sprite.spritecollide(self, self.game.orbs, False)
        if plathits or orbhits:
            self.vel.y = -PLAYER_JUMP
            self.game.jump_sound.play()
            self.jumping = True

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        self.pos.x += PLAYER_SPEED
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.jumping:
            if now - self.last_update > 34:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                center = self.rect.center
                self.image = self.jumping_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        else:
            bottom = self.rect.bottom
            self.image = self.game.spritesheet.get_image(400, 0, 50, 50)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.current_frame = 0
        self.mask = pg.mask.from_surface(self.image)

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, texture):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_image(250, 0, 50, 50),
                  self.game.spritesheet.get_image(350, 0, 50, 25)]
        self.image = images[texture]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)

class Spike(pg.sprite.Sprite):
    def __init__(self,game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image(300, 25, 50, 25)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)
        self.mask = pg.mask.from_surface(self.image)

class Orb(pg.sprite.Sprite):
    def __init__(self,game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(0, 218, 60, 60)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)

    def load_images(self):
        self.frames = [self.game.spritesheet.get_image(0, 218, 60, 60),
                       self.game.spritesheet.get_image(60, 218, 60, 60),
                       self.game.spritesheet.get_image(120, 218, 60, 60),
                       self.game.spritesheet.get_image(180, 218, 60, 60)]
        for frame in self.frames:
            frame.set_colorkey(BLACK)

    def update(self):
        self.animate()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class Boost(pg.sprite.Sprite):
    def __init__(self,game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(0, 0, 50, 50)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)

    def load_images(self):
        self.frames = [self.game.spritesheet.get_image(0, 0, 50, 50),
                       self.game.spritesheet.get_image(50, 0, 50, 50),
                       self.game.spritesheet.get_image(100, 0, 50, 50),
                       self.game.spritesheet.get_image(150, 0, 50, 50),
                       self.game.spritesheet.get_image(200, 0, 50, 50),]
        for frame in self.frames:
            frame.set_colorkey(WHITE)

    def update(self):
        self.animate()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
