"""
Code for the corridor (narrow passage) detection and communication for the autonomous navigational robotics hackathon
from European Robotics Forum (ERF) 2022, implemented specifically for the Lely
Juno robot.
Team Unuversity of Amsterdam
Github: https://github.com/oskarbosgraaf/erf2022

Written and implemented by:
    Sjoerd Gunneweg
    Thijmen Nijdam
    Jurgen de Heus
    Francien Barkhof
    Oskar Bosgraaf
    Juell Sprott
    Sander van den Bent
    Derck Prinzhoorn

last updated: 3st of July, 2022
"""

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool


class Corridor:
    """
    Class for corridor detection and communication to the other Juno.
    """

    def __init__(self):
        self.cor_dist = 2.0 # breadth of the corridor

        # retreiving the data from the lidar scanner
        rospy.Subscriber('/scan', LaserScan, self.Lidar_cb)
        # creating publisher to communicate to the other Juno whether this Juno is in the corridor
        self.pub = rospy.Publisher('in_corridor_MC', Bool, queue_size=5)
        
        # boolean value that gets send to the other Juno
        self.in_corridor = False

        # variable that determines how many times a detection of a corridor must lead to a message being send
        self.count = 0


    def Lidar_cb(self, msg):
        """ 
        Function that determines, using the lidar data, whether the Juno is in the corridor
        and handles to communication to the other Juno.
        """

        # distance to the wall on the right and left side
        left  = min(msg.ranges[227:347])
        right = min(msg.ranges[800:920])

        # if left + right is smaller than the cor_dist (which is slightly bigger than the actual corridor breadth),
        # count is increased by 1 until it reaches 10
        if (left + right) < self.cor_dist and self.count <= 10:
            self.count += 1
        # if left + right is bigger than the cor_dist (which is slightly bigger than the actual corridor breadth),
        # count is decreased by 1 until it reaches 0
        elif (left + right) >= self.cor_dist and self.count >= 0: 
            self.count -= 1

        # if the Juno detects 10 times in a row it is in the corridor, the boolean value that is being send changes to true
        # this is done to improve consistency 
        if self.count > 10:
            self.in_corridor = True
        # if the Juno thereafter detects 10 times in a row it is not in the corridor, the boolean value that is being send changes to false
        elif self.count < 0:
            self.in_corridor = False

        # finally the boolean value is being send to the topic
        self.pub.publish(self.in_corridor)