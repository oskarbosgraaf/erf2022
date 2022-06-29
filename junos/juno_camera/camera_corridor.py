import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan


class Corridor:
    def __init__(self):
        # self.in_corridor = False
        self.other_in_corridor = False
        # self.corr_dist = 1.5
        # self.count = 0
        self.count_other = 0
        self.act = False


        rospy.Subscriber('in_corridor_MC', Bool, self.corridorCB)
        # rospy.Subscriber('/client_scan/scan', LaserScan, self.laserCB)

        # self.pub = rospy.Publisher('test_corridor', Bool, queue_size=10)


    def corridorCB(self, msg):
        if msg.data:
            self.other_in_corridor = True
        elif msg.data == False:
            self.count_other += 1

        if self.count_other > 10:
            self.other_in_corridor = False
            self.count_other = 0

    # def laserCB(self, data):
    #     if data.ranges[270] + data.ranges[90] < self.corr_dist and self.count <= 10:
    #         self.count += 1
    #     elif data.ranges[270] + data.ranges[90] >= self.corr_dist and self.count >= 0:
    #         self.count -= 1

    #     print(self.count)
    #     if self.count > 10:
    #         self.in_corridor = True
    #     if self.count < 0:
    #         self.in_corridor = False

    #     if self.in_corridor and self.other_in_corridor:
    #         self.act = True

    #     if self.act and self.other_in_corridor == False:
    #         self.act = False 

    #     self.pub.publish(self.in_corridor)

        

    


