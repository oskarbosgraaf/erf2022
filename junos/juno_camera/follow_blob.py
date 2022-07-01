
"""
Code for behaiour-based directional twist publishing for the autonomous
navigational robotics hackathon from European Robotics Forum (ERF) 2022,
implemented specifically for the Lely Juno robot.
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
from geometry_msgs.msg import Twist
import cv2
import shelly
import time


class FollowBlob():
"""Behavior publishing for the following of blob direction"""

    def __init__(self):
        rospy.init_node('FollowBlob', anonymous=False)
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        msg = Twist()
        msg.linear = 0.2
        self.pub.publish(msg)


    def adjust_left(self):
        self.move(0.1, 0.15, 0.1)


    def left(self):
        self.move(0.1, 0.25, 0.1)


    def adjust_right(self):
        self.move(0.1, -0.15, 0.1)


    def right(self):
        self.move(0.1, -0.25, 0.1)


    def move_forward(self):
        self.move(0.1, 0.0, 0.1)


    def turn(self):
        self.move(0, 0.2, 0.1)


    def wait(self):
        self.move(0, 0, 0.2)


    def lights_on(self):
        shelly.switchPlug("on")


    def lights_off(self):
        shelly.switchPlug("off")


    def decideBehavior(self, behavior):
        """Forward to behavior publish, based on chosen behavior"""
        if behavior == 0:
            self.left()

        elif behavior == 1:
            self.adjust_left()

        elif behavior == 2:
            self.move_forward()

        elif behavior == 3:
            self.adjust_right()

        elif behavior == 4:
            self.right()

        elif behavior == 5:
            self.turn()

        elif behavior == 10:
            self.lights_on()

        elif behavior == 11:
            self.lights_off()
        else:
            print('No valid action chosen.')
            return None


    def move(self, lin, ang, dur):
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.publish(msg)
        rospy.sleep(dur)

