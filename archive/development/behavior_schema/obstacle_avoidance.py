import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance:
    def __init__(self):
        self.detector = "Laser"
        self.pub = None
    
    def clbk_laser(self, msg):
        # regions_lidar = {
        # 'right':  min(msg.ranges[213:355]),
        # 'fright': min(msg.ranges[355:497]),
        # 'front':  min(msg.ranges[497:639]),
        # 'fleft':  min(msg.ranges[639:781]),
        # 'left':   min(msg.ranges[781:923]),
        # }
        regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:713]), 10),
        }
        # self.takeAction(regions_lidar)
        self.takeAction(regions)

    def takeAction(self, regions):
        msg = Twist()
        linear_x = 0
        angular_z = 0

        state_description = ''

        if regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] > 1:
            state_description = 'case 1 - nothing'
            linear_x = 0.6
            angular_z = 0
        elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
            state_description = 'case 2 - front'
            linear_x = 0
            angular_z = -0.3
        elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
            state_description = 'case 3 - fright'
            linear_x = 0
            angular_z = -0.3
        elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
            state_description = 'case 4 - fleft'
            linear_x = 0
            angular_z = 0.3
        elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
            state_description = 'case 5 - front and fright'
            linear_x = 0
            angular_z = -0.3
        elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
            state_description = 'case 6 - front and fleft'
            linear_x = 0
            angular_z = 0.3
        elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
            state_description = 'case 7 - front and fleft and fright'
            linear_x = 0
            angular_z = -0.3
        elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
            state_description = 'case 8 - fleft and fright'
            linear_x = 0
            angular_z = -0.3
        else:
            state_description = 'unknown case'
            rospy.loginfo(regions)

        rospy.loginfo(state_description)
        
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.pub.publish(msg)

        return None

    
    def avoidObstacle(self):
        global pub

        rospy.init_node('reading_laser')

        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, self.clbk_laser)

        rospy.spin()

        return None
    