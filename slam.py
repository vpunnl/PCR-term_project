from world import World
from robot import Robot

if __name__=='__main__':
    world = World()
    world.display()

    robot = Robot(world)
    # robot.display_robot_map()
    robot.camera_sensing(20, 10)
    robot.display_robot_map()