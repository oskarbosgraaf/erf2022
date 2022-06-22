#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from standard.msg import Bool

class corridor:
    def __init__(self):
        self.detector = 'Laser'

        # self.hz = 20                     # Cycle Frequency
        # self.inf = 5                     # Limit to Laser sensor range in meters, all distances above this value are 
                                         # considered out of sensor range
        self.breadth = 1                 # Breadth of corridor (this needs to be slighlty bigger than the actual breadth)
        
    def callback_detection(self, msg):
        left  = min(msg.ranges[720:863])
        right = min(msg.ranges[144:287])

        if left + right <= self.breadth:
            pub = rospy.Publisher('corridor', Bool, queue_size=10)
            rospy.init_node('client_master', anonymous=True)
            pub.publish(True)

            return True 

        return False

    def detect_corridor(self):
        rospy.init_node('reading_laser')
        sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, self.callback_detection)

    def corridor_problem(self):
        rospy.init_node('client_master')
        sub = rospy.Subscriber('corridor', Bool, self.callback_problem)
    
    def callback_problem(self, msg):
        if msg.data == True:
            return True
        
        return False

    def handle_corridor(self):
        rospy.init_node('reading_laser')
        sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, self.callback_handle)

    def callback_handle(self, msg):
        left  = min(msg.ranges[720:863])
        right = min(msg.ranges[144:287])

        pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        while left < self.breadth and right < self.breadth:
            msg = Twist()
            msg.linear.x = 0.2
            msg.linear.z = 0
            pub_.publish(msg)

        msg = Twist()
        msg.linear.x = 0
        msg.linear.z = 0
        pub_.publish(msg)

        self.wait_for_sign()

    def wait_for_sign(self):
        rospy.init_node('client_master')
        sub = rospy.Subscriber('corridor', Bool, self.callback_wait)

    def callback_wait(self, msg):
        while msg.data == True:
            pass

        return None


        


        



        


