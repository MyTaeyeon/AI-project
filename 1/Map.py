import color
import pygame

class Map:
    def __init__(self, size, cell_size):
        self.size = size
        self.canvas = pygame.Surface(self.size)
        self.colorkey = color.purple
        self.color = color.black
        self.canvas.set_colorkey(self.colorkey)
        self.canvas.fill(self.colorkey)
        self.cell = cell_size
        self.matrix = [[0]*(size[0]//cell_size+2)] + [[0]+[1] * (size[0]//cell_size)+[0] for i in range(size[1] // cell_size)] + [[0]*(size[0]//cell_size+2)]
        self.start = (0, 0)
        self.end = (0, 0)
        self.mode = 1
    
    def gridon(self):
        for i in range(len(self.matrix)):
            pygame.draw.line(self.canvas, self.color, (0, self.cell*i), (self.size[0], self.cell*i))
        for i in range(len(self.matrix)):
            pygame.draw.line(self.canvas, self.color, (self.cell*i, 0), (self.cell*i, self.size[1]))

    def draw(self, surface, pos=(0, 0)):
        surface.blit(self.canvas, pos)

    def left_mouse_hold(self):
        pressed_cell = None
        if pygame.mouse.get_pressed()[0] == True:
            pressed_cell = pygame.mouse.get_pos()
        if pressed_cell != None:
            return [pressed_cell[0] // self.cell + 1, pressed_cell[1] // self.cell + 1]
        else:
            return None
        
    def fill_cell(self, position, color):
        pygame.draw.rect(self.canvas, color, ((position[0]-1)*self.cell, (position[1]-1)*self.cell, self.cell, self.cell))
    
    def createMap(self):
        if self.mode == 1:
            pos = self.left_mouse_hold()
            if pos != None:
                self.matrix[pos[0]][pos[1]] = 0
                self.fill_cell(pos, self.color)
            return self.mode
        elif self.mode == 2:
            pos = self.left_mouse_hold()
            if pos != None and self.matrix[pos[0]][pos[1]] != 0:
                self.start = pos
                self.fill_cell(pos, color.green)
                return 3
            return self.mode
        elif self.mode == 3:
            pos = self.left_mouse_hold()
            if pos != None and pos!=self.start and self.matrix[pos[0]][pos[1]] != 0:
                self.fill_cell(pos, color.blue)
                self.end = pos
                return 4
            return self.mode
        else:
            return self.mode
