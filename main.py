import pygame
from random import randint
from random import seed
from pygame.locals import *
import constants

'''
https://www.redblobgames.com/grids/line-drawing.html for the line-drawing
'''


# Linear Interpolation
def lerp(start, end, t):
    return start + t * end


# Return Point on Line between two points
def lerp_point(p0, p1, t):
    return (lerp(p0[0], p1[0], t),
            lerp(p0[1], p1[1], t))


# Round potential floats to ints; Note: Python3 rounds x.5 DOWN -> i.e round(2.5) = 2
def round_point(p):
    return round(p[0]), round(p[1])


# Diagonal Distance between two points
def distance(p0, p1):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    return max(abs(dx), abs(dy))


# Draw line between two points
def line(p0, p1):
    points = []
    N = distance(p0, p1)
    for step in range(N):
        if N == 0:
            t = 0
        else:
            t = step/N
        points.append(round_point(lerp_point(p0, p1, t)))
    return points


def look(grid: list, pos_x: int, pos_y: int):
    # Line of Sight [0] - UP [1] - RIGHT [2] - DOWN [3] - LEFT
    los = [[], [], [], []]
    # 4 Directions:
    for i in range(4):
        if i == 0:
            # Check for Out-of-Bounds Up
            if pos_x - constants.MAX_DISTANCE < 0:
                # If there is at least one square before out-of-bounds
                if pos_x - constants.MAX_DISTANCE + 1 == 0:
                    for j in range(1, constants.MAX_DISTANCE):
                        los[0].append(grid[pos_x - j][pos_y])
                # If there are two squares before o-o-b
                elif pos_x - constants.MAX_DISTANCE + 2 == 0:
                    for j in range(1, constants.MAX_DISTANCE - 1):
                        los[0].append(grid[pos_x - j][pos_y])
                # If there are three squares before o-o-b
                elif pos_x - constants.MAX_DISTANCE + 3 == 0:
                    for j in range(1, constants.MAX_DISTANCE - 2):
                        los[0].append(grid[pos_x - j][pos_y])
            # If everything is within range
            else:
                for j in range(1, constants.MAX_DISTANCE + 1):
                    los[0].append(grid[pos_x - j][pos_y])
        elif i == 1:
            # Check for Out-of-Bounds RIGHT
            if pos_y + constants.MAX_DISTANCE >= constants.GRID_SIZE:
                # If there are two squares before o-o-b
                if pos_y + constants.MAX_DISTANCE - 1 == constants.GRID_SIZE - 1:
                    for j in range(1, constants.MAX_DISTANCE):
                        los[1].append(grid[pos_x][pos_y + j])
                # If there is one square before o-o-b
                elif pos_y + constants.MAX_DISTANCE - 2 == constants.GRID_SIZE - 1:
                    for j in range(1, constants.MAX_DISTANCE - 1):
                        los[1].append(grid[pos_x][pos_y + j])
                # Range 4 Tile one before o-o-b
                elif pos_y + constants.MAX_DISTANCE - 3 == constants.GRID_SIZE - 1:
                    for j in range(1, constants.MAX_DISTANCE - 2):
                        los[1].append(grid[pos_x][pos_y + j])
            else:
                for j in range(1, constants.MAX_DISTANCE + 1):
                    los[1].append(grid[pos_x][pos_y+j])
        elif i == 2:
            # Check for Out-of-Bounds DOWN
            if pos_x + constants.MAX_DISTANCE >= constants.GRID_SIZE:
                pass
            else:
                for j in range(1, constants.MAX_DISTANCE + 1):
                    los[2].append(grid[pos_x + j][pos_y])
        elif i == 3:
            # Check for Out-of-Bounds LEFT
            if pos_y - constants.MAX_DISTANCE < 0:
                pass
            else:
                for j in range(1, constants.MAX_DISTANCE + 1):
                    los[3].append(grid[pos_x][pos_y - j])
    print(los)


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
            print("Seeker Out of Bounds!")
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

    def drawRay(self):
        # Y and X are flipped, since in 2D arrays[x][y] y is the column, and x the row
        los = line((self.y, self.x), (self.y, self.x+3))    # Line of Sight Up
        print(los)


