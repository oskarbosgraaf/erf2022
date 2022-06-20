# ROS imports
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class corridorMovement:
    def __init__(self):
        self.detector = "Laser"
        self.pub = 0
    
    def clbk_laser(self, msg):
        regions_lidar = {
        'right':  min(msg.ranges[213:355]),
        'fright': min(msg.ranges[355:497]),
        'front':  min(msg.ranges[497:639]),
        'fleft':  min(msg.ranges[639:781]),
        'left':   min(msg.ranges[781:923]),
        }
        # regions = {
        # 'right':  min(min(msg.ranges[0:143]), 10),
        # 'fright': min(min(msg.ranges[144:287]), 10),
        # 'front':  min(min(msg.ranges[288:431]), 10),
        # 'fleft':  min(min(msg.ranges[432:575]), 10),
        # 'left':   min(min(msg.ranges[576:713]), 10),
        # }
        self.takeAction(regions_lidar)
        # self.takeAction(regions)