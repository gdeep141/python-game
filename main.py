import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(ICON)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    # loads high score and sounds
    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w+') as f:
            try:
                self.highscore = int(f.read())
            except ValueError:
                self.highscore = 0
        self.sound_dir = path.join(self.dir, 'sound')    # point sound_dir to sound directory
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, 'jumping.wav'))
        self.blueplat_sound = pg.mixer.Sound(path.join(self.sound_dir, 'blueplat.wav'))
        self.death_sound = pg.mixer.Sound(path.join(self.sound_dir, 'death.wav'))
       
    # new game
    def new(self):
        self.score = 0
        # game made harder when reaching these scores
        self.score_boundaries = [400, 600, 800, 1200, 2000, 2800, 3600, 4400, 5200]
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.num_of_platforms = NUMBER_OF_PLATFORMS
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.initial_platform = Platform(*INITIAL_PLATFORM)
        self.all_sprites.add(self.initial_platform)
        self.platforms.add(self.initial_platform)
        self.initial_platform.moving_chance = 0
        self.initial_platform.dangerous_chance = 0
        PLATFORMS = []

        # add platforms to PLATFORMS list
        for i in range(NUMBER_OF_PLATFORMS):
            plat = (random.randrange(0, WIDTH - PLATFORM_WIDTH),
                    random.randrange(0, HEIGHT))
            PLATFORMS.append(plat)

        for plat in PLATFORMS:
            p = Platform(*plat)
            # make sure none of the initial platforms are dangerous
            if p.dangerous_chance == 1:
                p.image = pg.image.load(os.path.join('img', 'green_grass_platform.png'))
                p.dangerous_chance = 0
            self.all_sprites.add(p)
            self.platforms.add(p)

        pg.mixer.music.load(path.join(self.sound_dir, 'playing.ogg'))   # loads gameplay music
        
        self.run()            

    # game running loop
    def run(self): 
        pg.mixer.music.play(loops=-1)       # loops music until run ends
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(30)

    # update all sprites
    def update(self):
        self.all_sprites.update()
        self.player.bounce()
        
        # scrolling
        if self.player.rect.top <= HEIGHT * 1/3:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:     
                    plat.kill()
                    self.score += 10    # increment score when platform is killed
   
        # randomly generated platforms
        while len(self.platforms) < self.num_of_platforms:
            p = Platform(random.randrange(0, WIDTH - PLATFORM_WIDTH),
                         -random.randrange(0, int(HEIGHT * 1/3)))
            self.platforms.add(p)
            self.all_sprites.add(p)

        # make game harder as score increases
        for s in self.score_boundaries:
            if self.score >= s:
                self.num_of_platforms -= 1
                del self.score_boundaries[0]  # ensure score passed is no longer checked

        # # game over condition
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)  # send platforms upwards off screen
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:   # end game when there are no more platforms
            self.playing = False
            self.death_sound.play()
            pg.mixer.music.fadeout(100)

    # check for exit condition           
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    # draw sprites to screen using image for surface and rect for location
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        
    # Start screen
    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.sound_dir, 'menu.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use the arrow keys to move left or right", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Hit the middle of a platform to jump higher", 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(200)

    # Game over screen
    def show_go_screen(self):
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.sound_dir, 'game over.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()

        self.wait_for_key()
        pg.mixer.music.fadeout(200)

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

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()

    # main game loop
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()
