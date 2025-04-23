import math
import random
from collections import Counter

class Robot:
    def __init__(self, world):
        self.facing_direction = 'up'
        self.position = (8, 8)
        self.grid = [['+' for _ in range(17)] for _ in range(17)]
        self.grid[8][8] = 'R'
        self.world = world
        self.camera_angle = 30 # Lets say default angle = 60 degree
        self.camera_depth = 5 # Lets say default depth for our camera = 5 grids
        self.won = False
        self.lost = False        

        self.moved = []
        self.questionmark = []
        self.safeposition = []
        self.sensed_danger_position = []
        self.sensed_win_position = []
        self.walls = []
        self.possible_winning_position = []

    def set_camera(self, angle, depth):
        self.camera_angle = int(angle / 2)
        self.camera_depth = depth

    def init_robot(self):
        self.facing_direction = 'up'
        self.camera_sensing()
        self.facing_direction = 'down'
        self.camera_sensing()
        self.facing_direction = 'right'
        self.camera_sensing()
        self.facing_direction = 'left'
        self.camera_sensing()

    def display_robot_map(self):
        color_map = {
            'W': '\033[93mW\033[0m',  # Yellow
            'L': '\033[91mL\033[0m',  # Red
            'X': '\033[2;90mX\033[0m',  # Grey
            'R': '\033[94mR\033[0m',  # Blue
            '+': '\033[30m+\033[0m',  # Black
            '-': '\033[97m-\033[0m',   # White
            '?': '\033[91m?\033[0m',  # Red
            '$': '\033[93m$\033[0m', # Yellow
            
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
            if (grid_y + dy, grid_x + dx) not in self.walls:
                    self.walls.append((grid_y + dy, grid_x + dx))
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
            if (x_grid[0], x_grid[1]) not in self.walls:
                    self.walls.append((x_grid[0], x_grid[1]))
        return
    
    def is_not_wall(self, position):
        y, x = position
        return self.grid[y][x] != 'X'
    
    def is_visited(self, position):
        return position in self.moved
    
    def is_safe(self, position):
        return position in self.safeposition
    
    def is_moved(self, position):
        return position in self.moved
    
    def update_possible_dangers(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for sy, sx in self.moved:
            flag_count = 0
            safe_count = 0
            rem_flag = None
            for dy, dx in directions:
                nsy, nsx = sy + dy, sx + dx
                if self.grid[nsy][nsx] == '?':
                    flag_count += 1
                    rem_flag = (nsy, nsx)
                elif self.grid[nsy][nsx] in {'-', 'X', 'S'}:
                    safe_count += 1

            if flag_count == 1 and safe_count == 3:
                if rem_flag not in self.moved and rem_flag not in self.safeposition:
                    self.grid[rem_flag[0]][rem_flag[1]] = 'L'
                    if rem_flag not in self.sensed_danger_position:
                        self.sensed_danger_position.append(rem_flag)

    def sense(self):
        y, x = self.world.robot_position  # actual position
        sy, sx = self.position            # sensed position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        if self.is_visited((sy, sx)):
            return

        sensed_danger = False
        sensed_win = False

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            nsy, nsx = sy + dy, sx + dx
            if self.world.grid[ny, nx] == 'L':
                sensed_danger = True
                if (sy, sx) not in self.sensed_danger_position:
                    self.sensed_danger_position.append((sy, sx))
            if self.world.grid[ny, nx] == 'W':
                sensed_win = True
                if (sy, sx) not in self.sensed_win_position:
                    self.sensed_win_position.append((sy, sx))

        if sensed_win and (sy, sx) not in self.sensed_win_position:
            self.sensed_win_position.append((sy, sx))
            print('sense win')

        if sensed_win:
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                nsy, nsx = sy + dy, sx + dx
                if (nsy, nsx) not in self.possible_winning_position and not self.grid[nsy][nsx] == 'X':
                    self.possible_winning_position.append((nsy, nsx))
            
            for pos in self.possible_winning_position:
                y, x = pos
                if ((y, x - 1) in self.sensed_win_position and (y, x + 1) in self.sensed_win_position) or \
                ((y - 1, x) in self.sensed_win_position and (y + 1, x) in self.sensed_win_position):
                    self.grid[y][x] = 'W'

        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            nsy, nsx = sy + dy, sx + dx
            if not sensed_danger and self.is_not_wall((nsy, nsx)) and not self.is_visited((nsy, nsx)):
                self.grid[nsy][nsx] = 'S'
                if (nsy, nsx) not in self.safeposition:
                    self.safeposition.append((nsy, nsx))
            elif sensed_danger and self.is_not_wall((nsy, nsx)) and not self.is_safe((nsy, nsx)) and not self.is_moved((nsy, nsx)):
                self.grid[nsy][nsx] = '?'
                if (nsy, nsx) not in self.questionmark:
                    self.questionmark.append((nsy, nsx))
        
        self.moved.append((sy, sx))
        print('S Positions : {0}'.format(self.safeposition))
        print('? Positions : {0}'.format(self.questionmark))
        print('Moved Positions : {0}'.format(self.moved))
        print('X Positions : {0}'.format(self.walls))
        print('Sensed Win Positions : {0}'.format(self.sensed_win_position))
        print('Sensed Danger Positions : {0}'.format(self.sensed_danger_position))
        print('Possible W Positions : {0}'.format(self.possible_winning_position))

    def random_move(self):
        directions = [((0, 1), 'right'),
                    ((0, -1), 'left'),
                    ((1, 0), 'down'),
                    ((-1, 0), 'up')]

        y, x = self.world.robot_position
        sy, sx = self.position

        while True:
            dy, dx, self.facing_direction = random.choice([(d[0][0], d[0][1], d[1]) for d in directions])


            # Calculate new positions
            ny, nx = y + dy, x + dx
            nsy, nsx = sy + dy, sx + dx

            # Check if it's a valid move
            if self.grid[nsy][nsx] not in {'X', 'L', '?'}:
                if self.world.grid[ny, nx] == 'W':
                    self.won = True

                self.world.grid[y, x] = '-'
                self.grid[sy][sx] = '-'
                self.world.grid[ny, nx] = 'R'
                self.grid[nsy][nsx] = 'R'

                self.world.robot_position = (ny, nx)
                self.position = (nsy, nsx)

                if self.position in self.safeposition:
                    self.safeposition.remove(self.position)

                self.sense()
                self.update_possible_dangers()
                self.camera_sensing()

                if self.world.robot_position in self.world.losing_positions:
                    self.lost = True
                break