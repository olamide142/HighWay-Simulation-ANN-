import sys
import random
from itertools import cycle
import pygame


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
# SCREEN_WIDTH = 400
# SCREEN_HEIGHT = 600
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SPEED = 20
SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet2.png")

#Create a white screen 
# DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF = pygame.display.set_mode((288,512))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('HighWay Simulation')



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-175))

    def up(self):
        if not self.rect.y <= 0:    
            self.rect.move_ip(0, -7)
    def down(self):
        if not self.rect.y >= 498:
            self.rect.move_ip(0,7)
    def left(self):
        if self.rect.left > 0:
            self.rect.move_ip(-7, 0)
    def right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(7, 0)

    def getRect(self):
        return self.rect

    def getSurf(self):
        return self.surf

P1 = Player()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))
        if SCORE % 3 == 1:
            self.rect = P1.getRect()
            self.surf = P1.getSurf()

    def move(self):
        global SCORE

        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1  #Agent gets a reward
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            return 1
        else:
            return 0.1


#Setting up Sprites
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

class GameState:
    global P1
    def __init__(self):
        self.crash = False
        self.score = 0

    def frame_step(self, input_actions):
        reward = 0.1
        terminal = False
        global SCORE
        global SPEED
        global all_sprites
        global E1
        global P1
        global enemies

        r = "tensor(1.)"

        #DO_NOTHING
        if str(input_actions[0]) == r:
            pass
        # UP
        if str(input_actions[1]) == r:
            P1.up()

        # DOWN
        if str(input_actions[2]) == r:
            P1.down()

        # RIGHT
        if str(input_actions[3]) == r:
            P1.right()

        # LEFT
        if str(input_actions[4]) == r:
            P1.left()

        # UP_RIGHT
        if str(input_actions[5]) == r:
            P1.up()
            P1.right()
        # UP_LEFT
        if str(input_actions[6]) == r:
            P1.up()
            P1.left()
        # DOWN_RIGHT
        if str(input_actions[7]) == r:
            P1.down()
            P1.right()
        # DOWN_LEFT
        if str(input_actions[8]) == r:
            P1.down()
            P1.left()

        self.score = SCORE
        # Cycles through all events occuring
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                  if SPEED <= 20:
                      SPEED += 0.5
                  else:
                      continue

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.blit(background, (0, 0))
        scores = font_small.render(str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            if entity != P1:
                if entity.move() == 1:
                    reward = 1

            # Add one more enemy
            # car half way
        if E1.rect.y == (SCREEN_HEIGHT / 2) and (len(all_sprites) < 4):
            E2 = Enemy()
            enemies.add(E2)
            all_sprites.add(E2)

        # To be ran if collision occurs between Player and Enemy
        # or  if the agent drives on the pedestrian lane
        if (pygame.sprite.spritecollideany(P1, enemies)):
        # or  (P1.rect.x > 315 or P1.rect.x <= 39):
            reward = -1
            terminal = True
        
            pygame.display.update()
            for entity in all_sprites:
                entity.kill()

            # Game Restarting
            P1 = Player()
            E1 = Enemy()
            # Creating Sprites Groups
            enemies = pygame.sprite.Group()
            enemies.add(E1)
            all_sprites = pygame.sprite.Group()
            all_sprites.add(P1)
            all_sprites.add(E1)
            SPEED = 10
            SCORE = 0

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        FramePerSec.tick(FPS)

        return image_data, reward, terminal