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


SCREEN_WIDTH = 600
VEL = 5
enemy = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
horizontal_border = pygame.sprite.Group()
vertical_border = pygame.sprite.Group()
SCREEN_HEIGHT = 800
ship_image = load_image("1.jpg")


def terminate():
    pygame.quit()
    sys.exit()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super(Ball, self).__init__(enemy)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color((0, 204, 204)),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-2, 2)
        self.vy = random.randint(1, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_border):
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_border):
            self.kill()


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
        super().__init__()
        self.image = pygame.transform.scale(ship_image, (40, 40))
        self.width = -500
        self.height = -1050
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.last_shot = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        keys = pygame.key.get_pressed()
        time_now = pygame.time.get_ticks()
        cooldown = 970
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
            self.last_shot = time_now


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Шарики')
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    fps = 50
    clock = pygame.time.Clock()
    running = True
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    player = Player(20, 20)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if len(enemy) < 20:
            Ball(20, random.randrange(50, 550), 20)
        screen.fill((0, 0, 0))
        player.move()
        player.draw()
        all_sprites.draw(screen)
        all_sprites.update()
        enemy.draw(screen)
        enemy.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()