import numpy as np
import random
from collections import deque

class World:
    def __init__(self, size=10):
        self.size = size
        self.won = False
        self.constrain = {'X','L', '?', '!'}
        self.pointless_walks = 0
        while True:
            self.actual_grid = np.zeros((size, size), dtype=str)
            self.set_grid()
            self.sensed_grid = np.zeros((17, 17), dtype=str)
            self.sensed_grid[:] = '+'
            self.sensed_grid[8,8] = 'R'
            if self.is_reachable():
                break
        

    def set_grid(self):
        self.actual_grid[:] = '0'
        self.actual_grid[0, :] = 'X'
        self.actual_grid[-1, :] = 'X'
        self.actual_grid[:, 0] = 'X'
        self.actual_grid[:, -1] = 'X'

        self.random_items('X', 6)
        self.random_items('L', 6)
        self.random_winning_position()
        self.random_robot_position()

    def random_items(self, item, count):
        empty_positions = [(i, j) for i in range(1, self.size-1) 
                           for j in range(1, self.size-1) if self.actual_grid[i, j] == '0']
        
        selected_positions = random.sample(empty_positions, min(count, len(empty_positions)))
        for pos in selected_positions:
            self.actual_grid[pos] = item

    def random_winning_position(self):
        while True:
            x, y = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.actual_grid[x, y] == '0':
                self.actual_grid[x, y] = 'W'
                self.win_position = (x, y)
                break

    def random_robot_position(self):
        while True:
            x, y = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.actual_grid[x, y] == '0':
                self.actual_grid[x, y] = 'R'
                self.actual_position = (x, y)
                self.sensed_position = (8,8) # middle of the map
                break

    def is_reachable(self):
        queue = deque([self.actual_position])
        visited = set()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            x, y = queue.popleft()
            if (x, y) == self.win_position:
                return True
            
            visited.add((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (1 <= nx < self.size-1 and 1 <= ny < self.size-1 and 
                    self.actual_grid[nx, ny] not in {'X', 'L'} and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        
        return False

    def display(self):
        color_map = {
            'W': '\033[93mW\033[0m',  # Yellow
            'L': '\033[91mL\033[0m',  # Red
            'X': '\033[2;90mX\033[0m',  # Grey
            'R': '\033[94mR\033[0m'   # Blue
        }
        for row in self.actual_grid:
            print(" ".join(color_map.get(cell, cell) for cell in row))
        print()
        
    def sense(self,visited):
        x, y = self.actual_position
        sx, sy = self.sensed_position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        cautious = False
        might_validate_coord = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            nsx, nsy = sx + dx, sy + dy
            might_validate_coord.append(((nx,ny),(nsx, nsy)))
            # print('around actual : ',self.actual_grid[nx, ny])
            if self.actual_grid[nx, ny] == 'L':
                cautious = True
            if self.actual_grid[nx, ny] == 'W':
                self.sensed_grid[nsx, nsy] = 'W'
            
        if cautious: # if surrounding is still unexplored("+"), mark it as "?". the one with different mark than "+" will remain the same
            if not visited:
                for actual,coord in might_validate_coord:
                    if self.actual_grid[actual] == 'X': # assume see walls
                        self.sensed_grid[coord] = 'X' # assume see walls
                    if self.sensed_grid[coord] == '+':
                        self.sensed_grid[coord] = '?'
                    elif self.sensed_grid[coord] == '?':
                        self.sensed_grid[coord] = '!'
                    elif self.sensed_grid[coord] == '!':
                        self.sensed_grid[coord] = 'L'
        else: 
            for actual,coord in might_validate_coord:
                if self.sensed_grid[coord] in {'+', '?', '!'}: # validation of the "?" and the unexplored area
                    if self.actual_grid[actual] == 'X': # assume see walls
                        self.sensed_grid[coord] = 'X' # assume see walls
                    else:
                        self.sensed_grid[coord] = 'S'



    def random_move(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        x, y = self.actual_position
        sx, sy = self.sensed_position
        while True:
            found_winning_pos = ''
            if not directions:
                #randomly choose direction
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                nx, ny = x + dx, y + dy
                nsx, nsy = sx + dx, sy + dy
            if directions:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if self.actual_grid[nx, ny] == 'W':
                        found_winning_pos = (dx, dy)
                        nsx, nsy = sx + dx, sy + dy
                        break
                if not found_winning_pos:
                    dx, dy = random.choice(directions)
                    nx, ny = x + dx, y + dy
                    nsx, nsy = sx + dx, sy + dy

            # assume see walls
            # if self.actual_grid[nx, ny] in {'X'}:
            #     self.sensed_grid[nsx, nsy] = 'X'
            visited = False
            # if self.sensed_grid[nsx, nsy] not in {'L', '?', '!'} and self.actual_grid[nx, ny] not in {'X'}:
            if self.pointless_walks > 100:
                self.constrain = {'X','L', '!'}
            elif self.pointless_walks > 200:
                self.constrain = {'X','L'}
            else:
                self.constrain = {'X','L', '?', '!'}

            if self.sensed_grid[nsx, nsy] not in self.constrain or not directions:
                if self.sensed_grid[nsx,nsy] == '-':
                    visited = True
                    self.pointless_walks+=1
                else:
                    self.pointless_walks = 0
                if self.actual_grid[nx, ny] == 'W':
                    self.won = True
                    self.actual_grid[x, y] = '-'
                    self.sensed_grid[sx, sy] = '-'
                    self.actual_grid[nx, ny] = 'R'
                    self.sensed_grid[nsx, nsy] = 'R'
                    print('moved')
                    break
                self.actual_grid[x, y] = '-'
                self.sensed_grid[sx, sy] = '-'
                self.actual_grid[nx, ny] = 'R'
                self.sensed_grid[nsx, nsy] = 'R'
                self.actual_position = (nx, ny)
                self.sensed_position = (nsx, nsy)
                print('moved')
                self.sense(visited)
                break
            else:
                directions.remove((dx, dy))
        
    def display_sensed(self):
        color_map = {
            'W': '\033[93mW\033[0m',  # Yellow
            'L': '\033[91mL\033[0m',  # Red
            'X': '\033[2;90mX\033[0m',  # Grey
            'R': '\033[94mR\033[0m',   # Blue
            '+': '\033[30m+\033[0m',  # Black
            '?': '\033[91m?\033[0m',  # Red
            '!': '\033[91m!\033[0m'  # Red
        }
        for row in self.sensed_grid:
            print(" ".join(color_map.get(cell, cell) for cell in row))
        print()


if __name__ == '__main__':
    world = World()
    count = 0
    world.display()
    world.sense(False)
    world.display_sensed()
    while world.won == False:
        print('------------------------------------new move------------------------------------')
        print(count)
        print('pointless walk : ',world.pointless_walks)
        print('constrain : ',world.constrain)

        world.random_move()
        world.display()
        world.display_sensed()
        count+=1
    world.display()        
    world.display_sensed()

