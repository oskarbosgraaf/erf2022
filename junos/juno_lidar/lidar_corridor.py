import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool


class Corridor:
    def __init__(self):
        print('init van corridor')
        self.cor_dist = 2.0
        rospy.Subscriber('/scan', LaserScan, self.Lidar_cb)
        self.pub = rospy.Publisher('in_corridor_MC', Bool, queue_size=5)
        self.in_corridor = False
        self.count = 0

        # print('init cor')

    def Lidar_cb(self, msg):
        # print('lidar cb')
        # front_left = min(msg.ranges[70:110]) # turtle
        # front_right  = min(msg.ranges[250:290]) # turtle
        front_left  = min(msg.ranges[227:347])
        front_right = min(msg.ranges[800:920])

        if (front_left + front_right) < self.cor_dist and self.count <= 10:
            # print('corridor detected')
            self.count += 1
        elif (front_left + front_right) >= self.cor_dist and self.count >= 0: 
            self.count -= 1
        if self.count > 20:
            self.in_corridor = True
            print('in corridor')
        elif self.count < 0:
            self.in_corridor = False

        # print(self.in_corridor)
        self.pub.publish(self.in_corridor)