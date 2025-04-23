from world import World
from robot import Robot

if __name__ == '__main__':
    world = World()
    world.display()

    robot = Robot(world)
    robot.set_camera(60, 5)
    robot.init_robot()
    robot.display_robot_map()
    robot.sense()
    robot.display_robot_map()
    
    count = 0
    while not (robot.won or robot.lost):
        print(f'------------------------------------------------------------------------------------')
        print(f'--------------------------------- move number {count} ------------------------------------')
        
        robot.random_move()
        print('the robot is now facing:', robot.facing_direction)
        count += 1

        print("\n")
        print("Actual Grid")
        world.display()
        print("\n")
        print("Robot's Perception")
        robot.display_robot_map()
        print("\n")

    print("\n")
    print('====================================== GAME OVER ======================================')
    if robot.lost:
        print('======================================= YOU LOST =======================================')
    elif robot.won:
        print('======================================= YOU WON! =======================================')
