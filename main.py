import os
import sys
import pygame
import random



def load_image(name):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image

pygame.mixer.init()
pygame.font.init()
SCORE=0
VEL = 5
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
player_group = pygame.sprite.Group()
enemy = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
horizontal_border = pygame.sprite.Group()
vertical_border = pygame.sprite.Group()
#direct = os.path.join(os.path.dirname(__file__), "assets")
ship_image = load_image("Ship (1).png")
metior_image = load_image("metior.png")
metior_23_image = load_image("mid_met-tran.png")
metior_34_image = load_image("new_met-tran.png")
shooting_sound = pygame.mixer.Sound("shoot.wav")
explo_sound = pygame.mixer.Sound("invaderkilled.wav")
#game_over_sound = pygame.mixer.Sound("explosion.wav")
FONT1 = pygame.font.Font("Quick Brown.ttf", 18)
bul_im = load_image("bul.png")
GRAVITY = 0.1

met_images = []
met_images.append(metior_23_image)
met_images.append(metior_image)
met_images.append(metior_34_image)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    #menu_sound = pygame.mixer.music.load("что-нибудь скачать")
    #pygame.mixer.music.play(-1)
    intro_text = ["Space defender", "", "", "",
                  "Лучший результат:", "", "",
                  "Нажмите конпку 'spase' чтобы начать игру",]
    global width, height
    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("Quick Brown.ttf", 15)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 239, 213))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        pygame.display.flip()
        clock.tick(fps)


class Particle(pygame.sprite.Sprite):
    fire = [load_image('metior.png')]
    for scale in (5, 10, 15, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super(Particle, self).__init__(all_sprites)
        self.image = random.choice(self.fire[1:])
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 5
    numbers = range(-5, 5)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Metior(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super(Metior, self).__init__(all_sprites)
        self.add(enemy)
        radius = random.randrange(50, 90, 20)
        self.radius = radius
        self.metior_image_1 = random.choice(met_images)
        metior_image = self.metior_image_1.copy()
        self.image = pygame.transform.scale(metior_image, (radius, radius))
        self.rect = pygame.Rect(x, y, radius, radius)
        self.vx = random.randint(-2, 2)
        self.vy = random.randint(1, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_border):
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_border):
            self.kill()


class Bulet(pygame.sprite.Sprite):
    global SCORE
    def __init__(self, x, y):
        super(Bulet, self).__init__(all_sprites)
        self.add(bullet_group)
        self.image = pygame.transform.scale(bul_im, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        shooting_sound.play()

    def update(self):
        self.rect.y -= 7
        if self.rect.top > 600:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy, True):
            explo_sound.play()
            self.kill()
            create_particles((self.rect.x, self.rect.y))


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_border)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_border)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__(all_sprites)
        self.add(player_group)
        self.image = pygame.transform.scale(ship_image, (40, 40))
        self.rect = pygame.Rect(20, 20, 40, 40)
        self.rect.center = (x, y)
        self.last_shot = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        keys = pygame.key.get_pressed()
        time_now = pygame.time.get_ticks()
        cooldown = 350
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= VEL
            if self.rect.x < 0:
                self.rect.x = 600
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += VEL
            if self.rect.x > 600:
                self.rect.x = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= VEL
            if self.rect.y < 0:
                self.rect.y = 600
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += VEL
            if self.rect.y > 600:
                self.rect.y = 0
        if keys[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            Bulet(self.rect.left + 20, self.rect.top)
            self.last_shot = time_now
        if pygame.sprite.spritecollide(self, enemy, False):
            terminate()


def draw_text(text, x, y):
    draw_text = FONT1.render(text, 1, (255, 255, 255))
    screen.blit(draw_text, (x, y))


def get_HighScore():
    with open("highscore.txt", "r") as f:
        return f.read()

try:
    highscore = int(get_HighScore())
except:
    highscore = 0


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Space defender')
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    fps = 50
    clock = pygame.time.Clock()
    screen_rect = (0, 0, width, height)
    start_screen()
    running = True
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    player = Player(300, 550)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if len(enemy) < 20:
            Metior(20, random.randrange(0, 550), 20)
        fon = pygame.transform.scale(load_image('Batl_fon2.png'), (width, height))
        screen.blit(fon, (0, 0))
        player.move()
        player.draw()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
        draw_text(f"Score: {SCORE}", 500, 650)
        if (highscore < SCORE):
            highscore = SCORE
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))
        draw_text(f"HighestScore: {highscore}", 30, 630)
        pygame.display.update()
    pygame.quit()