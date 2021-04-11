import pygame
import sys
from pygame.locals import *

pygame.init()

"""Sets size of window, can be changed later"""
screen = pygame.display.set_mode((600, 600))
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

pygame.draw.rect(screen, BLACK, (255, 505, 10, 10))
x = 255
y = 505
speed = 5
running = True
direction = None

UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

class Player:
    def __init__(self, life, speed, board):
        self.life = life
        self.speed = speed
        self.x = 250
        self.y = 500
        self.location = board.curr
        self.atCorner = False
        self.isPush = False
        self.pushNodes = []

    def move(self, direction, board):
        if self.isPush is True:
            if self.pushNodes[-1].orientation == direction:
                if direction == UP:
                    self.y -= self.speed
                elif direction == DOWN:
                    self.y += self.speed
                elif direction == LEFT:
                    self.x -= self.speed
                elif direction == RIGHT:
                    self.x += self.speed
            elif self.pushNodes[-1].orientation != direction * -1:
                if direction == RIGHT:
                    self.pushNodes.append(Node(self.x, self.y, RIGHT))
                    self.x += self.speed
                elif direction == LEFT:
                    self.pushNodes.append(Node(self.x, self.y, LEFT))
                    self.x -= self.speed
                elif direction == UP:
                    self.pushNodes.append(Node(self.x, self.y, UP))
                    self.y -= self.speed
                elif direction == DOWN:
                    self.pushNodes.append(Node(self.x, self.y, DOWN))
                    self.y += self.speed
        elif self.atCorner is False:
            if direction == LEFT and (self.location.orientation == LEFT or self.location.orientation == RIGHT):
                if self.location.orientation == LEFT and self.x - self.speed <= self.location.next.x:
                    self.x = self.location.next.x
                    self.atCorner = True
                
                elif self.location.orientation == RIGHT and self.x - self.speed <= self.location.x:
                    self.x = self.location.x
                    self.atCorner = True

                else:
                    self.x -= self.speed

            elif direction == RIGHT and (self.location.orientation == LEFT or self.location.orientation == RIGHT):
                if self.location.orientation == LEFT and self.x + self.speed >= self.location.x:
                    self.x = self.location.x
                    self.atCorner = True
                
                elif self.location.orientation == RIGHT and self.x + self.speed >= self.location.next.x:
                    self.x = self.location.next.x
                    self.atCorner = True

                else:
                    self.x += self.speed

            elif direction == UP and (self.location.orientation == UP or self.location.orientation == DOWN):
                if self.location.orientation == UP and self.y - self.speed <= self.location.next.y:
                    self.y = self.location.next.y
                    self.atCorner = True
                
                elif self.location.orientation == DOWN and self.y - self.speed <= self.location.y:
                    self.y = self.location.y
                    self.atCorner = True

                else:
                    self.y -= self.speed

            elif direction == DOWN and (self.location.orientation == UP or self.location.orientation == DOWN):
                if self.location.orientation == UP and self.y + self.speed >= self.location.y:
                    self.y = self.location.y
                    self.atCorner = True
                
                elif self.location.orientation == DOWN and self.y + self.speed >= self.location.next.y:
                    self.y = self.location.next.y
                    self.atCorner = True

                else:
                    self.y += self.speed
        else:
            if direction == UP:
                if self.location.next.x == self.x and self.location.next.orientation == UP:
                    self.location = self.location.next
                    board.curr = board.curr.next
                    self.y -= self.speed
                    self.atCorner = False
                elif self.location.prev.x == self.x and self.location.prev.orientation == DOWN:
                    self.location = self.location.prev
                    self.y -= self.speed
                    board.curr = board.curr.prev
                    self.atCorner = False
                elif self.location.x == self.x and self.location.y == self.y and self.location.orientation == UP:
                    self.y -= self.speed
                    self.atCorner = False
                elif self.location.next.x == self.x and self.location.next.y == self.y and self.location.orientation == DOWN:
                    self.y -= self.speed
                    self.atCorner = False

            elif direction == DOWN:
                if self.location.next.x == self.x and self.location.next.orientation == DOWN:
                    self.location = self.location.next
                    self.y += self.speed
                    board.curr = board.curr.next
                    self.atCorner = False
                elif self.location.prev.x == self.x and self.location.prev.orientation == UP:
                    self.location = self.location.prev
                    self.y += self.speed
                    board.curr = board.curr.prev
                    self.atCorner = False
                elif self.location.x == self.x and self.location.y == self.y and self.location.orientation == DOWN:
                    self.y += self.speed
                    self.atCorner = False
                elif self.location.next.x == self.x and self.location.next.y == self.y and self.location.orientation == UP:
                    self.y += self.speed
                    self.atCorner = False
                
            elif direction == LEFT:
                if self.location.next.y == self.y and self.location.next.orientation == LEFT:
                    self.location = self.location.next
                    self.x -= self.speed
                    board.curr = board.curr.next
                    self.atCorner = False
                elif self.location.prev.y == self.y and self.location.prev.orientation == RIGHT:
                    self.location = self.location.prev
                    self.x -= self.speed
                    board.curr = board.curr.prev
                    self.atCorner = False
                elif self.location.x == self.x and self.location.y == self.y and self.location.orientation == LEFT:
                    self.x -= self.speed
                    self.atCorner = False
                elif self.location.next.x == self.x and self.location.next.y == self.y and self.location.orientation == RIGHT:
                    self.x -= self.speed
                    self.atCorner = False

            elif direction == RIGHT:
                if self.location.next.y == self.y and self.location.next.orientation == RIGHT:
                    self.location = self.location.next
                    self.x += self.speed
                    board.curr = board.curr.next
                    self.atCorner = False
                elif self.location.prev.y == self.y and self.location.prev.orientation == LEFT:
                    self.location = self.location.prev
                    self.x += self.speed
                    board.curr = board.curr.prev
                    self.atCorner = False
                elif self.location.x == self.x and self.location.y == self.y and self.location.orientation == RIGHT:
                    self.x += self.speed
                    self.atCorner = False
                elif self.location.next.x == self.x and self.location.next.y == self.y and self.location.orientation == LEFT:
                    self.x += self.speed
                    self.atCorner = False

    def makePush(self):
        if self.isPush is not True:
            self.isPush = True
            if self.location.orientation == RIGHT:
                self.pushNodes.append(Node(self.x, self.y, UP))
                self.y -= self.speed
            elif self.location.orientation == LEFT:
                self.pushNodes.append(Node(self.x, self.y, DOWN))
                self.y += self.speed
            elif self.location.orientation == UP:
                self.pushNodes.append(Node(self.x, self.y, LEFT))
                self.x -= self.speed
            elif self.location.orientation == DOWN:
                self.pushNodes.append(Node(self.x, self.y, RIGHT))
                self.x += self.speed

    def resetPush(self):
        self.pushNodes = []

