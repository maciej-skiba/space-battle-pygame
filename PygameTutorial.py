import pygame
import os

#General

WINDOW_WIDTH, WINDOW_HEIGHT = 900, 500

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Tutorial")

WHITE = (255, 255, 255)
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WINDOW_WIDTH, WINDOW_HEIGHT))

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60

#end General

#Spaceships

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

VELOCITY = 5
BULLET_VELOCITY = 7

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#end Spaceships

def Yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w]:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s]:
        yellow.y += VELOCITY
    if keys_pressed[pygame.K_a] and yellow.x > yellow.height / 2:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x < WINDOW_WIDTH / 2 - yellow.width:
        yellow.x += VELOCITY

def Red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP]:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN]:
        red.y += VELOCITY
    if keys_pressed[pygame.K_LEFT] and red.x > WINDOW_WIDTH / 2 + red.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x < WINDOW_WIDTH - red.height * 3/2:
        red.x += VELOCITY

def Draw_window(yellow, red, yellow_bullets, red_bullets):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(YELLOW_SPACESHIP,
        (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,
        (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def Handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > WINDOW_WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def Main():
    yellow = pygame.Rect(
        WINDOW_WIDTH / 3 - SPACESHIP_HEIGHT/2,
        WINDOW_HEIGHT / 2 - SPACESHIP_WIDTH/2,
        SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(
        WINDOW_WIDTH * 2 / 3 - SPACESHIP_HEIGHT/2,
        WINDOW_HEIGHT / 2 - SPACESHIP_WIDTH/2,
         SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)                     #controls speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #if you click [X]
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.height, yellow.y + yellow.width // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x - red.height, red.y + red.width // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

        print(yellow_bullets, red_bullets)

        keys_pressed = pygame.key.get_pressed()  #first method of handling keyboard input

        Yellow_movement(keys_pressed, yellow)
        Red_movement(keys_pressed, red)

        Handle_bullets(yellow_bullets, red_bullets, yellow, red)

        Draw_window(yellow, red, yellow_bullets, red_bullets)

    pygame.quit()

if __name__ == "__main__":          #if filename you're in = main, run main().
    Main()                          #so it won't run if imported as module