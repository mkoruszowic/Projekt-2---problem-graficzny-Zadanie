import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # inicjalizacja okna gry, itp
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # ładowanie spriteow
        self.dir = path.dirname(__file__)

        # ładowanie dzwięku
        self.snd_dir = path.join(self.dir, "snd")
        self.img = path.join(self.dir, "img")
        self.spritesheet = Spritesheet(path.join(self.img, SPRITESHEET))
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump33.wav'))
        self.hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Hit_Hurt5.wav'))
        self.background = pg.image.load(path.join(self.img, 'background.png'))

    def new(self):
        # rozpoczęcie nowej gry
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.orbs = pg.sprite.Group()
        self.boosts = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for spike in SPIKE_LIST:
            s = Spike(self, *spike)
            self.all_sprites.add(s)
            self.spikes.add(s)
        for orb in ORB_LIST:
            o = Orb(self, *orb)
            self.all_sprites.add(o)
            self.orbs.add(o)
        for boost in BOOST_LIST:
            b = Boost(self, *boost)
            self.all_sprites.add(b)
            self.boosts.add(b)

        self.run()

    def run(self):
        # główna pętla gry
        pg.mixer.music.load(path.join(self.snd_dir, "music1.mp3"))
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # pętla gry - aktualizacja
        self.all_sprites.update()

        plathits = pg.sprite.spritecollide(self.player, self.platforms, False)

        if plathits:
            self.player.jumping = False
            if len(plathits) == 2 and plathits[0].rect.top != plathits[1].rect.top:
                self.hit_sound.play()
                self.playing = False

            else:
                if self.player.vel.y > 0:
                    if self.player.rect.right -4 > plathits[0].rect.left:
                        self.player.pos.y = plathits[0].rect.top
                        self.player.vel.y = 0
                    else:
                        self.hit_sound.play()
                        self.playing = False
                else:
                    self.hit_sound.play()
                    self.playing = False

        spikehits = pg.sprite.spritecollide(self.player, self.spikes, False, pg.sprite.collide_rect_ratio(0.8))
        if spikehits:
            self.hit_sound.play()
            self.playing = False

        boosthits = pg.sprite.spritecollide(self.player, self.boosts, False, pg.sprite.collide_rect_ratio(0.5))
        if boosthits:
            self.player.jump()


        # jeśli gracz przekroczy 1/3 erkanu
        if self.player.rect.right >= WIDTH / 3:
            self.player.pos.x -= PLAYER_SPEED
            for plat in self.platforms:
                plat.rect.x -= PLAYER_SPEED
                # pozbywanie się obiektów które opuściły ekran z lewej
                if plat.rect.right <= 0:
                    plat.kill()
                    self.score += 1
            for spike in self.spikes:
                spike.rect.x -= PLAYER_SPEED
                if spike.rect.right <= 0:
                    spike.kill()
            for orb in self.orbs:
                orb.rect.x -= PLAYER_SPEED
                if orb.rect.right <= 0:
                    orb.kill()
            for boost in self.boosts:
                boost.rect.x -= PLAYER_SPEED
                if boost.rect.right <= 0:
                    boost.kill()

        if self.player.pos.y <= 100:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
            for spike in self.spikes:
                spike.rect.y += abs(self.player.vel.y)
            for orb in self.orbs:
                orb.rect.y += abs(self.player.vel.y)
            for boost in self.boosts:
                boost.rect.y += abs(self.player.vel.y)

        if self.player.pos.y >= HEIGHT - 45:
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)
            for spike in self.spikes:
                spike.rect.y -= abs(self.player.vel.y)
            for orb in self.orbs:
                orb.rect.y -= abs(self.player.vel.y)
            for boost in self.boosts:
                boost.rect.y -= abs(self.player.vel.y)

        if self.player.pos.y > HEIGHT - 30:
            self.playing = False

    def events(self):
        # pętla gry - wydarzenia
        for event in pg.event.get():
            # sprawdzenie zamknięcia okna
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.player.jump()

    def draw(self):
        # pętla gry - rysowanie
        self.screen.blit(self.background, (0,0))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score * 100 // G_LENGTH ) + "%", 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # ekran startowy gry
        pg.mixer.music.load(path.join(self.snd_dir, "menu.mp3"))
        pg.mixer.music.play(loops=-1)
        self.screen.blit(self.background, (0,0))
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Skok - strzałka w górę", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Wciśnij dowolny przycisk", 26, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # koniec gry / kontynuuj
        if (self.score * 100 // G_LENGTH) == 100:
            pg.mixer.music.load(path.join(self.snd_dir, "menu.mp3"))
            pg.mixer.music.play(loops=-1)
            if not self.running:
                return
            self.screen.blit(self.background, (0,0))
            self.draw_text("WYGRAŁEŚ!", 26, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Wciśnij spację aby zagrać jeszcze raz", 22, WHITE, WIDTH / 2, HEIGHT / 2)
            pg.display.flip()
            self.press_space()
            pg.mixer.music.fadeout(500)
        else:
            self.go_screen = pg.image.load(path.join(self.img, 'gameover.png'))
            pg.mixer.music.load(path.join(self.snd_dir, "menu.mp3"))
            pg.mixer.music.play(loops=-1)
            if not self.running:
                return
            self.screen.blit(self.go_screen, (0,0))
            self.draw_text("Procent: " + str(self.score * 100 // G_LENGTH)+ "%", 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Wciśnij spację aby zagrać jeszcze raz", 26, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            pg.display.flip()
            self.press_space()
            pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def press_space(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
