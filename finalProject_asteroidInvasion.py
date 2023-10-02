# Filename: finalProject_asteroidInvasion.py
# Author: Alex Yao
# Date Created: November 11, 2020
# Description: Welcome to Asteroid Invasion. The goal of the game is to gain 5000 points.
# You need to dodge all the asteroids that will constantly be coming until you win/ lose.
# You will move around using your arrow keys (up, down, left, right). Be careful because you only have one life.

# Import & start pygame
import pygame, sys
import random
from pygame.locals import *
from os import path
pygame.init()
pygame.mixer.init()

# Definitions : Constants, variables and classes

# Constants: BLACK, BLUE, GREEN, RED, WHITE
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

# Variables: clock, countDownNum, pygame GUI components (screenWidth, screenHeight, screen, background, my_font, rulesDisplay1, rulesDisplay2, rulesDisplay3, rulesDisplay4, rulesDisplay5,rulesDisplay6, rulesDisplay7, rulesDisplay8), sound components (sound_dir), list (playSoundEffects), screen control components (keepGoingRules, keepGoingGame, spaceShipDies), Game Components (score)
clock = pygame.time.Clock()
countDownNum=8

#pygame GUI components
screenWidth=800
screenHeight=600
screen = pygame.display.set_mode((screenWidth,screenHeight))
background=pygame.image.load("space.jpg").convert() #background image
# set up rules
my_font = pygame.font.SysFont("comicsansms", 28)
rulesDisplay1 = my_font.render("Welcome to Asteroid Invasion!", True, WHITE)
my_font = pygame.font.SysFont("comicsansms", 18)
rulesDisplay2 = my_font.render("Rules are listed below:", True, WHITE)
rulesDisplay3 = my_font.render("1. Your mission is to avoid being hit by an asteroid.", True, WHITE)
rulesDisplay4 = my_font.render("2. Dodge the asteroids using your arrow keys (up, down, left, right).", True, WHITE)
rulesDisplay5 = my_font.render("4. You need to get a total of 250 points to beat the game. Points are accumulated by moving.", True, WHITE)
rulesDisplay6 = my_font.render("6. You only have one life so be careful.", True, WHITE)
rulesDisplay7 = my_font.render("Tip: Stay closer to the bottom of the screen so you have more time to react", True, WHITE)
my_font = pygame.font.SysFont("comicsansms", 22)
rulesDisplay8 = my_font.render("Press <s> to start", True, WHITE)


#sound components
sound_dir=path.join(path.dirname(__file__),"sound")
pygame.mixer.music.load("backgroundMusic.mp3") #used for music files

#list
playSoundEffects=[]     # list that contains sound effects
for sound in ["soundEffect1.wav","soundEffect2.wav","soundEffect3.wav"]:
    playSoundEffects.append(pygame.mixer.Sound(path.join(sound_dir,sound)))

#screen control components
keepGoingRules = True
keepGoingGame = True
spaceShipDies=True

# Game Components
score=0


# Sets up the score that will be displayed
textFont=pygame.font.match_font("comicsansms")
def draw_text (surf, text, size,x ,y):
    font=pygame.font.Font(textFont,size)
    text_surface=font.render(text, True, WHITE)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface, text_rect)

# Classes: SpaceShip and Asteroid

# SpaceShip is a sprite that moves using the arrow keys.
class SpaceShip(pygame.sprite.Sprite):
    # init() sets up its own self variables based on:  image, centerx, centery, speedx, speedy
    def __init__(self):
       pygame.sprite.Sprite.__init__(self) #construct the parent component
       self.image=pygame.image.load("spaceShip.png")
       self.rect=self.image.get_rect()     #loads the rect from the image
       self.rect.centerx =400
       self.rect.centery=450
       self.speedx=0 #speed when it moves left and right
       self.speedy=0 #speed when it moves up and down

    # update () modifies its movement and speed when an arrow key is pressed. Also modifies where the spaceship can and can't go on the screen.
    def update(self):
        self.speedx=0
        keyPressed=pygame.key.get_pressed()
        if keyPressed[pygame.K_LEFT]: #left arrow key
            self.speedx=-4
        if keyPressed[pygame.K_RIGHT]: #right arrow key
            self.speedx=4
        self.rect.x=self.rect.x+self.speedx

        # sets where the spaceShip can or can't go (left and right)
        if self.rect.right> screenWidth:
            self.rect.right=screenWidth
        if self.rect.left<0:
            self.rect.left=0
            self.speedx=0

        self.speedy=0
        keyPressed=pygame.key.get_pressed()
        if keyPressed[pygame.K_UP]: #up arrow key
            self.speedy=-2
        if keyPressed[pygame.K_DOWN]: #down arrow key
            self.speedy=2
        self.rect.y=self.rect.y+self.speedy

        #sets where the spaceship can or can't go (up and down)
        if self.rect.y>520:
            self.rect.y=520
        if self.rect.bottom<200:
            self.rect.bottom=200
# end of class spaceShip and update()