class Hider:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x  # X-Coordinate inside Grid
        self.y = y  # Y-Coordinate inside Grid
        self.grid[x][y] = 1  # Add Seeker (color)

    def move(self, direction):
        # Check for out-of-bounds
        if (direction == 1 and (self.y + 1 >= len(self.grid[0]))) or (
                direction == 2 and (self.x + 1 >= len(self.grid))) or (
                    direction == 3 and (self.y-1 < 0)) or (
                        direction == 0 and (self.x-1 < 0)):
            print("Hider Out of Bounds!")
            return self.grid
        # 0: Up 1: Right 2: Down 3: Left
        # Right
        if direction == 1 and self.grid[self.x][self.y + 1] == 3:
            self.grid[self.x][self.y + 1] = 1  # 1 is hider. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.y += 1  # Update location
        # Down
        elif direction == 2 and self.grid[self.x + 1][self.y] == 3:
            self.grid[self.x + 1][self.y] = 1  # 1 is hider. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.x += 1
        # Left
        elif direction == 3 and self.grid[self.x][self.y - 1] == 3:
            self.grid[self.x][self.y - 1] = 1  # 1 is hider. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.y -= 1
        # Up
        elif direction == 0 and self.grid[self.x - 1][self.y] == 3:
            self.grid[self.x - 1][self.y] = 1  # 1 is hider. more generally: self.grid[self.x][self.y]
            self.grid[self.x][self.y] = 3  # 3 is empty tile.
            self.x -= 1

        # else: penalise walking against wall.
        return self.grid


def createGrid():
    # Create Grid of Numbers/Objects
    grid = []
    for row in range(constants.GRID_SIZE):
        # For each row, we create a list that will represent an entire row
        grid.append([])
        for column in range(constants.GRID_SIZE):
            grid[row].append(3)
    # grid = [[3 for x in range(10)] for y in range(10)] -> Shortcut
    return grid


def populateGrid(grid):
    global seeker, hider

    # Some obstacles might overlap...
    for i in range(constants.OBSTACLE_COUNT):
        grid[randint(0, constants.GRID_SIZE-1)][randint(0, constants.GRID_SIZE-1)] = 2

    # Random Positions for hider and seeker
    seeker = Seeker(grid, randint(0, constants.GRID_SIZE-1), randint(0, constants.GRID_SIZE-1))
    # seeker = Seeker(grid, 1, 5)
    grid = seeker.grid  # Updated Grid with seeker in it.
    hider = Hider(grid, randint(0, constants.GRID_SIZE-1), randint(0, constants.GRID_SIZE-1))
    grid = hider.grid

    return grid


def drawThings(surface, grid):
    # Draw Grid
    for i in range(constants.GRID_SIZE):
        for j in range(constants.GRID_SIZE):
            if grid[i][j] == 0:
                color = constants.SEEKER_COLOR
            elif grid[i][j] == 1:
                color = constants.HIDER_COLOR
            elif grid[i][j] == 2:
                color = constants.WALL_COLOR
            else:
                color = constants.BACKGROUND
            pygame.draw.rect(surface, color,
                             pygame.Rect((constants.MARGIN + constants.TILE_SIZE) * j + constants.MARGIN,
                                         (constants.MARGIN + constants.TILE_SIZE) * i + constants.MARGIN,
                                         constants.TILE_SIZE, constants.TILE_SIZE))
    seeker.move(randint(0, 3))
    look(grid, seeker.x, seeker.y)
    hider.move(randint(0, 3))
    pygame.time.delay(100)


def main():
    pygame.init()

    FPS = 30  # frames per second setting
    fpsClock = pygame.time.Clock()

    pygame.display.set_caption('Hide and Seek')
    surface = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))

    background = pygame.Surface((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    background.fill(pygame.Color(248, 248, 255))  # Background Color

    grid = populateGrid(createGrid())

    running = True

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
