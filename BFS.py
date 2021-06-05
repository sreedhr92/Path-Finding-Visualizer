import queue
import pygame
from collections import deque
import time
from pygame.locals import *

WIDTH = 700
HEIGHT = 800
pygame.init()
WINDOW  = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Path Finder App")
font = pygame.font.SysFont(None, 25)


# Colors used in the GUI
WHITE = (255,255,255)
BLUE = (64,224,208)
GREEN = (50,205,50)
BLACK = (0,0,0)
ORANGE = (255,140,0)
CORAL = (0,128,228)
GREY = (119,136,153)
PINK = (128,0,128)

TIME = 0
NODES = 0

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

    def update_neighbors(self, box):
        self.neighbors=[]
        if self.row+1 < self.total_rows  and not box[self.row+1][self.col].is_obstacle():
            self.neighbors.append(box[self.row+1][self.col])
        
        if self.row-1 >= 0 and not box[self.row-1][self.col].is_obstacle():
            self.neighbors.append(box[self.row-1][self.col])
        
        if self.col+1 < self.total_rows and not box[self.row][self.col+1].is_obstacle():
            self.neighbors.append(box[self.row][self.col+1])
        
        if self.col-1 >= 0  and not box[self.row][self.col-1].is_obstacle():
            self.neighbors.append(box[self.row][self.col-1])

    def __lt__(self, other):
        return False
    

# Calculating the heuristic , we are using manhattan distance for the distance calculation

def build_path(parent, end , draw):
    current = end
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()


def breadth_first_search(draw, box, start, end):
    count  = 0
    frontier = deque()
    frontier.append(start)
    parent = {}

    
    algo ="Algo :BFS "
    start_time = time.time()
    frontier_hash = set() # Keep tracks of the Visited Nodes
    while len(frontier):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = frontier.popleft()
        frontier_hash.add(current)

        if current == end:
            build_path(parent,end,draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:

            if neighbor not in frontier_hash:
                count+=1
                frontier.append(neighbor)
                frontier_hash.add(neighbor)
                neighbor.make_open()

        TIME = time.time()-start_time
        NODES = count
        draw_stats(NODES,TIME,algo)
        draw()

        if current !=start:
            current.make_closed()

    return False

def make_box(rows, width):
    box = []
    gap = width // rows
    for i in range(rows):
        box.append([])
        for j in range(rows):
            node =  Node(i, j, gap, rows)
            box[i].append(node)
    return box

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)

def draw_stats(count , time, algo):
    draw_text(algo,font,BLACK,WINDOW,15, 725)
    draw_text("Time : "+str(time),font,BLACK,WINDOW,200, 725)
    draw_text("Visited Nodes count :"+ str(count),font,BLACK,WINDOW,450, 725)
    pygame.display.update()  

# Drawing a border for every node in the box
def draw_box(win, rows, width):
    gap = width // rows
    for i in range(rows+1):
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
    ROWS = 50
    box = make_box(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, box, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # left mouse button do the change

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_position(pos, ROWS, width)
                if row >= len(box) or col >= len(box[0]):
                    continue
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
                if event.key == pygame.K_SPACE and start and end:
                    for row in box:
                        for node in row:
                            node.update_neighbors(box)

                    breadth_first_search(lambda: draw(win, box, ROWS, width), box, start, end)
                
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    box = make_box(ROWS, width)

    
    pygame.quit()

def main_menu():
    pass

main(WINDOW, WIDTH)

    

        