# Asteroid is a sprite that moves from the top to the bottom of the screen.
class Asteroid(pygame.sprite.Sprite):
    # init() sets up its own self variables based on:  image, x, y, speedy
    def __init__(self):
       pygame.sprite.Sprite.__init__(self) #construct the parent component
       self.image=pygame.image.load("asteroid.png")
       self.rect=self.image.get_rect()
       self.rect.x=random.randrange(0,760) #random x coordinate from 0 to 760
       self.rect.y= random.randrange(-150,-80) #random y coordinate from -150 to -80
       self.speedy=random.randrange(1,4) #random speed from 1 to 4


    # update() modifies the speed and the range where the asteroids will come from.

    def update(self):

        self.rect.y=self.rect.y+self.speedy
        if self.rect.top>screenHeight+1:
            self.rect.x=random.randrange(0,760)
            self.rect.y=random.randrange(-80,0)
            self.speedy=random.randrange(1,4)
# end of class Asteroid and update()

# Pygame commands
# Setup pygame & screen commands
pygame.display.set_caption("Asteroid Invasion")
screen.fill(WHITE)                  # make buffer screen white

pygame.mixer.music.play(-1)  #play background music repeatedly

# start of keepGoingRules
while keepGoingRules:  # Display Rules screen until user closes it or if they press <s>
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoingRules = False
            sys.exit()  #exit the program
            screen.blit(background, [0,0])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  #If the user presses <s> the game will start
                random.choice(playSoundEffects).play() #When the user presses <s> to start the game, it will play a sound effect randomly chosen from the playSoundEffects list.

                pygame.display.set_caption("Asteroid Invasion")
                keepGoingRules = False
            #end of if event.key
        #end of if event
    #end for event

    #display the rules to the screen
    screen.blit(background, (0, 0))
    screen.blit(rulesDisplay1, (20, 20))
    screen.blit(rulesDisplay2, (20, 90))
    screen.blit(rulesDisplay3, (20, 150))
    screen.blit(rulesDisplay4, (20, 190))
    screen.blit(rulesDisplay5, (20, 230))
    screen.blit(rulesDisplay6, (20, 270))
    screen.blit(rulesDisplay7, (20, 310))
    screen.blit(rulesDisplay8, (20, 350))
    pygame.display.flip()
#end while keepGoingRules


allSprites= pygame.sprite.Group() #group for all the sprites
spaceShip=SpaceShip()
allSprites.add((spaceShip)) #adds spaceShip to allSprites
asteroidsGroup= pygame.sprite.Group() #group for asteroids

# display the asteroids
for i in range(10):
    asteroids=Asteroid()
    allSprites.add(asteroids)
    asteroidsGroup.add(asteroids)



my_font=pygame.font.SysFont("comicsansms",44)

# start of keepGoingGame
while keepGoingGame:
    screen.blit(background, (0, 0))    #display screen until user closes it
    for event in pygame.event.get():
        score = score + 1
        if event.type == pygame.QUIT:
            keepGoingGame = False
            sys.exit()  #exit the program

    allSprites.update() #updates all the sprites

    collision=pygame.sprite.spritecollide(spaceShip,asteroidsGroup, False)  # if an asteroid hits the spaceShip
    if (collision): # If the user dies before 5000 point is earned, they lose.
        for i in range(countDownNum,0,-1):  # counts down from 8 before closing the program
            # Display to temporary buffer screen
            answerText1="You Lose!"
            answerText2="Program closes in: "+str(i)
            answer_display1=my_font.render(answerText1, True, WHITE)
            answer_display2=my_font.render(answerText2, True, WHITE)
            screen.blit(background, (0, 0))
            screen.blit(answer_display1,(300,170))
            screen.blit(answer_display2,(200,260))

            # Display the temporary buffer to the visible screen
            pygame.display.flip()
            pygame.time.wait(1000)
            keepGoingGame=False

    if (score==250): # If the user reaches a score of 5000, they win.
        for i in range(countDownNum,0,-1): # counts down from 8 before closing the program
            # Display to temporary buffer screen
            answerText3="You Win!"
            answerText4="250 points earned"
            answerText5="Program closes in: "+str(i)
            answer_display3=my_font.render(answerText3, True, WHITE)
            answer_display4=my_font.render(answerText4, True, WHITE)
            answer_display5=my_font.render(answerText5, True, WHITE)
            screen.blit(background, (0, 0))
            screen.blit(answer_display3,(300,170))
            screen.blit(answer_display4,(200,260))
            screen.blit(answer_display5,(200,350))

            # Display the temporary buffer to the visible screen
            pygame.display.flip()
            pygame.time.wait(1000)
            keepGoingGame=False
        #end of if event
    #end for event

    allSprites.draw(screen) #draws all the sprites onto the visible screen
    draw_text(screen, str(score),20, 50,50) #draws the score onto the visible screen
    clock.tick(120) #updates graphics up to 120 times per second
    pygame.display.flip() #Display temporary buffer to the visible screen
#end of while keepGoingGame
