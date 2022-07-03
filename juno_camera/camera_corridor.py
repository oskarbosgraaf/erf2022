
"""
Code for corridor information for the autonomous navigational robotics hackathon
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

last updated: 1st of July, 2022
"""

import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan


class Corridor:
    """Information class for keeping track of the other Juno's corridor state."""

    def __init__(self):
        self.other_in_corridor = False
        self.count_other = 0
        self.act = False
        rospy.Subscriber('in_corridor_MC', Bool, self.corridorCB)


    def corridorCB(self, msg):
        """Keep track of the other Juno's corridor state."""
        if msg.data:
            self.other_in_corridor = True
        elif msg.data == False:
            self.count_other += 1

        if self.count_other > 10:
            self.other_in_corridor = False
            self.count_other = 0

