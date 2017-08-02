import pygame
import random
from settings import *
from sprites import *
from time import sleep


class Game():

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)

    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.ground_sprite = pygame.sprite.Group()
        for cloud in CLOUDS_LIST:
            c = Background(*cloud)
            self.clouds.add(c)
        self.bird = Bird(self, BIRD_IMAGE)
        self.all_sprites.add(self.bird)
        self.ground = Background(0, HEIGHT - 40, WIDTH, 40, "images/ground.png")
        self.ground_sprite.add(self.ground)
        self.paused = False
        for pipe in PIPES_LIST:
            p = Pipe(*pipe)
            self.all_sprites.add(p)
            self.pipes.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        self.win = False
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # Check if bird hits a pipe
        hits = pygame.sprite.spritecollide(self.bird, self.pipes, False)
        if hits:
            self.playing = False

        # if bird reaches screen's width/2
        if self.bird.rect.x + self.bird.rect.width >= WIDTH / 2:
            self.bird.pos.x -= abs(self.bird.vel.x)
            for cloud in self.clouds:
                cloud.rect.x -= abs(self.bird.vel.x)
                if cloud.rect.x + cloud.rect.width < 0:
                    cloud.kill()
            for pipe in self.pipes:
                pipe.rect.x -= abs(self.bird.vel.x)
                if pipe.rect.x + pipe.rect.width < 0:
                    pipe.rect.x -= abs(self.bird.vel.x)
                    pipe.kill()
                if self.bird.pos.x >= pipe.rect.x + pipe.rect.width and pipe.active:
                    self.score += 1
                    pipe.de_activate()

        # spawn clouds
        while len(self.clouds) < 4:
            width = random.randrange(80, 120)
            height = random.randrange(40, 80)
            cloud_pos = random.randrange(0, 400)
            cloud = Background(WIDTH,
                               (HEIGHT / 2 + CLOUD_GAP_Y - cloud_pos),
                               width, height, CLOUD_IMAGE)
            self.clouds.add(cloud)

        # spawn new pipes
        while len(self.pipes) < 6:

            for i in range(1, 14):
                if i != 14:
                    r_high = random.randint(0, 1)
                    r_low = random.randint(2, 3)
                elif i == 14:
                    r_high = 1
                    r_low = 3

                p_high = Pipe(PIPES_LIST[3][0] + i * CONSEUTIVE_PIPE_GAP,
                              0, PIPE_WIDTH,
                              random.randrange(80, HEIGHT * 3 / 5),
                              PIPE_IMAGES_LIST[r_high])
                p_low = Pipe(PIPES_LIST[3][0] + i * CONSEUTIVE_PIPE_GAP,
                             p_high.rect.y + p_high.rect.height + PIPE_BW_GAP,
                             PIPE_WIDTH, HEIGHT * 3 / 4,
                             PIPE_IMAGES_LIST[r_low])

                self.pipes.add(p_high)
                self.all_sprites.add(p_high)
                self.pipes.add(p_low)
                self.all_sprites.add(p_low)

        # Die if fall!
        if self.bird.rect.bottom > self.ground.rect.top:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.bird.vel.y, 10)
                if sprite.rect.y >= 0:
                    sprite.kill()

            self.playing = False

        # Winning condition
        if self.score >= WIN_SCORE:
            sleep(1)
            self.playing = False
            self.win = True
            self.running = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.bird.fly()
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(BGCOLOR)
        self.clouds.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.ground_sprite.draw(self.screen)
        self.draw_text('Score: {0}'.format(self.score), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()

    def show_start_screen(self):
        # Game start screen
        self.screen.fill(ORANGE)
        self.draw_text(TITLE, 100, BLACK, WIDTH / 2, HEIGHT / 5)
        self.draw_text("Press UP to Fly...", 30,
                       BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("& SPACE + UP for Fly Boost!!",
                       30, BLUE, WIDTH / 2, HEIGHT / 2 + 50)
        self.draw_text("Press SPACE to Play!!", 30,
                       BLUE, WIDTH / 2, HEIGHT * 4 / 5)
        pygame.display.flip()
        self.wait_for_mouse_press()

    def show_game_over_screen(self):
        # Game over
        if not self.running:
            return
        self.screen.fill(RED)
        self.draw_text("GAME OVER :(", 72, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Your Score: {0}".format(
            self.score), 50, BLUE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press SPACE to Play Again!!",
                       50, BLUE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_mouse_press()

    def show_win_screen(self):
        if not self.running:
            return
        self.screen.fill(LIGHTBLUE)
        self.draw_text("YOU WIN :D", 72, BLACK, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Your Score: {0}".format(
            self.score), 50, ORANGE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press SPACE to go to Menu Screen...",
                       50, ORANGE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_mouse_press()

    def wait_for_mouse_press(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    if not g.win:
        g.show_game_over_screen()
    elif g.win:
        g.show_win_screen()
        g.show_start_screen()

pygame.quit()
