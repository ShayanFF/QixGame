import pygame
from pygame.locals import *

pygame.init()

"""Sets size of window, can be changed later"""
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Qix')

"""Some placeholder colours to be used later"""
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
AQUA = (0, 255, 255)

screen.fill(AQUA)
"""
Experimenting with drawing lines to try and create the look of the board

pygame.draw.line(screen, RED, (775, 25), (775, 575), 5)
pygame.draw.line(screen, RED, (25, 25), (25, 575), 5)
pygame.draw.line(screen, RED, (25, 780), (580, 780), 5)
pygame.draw.line(screen, RED, (20, 20), (780, 20), 5)"""

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()

    pygame.display.update()

# Board Object
class Board:
    def __init__(self, start, size):
        self.maxHeight, self.maxWidth = start + size
        self.minHeight, self.minWidth = start

    def getMaxWidth(self):
        return self.maxWidth
    def getMaxHeight(self):
        return self.maxHeight
    def getMinWidth(self):
        return self.minWidth
    def getMinHeight(self):
        return self.minHeight

class Player:
    def __init__(self, life, speed):
        self.life = life
        self.speed = speed
        self.x = 0
        self.y = 0

    # This one will be able to control it's own movement
    def move(self, moveX, moveY):
        self.x += moveX
        self.y += moveY

    # This allows it to create a path
    def push(self, board):
        if self.x == board.getMinWidth():
            
            
        elif self.x == board.getMaxWidth():


        elif self.y == board.getMinHeight():
        
        elif self.y == board.getMaxHeight():

class Qix(Player):
    def __init__(self, life, speed, damage):
        super().__init__(life, speed)
        self.x = 0
        self.y = 0
        self.direction = "Right"
        self.damage = damage
    
    # This one will move in a circle
    def move(self, board):
        if self.direction == "Up:
            if self.y += (10 * self.speed) >= board.getMaxHeight():
                self.y = board.getMaxHeight()
            else:
                self.y += 10 * self.speed
        elif self.direction == "Down":
            if self.y -= (10 * self.speed) <= board.getMinHeight():
                self.y = board.getMinHeight()
            else:
                self.y -= 10 * self.speed
        elif self.direction == "Left":
            if self.x -= (10 * self.speed) <= board.getMinWidth():
                self.x = board.getMinWidth()
            else:
                self.x -= 10 * self.speed
        else:
            if self.x += (10 * self.speed) >= board.getMaxWidth():
                self.x = board.getMaxWidth()
            else:
                self.x += 10 * self.speed

# Will fix this later
'''class Sparx(Qix):
    # This one will be able to move on other lines, so overriding other method
    def move(self):'''