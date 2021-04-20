import pygame
from random import randint
from random import seed
from pygame.locals import *


class Seeker:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x  # X-Coordinate inside Grid
        self.y = y  # Y-Coordinate inside Grid
        self.grid[x][y] = 0  # Add Seeker (color)

    def move(self, direction):
        # Check for out-of-bounds
        if (direction == 1 and (self.y + 1 >= len(self.grid[0]))) or (
                direction == 2 and (self.x + 1 >= len(self.grid))) or (
                    direction == 3 and (self.y-1 < 0)) or (
                        direction == 0 and (self.x-1 < 0)):
            print("Out of Bounds!")
            return self.grid
        # 0: Up 1: Right 2: Down 3: Left
        # Right
        if direction == 1 and self.grid[self.x][self.y + 1] == 3:
            self.grid[self.x][self.y + 1] = 0  # 0 is seeker. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.y += 1  # Update location
        # Down
        elif direction == 2 and self.grid[self.x + 1][self.y] == 3:
            self.grid[self.x + 1][self.y] = 0  # 0 is seeker. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.x += 1
        # Left
        elif direction == 3 and self.grid[self.x][self.y - 1] == 3:
            self.grid[self.x][self.y - 1] = 0  # 0 is seeker. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.y -= 1
        # Up
        elif direction == 0 and self.grid[self.x - 1][self.y] == 3:
            self.grid[self.x - 1][self.y] = 0  # 0 is seeker. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.x -= 1

        # else: penalise walking against wall.
        return self.grid


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


def populateGrid(grid):
    seed(1)
    global seeker
    # Amount of obstacles dispersed on grid
    obstacle_count = 30

    # Some obstacles might overlap...
    for i in range(obstacle_count):
        grid[randint(0, 18)][randint(0, 18)] = 2

    # Random Positions for hider and seeker
    seeker = Seeker(grid, randint(0, 18), randint(0, 18))
    grid = seeker.grid  # Updated Grid with seeker in it.

    # grid[randint(0, 18)][randint(0, 18)] = 0  # Seeker
    grid[randint(0, 18)][randint(0, 18)] = 1  # Hider

    return grid


def drawThings(surface, grid):
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (250, 218, 94)
    default = '#202020'

    # Margin between tiles
    margin = 2
    dimension = 40  # Width and Height of Tiles

    # Draw Grid
    for i in range(19):
        for j in range(19):
            if grid[i][j] == 0:
                color = red
            elif grid[i][j] == 1:
                color = blue
            elif grid[i][j] == 2:
                color = yellow
            else:
                color = default
            pygame.draw.rect(surface, color,
                             pygame.Rect((margin + dimension) * j + margin,
                                         (margin + dimension) * i + margin,
                                         dimension, dimension))
    grid = seeker.move(0)


def main():
    pygame.init()
    # GUI Dimensions
    width = 800
    height = 800

    FPS = 30  # frames per second setting
    fpsClock = pygame.time.Clock()

    pygame.display.set_caption('Hide and Seek')
    surface = pygame.display.set_mode((width, height))

    background = pygame.Surface((width, height))
    background.fill(pygame.Color(248, 248, 255))  # Background Color

    grid = populateGrid(createGrid())

    running = True
    control = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Click")

        surface.blit(background, (0, 0))

        drawThings(surface, grid)

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
