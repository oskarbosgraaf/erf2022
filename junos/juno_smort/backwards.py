import rospy
from geometry_msgs.msg import Twist
import cv2


class Backwards():

    def __init__(self):
        rospy.init_node('FollowBlob', anonymous=False)
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        msg = Twist()
        msg.linear = 0.2
        self.pub.publish(msg)

    def backwards(self):
        self.move(-0.1, 0.0, 2)

    def move(self, lin, ang, dur):
        print('in move')
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.publish(msg)
        # print(f'msg = {msg}')
        rospy.sleep(dur)



if __name__ == '__main__':
    print( " === Starting Program === " )
    
    b = Backwards()
    b.backwards()