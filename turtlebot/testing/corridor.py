import rospy
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan


class Corridor:
    def init(self):
        self.in_corridor = False
        self.other_in_corridor = False
        self.corr_dist = 1

        rospy.Subscriber('in_corridor_mc', Bool, self.corridorCB)

        rospy.Subscriber('/scan', LaserScan, self.laserCB)


    def corridorCB(self, msg):
        if msg.data == True:
            self.other_in_corridor = True
        else:
            self.other_in_corridor = False

    def laserCB(self, data):
        # update naar 3 x achter elkaar
        if data.ranges[270] + data.ranges[90] < self.corr_dist:
            self.in_corridor = True
        else:
            self.in_corridor = False