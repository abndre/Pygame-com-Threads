import pygame
import random
from threading import Thread
import time
import pdb
import os
import pygame.gfxdraw
from pygame.locals import *

pygame.init()
# Initialize Pygame

#Define Globals
TIMEGAME=0

PLAYERGLOBALX=0
PLAYERGLOBALY=0
get_punc=False
#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Current score
score = 0

# Current level
level = 1


# Set the height and width of the screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
DW_HALF = SCREEN_WIDTH / 2
DH_HALF = SCREEN_HEIGHT / 2

#Background
background_filename = 'Imagens/Fundo2.jpeg'
background = pygame.image.load(background_filename).convert()

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
block_list_enemy = pygame.sprite.Group()
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)


#Trhead TIME
class TimeThread(Thread):

    def __init__ (self):
          Thread.__init__(self)
          self.time=TIMEGAME


    def run(self):
        while not done:
            time.sleep(1)
            self.time = self.time +1

    def get(self):
        return self.time


timegame=TimeThread()
timegame.start()
#End Thread TIME

#Thread Effect
class soundPunch(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        BackgroundSound = pygame.mixer.Sound( os.path.join( "Sons", "AUU.ogg") )
        BackgroundSound.play(0)
#Thread Effect


#Thread Sound Fase
class SoundThread(Thread):

    def __init__ (self):
          Thread.__init__(self)

    def run(self):
        BackgroundSound = pygame.mixer.Sound( os.path.join( "Sons", "bloodRUNSPEED.ogg") )
        BackgroundSound.play(-1)

soundf=SoundThread()
soundf.start()
#Thread Sound Fase


#Thread Enemy move-> this is away to player
class ThreadEnemy(Thread):
    def __init__(self):
            Thread.__init__(self)
            self.block = Block("Imagens/BacNeutropq.png", BLACK)
            # Set a random location for the block
            self.block.rect.x = random.randrange(30,SCREEN_WIDTH-30)
            self.block.rect.y = random.randrange(30,SCREEN_HEIGHT-30)
            self.block.angle = random.randrange(360)
            self.block.angle_change = random.randrange(-1, 2)
            if random.randrange(1,3)%2:
                self.timesleep=0.01
                self.tipe=1
            else:
                self.timesleep=0.05
                self.tipe=2

            # Add the block to the list of objects
            block_list.add(self.block)
            all_sprites_list.add(self.block)

    def run(self):
        #enemy move against the player
        while not done:
            time.sleep(self.timesleep)

            if self.block.rect.x > (SCREEN_WIDTH-40) or self.block.rect.x < 5:
                pass
            elif self.block.rect.y > (SCREEN_HEIGHT-40) or self.block.rect.y < 5:
                pass
            else:
                if self.block.rect.x > PLAYERGLOBALX:
                    self.block.rect.x = self.block.rect.x +1
                else:
                    self.block.rect.x = self.block.rect.x -1

                if self.block.rect.y > PLAYERGLOBALY:
                    self.block.rect.y = self.block.rect.y +1
                else:
                    self.block.rect.y = self.block.rect.y -1
#Thread Enemy move


#Thread Enemy move 2 -> this is go to player
class EnemyThreadEnemy(Thread):
    def __init__(self):
            Thread.__init__(self)
            self.block = Block("Imagens/BacEnemy_game.png", BLACK)
            # Set a random location for the block
            self.block.rect.x = random.randrange(30,SCREEN_WIDTH-30)
            self.block.rect.y = random.randrange(30,SCREEN_HEIGHT-30)
            self.block.angle = random.randrange(360)
            self.block.angle_change = random.randrange(-1, 2)

            self.timesleep=0.01
            # Add the block to the list of objects
            block_list_enemy.add(self.block)
            all_sprites_list.add(self.block)

    def run(self):
        #enemy move against the player
        while not done:
            time.sleep(self.timesleep)

            if self.block.rect.x > PLAYERGLOBALX:
                self.block.rect.x = self.block.rect.x -1
            else:
                self.block.rect.x = self.block.rect.x +1

            if self.block.rect.y > PLAYERGLOBALY:
                self.block.rect.y = self.block.rect.y -1
            else:
                self.block.rect.y = self.block.rect.y +1




#class for creath enemy and player instance
class Block(pygame.sprite.Sprite):

    def __init__(self, filename, colorkey):
        # Call the parent class (Sprite) constructor
        super(Block,self).__init__()


        self.original_image = pygame.image.load(filename).convert()
        self.image = self.original_image


        self.image.set_colorkey(colorkey)


        self.rect = self.image.get_rect()

        self.angle = 0
        self.angle_change = 0

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.angle += self.angle_change
        self.angle = self.angle % 360


#Thread colision, socre, creat enemy
class Colistion(Thread):

    def __init__(self):
            Thread.__init__(self)

    def run(self):
        global score,level,block_list,block_list_enemy,get_punc
        while not done:
            blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
            for block in blocks_hit_list:
                score += 1


            blocks_hit_list = pygame.sprite.spritecollide(player, block_list_enemy, False)
            for block in blocks_hit_list:
                score -= 1
                get_punc=True
                time.sleep(0.5)
                get_punc=False

            if len(block_list) <= 0:
                level+=1
                instancelist = [ ThreadEnemy() for i in range(level)]
                for i in instancelist:
                    i.start()



class Player(pygame.sprite.Sprite):
    def __init__(self, filename, colorkey):
        # Call the parent class (Sprite) constructor
        super(Player,self).__init__()


        self.original_image = pygame.image.load(filename).convert()
        self.image = self.original_image


        self.image.set_colorkey(colorkey)

        self.rect = self.image.get_rect()


        self.x=PLAYERGLOBALX
        self.y=PLAYERGLOBALY
        self.h=self.rect.h
        self.w=self.rect.w






# Create a player block
player = Player("Imagens/BacPlayerpq.png", BLACK)
all_sprites_list.add(player)

enemy =EnemyThreadEnemy()
enemy.start()

colision=Colistion()
colision.start()


XX=0
current_scale=1
# -------- Main Program Loop -----------
while not done:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

    pos = pygame.mouse.get_pos()


    player.rect.centerx = pos[0]
    player.rect.centery = pos[1]

    PLAYERGLOBALX=pos[0]
    PLAYERGLOBALY=pos[1]



    all_sprites_list.update()


    value= background.get_rect().width
##    screen.blit(background, (rel_x-background.get_rect().width, 0))
    if XX<-1*value:
        XX=0
    screen.blit(background, (XX, 0))
    screen.blit(background, (XX+value, 0))
    XX-=1
    if get_punc:
        screen.fill(RED)

    all_sprites_list.draw(screen)

    text = font.render("Score: "+str(score), True, WHITE)
    screen.blit(text, [10, 10])

    text = font.render("Level: "+str(level), True, WHITE)
    screen.blit(text, [10, 40])

    text = font.render("Tempo: "+str(timegame.get()),True, WHITE)
    screen.blit(text,[10,70])

    if get_punc:
        text = font.render("Punch!",True,WHITE)
        PLAYERGLOBALXGET=PLAYERGLOBALX
        PLAYERGLOBALYGET=PLAYERGLOBALY
        screen.blit(text, [PLAYERGLOBALXGET, PLAYERGLOBALYGET])

    if get_punc:
        getsound=soundPunch()
        getsound.start()


    pygame.display.flip()

    clock.tick(60)


pygame.quit()