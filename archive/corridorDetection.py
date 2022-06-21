# ROS imports
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class corridorDetection:
    def __init__(self):
        self.detector = "Laser"
        self.pub = None
        self.corridor_distance = 1

    def clbk_laser(self, msg):

        # get distance to the right and left
        left = min(msg.ranges[213:355])
        right = min(msg.ranges[781:923])

        self.checkCorridor(left, right)
    
    def checkCorridor(self, left, right):

        if (left + right) < self.corridor_distance:
            return True
    
    def detectCorridor(self):
        rospy.init_node('reading_laser')

        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, self.clbk_laser)

        rospy.spin()
