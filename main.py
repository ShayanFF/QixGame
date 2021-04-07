import pygame
import sys
from pygame.locals import *

pygame.init()

"""Sets size of window, can be changed later"""
screen = pygame.display.set_mode((510, 510))
pygame.display.set_caption('Qix')
clock = pygame.time.Clock()

"""Some placeholder colours to be used later"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)

screen.fill(AQUA)
playerSurf = pygame.Surface((510, 510))
playerSurf.fill(AQUA)
"""
You can increment these with maxWidth and height to draw the original border
Replace:
775 with (maxHeight - 25)
575 with (maxWidth - 25)
and 25 should be able to stay the same although I haven't tested it yet
"""


# pygame.draw.line(screen, RED, (775, 25), (775, 575), 1)
# pygame.draw.line(screen, RED, (25, 25), (25, 575), 1)
# pygame.draw.line(screen, RED, (25, 575), (775, 575), 1)
# pygame.draw.line(screen, RED, (25, 25), (775, 25), 1)


# Board Object
class Board:
    def __init__(self, start, size):
        self.maxHeight = start + size
        self.maxWidth = start + size
        self.minHeight = start
        self.minWidth = start
        self.boarder = []
        for i in range(start, size, 5):
            self.boarder.append((i, start))
        for i in range(start, size, 5):
            self.boarder.append((self.maxWidth, i))
        for i in range(self.maxHeight, start, -5):
            self.boarder.append((i, self.maxHeight))
        for i in range(self.maxHeight, start, -5):
            self.boarder.append((start, i))

    def getMaxWidth(self):
        return self.maxWidth

    def getMaxHeight(self):
        return self.maxHeight

    def getMinWidth(self):
        return self.minWidth

    def getMinHeight(self):
        return self.minHeight

    def drawBoard(self):
        pygame.draw.polygon(screen, RED, self.boarder, 1)
        pygame.draw.polygon(playerSurf, RED, self.boarder, 1)

    def getCoord(self, n):
        return self.boarder[n]


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
    '''
    def push(self, board):
        if self.x == board.getMinWidth():


        elif self.x == board.getMaxWidth():


        elif self.y == board.getMinHeight():

        elif self.y == board.getMaxHeight():
    '''


class Qix(Player):
    def __init__(self, life, speed, damage):
        super().__init__(life, speed)
        self.x = 0
        self.y = 0
        self.direction = "Right"
        self.damage = damage

    # This one will move in a circle
    def move(self, board):
        if self.direction == "Up":
            if self.y + (10 * self.speed) >= board.getMaxHeight():
                self.y = board.getMaxHeight()
            else:
                self.y += 10 * self.speed
        elif self.direction == "Down":
            if self.y - (10 * self.speed) <= board.getMinHeight():
                self.y = board.getMinHeight()
            else:
                self.y -= 10 * self.speed
        elif self.direction == "Left":
            if self.x - (10 * self.speed) <= board.getMinWidth():
                self.x = board.getMinWidth()
            else:
                self.x -= 10 * self.speed
        else:
            if self.x + (10 * self.speed) >= board.getMaxWidth():
                self.x = board.getMaxWidth()
            else:
                self.x += 10 * self.speed


# Will fix this later
class Sparx(Qix):
    def __init__(self, life, speed, damage):
        super().__init__(life, speed, damage)
        # pos represents the item in the board coords list that the sparx is currently at
        self.pos = 10
        self.x = 0
        self.y = 0

    # This one will be able to move on other lines, so overriding other method
    def move(self, board):
        newpos = board.getCoord(self.pos)
        self.x = newpos[0]
        self.y = newpos[1]
        # use ints if updating speed
        if self.pos + self.speed < len(board.boarder):
            self.pos += self.speed
        else:
            self.pos = 0

    def draw(self):
        # draw a diamond at the sparx location
        points = [(self.x + 5, self.y), (self.x, self.y + 5), (self.x - 5, self.y), (self.x, self.y - 5)]
        pygame.draw.polygon(screen, BLUE, points, 0)
        '''pygame.draw.polygon(playerSurf, GREEN, points, 1)'''


# initialize board object
board = Board(5, 500)
# initialize sparx object
sparx = Sparx(4, 1, 1)

pygame.draw.rect(screen, BLACK, (255, 505, 10, 10))
x = 255
y = 505
speed = 5
running = True
direction = None

def player(direction):
    for i in range (0,5):
        if direction == 0:
            playerSurf.set_at((x, y-i), RED)
        elif direction == 1:
            playerSurf.set_at((x-i, y), RED)
        elif direction == 3:
            playerSurf.set_at((x, y+i), RED)
        elif direction == 4:
            playerSurf.set_at((x+i, y), RED)
    pygame.draw.rect(screen, BLACK, (x-5, y-5, 10, 10))


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
    # draw the board
    keys = pygame.key.get_pressed()

    direction = None
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and x > 5:
        x -= speed
        direction = 4
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x < 505:
        x += speed
        direction = 1
    elif (keys[pygame.K_UP] or keys[pygame.K_w]) and y > 5:
        y -= speed
        direction = 3
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and y < 505:
        y += speed
        direction = 0

    '''screen = pygame.Surface.copy(screen)'''
    clock.tick(60)
    screen.fill(AQUA)
    screen.blit(playerSurf, (0, 0))
    player(direction)
    board.drawBoard()
    sparx.move(board)
    sparx.draw()
    pygame.display.update()

