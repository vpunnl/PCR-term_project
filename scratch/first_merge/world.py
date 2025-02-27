import numpy as np
import random
from collections import deque

class World:
    def __init__(self, size=10):
        self.size = size
        self.robot_position = (0, 0)
        # self.losing_positions = []
        # self.winning_position = (0, 0)
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
        self.losing_positions = self.random_items('L', 6)
        self.winning_position = self.random_winning_position()
        self.random_robot_position()

    def random_items(self, item, count):
        empty_positions = [(i, j) for i in range(1, self.size-1) 
                           for j in range(1, self.size-1) if self.grid[i, j] == '0']
        
        selected_positions = random.sample(empty_positions, min(count, len(empty_positions)))
        for pos in selected_positions:
            self.grid[pos] = item
        return selected_positions

    def random_winning_position(self):
        while True:
            y, x = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.grid[y, x] == '0':
                self.grid[y, x] = 'W'
                self.win_position = (y, x)
                return (y, x)

    def random_robot_position(self):
        while True:
            y, x = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.grid[y, x] == '0':
                self.grid[y, x] = 'R'
                self.robot_position = (y, x)
                break

    def is_reachable(self):
        queue = deque([self.robot_position])
        visited = set()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            y, x = queue.popleft()
            if (y, x) == self.win_position:
                return True
            
            visited.add((y, x))
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if (1 <= ny < self.size-1 and 1 <= nx < self.size-1 and 
                    self.grid[ny, nx] not in {'X', 'L'} and (ny, nx) not in visited):
                    queue.append((ny, nx))
                    visited.add((ny, nx))
        
        return False

    def display(self):
        color_map = {
            'W': '\033[93mW\033[0m',  # Yellow
            'L': '\033[91mL\033[0m',  # Red
            'X': '\033[2;90mX\033[0m',  # Grey
            'R': '\033[94mR\033[0m',   # Blue
            '+': '\033[30mB\033[0m'
        }
        for row in self.grid:
            print(" ".join(color_map.get(cell, cell) for cell in row))
        print()