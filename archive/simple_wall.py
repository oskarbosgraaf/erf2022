import rclpy
from rclpy.node import Node

from rclpy.qos import qos_profile_sensor_data, QoSProfile
from std_msgs.msg import String
from geometry_msgs.msg import Twist

from sensor_msgs.msg import LaserScan
import rclpy

# Util imports
import random
from geometry_msgs.msg import Twist
import math
import time

inf = 5 

def clbk_laser(msg):


    # Determination of minimum distances in each region
    regions = {
        'bleft' : min(min(msg.ranges[90:126]), inf),
        'left': min(min(msg.ranges[54:90]),inf),
        'fleft':min(min(msg.ranges[18:54]),inf),
        'front':min(min(min(msg.ranges[0:18]), min(msg.ranges[342:359])),inf),
        'fright':min(min(msg.ranges[306:342]), inf),
        'right': min(min(msg.ranges[270:306]), inf),
        'bright': min(min(msg.ranges[234:270]), inf)
        }

        
    take_action(regions)

def take_action(regions):
    
