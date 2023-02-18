import time
import pygame
import os

pygame.font.init()
pygame.display.set_caption('Space-War')
pygame.mixer.init()

font = pygame.font.Font('freesansbold.ttf', 20)
font2 = pygame.font.Font('freesansbold.ttf', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'win.wav'))

WIDTH, HEIGHT = 900, 500
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
WIN = pygame.display.set_mode((900, 500))
pygame.display.init()
FPS = 60

BORDER = pygame.Rect(440, 0, 4, HEIGHT)  # 2 for position, 2 for proportion

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

VEL = 5
BULLET_VEL = 7
MAX_BULL = 4

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')),
                           (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')),
                           (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (900, 500))


def moving_SpaceShip(red, yellow, key):
    if key[pygame.K_UP] and red.y > 0:
        red.y -= VEL
    if key[pygame.K_DOWN] and red.y < 500 - SPACESHIP_WIDTH:
        red.y += VEL
    if key[pygame.K_LEFT] and red.x > 460:
        red.x -= VEL
    if key[pygame.K_RIGHT] and red.x < 900 - SPACESHIP_WIDTH:
        red.x += VEL

    if key[pygame.K_w] and yellow.y > 0:
        yellow.y -= VEL
    if key[pygame.K_s] and yellow.y < 500 - SPACESHIP_WIDTH:
        yellow.y += VEL
    if key[pygame.K_a] and yellow.x > 0:
        yellow.x -= VEL
    if key[pygame.K_d] and yellow.x < 450 - SPACESHIP_WIDTH:
        yellow.x += VEL


def bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if bullet.x < 0:
            red_bullets.remove(bullet)
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)


def draw_winner(red_health, yellow_health):
    if red_health <= 0:
        winner = font2.render('Yellow Wins!', True, WHITE)
        WIN.blit(winner, (150, 200))
        pygame.mixer.Sound.play(WIN_SOUND)
        pygame.display.update()
        pygame.time.delay(5000)
        main()

    if yellow_health <= 0:
        winner = font2.render('Red Wins!', True, WHITE)
        WIN.blit(winner, (230, 200))
        pygame.mixer.Sound.play(WIN_SOUND)
        pygame.display.update()
        pygame.time.delay(5000)
        main()

def draw_to_screen(WIN, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    text = font.render('Health: ' + str(red_health), True, WHITE)
    text2 = font.render('Health: ' + str(yellow_health), True, WHITE)
    WIN.blit(text, (WIDTH - 110, 10))
    WIN.blit(text2, (10, 10))

    pygame.display.update()


def main():
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_health = 10
    yellow_health = 10
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULL:
                    pygame.mixer.Sound.play(BULLET_FIRE_SOUND)
                    bullet = pygame.Rect(red.x, red.y + SPACESHIP_WIDTH // 2, 10, 5)
                    red_bullets.append(bullet)

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULL:
                    pygame.mixer.Sound.play(BULLET_FIRE_SOUND)
                    bullet = pygame.Rect(yellow.x + 25, yellow.y + SPACESHIP_WIDTH // 2, 10, 5)
                    yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
                pygame.mixer.Sound.play(BULLET_HIT_SOUND)
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                pygame.mixer.Sound.play(BULLET_HIT_SOUND)

        draw_winner(red_health, yellow_health)
        bullets(red_bullets, yellow_bullets, red, yellow)
        keys = pygame.key.get_pressed()
        moving_SpaceShip(red, yellow, keys)
        print(red_bullets, yellow_bullets)
        draw_to_screen(WIN, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

if __name__ == "__main__":
    main()
