import pygame

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
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
