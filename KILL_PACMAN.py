import pygame, sys, os, random, math

# Force static position of screen
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Constants
SHIP_WIDTH = SHIP_HEIGHT = 13
size = width, height = 920, 570
PILL_HEIGHT = 25
PILL_WIDTH = 7

# Colors
WHITE = (255, 255, 255)
RED = (185, 45, 45)
YELLOW = (230, 230, 0)
BLUE = (45, 115, 185)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
PURPLE = (192, 42, 222)
GRAY = (80, 80, 80)
AQUA = (29, 208, 219)


class Game:
    def __init__(self):
        self.fps = 30
        self.top_buffer = 50
        self.screen = pygame.display.set_mode(size, pygame.SRCALPHA)
        self.P1_WIN = Text(100, "P One WINS", width / 2, height / 5, "fonts/PAC-FONT.TTF")
        self.P2_WIN = Text(100, "P Two WINS", width / 2, height / 5, "fonts/PAC-FONT.TTF")
        self.title = Text(100, "KILL PACMAN", width / 2, height / 4, "fonts/PAC-FONT.TTF")
        self.click = Text(50, "click here", width / 2, height / 1.5, "fonts/PAC-FONT.TTF")

        self.intro_back = pygame.image.load("untitled folder 6/background3.jpg").convert()
        self.intro_back = pygame.transform.scale(self.intro_back, (width, height))
        self.back = pygame.image.load("untitled folder 6/game_background.jpg").convert()
        self.back = pygame.transform.scale(self.back, (width, height))
        self.outro_back = pygame.image.load("untitled folder 6/tombstone_real.jpg").convert()
        self.outro_back = pygame.transform.scale(self.outro_back, (width, height))

        self.left_score = Text(35, "0", width / 4, height / 45, "fonts/FunSized.ttf")
        self.right_score = Text(35, "0", width / 1.3, height / 45, "fonts/FunSized.ttf")
        self.lb1 = Text(25, "lb", width / 2.7, height / 45, "fonts/FunSized.ttf")
        self.lb2 = Text(25, "lb", width / 1.13, height / 45, "fonts/FunSized.ttf")

        self.clock = pygame.time.Clock()
        self.intro = self.play = True
        self.end = False
        self.timer = 0

        self.vertical = pygame.Surface((1, height - self.top_buffer)).convert()
        self.horizontal = pygame.Surface((width, 1)).convert()
        self.music_fruit = pygame.mixer.Sound("sound/pacman-eatfruit.ogg")
        self.music_ghost = pygame.mixer.Sound("sound/ghost.ogg")
        self.music_oof = pygame.mixer.Sound("sound/oof.ogg")

    def blink(self):
        if pygame.time.get_ticks() % 1000 < 500:
            self.screen.blit(self.click.image, self.click.rect)


class Text:
    def __init__(self, size, text, xpos, ypos, font):
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, 1, YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.y = ypos


