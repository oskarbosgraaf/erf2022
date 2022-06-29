#!/usr/bin/env python
from pyrsistent import s
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class test():
    def __init__(self, rate):
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.laserCb)
        self.rate = rate

    def run(self):
        rate2 = rospy.Rate(10)
        while not rospy.is_shutdown():
            msg = Twist()
            msg.linear.x = 0.1
            msg.angular.z = 0.0
            # self.pub.publish(msg)
            rate2.sleep()

    def laserCb(self, msg):
        print(msg.ranges)


if __name__ == '__main__':
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    tst = test(rate) # 10hz
    print("start program")
    tst.run()
