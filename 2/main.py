import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()
fps = 150

size = (width, height) = (700, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze")
background = (255, 255, 255)
screen.fill(background)

canvas = pygame.Surface(size)
canvas.fill(background)
canvas.set_colorkey(background)

path = pygame.Surface(size)
path.fill(background)
path.set_colorkey(background)

cell = 20
maze_size = 35
goal = [maze_size-1, maze_size-1]

movement = (down, right, up, left) = ((0, 1), (1, 0), (0, -1), (-1, 0))

pygame.draw.rect(screen, (255, 0, 0), (0, 0, cell, cell))
pygame.draw.rect(screen, (0, 255, 255), (width-cell, height-cell, cell, cell))

class MazeGenerator:
    def __init__(self):
        self.size = maze_size
        self.matrix = [[[0, 0, 0, 0] for i in range(self.size)] for i in range(self.size)]
        self.visited = [[True] * (self.size+2)] + [[True] + [False] * self.size + [True] for i in range(self.size)] + [[True] * (self.size+2)]
        self.stack = [(1, 1)]
    
    def gen(self, surface):
        global movement

        front = self.stack[-1]
        self.visited[front[0]][front[1]] = True
        self.white(surface, front[0]-1, front[1]-1)
        choice_list = []
        for dir in movement:
            if self.visited[front[0]+dir[0]][front[1]+dir[1]] == False:
                choice_list.append(dir)
        
        if len(choice_list) != 0:
            next_move = random.choice(choice_list)
            self.stack.append([front[0]+next_move[0], front[1]+next_move[1]])
            if next_move == up:
                self.matrix[front[0]-1][front[1]-1][2] = 1
                self.matrix[front[0]-1][front[1]-2][0] = 1
            elif next_move == left:
                self.matrix[front[0]-1][front[1]-1][3] = 1
                self.matrix[front[0]-2][front[1]-1][1] = 1
            elif next_move == down:
                self.matrix[front[0]-1][front[1]-1][0] = 1
                self.matrix[front[0]-1][front[1]][2] = 1
            else:
                self.matrix[front[0]-1][front[1]-1][1] = 1
                self.matrix[front[0]][front[1]-1][3] = 1
        else:
            self.stack.pop()

    def white(self, surface, i, j):
        if self.matrix[i][j][2] == 1:
            pygame.draw.line(surface, background, (i*cell+1, j*cell), ((i+1)*cell-1, j*cell))
        if self.matrix[i][j][3] == 1:
            pygame.draw.line(surface, background, (i*cell, j*cell+1), (i*cell, (j+1)*cell-1))
        if self.matrix[i][j][0] == 1:
            pygame.draw.line(surface, background, (i*cell+1, (j+1)*cell), ((i+1)*cell-1, (j+1)*cell))
        if self.matrix[i][j][1] == 1:
            pygame.draw.line(surface, background, ((i+1)*cell, j*cell+1), ((i+1)*cell, (j+1)*cell-1))
    
    def gridon(self, surface):
        for i in range(self.size):
            pygame.draw.line(surface, (0, 0, 0), (i*cell, 0), (i*cell, height))
        for i in range(self.size):
            pygame.draw.line(surface, (0, 0, 0), (0, i*cell), (width, i*cell))

class Solver:
    def __init__(self, size, start, goal):
        self.visited = [[False] * size for i in range(size)]
        self.stack = [start]
        self.visited[start[0]][start[1]] = True
        self.goal = goal
        self.color = {'go': (0, 255, 0), 'return': background}

    def move(self, neighbors, surface):
        for i in neighbors:
            if self.visited[i[0]][i[1]] == False:
                self.visited[i[0]][i[1]] = True
                self.stack.append(i)
                self.draw(surface, 'go')
                return None
        self.draw(surface, 'return')
        self.stack.pop()

    def draw(self, surface, mode='go'):
        pygame.draw.rect(surface, self.color[mode], (self.stack[-1][0]*cell, self.stack[-1][1]*cell,cell, cell))

run = True

maze = MazeGenerator()
maze.gridon(canvas)

while len(maze.stack) != 0:
    maze.gen(canvas)
    screen.fill(background)
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, cell, cell))
    pygame.draw.rect(screen, (0, 255, 255), (width-cell, height-cell, cell, cell))
    screen.blit(canvas, (0, 0))
    pygame.display.flip()

solver = Solver(maze_size, [0, 0], goal)
solver.draw(path)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(background)
    pygame.draw.rect(screen, (0, 255, 255), (width-cell, height-cell, cell, cell))

    now = solver.stack[-1]
    if now == goal:
        break
    neighbors = [[now[0]+movement[i][0], now[1]+movement[i][1]] for i in range(4) if maze.matrix[now[0]][now[1]][i] == 1]
    solver.move(neighbors, path)

    screen.blit(path, (0, 0))
    screen.blit(canvas, (0, 0))
    
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()