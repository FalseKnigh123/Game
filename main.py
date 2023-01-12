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


VEL = 5
enemy = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
horizontal_border = pygame.sprite.Group()
vertical_border = pygame.sprite.Group()
ship_image = load_image("Ship (1).png")
metior_image = load_image("metior.png")
bul_im = load_image("bul.png")
GRAVITY = 0.1
scor = 0
with open("schor", "r") as f:
    best_scor = int(f.read())


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global best_scor
    with open("schor", "r") as f:
        best_scor = int(f.read())
    intro_text = ["Space defender", "", "", "",
                  f" Лучший результат: {best_scor}", "", "",
                  "Назмите конпку 'spase' чтобы начать игры",]
    global width, height
    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
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


def final_screen():
    global width, height, running, scor
    intro_text = ["Defead", "", "", "",
                  f"Результат: {scor}", "", "",
                  "Нажмите любую кнопу чтобы вернуктся ",""
                  "на стартовый экран",]
    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
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
                if best_scor < scor:
                    with open("schor", "w") as f:
                        f.write(str(scor))
                terminate()
            elif event.type == pygame.KEYDOWN:
                running = False
                if best_scor < scor:
                    with open("schor", "w") as f:
                        f.write(str(scor))
                scor = 0
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
        self.radius = radius
        self.image = pygame.transform.scale(metior_image, (50, 50))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-1, 1)
        self.vy = 1 + scor / 500

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_border):
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_border):
            self.kill()


class Bulet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bulet, self).__init__(all_sprites)
        self.add(bullet_group)
        self.image = pygame.transform.scale(bul_im, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        global scor
        self.rect.y -= 7
        if self.rect.top > 600:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy, True):
            self.kill()
            create_particles((self.rect.x, self.rect.y))
            scor += 10


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
        global player_group, all_sprites, bullet_group, horizontal_border, vertical_border, enemy
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
            final_screen()
            self.kill()
            player_group = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            bullet_group = pygame.sprite.Group()
            horizontal_border = pygame.sprite.Group()
            vertical_border = pygame.sprite.Group()
            enemy = pygame.sprite.Group()


if __name__ == '__main__':
    pygame.init()
    main_run = True
    while main_run:
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
    pygame.quit()