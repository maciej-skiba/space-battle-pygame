import pygame
import os
from typing import List

pygame.font.init()
pygame.mixer.init()

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

HEALTH_FONT = pygame.font.SysFont("Corbel" , 40)
WINNER_FONT = pygame.font.SysFont("Corbel", 100)

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
BULLET_YELLOW_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser_gun_left.wav'))
BULLET_RED_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser_gun_right.wav'))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#end Spaceships

def Yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y < WINDOW_HEIGHT - SPACESHIP_WIDTH:
        yellow.y += VELOCITY
    if keys_pressed[pygame.K_a] and yellow.x > yellow.height / 2:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x < WINDOW_WIDTH / 2 - yellow.width:
        yellow.x += VELOCITY

def Red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y < WINDOW_HEIGHT - SPACESHIP_WIDTH:
        red.y += VELOCITY
    if keys_pressed[pygame.K_LEFT] and red.x > WINDOW_WIDTH / 2 + red.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x < WINDOW_WIDTH - red.height * 3/2:
        red.x += VELOCITY

def Draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    # Background
    WIN.blit(SPACE, (0, 0) )

    # Health
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE )
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE )

    WIN.blit(yellow_health_text, (10, WINDOW_HEIGHT//20))
    WIN.blit(red_health_text, (WINDOW_WIDTH - 148, WINDOW_HEIGHT//20))

    # Spaceships
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def Handle_bullets(yellow_bullets: List[pygame.Rect], red_bullets: list, yellow: pygame.Rect, red: pygame.Rect):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WINDOW_WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def Draw_Winner(text, keys_pressed):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WINDOW_WIDTH/2 - draw_text.get_width()/2, WINDOW_HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()

    pygame.time.delay(5000) #in ms

    Main()

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

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    pygame.event.clear()
    winner_text = ""

    while run:
        clock.tick(FPS)                     #controls speed of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #if you click [X]
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(yellow.x + yellow.height, yellow.y + yellow.width // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_YELLOW_SOUND.play()
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x - red.height, red.y + red.width // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_RED_SOUND.play()

            winner_text = ""
            if event.type == YELLOW_HIT:
                print("Yellow hit")
                yellow_health -= 1
                if yellow_health <= 0:
                    winner_text = "Red Wins!"
            if event.type == RED_HIT:
                print("Red hit")
                red_health -= 1
                if red_health <= 0:
                    winner_text = "Yellow Wins!"

        keys_pressed = pygame.key.get_pressed()  #first method of handling keyboard input

        Yellow_movement(keys_pressed, yellow)
        Red_movement(keys_pressed, red)

        Handle_bullets(yellow_bullets, red_bullets, yellow, red)

        Draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

        if(winner_text != ""):
            yellow_bullets = []
            red_bullets = []
            Draw_Winner(winner_text, keys_pressed)

    pygame.quit()

if __name__ == "__main__":          #if filename you're in = main, run main().
    Main()                          #so it won't run if imported as module