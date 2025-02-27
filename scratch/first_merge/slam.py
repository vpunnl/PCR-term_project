from world import World
from robotRevised import Robot

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
        print('------------------------------------new move------------------------------------')
        print(count)
        print('pointless walk : ',robot.pointless_walks)
        print('constrain : ',robot.constrain)

        robot.random_move()
        # robot.camera_sensing()
        print('the robot is now facing :',robot.facing_direction)
        count+=1
        if robot.position in world.losing_positions:
            robot.lost = True
            print('You lost')

        if robot.position == world.winning_position:
            robot.won = True
            print('You won')
        world.display()
        robot.display_robot_map()

    print('GAME OVER')
    world.display()        
    robot.display_robot_map()
