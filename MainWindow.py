import os
import math
import pygame
from pygame.locals import *
import random

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
WORLD_SPEED = 1
WINDOW_TITLE = "Flappy"

def load_sprite(imageName):
    "load an image and return a Surface"
    fullPath = os.path.join("data", "images", imageName)

    try:
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load(fullPath)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.topleft = (0, 0)
        

    except pygame.error, message:
        print "Cannot load image: %s" % (fullPath)
        raise SystemExit, message

    return sprite

class Pointer(pygame.sprite.Sprite):
    def __init__(self, imageName):
        pygame.sprite.Sprite.__init__(self)

        pygame.mouse.set_visible(True)
        
        self.image = load_sprite(imageName)
        self.rect.TopLeft = (0, 0)
 
    def update(self):
        self.rect.topleft = pygame.mouse.get_pos() 
 
class Land():
    #the def will decide how many pictures to load and load them in the right place
    def __init__(self, imageName):
        sprite = load_sprite(imageName)
        rect = sprite.rect
        
        #int - that hold the number of pictures needed
        self.Num_lands = int(math.ceil(float(SCREEN_WIDTH) / rect[2] + 1))
        self.Lands = []
        for i in xrange(self.Num_lands):
            sprite = load_sprite(imageName)
            sprite.rect.bottomleft = (i * rect[2], SCREEN_HEIGHT)
            self.Lands.append(sprite)
            
        
    def update(self):
        for i in self.Lands:
            x = i.rect[0]
            if x == -i.rect[2]:
                x += i.rect[2] * self.Num_lands
            i.rect.bottomleft = (x - WORLD_SPEED, SCREEN_HEIGHT)
 
class Bird():
    def __init__(self, imageBird):
        self.Bird_width = 18
        self.Bird_Hieght = 209  
        self.j = False
        # Load Bird
        
        self.sprite = load_sprite(imageBird)
        self.sprite.rect.topleft = (self.Bird_width, self.Bird_Hieght)
        
    # Bird place
    def update(self):
        if self.j == False:
            self.Bird_Hieght += 2
            self.sprite.rect.topleft = (self.Bird_width, self.Bird_Hieght) 
        else:
            self.j = False  
        
    def Jump(self):
        self.Bird_Hieght -= 60
        self.j = True
        
   
class Pole():
    def __init__(self, imageName, imageName2):
        # CLASS CONSTANTS
        self.Dist_poles = 190 # Distance between each pole
        self.Space_poles = 130 # Distance between top and bottom pole
        # POLE GENERATOR
        self.Num_poles = int(math.ceil(float(SCREEN_WIDTH) / self.Dist_poles + 1))
        self.Poles = []
        self.Poles_body = []
        print "number of poles", self.Num_poles
        for i in xrange(self.Num_poles):
            sprite = load_sprite(imageName)
            tpole_height = self.ran()
            sprite.rect.topleft = (SCREEN_WIDTH + i * self.Dist_poles, tpole_height)
            self.Poles.append(sprite)
            sprite2 = load_sprite(imageName2)
            sprite2.rect.topleft = (SCREEN_WIDTH + i * self.Dist_poles, tpole_height + self.Space_poles)
            self.Poles.append(sprite2)
           
            """Adds pole body"""
            
            """if i % 2 == 0:
                for p in xrange(self.Poles[i].rect[2]):
                    sprite3 = load_sprite(imageName3)
                    sprite3.rect.topleft = (self.Poles[i].rect[2], p)
                    self.Poles_body.append(sprite3)
            else:    
                for p in xrange(self.Poles[i].rect[2] + 26, SCREEN_HEIGHT):
                    sprite3 = load_sprite(imageName3)
                    sprite3.rect.topleft = (self.Poles[i].rect[2], p)
                    self.Poles_body.append(sprite3)
                """
    def ran (self):
        return(random.randint(0, SCREEN_HEIGHT - 26 - self.Space_poles - 112))
        
    def update(self):
        for i in xrange(len(self.Poles)):
            x = self.Poles[i].rect[0]
            if x == -self.Poles[i].rect[2]:
                if  i % 2 == 0:
                    x += self.Num_poles * (self.Dist_poles)
                    y = self.ran()
                    self.Poles[i].rect.topleft = (x - WORLD_SPEED, y)
                else:
                    x += self.Num_poles * (self.Dist_poles)
                    self.Poles[i].rect.topleft = (x - WORLD_SPEED, y + self.Space_poles)
                   
                
            else:            
                self.Poles[i].rect.topleft = (x - WORLD_SPEED, self.Poles[i].rect[1])         
        
            
                    
                     
        
