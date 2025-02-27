from world import World
from robotFinalized import Robot

if __name__=='__main__':
    world = World()
    world.display()

    robot = Robot(world)
    robot.set_camera(60, 5)
    # robot.display_robot_map()

    robot.facing_direction = 'up'
    robot.camera_sensing()
    # robot.display_robot_map()

    robot.facing_direction = 'down'
    robot.camera_sensing()
    # robot.display_robot_map()

    robot.facing_direction = 'right'
    robot.camera_sensing()
    # robot.display_robot_map()

    robot.facing_direction = 'left'
    robot.camera_sensing()
    robot.sense(False)
    robot.display_robot_map()
    count = 0
    while (robot.won or robot.lost) == False:
        print(f'------------------------------------------------------------------------------------')
        print(f'---------------------------------move number {count}------------------------------------')
        print('pointless walk : ',robot.pointless_walks)
        print('constrain : ',robot.constrain)

        robot.random_move()
        # robot.camera_sensing()
        print('the robot is now facing :',robot.facing_direction)
        count+=1

            
        print("\n")
        print("Actual Grid")
        world.display()
        print("\n")
        print("Robot's Perception")
        robot.display_robot_map()
        print("\n")

    print("\n")
    print('======================================GAME OVER======================================')
    if robot.lost == True:
        print('=======================================you lost======================================')

    if robot.won == True:
        print('=======================================YOU WON!======================================')
        
    print("\n")
    print("Actual Grid")
    world.display()
    print("\n")
    print("Robot's Perception")
    robot.display_robot_map()