class Pill(pygame.sprite.Sprite):
    def __init__(self, xval, density):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.density = density
        self.image = pygame.Surface((20, 20)).convert()
        self.image = self.ghost_image()
        self.image = self.image = pygame.transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(xval, PILL_HEIGHT * 1.8, PILL_WIDTH, PILL_HEIGHT)

    def ghost_image(self):
        if self.density == 1:
            self.speed = 4
            return pygame.image.load("untitled folder 6/vulnerable.png").convert_alpha()
        elif self.density == 2:
            self.speed = 5
            return pygame.image.load("untitled folder 6/blinky.png").convert_alpha()
        elif self.density == 3:
            self.speed = 6
            return pygame.image.load("untitled folder 6/inky.png").convert_alpha()
        elif self.density == 4:
            self.speed = 7
            return pygame.image.load("untitled folder 6/clyde.png").convert_alpha()
        elif self.density == 5:
            self.speed = 4
            return pygame.image.load("untitled folder 6/veggie.jpeg").convert_alpha()
        elif self.density == 6:
            self.speed = 15
            return pygame.image.load("untitled folder 6/strawberry.PNG").convert_alpha()
        elif self.density == 7:
            self.speed = 10
            return pygame.image.load("untitled folder 6/pinky.png").convert_alpha()

    def update(self):
        self.rect = self.rect = self.rect.move((0, self.speed))

        if self.rect.y > height:
            self.kill()


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, side):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.density = SHIP_WIDTH * SHIP_HEIGHT
        self.image = pygame.image.load("untitled folder 6/pacman.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SHIP_WIDTH, SHIP_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.type = side

    def update(self, run, pill_group, ship_group):
        key = pygame.key.get_pressed()

        if self.type == "left":
            #if key[pygame.K_w]:
                #self.rect.y -= self.speed
            if key[pygame.K_d]:
                self.rect.x += self.speed
            if key[pygame.K_a]:
                self.rect.x -= self.speed
            #if key[pygame.K_s]:
                #self.rect.y += self.speed

            # Boundaries Left
            if self.rect.right > width / 2:
                self.rect.right = width / 2

            elif self.rect.left < 0:
                self.rect.left = 0

            elif self.rect.top < width / 17.5:
                self.rect.top = width / 17.5

            elif self.rect.bottom > height:
                self.rect.bottom = height

        if self.type == "right":
            #if key[pygame.K_UP]:
                #self.rect.y -= self.speed
            if key[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if key[pygame.K_RIGHT]:
                self.rect.x += self.speed
            #if key[pygame.K_DOWN]:
                #self.rect.y += self.speed

            # Boundaries Right
            if self.rect.right > width:
                self.rect.right = width

            elif self.rect.left < width / 2:
                self.rect.left = width / 2

            elif self.rect.top < width / 17.5:
                self.rect.top = width / 17.5

            elif self.rect.bottom > height:
                self.rect.bottom = height

        collisions = pygame.sprite.spritecollide(self, pill_group, True)
        for p in collisions:
            if p.density == 5:
                if self.density - p.density > 169:
                    self.density -= p.density * 10
                    run.music_oof.play(0)
                for s in ship_group:
                    if s.type != self.type:
                        s.density += p.density * 10
                        if s.type == "left":
                            run.left_score.image = run.left_score.font.render(str(s.density - 169), 1, YELLOW)
                        else:
                            run.right_score.image = run.right_score.font.render(str(s.density - 169), 1, YELLOW)

            elif p.density == 6:
                run.music_fruit.play(0)
                self.density += p.density * 100
            else:
                run.music_ghost.play(0)
                self.density += p.density * 50

            if self.type == "left":
                run.left_score.image = run.left_score.font.render(str(self.density - 169), 1, YELLOW)
            else:
                run.right_score.image = run.right_score.font.render(str(self.density - 169), 1, YELLOW)

        if self.density >= 10000:
            run.end = True
            run.play = False

        if self.density >= 2000:
            self.speed = 4
        if self.density >= 4000:
            self.speed = 3
        if self.density >= 6000:
            self.speed = 2
        if self.density >= 8000:
            self.speed = 1

        self.rect.width = self.rect.height = math.sqrt(self.density)
        self.image = pygame.image.load("untitled folder 6/pacman.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))


def main():
    # Runs imported module
    pygame.init()

    run = Game()

    # Local variables
    pygame.display.set_caption("PACMAN TWO")

    ship_l = Ship(width / 4 - SHIP_WIDTH / 2, height - (4 * SHIP_HEIGHT), "left")
    ship_r = Ship((width * 3 / 4) - SHIP_WIDTH / 2, height - (4 * SHIP_HEIGHT), "right")
    p1 = ship_l
    p2 = ship_r

    # Groups
    ship_group = pygame.sprite.Group()
    ship_group.add(ship_l, ship_r)
    pill_group = pygame.sprite.Group()

    # Music
    music_intro = pygame.mixer.Sound("sound/pacman_intro.ogg")
    music_select = pygame.mixer.Sound("sound/select.ogg")
    music_intro.play(-1)

    music_death = pygame.mixer.Sound("sound/pacman-death.ogg")

    while True:
        while run.intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    run.intro = False
                    music_intro.stop()
                    music_select.play(0)

            # Bliting
            run.screen.blit(run.intro_back, (0, 0))
            run.screen.blit(run.title.image, run.title.rect)
            run.blink()

            pygame.display.flip()

        while run.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            # Update groups
            if run.timer % 10 == 0:
                pill = Pill(random.randrange(0, (width / 2) - PILL_WIDTH), int(random.choice('111111111111111111112222233344555555555555555555555555555567')))
                pill2 = Pill(random.randrange((width / 2), width - PILL_WIDTH), int(random.choice('1111111111111111111122222333445555555555555555555555567')))
                pill_group.add(pill, pill2)

            ship_group.update(run, pill_group, ship_group)
            pill_group.update()

            # Draw groups
            run.screen.blit(run.back, (0, 0))
            ship_group.draw(run.screen)
            pill_group.draw(run.screen)
            run.screen.blit(ship_l.image, ship_l.rect)
            run.screen.blit(ship_r.image, ship_r.rect)
            run.screen.blit(run.vertical, (width/2, run.top_buffer))
            run.screen.blit(run.horizontal, ((width/1000), run.top_buffer))
            run.screen.blit(run.left_score.image, run.left_score.rect)
            run.screen.blit(run.right_score.image, run.right_score.rect)
            run.screen.blit(run.lb1.image, run.lb1.rect)
            run.screen.blit(run.lb2.image, run.lb2.rect)


            # limits frames per iteration of while loop
            run.timer += 1
            run.clock.tick(run.fps)

            # writes main surface
            pygame.display.flip()

        while run.end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                music_death.play(0)

                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    music_death.stop()
                    run.intro = run.play = True
                    run.end = False
                    ship_l.density = 169
                    ship_r.density = 169
                    run.left_score.image = run.left_score.font.render(str(ship_l.density), 1, YELLOW)
                    run.right_score.image = run.right_score.font.render(str(ship_r.density), 1, YELLOW)
                    ship_l.rect.x = width / 4
                    ship_l.rect.y = height / 1.1
                    ship_r.rect.x = width / 1.35
                    ship_r.rect.y = height / 1.1
                    ship_l.speed = 5
                    ship_r.speed = 5

            run.screen.blit(run.outro_back, (0, 0))

            if p1.density >= 10000:
                run.screen.blit(run.P1_WIN.image, run.P1_WIN.rect)
            elif p2.density >= 10000:
                run.screen.blit(run.P2_WIN.image, run.P2_WIN.rect)

            run.blink()

            pygame.display.flip()

if __name__ == "__main__":
    main()
