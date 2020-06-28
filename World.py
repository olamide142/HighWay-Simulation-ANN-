#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SPEED = 5
SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet2.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((288,512))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")



class Player(pygame.sprite.Sprite):
    genSurf = pygame.Surface((40, 75))
    genRect = genSurf.get_rect(center = (160, 520))

    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))
       
    def move(self):

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP] and not (self.rect.y <= 0):
            self.rect.move_ip(0, -7)
        if pressed_keys[K_DOWN] and not (self.rect.y >= 498):
            self.rect.move_ip(0,7)
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:  
                  self.rect.move_ip(-7, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(7, 0)

        Player.genRect = self.rect
         

class Enemy(pygame.sprite.Sprite):
    size = 0

    def __init__(self):
        super().__init__()
        Enemy.size += 1
        self.image = pygame.image.load("Enemy.png")
        self.surf = pygame.Surface((42/2, 70/2))
        if Enemy.size % 3 != 0:
            self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))
        else:
            self.rect = (Player.genRect.x, 0)




    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1  #Agent gets a reward
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


        

#Setting up Sprites
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5 
              if SPEED >= 20: #When speed gets too high reduce speed to 10
                  SPEED = 10
        if event.type == QUIT:
            pygame.quit()
            sys.exit()



    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))


    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):

          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)

        # Game Restarting
          P1 = Player()
          E1 = Enemy()

          #Creating Sprites Groups
          enemies = pygame.sprite.Group()
          enemies.add(E1)
          all_sprites = pygame.sprite.Group()
          all_sprites.add(P1)
          all_sprites.add(E1)
          SPEED = 4.5
          SCORE = 0

          #   pygame.quit()
        #   sys.exit()
    pygame.display.update()
    FramePerSec.tick(FPS)
    