class Node:    
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None
        self.orientation = orientation
    
    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getOrientation(self):
        return self.orientation

def chkBtwn(node1, node2, node3):
    if node2.x == node1.x and node3.x == node2.x:
        if node2.y > node1.y:
            if node3.y >= node1.y and node3.y < node2.y:
                return True
        if node2.y < node1.y:
            if node3.y > node2.y and node3.y <= node1.y:
                return True

    if node2.y == node1.y and node3.y == node2.y:
        if node2.x > node1.x:
            if node3.x >= node1.x and node3.x < node2.x:
                return True
        if node2.x < node1.x:
            if node3.x > node2.x and node3.x <= node1.x:
                return True
    return False

def findAreaList(listNodes):
    sum1, sum2 = 0
    for i in range(len(listNodes) - 1):
        sum1 += listNodes[i].x * listNodes[i + 1].y
        sum2 += listNodes[i].y * listNodes[i + 1].x
    return (sum1 - sum2) / 2

class Board:  
    def __init__(self):    
        startingNodes = [Node(10, 500, RIGHT), Node(500, 500, UP), Node(500, 10, LEFT), Node(10, 10, DOWN)]
        startingNodes[0].prev = startingNodes[3]
        startingNodes[1].prev = startingNodes[0]
        startingNodes[2].prev = startingNodes[1]
        startingNodes[3].prev = startingNodes[2]
        startingNodes[0].next = startingNodes[1]
        startingNodes[1].next = startingNodes[2]
        startingNodes[2].next = startingNodes[3]
        startingNodes[3].next = startingNodes[0]
        self.curr = startingNodes[0]
        self.startingArea = self.getArea()
        
    def addPush(self, nodes):
        reversedNodes = nodes.reverse()
        current = self.curr
        tempList = [nodes[0]]
        while chkBtwn(current, current.next, nodes[-1]) is not True:
            current = current.next
            tempList.append(current)
        tempList.extend(reversedNodes)
        if findAreaList(tempList) <= self.getArea() / 2:
            self.curr.next = nodes[0]
            for x in range(1, len(nodes) - 1):
                nodes[x].prev = nodes[x-1]
                nodes[x].next = nodes[x+1]
            nodes[-1].prev = nodes[-2]
            nodes[-1].next = current.next
            while self.curr is not nodes[-1]:
                self.curr = self.curr.next
        else:
            for x in nodes:
                x.orientation *= -1
            self.curr.next.prev = nodes[0]
            current.next = nodes[-1]
            for x in range(1, len(nodes) - 1):
                nodes[x].prev = nodes[x+1]
                nodes[x].next = nodes[x-1]
            nodes[-1].prev = current
            nodes[-1].next = nodes[-2]
            while self.curr is not nodes[-1]:
                self.curr = self.curr.next

    def getArea(self):
        current = self.curr
        firstNode = current
        sum1 = 0
        sum2 = 0
        current = current.next
        sum1 += firstNode.x * current.y
        sum2 += firstNode.y * current.x
        while current is not firstNode:
            sum1 += current.x * current.next.y
            sum2 += current.y * current.next.x
            current = current.next
        return (sum1 - sum2) / 2

    def checkWin(self, percent):
        if self.getArea() <= ((percent / 100) * self.startingArea):
            return True
        else:
            return False

board = Board()
player = Player(100, 10, board)
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
    # draw the board
    keys = pygame.key.get_pressed()

    direction = None
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move(LEFT, board)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move(RIGHT, board)
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        player.move(UP, board)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.move(DOWN, board)
    elif keys[pygame.K_SPACE]:
        player.makePush()

    '''screen = pygame.Surface.copy(screen)'''
    clock.tick(60)
    screen.fill(AQUA)
    screen.blit(playerSurf, (0, 0))
    pygame.draw.rect(screen, BLACK, (player.x, player.y, 10, 10))
    pygame.display.update()

