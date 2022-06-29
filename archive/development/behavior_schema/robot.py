from mirte_robot_lokaal import robot

# # Import rospy
import rospy
from geometry_msgs.msg import Twist

# import behaviors
from obstacle_avoidance import ObstacleAvoidance

class JunoRobot:
    def __init__(self, position, velocity):
        self.mirte_robot = robot.createRobot()
        self.req_distance_to_wall = None
        self.obstacle_avoider = ObstacleAvoidance()
        
    