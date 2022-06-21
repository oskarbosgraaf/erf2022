# test lidar input

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

print('runt')

def callback(dt):
    print(f'data at 0 {dt.ranges[0]}')
    print(f'data at 15? {dt.ranges[15]}')

move = Twist()
rospy.init_node('test laser scan')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/scan', LaserScan, callback)

rospy.spin()


