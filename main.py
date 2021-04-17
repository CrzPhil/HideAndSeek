import pygame
from pygame.locals import *


def createGrid():
    # Create Grid of Numbers/Objects
    grid = []
    for row in range(19):
        # For each row, we create a list that will represent an entire row
        grid.append([])
        for column in range(19):
            grid[row].append(3)
    # grid = [[3 for x in range(10)] for y in range(10)] -> Shortcut
    return grid


def drawThings(surface):
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (100, 100, 100)
    default = '#202020'

    grid = createGrid()
    grid[18][5] = 0

    # Margin between tiles
    margin = 2
    dimension = 40  # Width and Height of Tiles

    # Default empty-tile color
    color = default

    # Draw Grid
    for i in range(19):
        for j in range(19):
            if grid[i][j] == 0:
                color = red
            else:
                color = default
            pygame.draw.rect(surface, color,
                             pygame.Rect((margin + dimension) * j + margin,
                                         (margin + dimension) * i + margin,
                                         dimension, dimension))


def main():
    pygame.init()
    # GUI Dimensions
    width = 800
    height = 800

    pygame.display.set_caption('Hide and Seek')
    surface = pygame.display.set_mode((width, height))

    background = pygame.Surface((width, height))
    background.fill(pygame.Color(248, 248, 255))  # Background Color

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Click")

        surface.blit(background, (0, 0))
        drawThings(surface)

        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main()
