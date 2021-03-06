import pygame
import sys
import random
from pygame.locals import *
from random import randrange

pygame.init()

"""Sets size of window, can be changed later"""
screen = pygame.display.set_mode((765, 800))
temp = 1
pygame.display.set_caption('Qix')
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
titleFont = pygame.font.SysFont('arial', 60)
instrucFont = pygame.font.SysFont('arial', 16)
startNum = 10
endNum = 750
LabelNum = endNum / 4
start = True

"""Some placeholder colours to be used later"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)
startScreenText = titleFont.render('QIX', True, BLACK)
startScreenText2 = font.render('Press R to start', True, BLACK)
LevelText1 = font.render('LEVEL: ', True, BLACK)
LevelText2 = font.render(str(temp), True, BLACK)
HealthText1 = font.render('HEALTH: ', True, BLACK)
HealthText2 = font.render(str(temp), True, BLACK)
CompletionText1 = font.render('BOARD %: ', True, BLACK)
CompletionText2 = font.render(str(temp), True, BLACK)
gameOverScreen1 = titleFont.render('GAME OVER', True, RED)
gameOverScreen2 = font.render('Press R to restart', True, RED)
victoryText1 = titleFont.render('YOU WIN!', True, BLACK)
victoryText2 = font.render('Press R to replay', True, BLACK)
levelCompleteText = titleFont.render('LEVEL COMPLETE!', True, BLACK)
instruc1 = instrucFont.render('WASD / Arrow Keys to Move', True, BLACK)
instruc2 = instrucFont.render('Space to Start Push', True, BLACK)
instruc3 = instrucFont.render('Qix is Red, Sparx is Blue, You are Green', True, BLACK)
instruc4 = instrucFont.render('5 Levels to Beat', True, BLACK)
screen.fill(AQUA)
playerSurf = pygame.Surface((765, 800))
playerSurf.fill(AQUA)
"""
You can increment these with maxWidth and height to draw the original border
Replace:
775 with (maxHeight - 25)
575 with (maxWidth - 25)
and 25 should be able to stay the same although I haven't tested it yet
"""

newStart = endNum // 2
pygame.draw.rect(screen, BLACK, ((newStart), (newStart - 5), 10, 10))
x = newStart
y = newStart - 5
speed = 5
running = True
direction = None

# Constants to store direction of nodes
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

# Constants to store conditions of push collision checks
FAIL = 0
PASS = 1
NONE = 2
QIX = 3
SPARX = 4

# Constants to store state of the game
GAME_RUNNING = 0
GAME_OVER = 1
GAME_WON = 2
GAME_START = 3

# Player class
class Player:
    # Initialize the player object and it's hitbox
    def __init__(self, life, speed, board):
        self.life = life
        self.speed = speed
        self.x = newStart
        self.y = endNum
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect.center = (self.x, self.y)
        self.location = board.curr
        self.atCorner = False
        self.isPush = False
        self.pushNodes = []
        self.immunity = 0

    # Move function, allows player to move around the board based off user input
    def move(self, direction, board):
        
        # If the player is currently in an active Push, then it will move accordinly on the push
        # This means the player cannot move backwards
        # Everytime the player turns, the push will store a new node to eventually be added to the board if the push succeeds
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
                self.pushNodes[-1].prev = self.pushNodes[-2]
                self.pushNodes[-2].next = self.pushNodes[-1]
                self.pushNodes[-2].updateRect()

        # If the player is not in an active push, then the move function will go through a bunch of checks
        # These checks will make sure that the player cannot pass the current node and move off of the board
        # The player will essentially be limited to moving on the circular list of nodes
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
        
        # If the player is at a corner (at a node), then the player must move to either the next node or stay on the current node
        # This part of the move function will ensure that the player is moved to the appropriate nodef
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
        # Update the pygame.rect hitbox of the player after it moves
        self.moveHitbox()

    # Function that updates the pygame.rect hitbox of the player to it's current location
    def moveHitbox(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.center = (self.x, self.y)

    # Function that returns player hitbox
    def getHitbox(self):
        return self.rect

    # Function that starts push if called
    # First the function checks if the player is not in active push or at a corner (preconditions)
    # Then the function will move the player and start adding nodes to store for if the push succeeds
    def makePush(self):
        if self.isPush is not True and self.atCorner is not True:
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
            self.moveHitbox()

    # Ends the current push and empties the list of nodes
    def endPush(self):
        self.pushNodes = []
        self.isPush = False

    # Checks collision of player if they are in a push in this order
    # 1. First check if the Qix is colliding with the player
    # 2. Next check if the sparx is colliding with the start of the push
    # 3. After check if the player is colliding with their own push (like in snake, trying to eat itself)
    # 4. Then check if the Qix is hitting those same lines
    # If all of these are not true, then it will after check if the player is intersecting with the board
    # If they are, the push is finished and the board is updated
    def checkCollisionPush(self, qix, sparxList, board):
        if self.rect.colliderect(qix.rect):
            return QIX
        for i in sparxList:
            if self.pushNodes[0].x == i.x and self.pushNodes[0].y == i.y:
                return SPARX
        for i in self.pushNodes:
            if i.rect is not None and i.rect.collidepoint(self.rect.center):
                return FAIL
            if i.rect is not None and i.rect.colliderect(qix.rect):
                return QIX
        current = board.curr
        firstNode = current
        while current.next is not firstNode:
            if current.rect.collidepoint(self.rect.center):
                self.pushNodes.append(Node(self.x, self.y, current.getOrientation()))
                board.addPush(self.pushNodes, current)
                self.location = board.curr
                self.atCorner = True
                return PASS
            current = current.next
            if current.rect.collidepoint(self.rect.center):
                self.pushNodes.append(Node(self.x, self.y, current.getOrientation()))
                board.addPush(self.pushNodes, current)
                self.location = board.curr
                self.atCorner = True
                return PASS
        return NONE

    # This immunity function is to ensure the player doesn't instantly die when they are hit by a sparx
    def checkImmunity(self):
        if self.immunity > 0:
            self.immunity -= 1

    # Resets the push and deals damage if needed
    def resetPush(self, damage):
        self.x = self.pushNodes[0].getx()
        self.y = self.pushNodes[0].gety()
        self.moveHitbox()
        self.isPush = False
        self.pushNodes = []
        self.life -= damage
        self.immunity = 60

    # Checks collision between player and sparx
    # Deals damage if the collision check is true
    def checkCollision(self, sparxList):
        if self.immunity == 0:
            for x in sparxList:
                if self.rect.colliderect(x.rect):
                    self.life -= x.damage
                    self.immunity = 60

# Qix Class
class Qix:
    # The Qix is initialized to be starting at a random spot in the board, and head in a random direction
    def __init__(self, speed, board, damage):
        randomInt1 = random.randint(0, 1)
        randomInt2 = random.randint(0, 1)
        if randomInt1 == 0:
            self.xSpeed = speed
        else:
            self.xSpeed = speed * -1
        if randomInt2 == 0:
            self.ySpeed = speed
        else:
            self.ySpeed = speed * -1
        self.damage = damage
        self.x = random.randint(startNum + (speed * 4), endNum - (speed * 4))
        self.y = random.randint(startNum + (speed * 4), endNum - (speed * 4))
        self.location = board.curr
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect.center = (self.x, self.y)

    # Return hitbox
    def getHitbox(self):
        return self.rect

    # Return damage
    def getDamage(self):
        return self.damage

    # Move the Qix and check collision with board
    def move(self):
        self.checkCollision()
        self.x += self.xSpeed
        self.y += self.ySpeed
        # Update hitbox
        self.moveHitbox()

    # Move the Qix hitbox
    def moveHitbox(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.center = (self.x, self.y)

    # Check collision with the qix and the board
    # If the Qix collides with top or bottom, reverse it's y speed
    # If it collides with left or right, reverse it's x speed
    def checkCollision(self):
        current = self.location
        firstNode = current
        while current.next is not firstNode:
            if self.rect.colliderect(current.rect):
                if current.orientation == UP or current.orientation == DOWN:
                    self.xSpeed *= -1
                elif current.orientation == LEFT or current.orientation == RIGHT:
                    self.ySpeed *= -1
            current = current.next
        if self.rect.colliderect(current.rect):
            if current.orientation == UP or current.orientation == DOWN:
                self.xSpeed *= -1
            elif current.orientation == LEFT or current.orientation == RIGHT:
                self.ySpeed *= -1

    # Update the Qix board when the board changes
    def updateBoard(self, boardNode):
        self.location = boardNode

# Sparx Class
class Sparx:
    # Initialize depending on if there is 1 or 2 sparx, initialize locations as well
    def __init__(self, speed, board, damage, loc):
        self.speed = speed
        self.damage = damage
        if loc == 0:
            self.location = board.curr.next.next
            self.x = endNum / 2
            self.y = startNum
        else:
            self.location = board.curr.next
            self.x = endNum
            self.y = endNum / 2
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect.center = (self.x, self.y)

    # Return hitbox
    def getHitbox(self):
        return self.rect

    # Return damage
    def getDamage(self):
        return self.damage

    # Update the pygame.rect hitbox of the sparx
    def moveHitbox(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.center = (self.x, self.y)

    # Move the sparx in a circle
    # Essentially just follows the circular list of nodes
    # If it reaches a corner, it moves on to the next node
    def moveCircle(self):
        if self.x == self.location.next.x and self.y == self.location.next.y:
            self.location = self.location.next
        if self.location.orientation == UP:
            self.y -= self.speed
        elif self.location.orientation == DOWN:
            self.y += self.speed
        elif self.location.orientation == LEFT:
            self.x -= self.speed
        elif self.location.orientation == RIGHT:
            self.x += self.speed
        # Update hitbox after moving
        self.moveHitbox()

    # Update the location of the sparx to the node passed in the parameter
    def updateLocation(self, node):
        self.location = node
        self.x = self.location.x
        self.y = self.location.y
        self.moveHitbox()

    # Check collision of board, if the sparx is not on the board it will need to be teleported back to the board
    def checkCollision(self, board):
        current = self.location
        firstNode = current
        while current.next is not firstNode:
            if self.rect.colliderect(current.rect):
                return True
            current = current.next
        if self.rect.colliderect(current.rect):
            return True
        return False

# Class Node
class Node:
    # Initialize
    # Every node will have an x, y and direction
    # This direction will be the direction of the edge following the node in the circular linked list
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None
        self.orientation = orientation
        self.rect = None

    # Return x
    def getx(self):
        return self.x

    # Return y
    def gety(self):
        return self.y

    # Return direction
    def getOrientation(self):
        return self.orientation

    # Return hitbox (1 pixel wide)
    def getHitbox(self):
        return self.rect

    # Update hitbox automatically
    # It will do this by checking where the node after it is
    # And assigning a pygame.rect hitbox respectively
    def updateRect(self):
        if self.next is not None:
            if self.orientation == DOWN or self.orientation == RIGHT:
                self.rect = pygame.Rect(self.x, self.y, self.next.x - self.x + 1, self.next.y - self.y + 1)
            else:
                self.rect = pygame.Rect(self.next.x, self.next.y, self.x - self.next.x + 1, self.y - self.next.y + 1)

# Board class AKA the circular linked list
class Board:
    # Initialize the initial board of just 4 vertices
    def __init__(self):
        startingNodes = [Node(startNum, endNum, RIGHT), Node(endNum, endNum, UP), Node(endNum, startNum, LEFT),
                         Node(startNum, startNum, DOWN)]
        startingNodes[0].prev = startingNodes[-1]
        startingNodes[-1].prev = startingNodes[-2]
        startingNodes[0].next = startingNodes[1]
        startingNodes[-1].next = startingNodes[0]
        for x in range(1, len(startingNodes) - 1):
            startingNodes[x].prev = startingNodes[x - 1]
            startingNodes[x].next = startingNodes[x + 1]
        self.curr = startingNodes[0]
        self.startingArea = self.getArea()

    # Function to add a push
    # The function is assuming the push was successful as the player object would verify this first
    # Then it will check if the push was done in reverse or not
    # It will respectively put the nodes in and update the hitboxes of the board as well
    # Will make sure the circular linked list stays intact and gets rid of all nodes that are unused after
    def addPush(self, nodes, nodeBefore):
        nodes.reverse()
        current = self.curr
        tempList = []
        tempList.append(nodes[0])
        while current is not nodeBefore:
            current = current.next
            tempList.append(current)
        nodes.reverse()
        tempList.extend(nodes)
        sameLineBefore = False
        if self.curr is nodeBefore:
            if self.curr.orientation == RIGHT and nodes[-1].x < nodes[0].x:
                sameLineBefore = True
            elif self.curr.orientation == LEFT and nodes[-1].x > nodes[0].x:
                sameLineBefore = True
            elif self.curr.orientation == UP and nodes[-1].y > nodes[0].y:
                sameLineBefore = True
            elif self.curr.orientation == DOWN and nodes[-1].y < nodes[0].y:
                sameLineBefore = True

        if findAreaList(tempList) >= self.getArea() / 2 and sameLineBefore is not True:
            nodes[0].prev = self.curr
            nodes[-2].next = nodes[-1]
            nodes[-1].prev = nodes[-2]
            nodes[-1].next = current.next
            nodes[-1].next.prev = nodes[-1]
            self.curr.next = nodes[0]
            self.curr = nodes[-1]
        else:
            for x in range(len(nodes) - 1, 0, -1):
                nodes[x].orientation = nodes[x - 1].orientation * -1
            nodes[0].orientation = self.curr.orientation
            nodes[0].next = self.curr.next
            nodes[0].prev = nodes[1]
            for x in range(1, len(nodes) - 1):
                nodes[x].prev = nodes[x + 1]
                nodes[x].next = nodes[x - 1]
            current.next = nodes[-1]
            nodes[-1].prev = current
            nodes[-1].next = nodes[-2]
            self.curr = nodes[-1]

    # Gets the area of the board
    # Mathematical function that checks from vertice to vertice
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

    # Checks if the board has won
    # Returns true if it has, false otherwise
    # Percent parameter is used to check win condition
    def checkWin(self, percent):
        if self.getArea() > (((100 - percent) / 100) * self.startingArea):
            return True
        else:
            return False

# Function that calculates area of a list of nodes
# This is used to get the area of the pushNodes the player makes to compare to the board size
def findAreaList(listNodes):
    sum1 = 0
    sum2 = 0
    for i in range(len(listNodes) - 1):
        sum1 += listNodes[i].x * listNodes[i + 1].y
        sum2 += listNodes[i].y * listNodes[i + 1].x
    return (sum1 - sum2) / 2

# Draw the board object
# The board will be updated everytime a new push is added
# This ensures the old board isn't drawn and the new board is drawn
def drawBoard(board):
    global qix
    current = board.curr
    firstNode = current
    while current.next is not firstNode:
        current.updateRect()
        pygame.draw.rect(screen, BLACK, current.rect)
        current = current.next
    current.updateRect()
    pygame.draw.rect(screen, BLACK, current.rect)
    qix.updateBoard(current)

# Draw all other objects in the game (player, qix, sparx)
def drawObjects(player, qix, sparxLists):
    pygame.draw.rect(screen, GREEN, player.rect)
    pygame.draw.rect(screen, RED, qix.rect)
    for i in sparxLists:
        pygame.draw.rect(screen, BLACK, i.rect)

# Draw the push if the player is making one
# This will draw lines following the player
def drawPush(player):
    for i in player.pushNodes:
        if i.getHitbox() is not None:
            pygame.draw.rect(screen, BLACK, i.rect)
        elif i.getOrientation() == DOWN or i.getOrientation() == RIGHT:
            pygame.draw.rect(screen, BLACK, (i.getx(), i.gety(), player.x - i.getx() + 1, player.y - i.gety() + 1))
        else:
            pygame.draw.rect(screen, BLACK, (player.x, player.y, i.getx() - player.x + 1, i.gety() - player.y + 1))

# Function to cycle through the levels
# This function will add a sparx at level 5
def cycleLevel(board, sparxList, level):
    if level == 5:
        sparxList.append(Sparx(sparxList[0].speed, board, 1, 1))
    for x in range(len(sparxList)):
        sparxList[x] = Sparx(sparxList[x].speed, board, sparxList[x].damage, x)
    return sparxList

# Initialize objects
board = Board()
qix = Qix(5, board, 1)
sparxList = [Sparx(5, board, 1, 0)]
player = Player(5, 5, board)

# Initialize level
level = 1
prevLevel = 1
percent = 50

# Initialize game state
gameState = GAME_START

# Function to reset the game
# Sets all parameters to the default parameters
# Sets game state back to the start screen
def restartGame():
    global board, qix, sparxList, player, level, prevLevel, gameState
    gameState = GAME_START
    startScreen()
    board = Board()
    qix = Qix(5, board, 1)
    sparxList = [Sparx(5, board, 1, 0)]
    player = Player(5, 5, board)
    level = 1
    prevLevel = 1

# Start screen
# Displays at the beginning of the game
# Prompts user and gives instructions
def startScreen():
    global start
    global gameState
    while gameState == GAME_START:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            gameState = GAME_RUNNING
            return 0
        screen.fill(WHITE)
        screen.blit(startScreenText, (endNum / 2 - 35, endNum / 2 - 100))
        screen.blit(startScreenText2, (endNum / 2 - 50, endNum / 2))
        screen.blit(instruc1, (endNum / 2 - 75, endNum / 2 + 50))
        screen.blit(instruc2, (endNum / 2 - 50, endNum / 2 + 100))
        screen.blit(instruc3, (endNum / 2 - 105, endNum / 2 + 150))
        screen.blit(instruc4, (endNum / 2 - 40, endNum / 2 + 200))
        pygame.display.update()

        clock.tick(15)

# Game over screen
# Screen that is displayed if user loses all lives
# The user is prompted to restart
def gameOverScreen():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        restartGame()
        return 0
    screen.blit(gameOverScreen1, (endNum / 2 - 140, endNum / 2 - 100))
    screen.blit(gameOverScreen2, (endNum / 2 - 50, endNum / 2))
    pygame.display.update()

    clock.tick(15)

# Victory screen
# Shown when the player beats level 5
# The user is prompted to restart to play again
def victoryScreen():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        restartGame()
        return 0
    screen.fill(WHITE)
    screen.blit(victoryText1, (endNum / 2 - 100, endNum / 2 - 100))
    screen.blit(victoryText2, (endNum / 2 - 50, endNum / 2))
    pygame.display.update()

    clock.tick(15)

# Level complete overlay
# Prompts the user that the current level has been beaten
def levelCompleteScreen():
    screen.blit(levelCompleteText, (endNum/2 -225, endNum/2 - 100))
    pygame.display.update()
    clock.tick(30)

# Initialize the start screen
startScreen()

# Game loop
while running:
    # Display or do certain actions based on the game state
    if gameState == GAME_OVER:
        gameOverScreen()
    elif gameState == GAME_WON:
        victoryScreen()
    elif gameState == GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # If the level is a new level, pause to give the user time to adjust
        if level != prevLevel:
            pygame.time.wait(2000)
            prevLevel = level

        # Check for user input and do action respectively
        keys = pygame.key.get_pressed()
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

        # Drawings
        # Will draw all visuals on the screen and update texts as needed
        clock.tick(30)
        screen.fill(AQUA)
        screen.blit(playerSurf, (0, 0))
        LevelText2 = font.render(str(level), True, BLACK)
        HealthText2 = font.render(str(player.life), True, BLACK)
        CompletionText2 = font.render(str(100 - round((board.getArea() / board.startingArea) * 100)) + "/" + str(percent), True, BLACK)
        screen.blit(LevelText1, (LabelNum - 40, endNum + 15))
        screen.blit(LevelText2, (LabelNum + 20, endNum + 15))
        screen.blit(HealthText1, (LabelNum * 2 - 40, endNum + 15))
        screen.blit(HealthText2, (LabelNum * 2 + 30, endNum + 15))
        screen.blit(CompletionText1, (LabelNum * 3 - 40, endNum + 15))
        screen.blit(CompletionText2, (LabelNum * 3 + 50, endNum + 15))
        drawBoard(board)

        # If the player is in a push the game does a series of checks
        # First checks for collisions during a push
        # If the collisions return something other than none, will do action respectively
        # If the push is successful, the game checks for win
        # If the current level is won, then the next level is presented
        # If the game is won, then the end screen is presented
        if player.isPush is True:
            drawPush(player)
            check = player.checkCollisionPush(qix, sparxList, board)
            if check != NONE:
                screen.fill(AQUA)
                if check == PASS:
                    if board.checkWin(percent) is True and level == 5:
                        gameState = GAME_WON
                    elif board.checkWin(percent) is True:
                        drawBoard(board)
                        drawObjects(player, qix, sparxList)
                        pygame.display.update()
                        levelCompleteScreen()
                        pygame.time.wait(3000)
                        screen.fill(AQUA)
                        pygame.display.update()
                        level += 1
                        board = Board()
                        sparxList = cycleLevel(board, sparxList, level)
                        qix = Qix(qix.xSpeed + 1, board, qix.damage)
                        player = Player(player.life, player.speed, board)
                        drawBoard(board)
                        percent += 5
                    else:
                        drawBoard(board)
                        if sparxList[0].checkCollision(board) is False:
                            sparxList[0].updateLocation(player.pushNodes[0])
                        if level == 5 and sparxList[1].checkCollision(board) is False:
                            sparxList[1].updateLocation(player.pushNodes[0].next)
                        player.endPush()
                elif check == QIX:
                    player.resetPush(qix.getDamage())
                elif check == SPARX:
                    player.resetPush(sparxList[0].getDamage())
                elif check == FAIL:
                    player.resetPush(0)
                # If lives are zero, game is over
                if player.life == 0:
                    gameState = GAME_OVER
        # Check sparx collisions
        # If lives are zero, game is over
        else:
            if player.immunity == 0:
                player.checkCollision(sparxList)
            else:
                player.checkImmunity()
            if player.life == 0:
                gameState = GAME_OVER
        # If the game is not over, move the Sparx and Qix objects
        if level == prevLevel and gameState != GAME_WON:
            for x in sparxList:
                x.moveCircle()
            qix.move()
        # Draw the objects and update the display
        drawObjects(player, qix, sparxList)
        pygame.display.update()
