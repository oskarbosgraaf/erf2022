import rospy
from geometry_msgs.msg import Twist

class FollowBlob():

    def __init__(self):
        self.camera = ...
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

    def adjust_left(self):
        self.move(0.2, 2, 0.1)

    def adjust_right(self):
        self.move(0.2, -2, 0.1)

    def move_forward(self):
        self.move(0.2, 0, 0.1)

    def move(self, lin, ang, dur):
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.Publish(msg)
        rospy.sleep(dur)

    
if __name__ == '__main__':
    rospy.init_node('FollowBlob', anonymous=False)
    print( " === Starting Program === " )
    fb = FollowBlob()