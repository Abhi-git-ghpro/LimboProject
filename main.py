import pygame
#Comment
from random import randint,choice
from sys import exit
pygame.init()

sky=pygame.image.load('limbo_bg.jpg')
font=pygame.font.Font(None,50)
screen = pygame.display.set_mode((1500, 800))
clock=pygame.time.Clock()
start_time=0
score=0
collision_cart=300


#creating player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1=pygame.image.load('player1.png').convert_alpha()
        player_walk_1.set_colorkey((225,0,0))
        player_walk_2=pygame.image.load('player2.png').convert_alpha()
        player_walk_2.set_colorkey((225,0,0))
        player_hold=pygame.image.load('player_hold.png').convert()
        self.player_walk=[player_walk_1,player_walk_2]
        self.player_index=0
        self.floor=300
        
        self.image=self.player_walk[self.player_index]
        self.rect=self.image.get_rect(midbottom=(80,500))
        self.gravity=0

        #Improving the jump mechanics
        self.jumping=False
    def floor_fun(self):
        if(self.rect.x>90 and self.rect.x<100):
            self.floor=600
        elif pygame.sprite.spritecollide(self,cart1,False):
            hit=pygame.sprite.spritecollide(self,cart1,False)
            keys=pygame.key.get_pressed()
            if keys[pygame.K_UP] and (keys[pygame.K_RIGHT]) or (keys[pygame.K_UP] and keys[pygame.K_LEFT]) :
                pass
            else :self.floor=hit[0].rect.top+1
        elif(self.rect.right>500 and self.rect.left<600 and self.rect.y<300):
            self.floor=300
        else:
            self.floor=500

    def jump(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom==self.floor and not self.jumping:
            self.jumping=True
            self.gravity=-16.5
            self.rect.y+=self.gravity

    def right(self,keys):
            if self.rect.right>500 and self.rect.right<600 and self.rect.bottom>350:
                pass
            elif self.rect.bottom<=500:
                keys=pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    self.rect.x+=5
                    self.animation_state()
    def left(self,keys):

        #print(self.rect.left)
        if self.rect.bottom<=500:
            if self.rect.left>500 and self.rect.left<590 and self.rect.bottom>350: pass
            elif keys[pygame.K_LEFT]:
                self.rect.x-=5
                self.animation_state()
            
    def movement(self):
        keys=pygame.key.get_pressed()
        self.right(keys)
        self.left(keys)

    def cancel_jump(self):
        if self.jumping:
            if self.gravity<-2:
                self.gravity=-2
    def apply_gravity(self):
        if self.rect.bottom<self.floor:
            self.gravity+=1
            self.rect.y+=self.gravity
    def landing(self):
        if self.rect.bottom==self.floor:
            self.jumping=False

    def animation_state(self):
        if self.rect.bottom==self.floor:
            self.player_index+=0.2
            if self.player_index>len(self.player_walk):
                self.player_index=0
        self.image=self.player_walk[int(self.player_index)]
    def game_over(self):
        if self.rect.bottom>600:
            global Running,collision_cart
            Running=False
            self.rect.midbottom=(80,500)
            collision_cart=300

    def collsion_cart_player(self):
        global collision_cart
        if (self.floor==500 and self.rect.x-collision_cart<=128 and event.type==pygame.KEYDOWN and event.key==pygame.K_UP ):
            keys=pygame.key.get_pressed()
            if (keys[pygame.K_RIGHT] and keys[pygame.K_UP]):
                collision_cart=self.rect.x+64
            if (keys[pygame.K_LEFT] and keys[pygame.K_UP]):
                collision_cart=self.rect.right -64
    def collision_2(self):
        if self.rect.colliderect(cart1.sprite):
            keys=pygame.key.get_pressed()
            if (keys[pygame.K_RIGHT] and keys[pygame.K_i]):
                collision_cart=self.rect.x+64
            if (keys[pygame.K_LEFT] and keys[pygame.K_i]):
                collision_cart=self.rect.right -64    
                print("collided")


    def update(self):
        if self.rect.bottom>self.floor:
            self.rect.bottom=self.floor
        self.floor_fun()
        self.movement()
        self.apply_gravity()
        self.game_over()
        self.collsion_cart_player()
        self.collision_2()
        self.landing()
  
class cart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('cart.png').convert_alpha()
        self.rect=self.image.get_rect(midbottom=(collision_cart,500))

    def makethismove(self):
        global collision_cart
        self.rect.x=collision_cart
    
def display_score():
    current_time=pygame.time.get_ticks()//1000-start_time
    score_surf=font.render(f'Score:{current_time}',False,"Blue")
    score_rect=score_surf.get_rect(center=(750,400))
    screen.blit(score_surf,score_rect)
    return current_time

def draw_floor():
    #ditch
    pygame.draw.line(screen,"white",(0,500),(102,500))
    pygame.draw.line(screen,"white",(102,500),(102,600))
    pygame.draw.line(screen,"white",(102,600),(160,600))
    pygame.draw.line(screen,"white",(160,600),(160,500))
    pygame.draw.line(screen,"white",(160,500),(1500,500))
    
    #tower
    pygame.draw.line(screen,"white",(500,500),(500,300))
    pygame.draw.line(screen,"white",(500,300),(600,300))
    pygame.draw.line(screen,"white",(600,300),(600,500))
    #hava mein square
    pygame.draw.line(screen,"white",(748,300),(748,200))
    pygame.draw.line(screen,"white",(748,200),(848,200))
    pygame.draw.line(screen,"white",(848,200),(848,300))
    pygame.draw.line(screen,"white",(848,300),(748,300))


     
#creating group of player sprite class
player=pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group=pygame.sprite.Group()
#cart
cart1=pygame.sprite.GroupSingle()
cart1.add(cart())

#Icon and title of game
pygame.display.set_caption("Limbo inspired test")

enemy_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(enemy_animation_timer,500)

Running =False  #keeps track of state of game
while(True):

    screen.fill((200,0,50))
    #screen.blit(sky,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.sprite.jump()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE:
                player.sprite.cancel_jump()     #Cancel the jump when release space button
        
        #intro page
        if Running==False:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                Running =True
                start_time=pygame.time.get_ticks()//1000

    if Running:
        score=display_score()
        draw_floor()
        player.draw(screen)
        player.update()
        cart1.draw(screen)
        cart1.sprite.makethismove()
      
        obstacle_group.draw(screen)
        obstacle_group.update()

    

    else:

        screen.fill("White")
        score_message=font.render(f'Your Score:{score}',False,"Pink")
        score_over=font.render(f'Game Over',False,"Red")
        game_over_rect=score_over.get_rect(center=(750,200))
        score_rect=score_message.get_rect(center=(750,400))
        game_message=font.render("Press space to start game",False,"Pink")
        game_message_rect=game_message.get_rect(center=(750,400))

        if score:
            
            screen.blit(score_over,game_over_rect)
            pygame.time.delay(1* 500)
            screen.blit(score_message,score_rect)
            pygame.time.delay(1* 500)
            
        else:
            screen.blit(game_message,game_message_rect)
    pygame.display.update()
    clock.tick(60)
