from world import World
from robot import Robot

if __name__=='__main__':
    world = World()
    world.display()

    robot = Robot(world)
    # robot.display_robot_map()

    robot.facing_direction = 'up'
    robot.camera_sensing(30, 5)
    # robot.display_robot_map()

    robot.facing_direction = 'down'
    robot.camera_sensing(30, 5)
    # robot.display_robot_map()

    robot.facing_direction = 'right'
    robot.camera_sensing(30, 5)
    # robot.display_robot_map()

    robot.facing_direction = 'left'
    robot.camera_sensing(30, 5)
    robot.display_robot_map()