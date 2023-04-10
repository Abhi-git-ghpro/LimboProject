import pygame
from sys import exit
pygame.init()

sky=pygame.image.load('background.png')
font=pygame.font.Font(None,50)
screen = pygame.display.set_mode((800, 400))
clock=pygame.time.Clock()
start_time=0
score=0

#creating player sprite class
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

    def jump(self,keys):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom==300:
            self.gravity=-20
            self.rect.y+=self.gravity

    def right(self,keys):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x+=5
            self.animation_state()

    def left(self,keys):
        if keys[pygame.K_LEFT]:
            self.rect.x-=5
            self.animation_state()
        
    def movement(self):
        keys=pygame.key.get_pressed()
        self.jump(keys)
        self.right(keys)
        self.left(keys)

    def apply_gravity(self):
        if self.rect.bottom<300:
            self.gravity+=1
            self.rect.y+=self.gravity

    def animation_state(self):
        if self.rect.bottom==300:
            self.player_index+=0.2
            if self.player_index>len(self.player_walk):
                self.player_index=0
        self.image=self.player_walk[int(self.player_index)]

    def update(self):
        self.movement()
        self.apply_gravity()

def display_score():
    current_time=pygame.time.get_ticks()//1000-start_time
    score_surf=font.render(f'Score:{current_time}',False,"Blue")
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time

#creating group of player sprite class
player=pygame.sprite.GroupSingle()
player.add(Player())

#Icon and title of game
pygame.display.set_caption("Limbo inspired test")


Running =False  #keeps track of state of game
while(True):
    screen.blit(sky,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        #intro page
        if Running==False:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                Running =True
                start_time=pygame.time.get_ticks()//1000

    if Running:
        score=display_score()
        player.draw(screen)
        player.update()

    else:
        screen.fill("White")
        score_message=font.render(f'Your Score:{score}',False,"Pink")
        score_rect=score_message.get_rect(center=(400,300))
        game_message=font.render("Press space to start game",False,"Pink")
        game_message_rect=game_message.get_rect(center=(400,300))

        if score:
            screen.blit(score_message,score_rect)
        else:
            screen.blit(game_message,game_message_rect)
    pygame.display.update()
    clock.tick(60)