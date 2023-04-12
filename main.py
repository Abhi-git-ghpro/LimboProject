import pygame
from random import randint,choice
from sys import exit
pygame.init()

sky=pygame.image.load('background.png')
font=pygame.font.Font(None,50)
screen = pygame.display.set_mode((1500, 800))
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
        self.floor=300
        
        self.image=self.player_walk[self.player_index]
        self.rect=self.image.get_rect(midbottom=(80,500))
        self.gravity=0

    def floor_fun(self):
        if(self.rect.x>90 and self.rect.x<100):
            self.floor=600
        else:
            self.floor=500

    def jump(self,keys):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom==self.floor:
            self.gravity=-15
            self.rect.y+=self.gravity

    def right(self,keys):
        if self.rect.bottom<=500:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.rect.x+=5
                self.animation_state()

    def left(self,keys):
        if self.rect.bottom<=500:
            if keys[pygame.K_LEFT]:
                self.rect.x-=5
                self.animation_state()
            
    def movement(self):
        keys=pygame.key.get_pressed()
        self.jump(keys)
        self.right(keys)
        self.left(keys)

    def apply_gravity(self):
        if self.rect.bottom<self.floor:
            self.gravity+=1
            self.rect.y+=self.gravity

    def animation_state(self):
        if self.rect.bottom==self.floor:
            self.player_index+=0.2
            if self.player_index>len(self.player_walk):
                self.player_index=0
        self.image=self.player_walk[int(self.player_index)]

    def update(self):
        self.floor_fun()
        self.movement()
        self.apply_gravity()

class obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type=='enemy':
            enemy=pygame.image.load('obstacle.png')
            self.enemy_walk=[enemy]

        self.animation_index=0
        self.image=self.enemy_walk[self.animation_index]
        self.rect=self.image.get_rect(midbottom=(randint(900,1100),500))                              

    def animation_state(self):
        self.animation_index+=0.1
        if self.animation_index>len(self.enemy_walk):
            self.animation_index=0
        self.image=self.enemy_walk[int(self.animation_index)]

    def destory(self):
        if self.rect.x<=-100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x-=6
        self.destory()

def display_score():
    current_time=pygame.time.get_ticks()//1000-start_time
    score_surf=font.render(f'Score:{current_time}',False,"Blue")
    score_rect=score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def draw_floor():
    pygame.draw.line(screen,"white",(0,500),(102,500))
    pygame.draw.line(screen,"white",(102,500),(102,600))
    pygame.draw.line(screen,"white",(102,600),(162,600))
    pygame.draw.line(screen,"white",(162,600),(162,500))
    pygame.draw.line(screen,"white",(162,500),(1500,500))


#creating group of player sprite class
player=pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group=pygame.sprite.Group()

#Icon and title of game
pygame.display.set_caption("Limbo inspired test")

obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)

enemy_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(enemy_animation_timer,500)

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

        else:
            if event.type==obstacle_timer:
                obstacle_group.add(obstacle(choice(['enemy'])))

    if Running:
        score=display_score()
        draw_floor()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

    else:
        screen.fill("White")
        score_message=font.render(f'Your Score:{score}',False,"Pink")
        score_rect=score_message.get_rect(center=(400,500))
        game_message=font.render("Press space to start game",False,"Pink")
        game_message_rect=game_message.get_rect(center=(400,500))

        if score:
            screen.blit(score_message,score_rect)
        else:
            screen.blit(game_message,game_message_rect)
    pygame.display.update()
    clock.tick(60)