import pygame
import time
pygame.init()

screen = pygame.display.set_mode((800, 600))


#Icon and title of game
pygame.display.set_caption("Limbo inspired test")

playerImg = pygame.image.load('player1.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change=0

def player(x, y):
    screen.blit(playerImg, (x, y))
running =True
while(running):

    screen.fill((225,225,225))
    #screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
                playerX += playerX_change
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
                playerX += playerX_change
            if event.key == pygame.K_SPACE:
                playerY_change=-1
                while(playerY!=350):
                    #time.sleep(0.1)
                    playerY+=playerY_change
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                time.sleep(0.5)
                playerY=480
    player(playerX,playerY)
    playerX+=playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    pygame.display.update()