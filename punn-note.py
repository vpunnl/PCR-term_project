import numpy as np
import random
from collections import deque

class World:
    def __init__(self, size=10):
        self.size = size
        self.won = False
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
    
    def random_move(self):

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        x, y = self.actual_position # position on the actual grid
        sx, sy = self.sensed_position # position on the grid that the robot can see
        while True: # loop until found a valid movement then break the loop

            # heuristic, check surrounding area
            winning = ''

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if self.actual_grid[nx, ny] == 'W':
                    winning = (dx, dy)
                    nsx, nsy = sx + dx, sy + dy
                    break
            if not winning:
                dx, dy = random.choice(directions)
                nx, ny = x + dx, y + dy
                nsx, nsy = sx + dx, sy + dy

            # do the logic of moving within the map, not hitting the walls, and not hitting the L, trying to move to the area that hasnt been explored yet
            if self.actual_grid[nx, ny] not in {'X', 'L'}:
                if self.actual_grid[nx, ny] == 'W':
                    print("Winning position reached")
                    self.won = True
                # setting visited area
                self.actual_grid[x, y] = '-'
                self.sensed_grid[sx, sy] = '-'
                # current robot position
                self.actual_grid[nx, ny] = 'R'
                self.sensed_grid[nsx, nsy] = 'R'
                # update the position
                self.actual_position = (nx, ny)
                self.sensed_position = (nsx, nsy)
                
                for dx, dy in directions:
                    x, y = self.actual_position
                    sx, sy = self.sensed_position
                    nx, ny = x + dx, y + dy
                    nsx, nsy = sx + dx, sy + dy
                    if self.actual_grid[nx, ny] in {'W', 'L'}:
                        self.sensed_grid[nsx, nsy] = self.actual_grid[nx, ny]
                break
            else: # see X or L
                self.sensed_grid[nsx, nsy] = self.actual_grid[nx, ny]
            
            # done moving, now will magically know
            for dx, dy in directions:
                x, y = self.actual_position
                nx, ny = x + dx, y + dy
                if self.actual_grid[nx, ny] in {'W', 'L'}:
                    self.sensed_grid[nsx, nsy] = self.actual_grid[nx, ny]
        
    def display_sensed(self):
        color_map = {
            'W': '\033[93mW\033[0m',  # Yellow
            'L': '\033[91mL\033[0m',  # Red
            'X': '\033[2;90mX\033[0m',  # Grey
            'R': '\033[94mR\033[0m',   # Blue
            '+': '\033[30m+\033[0m'  # Black
        }
        for row in self.sensed_grid:
            print(" ".join(color_map.get(cell, cell) for cell in row))
        print()


if __name__ == '__main__':
    world = World()
    count = 0
    while world.won == False:
        world.random_move()
        # world.display()
        world.display_sensed()
        count+=1
    # world.display()
