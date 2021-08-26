import pygame
from pygame import mixer
import warnings
import math
import random

warnings.filterwarnings("ignore", category=DeprecationWarning)
# initialize pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# create title and icon
pygame.display.set_caption("Space Race")
icon = pygame.image.load("project.png")
pygame.display.set_icon(icon)

# create a background
background = pygame.image.load("space.jpg")

# background music
mixer.music.load("background_music.mp3")
mixer.music.play(-1)
# player
playerimg = pygame.image.load("spaceship3.png")
playerx = 370
playery = 480
playerx_change = 0

# enemy
blastimg = pygame.image.load("flame.png")
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
no_of_enemy = 6
for i in range(no_of_enemy):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(2.5)
    enemyy_change.append(40)

# bullet
bulletimg = []
bulletx = []
bullety = []
bullet_state = []
bulletx_change = 0
bullety_change = 10

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


# this is to show the collision fire
def fire(x, y):
    screen.blit(blastimg, (x, y))


# To show the score the text
def show_text(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# To display the spaceship
def player(x, y):
    screen.blit(playerimg, (x, y))


# To display the enemy
def enemy(x, y, h):
    screen.blit(enemyimg[h], (x, y))


# To display the bullet
def fire_bullet(x, y, h):
    global bullet_state
    bullet_state[h] = "fire"
    screen.blit(bulletimg[h], (x + 16, y + 10))


# To check if collision occurs
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


# To show game over text
def game_over():
    game_over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


# game loop
running = True
while running:

    # fill the screen with black colour
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))
    # check for the event happen in pygame
    for event in pygame.event.get():

        # check if exit key is pressed
        if event.type == pygame.QUIT:
            running = False

        # check if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -3
            if event.key == pygame.K_RIGHT:
                playerx_change = 3
            if event.key == pygame.K_SPACE:
                bulletimg.append(pygame.image.load("bullet2.png"))
                bulletx.append(0)
                bullety.append(480)
                bullet_state.append("ready")
                for i in range(len(bulletimg)):
                    if bullet_state[i] == "ready":
                        bullet_sound = mixer.Sound("shoot.wav")
                        bullet_sound.play()
                        bulletx[i] = playerx
                        fire_bullet(bulletx[i], bullety[i], i)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # check the player boundary
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # check the enemy boundary
    for i in range(no_of_enemy):

        # game over
        if enemyy[i] > 440:
            for j in range(no_of_enemy):
                enemyy[j] = 2000
            game_over()
            break

        # enemy movement
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 2.5
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -2.5
            enemyy[i] += enemyy_change[i]

        # collision detection
        for j in range(len(bulletimg)):
            try:
                collision = is_collision(enemyx[i], enemyy[i], bulletx[j], bullety[j])
                if collision:
                    fire(enemyx[i], enemyy[i])
                    collision_sound = mixer.Sound("explosion.wav")
                    collision_sound.play()
                    bullety.pop(j)
                    bulletx.pop(j)
                    bulletimg.pop(j)
                    bullet_state.pop(j)
                    score_value += 1
                    enemyx[i] = random.randint(0, 735)
                    enemyy[i] = random.randint(50, 150)
            except:
                pass

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    for i in range(len(bulletimg)):
        try:
            if bullety[i] < 0:
                bulletimg.pop(i)
                bullety.pop(i)
                bulletx.pop(i)
                bullet_state.pop(i)
        except:
            pass

    # To make bullet movement
    for i in range(len(bulletimg)):
        if bullet_state[i] == "fire":
            fire_bullet(bulletx[i], bullety[i], i)
            bullety[i] -= bullety_change

    # To change players x coordinate
    playerx += playerx_change
    player(playerx, playery)
    show_text(textx, texty)
    pygame.display.update()
