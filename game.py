import pygame
import random
import math
from sys import exit

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/player1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect= self.image.get_rect(center = (300, 300))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top >= 35:
            self.rect.y -= 2
        if keys[pygame.K_s] and self.rect.bottom <= 565:
            self.rect.y += 2
        if keys[pygame.K_a] and self.rect.left >= 35:
            self.rect.x -= 2
        if keys[pygame.K_d] and self.rect.right <= 565:
            self.rect.x += 2
    
    def shoot_bullet(self):
        return Bullet(self.rect.center, mouse_x, mouse_y)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_pos, mouse_x, mouse_y):
        super().__init__()
        self.image = pygame.image.load("graphics/bullet.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center = player_pos)
        angle = math.atan2(mouse_y - player_pos[1], mouse_x - player_pos[0])
        self.x_change = math.cos(angle)
        self.y_change = math.sin(angle)
        self.speed = 5

    def update(self):

        self.rect.x += self.x_change * self.speed
        self.rect.y += self.y_change * self.speed

        if self.rect.x >= 565 or self.rect.x <= 35:
            self.kill()
            
        if self.rect.y >= 565 or self.rect.y <= 35:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.x_pos = 0
        self.y_pos = 0
        self.speed = 1

        tunnel = random.randint(0, 3)

        if tunnel == 0:
            x_pos = random.randint(-300, -100)
            y_pos = random.randint(0, 600)
        elif tunnel == 1:
            x_pos = random.randint(0, 600)
            y_pos = random.randint(-300, -100)
        elif tunnel == 2:
            x_pos = random.randint(700, 900)
            y_pos = random.randint(0, 600)
        else:
            x_pos = random.randint(0, 600)
            y_pos = random.randint(700, 900)

        if type == 'zombie':
            self.image = pygame.image.load("graphics/zombie1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        elif type == "mummy":
            self.image = pygame.image.load("graphics/mummy1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.speed = 1.8


        self.rect = self.image.get_rect(center = (x_pos, y_pos))
    
    def move_to_player(self, player):
        if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        if player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        if player.rect.y > self.rect.y:
            self.rect.y += self.speed
        if player.rect.y < self.rect.y:
            self.rect.y -= self.speed

def check_enemy_collision():
    if pygame.sprite.groupcollide(player_group, enemy_group, False, True):
        return False
    else:
        return True

def check_bullet_collision():
    pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)

def spawn_enemy():
    enemy_timer = int(pygame.time.get_ticks()/1000) - start_time
    enemy_start_time = 0

    if enemy_timer < 10:
        if enemy_timer - enemy_start_time > 5 and len(enemy_group) <= 5:
            enemy_start_time = enemy_timer
            enemy_group.add(Enemy('zombie'))
    else:
        if enemy_timer - enemy_start_time > 7 and len(enemy_group) <= 5:
            enemy_start_time = enemy_timer
            enemy_group.add(Enemy('mummy'))
            enemy_group.add(Enemy('zombie'))

def display_time():
    time = int(pygame.time.get_ticks()/1000) - start_time
    time_surf = time_font.render(f'TIME: {time}', False, "black")
    time_rect = time_surf.get_rect(center = (80, 50))
    screen.blit(time_surf, time_rect)
    return time

def display_game_over():
    game_over_surf = game_over_font.render('GAME OVER', False, "white")
    game_over_rect = game_over_surf.get_rect(center = (300, 300))
    click_surf = time_font.render(f'CLICK TO START', False, "white")
    click_rect = click_surf.get_rect(center = (300, 350))
    screen.blit(game_over_surf, game_over_rect)
    screen.blit(click_surf, click_rect)

width = 600
height = 600
screen = pygame.display.set_mode((width, height))

background = pygame.image.load("graphics/JOPK_Level_1_1.png").convert()
background = pygame.transform.scale(background, (600,600))

player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullet_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()
num_enemies = 0

start_time = 0
time_font = pygame.font.Font('font/pixel.ttf', 20)
game_over_font = pygame.font.Font('font/pixel.ttf', 50)

clock = pygame.time.Clock()

active = True

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if active:
            if event.type == pygame.MOUSEBUTTONDOWN and len(bullet_group) == 0:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullet_group.add(player.shoot_bullet())
        else:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                for enemy in enemy_group:
                    enemy.kill()
                player.rect.center = (300,300)
                start_time = int(pygame.time.get_ticks()/1000)
                num_enemies = 0
                active = True

    if active:
            
        screen.blit(background, (0,0))
        display_time()
        spawn_enemy()

        player_group.draw(screen)
        player_group.update()

        enemy_group.draw(screen)
        for enemy in enemy_group:
            enemy.move_to_player(player)
            
        active = check_enemy_collision()
        check_bullet_collision()

        bullet_group.draw(screen)
        bullet_group.update()
    
    else:

        screen.fill("black")
        display_game_over()

    pygame.display.update()
    clock.tick(60)
        
        