class MainMenu():
    def __init__(self, splash, gameover):
        self.splash = load_sprite(splash)
        self.gameover = load_sprite(gameover)
        
     
        
                  

class MainWindow(object):
    # Variables
    MousePointer = None
    Land = None
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
       
        
        #self.MousePointer = Pointer("pointer.png")
        self.Mainmenu = MainMenu("splash.png", "gameover.png")
        self.SPLASH = self.Mainmenu.splash
        self.bird = Bird("bird1.png")
        self.Land = Land("land.png")
        self.font = pygame.font.Font(None, 26)
        self.clock = pygame.time.Clock()
        self.Pole = Pole("poleu.png", "poled.png")
        
        self.running = True
        self.Menu = True
        
    def MainLoop(self):
        

        while self.running and self.Menu is False:
            # tick the clock and try to maintain 60 fps
            self.clock.tick(60)
        
            # event loop
            for event in pygame.event.get():
                print event
                if event.type == QUIT:
                    running = False
                     
                elif event.type == KEYDOWN and event.dict['key'] == 32:
                    self.bird.Jump()
                
            self.Update()
            self.Draw()
        
        while self.running and self.Menu:
             # tick the clock and try to maintain 60 fps
            self.clock.tick(60)
        
            # event loop
            for event in pygame.event.get():
                print event
                if event.type == QUIT:
                    self.running = False
                     
                elif event.type == KEYDOWN:
                    if self.SPLASH.rect == self.Mainmenu.gameover.rect:
                        self.SPLASH = self.Mainmenu.splash
                    else:
                        self.SPLASH.rect == self.Mainmenu.splash.rect
                        self.Menu = False
                        MainWindow() 
                        self.MainLoop()
            
            # get our FPS and put it into a surface so we can write it
            # to the screen
            fpsMessage = "fps: %s" % (round(self.clock.get_fps(), 2))
            fpsMessageSurface = self.font.render(fpsMessage, 1, (255, 255, 255))
    
            self.screen.fill((0, 0, 255))
            #self.screen.blit(self.MousePointer.image, self.MousePointer.rect)
  
            self.screen.blit(self.SPLASH.image, self.SPLASH.rect)
              
            self.screen.blit(fpsMessageSurface, (0, 0))
            pygame.display.flip() 
            
    def Update(self):
        self.bird.update()
        self.Land.update()
        self.Pole.update()
        # update our mouse pointer sprite
        #self.MousePointer.update()
    
    #Checking for collision
    
        for i in xrange(len(self.Pole.Poles)):
            if self.Pole.Poles[i].rect.colliderect(self.bird.sprite.rect) == 1:
                self.SPLASH = self.Mainmenu.gameover
                self.Menu = True
                MainWindow()
                
            
        for i in xrange(len(self.Land.Lands)):
            if self.Land.Lands[i].rect.colliderect(self.bird.sprite.rect):
                self.SPLASH = self.Mainmenu.gameover
                self.Menu = True
                MainWindow()
                
                
                
              
    
    def Draw(self):
        # get our FPS and put it into a surface so we can write it
        # to the screen
        fpsMessage = "fps: %s" % (round(self.clock.get_fps(), 2))
        fpsMessageSurface = self.font.render(fpsMessage, 1, (255, 255, 255))
    
        self.screen.fill((0, 0, 255))
        #self.screen.blit(self.MousePointer.image, self.MousePointer.rect)
        
        for i in self.Land.Lands:
            self.screen.blit(i.image, i.rect)
            
        for i in self.Pole.Poles:
            self.screen.blit(i.image, i.rect)
            
        """for i in self.Pole.Poles_body:
            self.surface.blit(i.image, i.rect)"""
        
        self.screen.blit(self.bird.sprite.image, self.bird.sprite.rect)
              
        self.screen.blit(fpsMessageSurface, (0, 0))
        pygame.display.flip()