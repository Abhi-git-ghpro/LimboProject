import pygame
from sys import exit
pygame.init()

sky=pygame.image.load('background.png')
font=pygame.font.Font(None,50)
screen = pygame.display.set_mode((800, 400))
clock=pygame.time.Clock()
start_time=0
score=0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1=pygame.image.load('player1.png')
        player_walk_2=pygame.image.load('player2.png')
        self.player_walk=[player_walk_1,player_walk_2]
        self.player_index=0
        
        self.image=self.player_walk[self.player_index]
        self.rect=self.image.get_rect(midbottom=(80,300))
        self.gravity=0

    def jump(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom==300:
            self.gravity=-20
            self.rect.y+=self.gravity

    def right(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x+=5

    def left(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x-=5

    def apply_gravity(self):
        if self.rect.bottom<300:
            self.gravity+=1
            self.rect.y+=self.gravity

    def animation_state(self):
        self.player_index+=0.1
        if self.player_index>len(self.player_walk):
            self.player_index=0
        self.image=self.player_walk[int(self.player_index)]

    def update(self):
        self.jump()
        self.right()
        self.left()
        self.apply_gravity()
        self.animation_state()

def display_score():
    current_time=pygame.time.get_ticks()//1000-start_time
    score_surf=font.render(f'Score:{current_time}',False,"Blue")
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time

player=pygame.sprite.GroupSingle()
player.add(Player())

#Icon and title of game
pygame.display.set_caption("Limbo inspired test")

# playerImg = pygame.image.load('player1.png')
# playerX = 370
# playerY = 480
# playerX_change = 0
# playerY_change=0

# def player(x, y):
#     screen.blit(playerImg, (x, y))
running =True
jump=False
while(True):

 #   screen.fill((225,225,225))
    #screen.fill((0,0,0))
    screen.blit(sky,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        

        if running==False:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                Running =True
                start_time=pygame.time.get_ticks()//1000
        if event.type==pygame.KEYUP and event.key==pygame.K_SPACE:
            Running = False
            start_time=pygame.time.get_ticks()//1000
    if running:
        score=display_score()
        player.draw(screen)
        player.update()
        keys=pygame.key.get_pressed()

    else:
        screen.fill("White")
        score_message=font.render(f'Your Score:{score}',False,"Pink")
        score_rect=score_message.get_rect(center=(400,300))

        if score:
            screen.blit(score_message,score_rect)
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             playerX_change = -0.5
    #             playerX += playerX_change
    #         if event.key == pygame.K_RIGHT:
    #             playerX_change = 0.5
    #             playerX += playerX_change
    #         if event.key == pygame.K_SPACE:
    #             playerY_change=-1
    #             while(playerY!=350):
    #                 #time.sleep(0.1)
    #                 playerY+=playerY_change
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
    #             playerX_change = 0
    #         if event.key == pygame.K_SPACE:
    #             time.sleep(0.5)
    #             playerY=480
    # player(playerX,playerY)
    # playerX+=playerX_change
    # if playerX <= 0:
    #     playerX = 0
    # elif playerX >= 736:
    #     playerX = 736
    pygame.display.update()
    clock.tick(60)