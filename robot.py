import math

class Robot:
    def __init__(self, world):
        self.facing_direction = 'up'
        self.position = (8, 8)  # Center of the 17x17 grid
        self.grid = [['+' for _ in range(17)] for _ in range(17)]
        self.grid[8][8] = 'R'  # Place the robot in the center

        self.world = world
        # print('Robot Position : ('+str(self.position[0])+', '+str(self.position[1])+')')

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


    def camera_sensing(self, angle, depth):
        def in_grid(position):
            return 0 <= position[0] < 10 and 0 <= position[1] < 10
        
        def generate_points_pairs(walls_list):
            points_pairs = []
            # print(walls_list)
            for wall in walls_list:
                if self.facing_direction == 'up':
                    if wall[1] > self.position[1]:
                        points_pairs.append([[(wall[0] + 0.5, wall[1] - 0.5), (wall[0] + 0.5, wall[1] + 0.5)], [(wall[0] + 0.5, wall[1] - 0.5), (wall[0] - 0.5, wall[1] - 0.5)]])
                    elif wall[1] < self.position[1]:
                        points_pairs.append([[(wall[0] + 0.5, wall[1] - 0.5), (wall[0] + 0.5, wall[1] + 0.5)], [(wall[0] + 0.5, wall[1] + 0.5), (wall[0] - 0.5, wall[1] + 0.5)]])
                    else:
                        points_pairs.append([[(wall[0] + 0.5, wall[1] - 0.5), (wall[0] + 0.5, wall[1] + 0.5)]])
            return points_pairs
        
        def ccw(A, B, C):
            return (C[0] - A[0]) * (B[1] - A[1]) > (B[0] - A[0]) * (C[1] - A[1])

        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        
        def find_intersection(grid, points_pairs):
            index_hit = []
            for d_angle in range(-angle, angle + 1):
                for more_precise_angle in [0, 0.5]:
                    d_angle += more_precise_angle
                    for index, walls in enumerate(points_pairs):
                        for line in walls:
                            camera_line = [
                                (self.position[0], self.position[1]),
                                (self.position[0] - ((depth + 1) * math.cos(d_angle * math.pi / 180)),
                                self.position[1] + ((depth + 1) * math.sin(d_angle * math.pi / 180)))]
                            A, B = camera_line
                            C, D = line
                            if intersect(A, B, C, D):
                                index_hit.append(index)
                                break
                        else:
                            continue
                        break
            return list(set(index_hit))
        
        if self.world.grid[self.world.robot_position[0] - 1, self.world.robot_position[1]] == 'X':
            self.grid[self.position[0] - 1][self.position[1]] = 'X'
            return

        level = 0
        grid_within_angle = []
        while (level < depth):
            horizontal_sensing = math.ceil(abs(math.tan(angle * math.pi / 180) * (level + 0.5)) - 0.5)
            for i in range(0, -horizontal_sensing-2, -1):
                world_robot_position = self.world.robot_position
                sensing_position = (world_robot_position[0] - level - 1, world_robot_position[1] + i)
                robot_sensing_position = (self.position[0] - level - 1, self.position[1] + i)
                # if in_grid(sensing_position):
                #     self.grid[robot_sensing_position[0]][robot_sensing_position[1]] = self.world.grid[sensing_position[0]][sensing_position[1]]
                if (in_grid(sensing_position) and self.world.grid[sensing_position[0], sensing_position[1]] == 'X'):
                    grid_within_angle.append(robot_sensing_position)
            for i in range(0, horizontal_sensing + 2):
                world_robot_position = self.world.robot_position
                sensing_position = (world_robot_position[0] - level - 1, world_robot_position[1] + i)
                robot_sensing_position = (self.position[0] - level - 1, self.position[1] + i)
                # if in_grid(sensing_position):
                #     self.grid[robot_sensing_position[0]][robot_sensing_position[1]] = self.world.grid[sensing_position[0]][sensing_position[1]]
                if (in_grid(sensing_position) and self.world.grid[sensing_position[0], sensing_position[1]] == 'X'):
                    grid_within_angle.append(robot_sensing_position)
            level += 1
        # print(grid_in_angle)
        pairs = generate_points_pairs(grid_within_angle)
        # print('')
        sensed_index = find_intersection(grid_within_angle, pairs)
        for index in sensed_index:
            x_grid = grid_within_angle[index]
            self.grid[x_grid[0]][x_grid[1]] = 'X'
        return
