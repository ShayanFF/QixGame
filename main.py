import pygame
import sys
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
startNum = 10
endNum = 750
LabelNum = endNum/4
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
victoryText1 = titleFont.render('YOU WIN!', True, RED)
victoryText2 = font.render('Press R to replay', True, RED)

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


newStart = endNum//2
pygame.draw.rect(screen, BLACK, ((newStart), (newStart-5), 10, 10))
x = newStart
y = newStart-5
speed = 5
running = True
direction = None

UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

FAIL = 0
PASS = 1
NONE = 2
QIX = 3
SPARX = 4
        
class Player:
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
                self.pushNodes[-1].prev = self.pushNodes[-2]
                self.pushNodes[-2].next = self.pushNodes[-1]
                self.pushNodes[-2].updateRect()
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
        self.moveHitbox()

    def moveHitbox(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.center = (self.x, self.y)

    def getHitbox(self):
        return self.rect

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

    def endPush(self):
        self.isPush = False
        self.pushNodes = []

    def checkCollision(self, qix, sparxList, board):
        if self.rect.colliderect(qix.rect):
            return QIX
        for i in sparxList:
            if self.pushNodes[0].x == i.x and self.pushNodes[0].y == i.y:
                return SPARX
        for i in self.pushNodes:
            if i.rect is not None and i.rect.collidepoint(self.rect.center):
                return FAIL
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

    def checkImmunity(self):
        if self.immunity > 0:
            self.immunity -= 1

    def resetPush(self, damage):
        self.x = self.pushNodes[0].getx()
        self.y = self.pushNodes[0].gety()
        self.moveHitbox()
        self.isPush = False
        self.pushNodes = []
        self.life -= damage
        self.immunity = 300

class Qix:
    def __init__(self, speed, board, damage):
        self.speed = speed
        self.damage = damage
        self.x = endNum/2
        self.y = endNum/2
        self.location = board.curr
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect.center = (self.x, self.y)

    def getHitbox(self):
        return self.rect

    def getDamage(self):
        return self.damage

    def move(self):
        dir = self.getDirection()
        '''
        0 = UP
        1 = DOWN
        2 = LEFT
        3 = RIGHT'''
        if dir == 0:
            self.y -= self.speed
        elif dir == 1:
            self.y += self.speed
        elif dir == 2:
            self.x -= self.speed
        elif dir == 3:
            self.x += self.speed
        self.moveHitbox()

    def getDirection(self):
        num = randrange(4)
        return num

    def moveHitbox(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.center = (self.x, self.y)

    def checkCollision(self, dir, board):
        current = board.curr
        firstNode = current
        while current.next is not firstNode:
            if current.rect.collidepoint(self.rect.center):
                if dir == 0:
                    self.y += 35
                    return
                elif dir == 1:
                    self.y -= 35
                    return
                elif dir == 2:
                    self.x += 35
                    return
                elif dir == 3:
                    self.x += 35
                    return


class Sparx:
    def __init__(self, speed, board, damage):
        self.speed = speed
        self.damage = damage
        self.x = 250
        self.y = 10
        self.location = board.curr.next.next
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect.center = (self.x, self.y)

    def getHitbox(self):
        return self.rect

    def getDamage(self):
        return self.damage

    def moveHitbox(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.center = (self.x, self.y)

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
        self.moveHitbox()


class Node:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None
        self.orientation = orientation
        self.rect = None

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getOrientation(self):
        return self.orientation

    def getHitbox(self):
        return self.rect

    def updateRect(self):
        if self.next is not None:
            if self.orientation == DOWN or self.orientation == RIGHT:
                self.rect = pygame.Rect(self.x, self.y, self.next.x - self.x + 1, self.next.y - self.y + 1)
            else:
                self.rect = pygame.Rect(self.next.x, self.next.y, self.x - self.next.x + 1, self.y - self.next.y + 1)


def findAreaList(listNodes):
    sum1 = 0
    sum2 = 0
    for i in range(len(listNodes) - 1):
        sum1 += listNodes[i].x * listNodes[i + 1].y
        sum2 += listNodes[i].y * listNodes[i + 1].x
    return (sum1 - sum2) / 2


class Board:
    def __init__(self):
        startingNodes = [Node(startNum, endNum, RIGHT), Node(endNum, endNum, UP), Node(endNum, startNum, LEFT), Node(startNum, startNum, DOWN)]
        startingNodes[0].prev = startingNodes[-1]
        startingNodes[-1].prev = startingNodes[-2]
        startingNodes[0].next = startingNodes[1]
        startingNodes[-1].next = startingNodes[0]
        for x in range(1, len(startingNodes) - 1):
            startingNodes[x].prev = startingNodes[x - 1]
            startingNodes[x].next = startingNodes[x + 1]
        self.curr = startingNodes[0]
        self.startingArea = self.getArea()

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
            for x in range(len(nodes)-1,0,-1):
                nodes[x].orientation = nodes[x-1].orientation * -1
            nodes[0].orientation = self.curr.orientation
            nodes[0].next = self.curr.next
            nodes[0].prev = nodes[1]
            for x in range(1, len(nodes) - 1):
                nodes[x].prev = nodes[x+1]
                nodes[x].next = nodes[x-1]
            current.next = nodes[-1]
            nodes[-1].prev = current
            nodes[-1].next = nodes[-2]
            self.curr = nodes[-1]

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
        if self.getArea() > (((100-percent) / 100) * self.startingArea):
            return True
        else:
            return False
    def getPoint(self, nodes):
        point = (0,0)
        for i in range(0, len(nodes)-1):
            if nodes[i].getOrientation() != nodes[i + 1].getOrientation():
                if nodes[i].getOrientation() == UP:
                    if nodes[i+1].getOrientation() == LEFT:
                        point = (nodes[i+1].getx() - 1, nodes[i+1].gety() + 1)
                        return point
                    elif nodes[i+1].getOrientation() == RIGHT:
                        point = (nodes[i + 1].getx() + 1, nodes[i + 1].gety() + 1)
                        return point
                elif nodes[i].getOrientation() == DOWN:
                    if nodes[i+1].getOrientation() == LEFT:
                        point = (nodes[i + 1].getx() - 1, nodes[i + 1].gety() - 1)
                        return point
                    elif nodes[i+1].getOrientation() == RIGHT:
                        point = (nodes[i + 1].getx() + 1, nodes[i + 1].gety() - 1)
                        return point
                elif nodes[i].getOrientation() == LEFT:
                    if nodes[i+1].getOrientation() == UP:
                        point = (nodes[i + 1].getx() + 1, nodes[i + 1].gety() - 1)
                        return point
                    elif nodes[i+1].getOrientation() == DOWN:
                        point = (nodes[i + 1].getx() + 1, nodes[i + 1].gety() + 1)
                        return point
                elif nodes[i].getOrientation() == RIGHT:
                    if nodes[i+1].getOrientation() == UP:
                        point = (nodes[i + 1].getx() - 1, nodes[i + 1].gety() - 1)
                        return point
                    elif nodes[i+1].getOrientation() == DOWN:
                        point = (nodes[i + 1].getx() - 1, nodes[i + 1].gety() + 1)
                        return point
        return None

    def fillArea(self, nodes):
        area = []
        startPoint = self.getPoint(nodes)
        if startPoint is not None:
            print(startPoint)
            surfArray = pygame.surfarray.pixels2d(playerSurf)
            currentColour = surfArray[startPoint]
            print(currentColour)
            fillColour = playerSurf.map_rgb(BLACK)
            area.append(startPoint)
            while len(area) > 0:
                posX, posY = area.pop()
                try:
                    if surfArray[posX, posY] != currentColour:
                        continue
                except IndexError:
                    continue
                surfArray[posX, posY] = fillColour
                area.append((posX + 1, posY))
                area.append((posX - 1, posY))
                area.append((posX, posY + 1))
                area.append((posX, posY - 1))
            pygame.surfarray.blit_array(playerSurf, surfArray)

def drawBoard(board):
    current = board.curr
    firstNode = current
    while current.next is not firstNode:
        current.updateRect()
        pygame.draw.rect(screen, BLACK, current.rect)
        current = current.next
    current.updateRect()
    pygame.draw.rect(screen, BLACK, current.rect)

def drawObjects(player, qix, sparxLists):
    pygame.draw.rect(screen, GREEN, player.rect)
    pygame.draw.rect(screen, RED, qix.rect)
    for i in sparxLists:
        pygame.draw.rect(screen, BLACK, i.rect)

def drawPush(player):
    for i in player.pushNodes:
        if i.getHitbox() is not None:
            pygame.draw.rect(screen, BLACK, i.rect)
        elif i.getOrientation() == DOWN or i.getOrientation() == RIGHT:
            pygame.draw.rect(screen, BLACK, (i.getx(), i.gety(), player.x - i.getx() + 1, player.y - i.gety() + 1))
        else:
            pygame.draw.rect(screen, BLACK, (player.x, player.y, i.getx() - player.x + 1, i.gety() - player.y + 1))

def cycleLevel(board, sparxList, level):
    if level == 5:
        sparxList.append(Sparx(sparxList[0].speed, board.prev, 1))
        return sparxList
    for x in range(len(sparxList)):
        sparxList[x] = Sparx(sparxList[x].speed, board, sparxList[x].damage)
    return sparxList

SPEED_INC = 1

percent = 50

board = Board()
qix = Qix(5, board, 1)
sparxList = [Sparx(5, board, 1)]
player = Player(1, 5, board)
level = 1
prevLevel = 1

def restartGame():
    global board, qix, sparxList, player, level, prevLevel
    startScreen()
    board = Board()
    qix = Qix(5, board, 1)
    sparxList = [Sparx(5, board, 1)]
    player = Player(1, 5, board)
    level = 1
    prevLevel = 1

GAME_RUNNING = 0 
GAME_OVER = 1
GAME_WON = 2
gameState = 0

def startScreen():
    global start
    while start is True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            start = False
        screen.fill(WHITE)
        screen.blit(startScreenText, (endNum/2 -35, endNum/2 - 100))
        pygame.display.update()

        clock.tick(15)

def gameOverScreen():
    global gameState
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        gameState = GAME_RUNNING
        restartGame()
        return 0
    screen.blit(gameOverScreen1, (endNum/2 -140, endNum/2 - 100))
    screen.blit(gameOverScreen2, (endNum / 2 - 50, endNum / 2))
    pygame.display.update()

    clock.tick(15)
    
def victoryScreen():
    global gameState
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        gameState = GAME_RUNNING
        restartGame()
    screen.fill(WHITE)
    screen.blit(victoryText1, (endNum / 2 - 100, endNum / 2 - 100))
    screen.blit(victoryText2, (endNum / 2 - 50, endNum / 2))
    pygame.display.update()

    clock.tick(15)

startScreen()

while running:
    # draw the board
    if gameState == GAME_OVER:
        gameOverScreen()
    elif gameState == GAME_WON:
        victoryScreen()
    elif gameState == GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if level != prevLevel:
            pygame.time.wait(5000)
            prevLevel = level

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
        clock.tick(30)
        qix.move()
        screen.fill(AQUA)
        screen.blit(playerSurf, (0, 0))
        LevelText2 = font.render(str(level), True, BLACK)
        HealthText2 = font.render(str(player.life), True, BLACK)
        CompletionText2 = font.render(str(round((board.getArea() / board.startingArea) * 100)), True, BLACK)
        screen.blit(LevelText1, (LabelNum -40, endNum+15))
        screen.blit(LevelText2, (LabelNum + 20, endNum+15))
        screen.blit(HealthText1, (LabelNum*2 - 40, endNum+15))
        screen.blit(HealthText2, (LabelNum*2 + 30, endNum+15))
        screen.blit(CompletionText1, (LabelNum*3 - 40, endNum+15))
        screen.blit(CompletionText2, (LabelNum*3 + 50, endNum+15))
        drawBoard(board)
        if player.isPush is True:
            drawPush(player)
            check = player.checkCollision(qix, sparxList, board)
            if check != NONE:
                screen.fill(AQUA)
                if check == PASS:
                    player.endPush()
                    if board.checkWin(percent) is True and level == 5:
                        gameState = GAME_WON
                    elif board.checkWin(percent) is True:
                        drawBoard(board)
                        drawObjects(player, qix, sparxList)
                        pygame.display.update()
                        pygame.time.wait(5000)
                        screen.fill(AQUA)
                        pygame.display.update()
                        level += 1
                        board = Board()
                        sparxList = cycleLevel(board, sparxList, level)
                        qix = Qix(qix.speed + SPEED_INC, board, qix.damage)
                        player = Player(player.life, player.speed, board)
                        drawBoard(board)
                        percent += 5
                elif check == QIX:
                    player.resetPush(qix.getDamage())
                elif check == SPARX:
                    player.resetPush(sparxList[0].getDamage())
                elif check == FAIL:
                    player.resetPush(0)
                if player.life == 0:
                    gameState = GAME_OVER
        if level == prevLevel:
            for x in sparxList:
                x.moveCircle()
            qix.move()
        drawObjects(player, qix, sparxList)
        pygame.display.update()
