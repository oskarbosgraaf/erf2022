import rospy
from geometry_msgs.msg import Twist
import cv2
import shelly
import time


class FollowBlob():

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
<<<<<<< HEAD
    
    def stop(self):
        self.move(0, 0, 3)
        # time.sleep(5)
=======
>>>>>>> parent of a1c39a0 (aan)

    def lights(self):
        shelly.switchPlug("on")
        print("lights turned on")
        
    def lights_off(self):
        shelly.switchplug("off")
        print("lights turned off")
    
    def decideBehavior(self, behavior):
        
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

        elif behavior == 6:
            self.lights()
<<<<<<< HEAD

        elif behavior == 7:
            self.stop()

        elif behavior == 69:
            self.lights_off()

=======
>>>>>>> parent of a1c39a0 (aan)
        else:
            print(' no action')
            return None

    def move(self, lin, ang, dur):
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.publish(msg)
        rospy.sleep(dur)

