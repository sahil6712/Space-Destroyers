import pygame
import random
import math

import pygame.locals
from pygame import mixer

#initialize the pygame
pygame.init()

# Create the Screen
screen = pygame.display.set_mode((800,600))

#background 
background = pygame.image.load('background.png')

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Destroyers")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)



#Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

#bullet 
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready" 

#Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX  = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(90,180,207))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("Game Over",True,(234,135,45))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImg,(x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletY,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False

#game loop fps number of times game loop gona run in 1 second 1 iteration == 1 frame. when things update
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    #getting all the events
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

        # If keystroke is pressed
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT):
                playerX_change = -2
            if(event.key == pygame.K_RIGHT):
                playerX_change = 2
            if(event.key == pygame.K_SPACE):
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if(event.type == pygame.KEYUP):
            if(event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                playerX_change = 0
    # Player Movement
    playerX += playerX_change
    if(playerX<=0):
        playerX = 0
    elif(playerX>=736):
        playerX = 736
    #Enemy movement
    for i in range(num_of_enemies):
        #Game over 
        if(enemyY[i]>440):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if(enemyX[i]<=0):
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif(enemyX[i]>=736):
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i] 


    #bullet movement
    if bulletY<=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    #collision 
    for i in range(num_of_enemies):
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_state = 'ready'
            bulletY = 480
            score_value += 1
            
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
    player(playerX, playerY)
    show_score(textX,textY)
    for i in range(num_of_enemies):
        enemy(enemyX[i],enemyY[i],i)
    pygame.display.update()

