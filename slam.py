import numpy as np
import random
from collections import deque

class World:
    def __init__(self, size=10):
        self.size = size
        while True:
            self.grid = np.zeros((size, size), dtype=str)
            self.set_grid()
            if self.is_reachable():
                break

    def set_grid(self):
        self.grid[:] = '0'
        self.grid[0, :] = 'X'
        self.grid[-1, :] = 'X'
        self.grid[:, 0] = 'X'
        self.grid[:, -1] = 'X'

        self.random_items('X', 6)
        self.random_items('L', 6)
        self.random_winning_position()
        self.random_robot_position()

    def random_items(self, item, count):
        empty_positions = [(i, j) for i in range(1, self.size-1) 
                           for j in range(1, self.size-1) if self.grid[i, j] == '0']
        
        selected_positions = random.sample(empty_positions, min(count, len(empty_positions)))
        for pos in selected_positions:
            self.grid[pos] = item

    def random_winning_position(self):
        while True:
            x, y = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.grid[x, y] == '0':
                self.grid[x, y] = 'W'
                self.win_position = (x, y)
                break

    def random_robot_position(self):
        while True:
            x, y = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.grid[x, y] == '0':
                self.grid[x, y] = 'R'
                self.robot_position = (x, y)
                break

    def is_reachable(self):
        queue = deque([self.robot_position])
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
                    self.grid[nx, ny] not in {'X', 'L'} and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        
        return False

    def display(self):
        color_map = {
            'W': '\033[93mW\033[0m',  # Yellow
            'L': '\033[91mL\033[0m',  # Red
            'X': '\033[30mX\033[0m',  # Black
            'R': '\033[94mR\033[0m'   # Blue
        }
        for row in self.grid:
            print(" ".join(color_map.get(cell, cell) for cell in row))
        print()

if __name__ == '__main__':
    world = World()
    world.display()
