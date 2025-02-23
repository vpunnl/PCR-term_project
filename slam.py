from world import World
from robot import Robot

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
    robot.display_robot_map()