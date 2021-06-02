import pygame
import math
from queue import PriorityQueue

WIDTH = 800
HEIGHT = 800
WINDOW  = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("A* star Path Finder")


# Colors used in the GUI
WHITE = (255,255,255)
BLUE = (64,224,208)
GREEN = (50,205,50)
BLACK = (0,0,0)
ORANGE = (255,140,0)
CORAL = (240,128,128)
GREY = (119,136,153)
PINK = (128,0,128)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == BLUE
        
    def is_open(self):
        return self.color == ORANGE

    def is_obstacle(self):
        return self.color == GREY

    def is_start(self):
        return self.color == CORAL

    def is_end(self):
        return self.color == PINK

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = BLUE
    
    def make_open(self):
        self.color = ORANGE
    
    def make_start(self):
        self.color = CORAL
    
    def make_end(self):
        self.color = PINK

    def make_obstacle(self):
        self.color = GREY
    
    def make_path(self):
        self.color =  GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False
    

# Calculating the heuristic , we are using manhattan distance for the distance calculation
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def make_box(rows, width):
    box = []
    gap = width // rows
    for i in range(rows):
        box.append([])
        for j in range(rows):
            node =  Node(i, j, gap, rows)
            box[i].append(node)
    return box


# Drawing a border for every node in the box
def draw_box(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0 ), (j *gap,width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_box(win, rows, width)
    pygame.display.update()
        
def get_position(pos, rows,  width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 80
    box = make_box(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, box, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            # left mouse button do the change

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_position(pos, ROWS, width)
                node =  box[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node !=start:
                    end = node
                    end.make_end()

                elif node != start and node !=end:
                    node.make_obstacle()

            # right mouse button to undo the change
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_position(pos, ROWS, width)
                node =  box[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end == None  

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    pass

    
    pygame.quit()

main(WINDOW, WIDTH)

    

        