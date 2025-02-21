class Robot:
    def __init__(self, world):
        self.facing_direction = 'up'
        self.position = (8, 8)  # Center of the 17x17 grid
        self.grid = [['+' for _ in range(17)] for _ in range(17)]
        self.grid[8][8] = 'R'  # Place the robot in the center

        self.world = world

    def display_robot_map(self):
        color_map = {
            'W': '\033[93mW\033[0m',  # Yellow
            'L': '\033[91mL\033[0m',  # Red
            'X': '\033[2;90mX\033[0m',  # Grey
            'R': '\033[94mR\033[0m',  # Blue
            '+': '\033[30m+\033[0m',  # Black
            '-': '\033[97m-\033[0m'   # White
        }
        for row in self.grid:
            print(' '.join(color_map.get(cell, cell) for cell in row))


    def camera_sensing(self):
        world_robot_position = self.world.robot_position
        level = 0

        while True:
            level += 1
            if self.world.grid[world_robot_position[0] - level, world_robot_position[1]] == 'X':
                self.grid[self.position[0] - level][self.position[1]] = 'X'
                break
            else:
                self.grid[self.position[0] - level][self.position[1]] = '-'