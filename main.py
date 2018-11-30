# this file was created by Chris Cozort
# Sources: goo.gl/2KMivS 
# now available in github

'''
Curious, Creative, Tenacious(requires hopefulness)

Game ideas:
Walls closing in on player

'''
import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        #init game window
        # init pygame and create window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Golden Carrot")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        print("load data is called...")
        # sets up directory name
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # opens file with write options
        ''' with is a contextual option that handles both opening and closing of files to avoid
        issues with forgetting to close
        '''
        try:
            # changed to r to avoid overwriting error
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                print("exception")
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))       
        # load sounds
        # great place for creating sounds: https://www.bfxr.net/
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jump24.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump29.wav'))                     
    def new(self):
        self.score = 0
        # add all sprites to the pg group
        # below no longer needed - using LayeredUpdate group
        # self.all_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create platforms group
        self.platforms = pg.sprite.Group()
        self.brokenplatforms = pg.sprite.Group()
        '''add coins'''
        self.gold = pg.sprite.Group()
        self.silver = pg.sprite.Group()
        self.bronze = pg.sprite.Group()
        self.carrot = pg.sprite.Group()
        '''add spikes'''
        self.spikes = pg.sprite.Group()
        self.springs = pg.sprite.Group()
        self.flymob1_timer = 0
        self.flymob2_timer = 0
        # add a player 1 to the group
        self.player = Player(self)
        # add mobs
        self.flymobs1 = pg.sprite.Group()
        self.flymobs2 = pg.sprite.Group()

        # no longer needed after passing self.groups in Sprites library file
        # self.all_sprites.add(self.player)
        # instantiate new platform 
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        for plat in PLATFORM_LIST:
            BrokenPlatform(self, *plat)

        # load music
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))
        # call the run method
        self.run()
    def run(self):
        # game loop
        # play music
        pg.mixer.music.play(loops=-1)
        # set boolean playing to true
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)
    def update(self):
        self.all_sprites.update()
        
        # shall we spawn a mob?
        now = pg.time.get_ticks()
        '''flying mobs'''
        if now - self.flymob1_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.flymob1_timer = now
            FlyMob1(self)
        # check for mob collisions
        flymob1_hits = pg.sprite.spritecollide(self.player, self.flymobs1, False)
        if flymob1_hits:
            if self.player.pos.y - 35 < flymob1_hits[0].rect_top:
                print("hit top")
                print("player is " + str(self.player.pos.y))
                print("flymob1 is " + str(flymob1_hits[0].rect_top))
                self.player.vel.y = -BOOST_POWER
            else:
                print("player is " + str(self.player.pos.y))
                print("flymob1 is " + str(flymob1_hits[0].rect_top))
                self.playing = False

        if now - self.flymob2_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.flymob2_timer = now
            FlyMob2(self)
        # check for mob collisions
        flymob2_hits = pg.sprite.spritecollide(self.player, self.flymobs2, False)
        if flymob2_hits:
            if self.player.pos.y - 35 < flymob2_hits[0].rect_top:
                print("hit top")
                print("player is " + str(self.player.pos.y))
                print("flymob2 is " + str(flymob2_hits[0].rect_top))
                self.player.vel.y = -BOOST_POWER
            else:
                print("player is " + str(self.player.pos.y))
                print("flymob2 is " + str(flymob2_hits[0].rect_top))
                self.playing = False

        # check to see if player can jump - if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                # set var to be current hit in list to find which to 'pop' to when two or more collide with player
                find_lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > find_lowest.rect.bottom:
                        print("hit rect bottom " + str(hit.rect.bottom))
                        find_lowest = hit
                # fall if center is off platform
                if self.player.pos.x < find_lowest.rect.right + 10 and self.player.pos.x > find_lowest.rect.left - 10:
                    if self.player.pos.y < find_lowest.rect.centery:
                        self.player.pos.y = find_lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
            
                # scroll plats with player
        ''' changed values and variables so instead of scrolling upwards it scrolls to the right'''
        if self.player.rect.right >= WIDTH / 1.5:
            # creates slight scroll at the top based on player y velocity
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            '''coins scroll with the screen instead of staying in the same spot'''
            for gold in self.gold:
                gold.rect.x -= max(abs(self.player.vel.x), 2)
            for silver in self.silver:
                silver.rect.x -= max(abs(self.player.vel.x), 2)
            for bronze in self.bronze:
                bronze.rect.x -= max(abs(self.player.vel.x), 2)
            for carrot in self.carrot:
                carrot.rect.x -= max(abs(self.player.vel.x), 2)
            '''spikes scroll with the screen instead of staying in the same spot'''
            for spike in self.spikes:
                spike.rect.x -= max(abs(self.player.vel.x), 2)
            for spring in self.springs:
                spring.rect.x -= max(abs(self.player.vel.x), 2)
            '''mobs scroll with the screen'''
            for flymob1 in self.flymobs1:
                # creates slight scroll based on player y velocity
                flymob1.rect.x -= max(abs(self.player.vel.x), 2)
            for flymob2 in self.flymobs2:
                flymob2.rect.x -= max(abs(self.player.vel.x), 2)
            
            for plat in self.platforms:
                '''changed it so platforms disappear as the screen scrolls past them'''
                plat.rect.x -= max(abs(self.player.vel.x), 2)
                if plat.rect.right <= WIDTH - 800:
                    plat.kill()
            for plat in self.brokenplatforms:
                plat.rect.x -= max(abs(self.player.vel.x), 2)
                if plat.rect.right <= WIDTH - 800:
                    plat.kill()
            brokenplatformhits = pg.sprite.spritecollide(self.player, self.brokenplatforms, False)
            if brokenplatformhits:
                plat.kill()
        '''if player gets a coin'''
        gold_hits = pg.sprite.spritecollide(self.player, self.gold, True)
        for gold in gold_hits:
            if gold.type == 'gold':
                self.boost_sound.play()
                self.player.vel.y = -10
                self.player.jumping = False
                self.score += 10
        silver_hits = pg.sprite.spritecollide(self.player, self.silver, True)
        for silver in silver_hits:
            if silver.type == 'silver':
                self.boost_sound.play()
                self.player.vel.y = -10
                self.player.jumping = False
                self.score += 5
        bronze_hits = pg.sprite.spritecollide(self.player, self.bronze, True)
        for bronze in bronze_hits:
            if bronze.type == 'bronze':
                self.boost_sound.play()
                self.player.vel.y = -10
                self.player.jumping = False
                self.score += 1
        carrot_hits = pg.sprite.spritecollide(self.player, self.carrot, True)
        for carrot in carrot_hits:
            if carrot.type == 'carrot':
                self.boost_sound.play()
                self.player.vel.y = -10
                self.player.jumping = False
                '''win screen'''
                self.screen.fill(BLACK)
                self.draw_text("You Won!", 48, GOLD, WIDTH/2, HEIGHT/4)
                self.draw_text("WASD to move", 22, SKY_BLUE, WIDTH/2, HEIGHT/2)
                self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
                self.draw_text("High Score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 100)
                self.draw_text("Press ESCAPE to restart ", 22, WHITE, WIDTH / 2, 330)
                if self.score > self.highscore:
                    self.highscore = self.score
                    self.draw_text("New High Score!", 22, REDDISH, WIDTH / 2, HEIGHT/2 + 70)
                    with open(path.join(self.dir, HS_FILE), 'w') as f:
                        f.write(str(self.score))
                else:
                    self.draw_text("High Score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 100)

            pg.display.flip()
            self.wait_for_key()
        '''if player hits a spring'''
        spring_hits = pg.sprite.spritecollide(self.player, self.springs, True)
        for spring in spring_hits:
            if spring.type == 'spring':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
        ''' if player hits spikes'''
        spike_hits = pg.sprite.spritecollide(self.player, self.spikes, True)
        for spike in spike_hits:
            if spike.type == 'spike':
                self.playing = False

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
               sprite.rect.y -= max(self.player.vel.y, 10)
            if sprite.rect.bottom < 0:
                    sprite.kill()

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.playing = False
        
        if len(self.platforms) == 0:
            self.playing = False

        if len(self.brokenplatforms) == 0:
            self.playing = False

        '''platform generator'''
        while len(self.platforms) < 15:
            Platform(self, random.randrange(100, 1000), 
                            random.randrange(-1, 1000))
        while len(self.brokenplatforms) < 4:
            BrokenPlatform(self, random.randrange(100, 1000), 
                            random.randrange(-1, 1000))


    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_w:
                        # cuts the jump short if the space bar is released
                        self.player.jump_cut()
    def draw(self):
        self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        # not needed now that we're using LayeredUpdates
        # self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # double buffering - renders a frame "behind" the displayed frame
        pg.display.flip()
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
    def show_start_screen(self):
        # game splash screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, GOLD, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move", 22, SKY_BLUE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        self.draw_text("Press ESCAPE to restart ", 22, WHITE, WIDTH / 2, 330)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        # game splash screen
        if not self.running:
            print("not running...")
            return
        self.screen.fill(BLACK)
        self.draw_text("You Lost!", 48, REDDISH, WIDTH/2, HEIGHT/4)
        self.draw_text("WASD to move", 22, SKY_BLUE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High Score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 100)
        self.draw_text("Press ESCAPE to restart ", 22, WHITE, WIDTH / 2, 330)

        pg.display.flip()
        self.wait_for_key()
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
    try:
        g.show_go_screen()
    except:
        print("can't load go screen...")