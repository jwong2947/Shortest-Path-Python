# -*- coding: utf-8 -*-
"""
Module using Pygame to find the shortest pathway between 2 points on a 10x10 based grid

controls:
    
left click - > add obstruction (red)
right click - > remove any placed objects
middle mouse click - > add origin and destination (blue)
s - > find shortest path 
c - > clear board

"""
___author___ = "Jonathan Wong"

import sys, pygame
from copy import copy, deepcopy
import numpy as np

BLACK = (0,0,0)
WHITE = (200,200,200)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0,128,0)
window_height = 200
window_width = 200

GRID_HEIGHT = 10
GRID_WIDTH = 10

front_grid = []
for row in range(10):
    front_grid.append([])
    for column in range(10):
       front_grid[row].append(0)
       
back_grid = deepcopy(front_grid)


pygame.init()
screen = pygame.display.set_mode((window_width,window_height))
clock = pygame.time.Clock()       
       
       

def main():
    start_counter = 0
    done = False
    finished = False
    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and finished == False: # adds barriers
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x = pos[0]//20
                    y = pos[1]//20
                    if start_counter == 2:
                        if check_path(front_grid,x,y,True) == True:
                            if front_grid[x][y] == -2:
                                start_counter = start_counter - 1
                            front_grid[x][y] = -1
                        
                    else:
                        if front_grid[x][y] == -2:
                            start_counter = start_counter - 1
                        front_grid[x][y] = -1
                elif event.button == 2: # adds origin destination
                    if start_counter == 0:
                        pos = pygame.mouse.get_pos()
                        x = pos[0]//20
                        y = pos[1]//20
                        front_grid[x][y] = -2
                        start_counter += 1
                    elif start_counter == 1:
                    
                        pos = pygame.mouse.get_pos()
                        x = pos[0]//20
                        y = pos[1]//20
                        if check_path(front_grid,x,y) == True:
                             front_grid[x][y] = -2
                             start_counter += 1
                elif event.button == 3: # removes barriers or origin destination
                    pos = pygame.mouse.get_pos()
                    x = pos[0]//20
                    y = pos[1]//20
                    if front_grid[x][y] == -2:
                        start_counter = start_counter - 1
                    front_grid[x][y] = 0
            
            elif event.type == pygame.KEYDOWN and finished == False:
                 if event.key == pygame.K_s and start_counter == 2 and done == False:
                    
                    update_back_grid(front_grid)
                    print_grid(back_grid)
                    find_shortest_path(back_grid)
                    print_grid(back_grid)
                    path = backtrack_to_start(back_grid)
                    done = draw_path(path)
                    finished = True
                 elif event.key == pygame.K_c:
                     reset_board(front_grid)
                     start_counter = 0
                     done = False
            elif event.type == pygame.KEYDOWN and finished == True:
                 reset_board(front_grid)
                 start_counter = 0
                 done = False
                 finished = False
         
                
        pygame.display.update()
        
def drawGrid(): # draws the grid on the console
    blockSize = 20 #Set the size of the grid block
    for x in range(0, window_width, blockSize):
        for y in range(0, window_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            row = int(x/blockSize)
            column = int(y/blockSize)
            if front_grid[row][column] == -1:
                pygame.draw.rect(screen, RED, rect, 1)
            elif front_grid[row][column] == 0:
                pygame.draw.rect(screen, WHITE, rect, 1)
            elif front_grid[row][column] == -2:
                pygame.draw.rect(screen, BLUE, rect, 1)
            elif front_grid[row][column] == "*":
                pygame.draw.rect(screen, GREEN, rect, 1)
   
def flood_grid(grid,x,y,counter): # function floods the grid with the lowest steps to the destination
    if grid[x][y] == 0:
        grid[x][y] = counter
    elif grid[x][y] < 0:
        return 0
    elif counter >= grid[x][y]:
        return 0
    elif counter < grid[x][y]:
        grid[x][y] = counter
        
    if x+1 < len(grid[0]):
        flood_grid(grid,x+1,y,counter+1)
    if x-1 >= 0:
        flood_grid(grid,x-1,y,counter+1)
    if y+1 <  len(grid):
        flood_grid(grid,x,y+1,counter+1)
    if y-1 >= 0:
        flood_grid(grid,x,y-1,counter+1)       

def update_back_grid(grid): # updates the back end grid
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            back_grid[i][j] = grid[i][j]

def print_grid(grid):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in grid]))
    print("----------------------------")
       
def find_shortest_path(grid): # function labels the grid with the shortest steps to the destination through adjacent nodes
    n = deepcopy(grid)
    c = np.array(n)
    start = np.argwhere(c == -2)
    x1 = start[0][0]
    y1 = start[0][1]
    grid[x1][y1] = 0
    flood_grid(grid,x1,y1,1)
    
def backtrack_to_start(grid): # function retraces from the end back to the start
    n = deepcopy(grid)
    c = np.array(n)
    start = np.argwhere(c == -2)
    x = start[0][0]
    y = start[0][1]
    path = []
    path.append((x,y))
    found = False
    
    num = []
    if x+1 < len(grid[0]):
        if grid[x+1][y] != -1 and grid[x+1][y] != 0:
            num.append(grid[x+1][y])
    if x-1 >= 0:
        if grid[x-1][y] != -1 and grid[x-1][y] != 0:
            num.append(grid[x-1][y])
    if y+1 <  len(grid):
        if grid[x][y+1] != -1 and grid[x][y+1] != 0:
            num.append(grid[x][y+1])
    if y-1 >= 0:
        if grid[x][y-1] != -1 and grid[x][y-1] != 0:
            num.append(grid[x][y-1])
    print(num)
    counter = min(num) + 1
    print(counter)
    while not found:
       if grid[x][y] == 1:
           found = True
           break
       
       if x+1 < len(grid[0]) and grid[x+1][y] == counter-1:
           x = x +1
           path.append((x,y))
           counter = counter -1
       elif x-1 >=0 and grid[x-1][y] == counter-1:
           x = x-1
           path.append((x,y))
           counter = counter -1
       elif y+1 < len(grid) and grid[x][y+1] == counter-1:
           y = y+1
           path.append((x,y))
           counter = counter -1
       elif y-1 >= 0 and grid[x][y-1] == counter-1:
           y = y-1
           path.append((x,y))
           counter = counter -1
       else:
           break
           
    print(path)
    return path

def draw_path(path): # draws the shortest path in green on the screen
    for i in path:
        x = i[0]
        y = i[1]
        front_grid[x][y] = "*"
    return True
        
def reset_board(grid): # resets the front grid board
     for i in range(len(grid[0])):
        for j in range(len(grid)):
            grid[i][j] = 0

def check_path(grid,x,y,two_on = False): # function to check if there is at least one path from origin to destination
    if two_on == False:
        check = deepcopy(grid)
        c = np.array(check)
        start = np.argwhere(c == -2)
        #print(start)
        x1 = start[0][0]
        y1 = start[0][1]
        check[x1][y1] = 0
        flood_grid(check,x1,y1,1)
        if check[x][y] != 0:
            return True
        else:
            return False
    else:
        check = deepcopy(grid)
        c = np.array(check)
        start = np.argwhere(c == -2)
    #print(start)
        x1 = start[0][0]
        y1 = start[0][1]
        x2 = start[1][0]
        y2 = start[1][1]
        check[x1][y1] = 0
        check[x2][y2] = 0
        check[x][y] = -1
        flood_grid(check,x1,y1,1)
        #print_grid(check)
        if check[x2][y2] != 0:
            return True
        else:
            return False


main()