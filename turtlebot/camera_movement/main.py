import rospy
from geometry_msgs.msg import Twist
import camera
import cv2


class FollowBlob():

    def __init__(self):
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

    def adjust_left(self):
        self.move(0.2, 2, 0.1)

    def adjust_right(self):
        self.move(0.2, -2, 0.1)

    def move_forward(self):
        self.move(0.2, 0, 0.1)
    
    def decideBehavior(self, cam):
        print(f'video blob direction {cam.video_blob_direction()}' )
        # cam.show_video_blob()
        if cam.video_blob_direction() == 'adjustright':
            self.adjust_right()
        elif cam.video_blob_direction() == 'adjustleft':
            self.adjust_left()
        elif cam.video_blob_direction() == 'drivestraight':
            self.move_forward()
        else:
            return None

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
    for i in range(100):
        cam = camera.Camera(cv2.VideoCapture(1,cv2.CAP_DSHOW))
        cv2.VideoCapture(1,cv2.CAP_DSHOW)
        fb.decideBehavior(cam)