import math

class Robot:
    def __init__(self, world):
        self.facing_direction = 'up'
        self.position = (8, 8)
        self.grid = [['+' for _ in range(17)] for _ in range(17)]
        self.grid[8][8] = 'R'

        self.world = world
        self.camera_angle = 30 # Lets say default angle = 60 degree
        self.camera_depth = 5 # Lets say default depth for our camera = 5 grids

    def set_camera(self, angle, depth):
        self.camera_angle = int(angle / 2)
        self.camera_depth = depth

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
        def in_grid(position):
            return 0 <= position[0] < 10 and 0 <= position[1] < 10
        
        def generate_points_pairs(walls_list):
            points_pairs = []
            d = 0.5
            for wall in walls_list:
                y, x = wall
                if self.facing_direction == 'up':
                    if wall[1] > self.position[1]:
                        points_pairs.append([[(y + d, wall[1] - d), (y + d, x + d)], [(y + d, x - d), (y - d, x - d)]])
                    elif x < self.position[1]:
                        points_pairs.append([[(y + d, x - d), (y + d, x + d)], [(y + d, x + d), (y - d, x + d)]])
                    else:
                        points_pairs.append([[(y + d, x - d), (y + d, x + d)]])
                if self.facing_direction == 'down':
                    if x > self.position[1]:
                        points_pairs.append([[(y - d, x - d), (y - d, x + d)], [(y + d, x - d), (y - d, x - d)]])
                    elif x < self.position[1]:
                        points_pairs.append([[(y - d, x - d), (y - d, x + d)], [(y + d, x + d), (y - d, x + d)]])
                    else:
                        points_pairs.append([[(y - d, x - d), (y - d, x + d)]])
                if self.facing_direction == 'right':
                    if y > self.position[0]:
                        points_pairs.append([[(y + d, x - d), (y - d, x - d)], [(y - d, x + d), (y - d, x - d)]])
                    elif y < self.position[0]:
                        points_pairs.append([[(y + d, x - d), (y - d, x - d)], [(y + d, x - d), (y + d, x + d)]])
                    else:
                        points_pairs.append([[(y + d, x - d), (y - d, x - d)]])
                if self.facing_direction == 'left':
                    if y > self.position[0]:
                        points_pairs.append([[(y - d, x + d), (y + d, x + d)], [(y - d, x + d), (y - d, x - d)]])
                    elif y < self.position[0]:
                        points_pairs.append([[(y - d, x + d), (y + d, x + d)], [(y + d, x - d), (y + d, x + d)]])
                    else:
                        points_pairs.append([[(y - d, x + d), (y + d, x + d)]])
            return points_pairs
        
        def ccw(A, B, C):
            return (C[0] - A[0]) * (B[1] - A[1]) > (B[0] - A[0]) * (C[1] - A[1])

        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        
        def find_intersection(points_pairs, direction_offsets):
            index_hit = []
            dy, dx = direction_offsets.get(self.facing_direction, (0, 0))
            for d_angle in range(-self.camera_angle, self.camera_angle + 1):
                for more_precise_angle in [0, 0.5]:
                    d_angle += more_precise_angle
                    for index, walls in enumerate(points_pairs):
                        for line in walls:
                            if self.facing_direction in ['up', 'down']:
                                camera_line = [
                                    (self.position[0], self.position[1]),
                                    (self.position[0] + ((self.camera_depth + 1) * math.cos(d_angle * math.pi / 180) * dy),
                                    self.position[1] + ((self.camera_depth + 1) * math.sin(d_angle * math.pi / 180)))]
                            elif self.facing_direction in ['left', 'right']:
                                camera_line = [
                                    (self.position[0], self.position[1]),
                                    (self.position[0] + ((self.camera_depth + 1) * math.sin(d_angle * math.pi / 180)),
                                    self.position[1] + ((self.camera_depth + 1) * math.cos(d_angle * math.pi / 180) * dx))]
                            A, B = camera_line
                            C, D = line
                            if intersect(A, B, C, D):
                                index_hit.append(index)
                                break
                        else:
                            continue
                        break
            return list(set(index_hit))
        
        direction_offsets = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)}

        dy, dx = direction_offsets.get(self.facing_direction, (0, 0))
        robot_y, robot_x = self.world.robot_position
        grid_y, grid_x = self.position

        if self.world.grid[robot_y + dy, robot_x + dx] == 'X':
            self.grid[grid_y + dy][grid_x + dx] = 'X'
            return

        level = 0
        grid_within_angle = []
        while (level < self.camera_depth):
            world_robot_position = self.world.robot_position
            sensing_grid = math.ceil(abs(math.tan(self.camera_angle * math.pi / 180) * (level + 0.5)) - 0.5)
            if self.facing_direction in ['up', 'down']:
                for i in range(0, -sensing_grid-2, -1):
                    sensing_position = (world_robot_position[0] + (level + 1) * dy, world_robot_position[1] + i)
                    robot_sensing_position = (self.position[0] + (level + 1) * dy, self.position[1] + i)
                    if (in_grid(sensing_position) and self.world.grid[sensing_position[0], sensing_position[1]] == 'X'):
                        grid_within_angle.append(robot_sensing_position)
                for i in range(0, sensing_grid + 2):
                    sensing_position = (world_robot_position[0] + (level + 1) * dy, world_robot_position[1] + i)
                    robot_sensing_position = (self.position[0] + (level + 1) * dy, self.position[1] + i)
                    if (in_grid(sensing_position) and self.world.grid[sensing_position[0], sensing_position[1]] == 'X'):
                        grid_within_angle.append(robot_sensing_position)

            if self.facing_direction in ['left', 'right']:
                for i in range(0, -sensing_grid-2, -1):
                    sensing_position = (world_robot_position[0] + i, world_robot_position[1] + (level + 1) * dx)
                    robot_sensing_position = (self.position[0] + i, self.position[1] + (level + 1) * dx)
                    if (in_grid(sensing_position) and self.world.grid[sensing_position[0], sensing_position[1]] == 'X'):
                        grid_within_angle.append(robot_sensing_position)
                for i in range(0, sensing_grid + 2):
                    sensing_position = (world_robot_position[0] + i, world_robot_position[1] + (level + 1) * dx)
                    robot_sensing_position = (self.position[0] + i, self.position[1] + (level + 1) * dx)
                    if (in_grid(sensing_position) and self.world.grid[sensing_position[0], sensing_position[1]] == 'X'):
                        grid_within_angle.append(robot_sensing_position)
            level += 1

        pairs = generate_points_pairs(grid_within_angle)
        sensed_index = find_intersection(pairs, direction_offsets)
        for index in sensed_index:
            x_grid = grid_within_angle[index]
            self.grid[x_grid[0]][x_grid[1]] = 'X'
        return
