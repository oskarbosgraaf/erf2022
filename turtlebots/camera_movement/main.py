import rospy
from geometry_msgs.msg import Twist
import camera
import cv2


class FollowBlob():

    def __init__(self):
        rospy.init_node('FollowBlob', anonymous=False)
        self.pub = rospy.Publisher("/client/cmd_vel", Twist, queue_size=10)
        msg = Twist()
        msg.linear = 0.2
        self.pub.publish(msg)

    def adjust_left(self):
        self.move(0.1, 1.0, 0.2)
    
    def left(self):
        self.move(0.1, 2.0, 0.2)

    def adjust_right(self):
        self.move(0.1, -1.0, 0.2)

    def right(self):
        self.move(0.1, -2.0, 0.2)

    def move_forward(self):
        self.move(0.2, 0.0, 0.2)
    
    def turn(self):
        self.move(0, -2.0, 0.2)
    
    def decideBehavior(self, cam):
        print(f'video blob direction {cam.video_blob_direction()}' )
        print(f'video blob direction {type(cam.video_blob_direction())}' )
        
        # if cam.behavior == 0:
        #     print('left')
        #     self.left()
        
        # elif cam.behavior == 1:
        #     print('adjust left')
        #     self.adjust_left()
        
        # elif cam.behavior == 2:
        #     print('move forward')
        #     self.move_forward()

        # elif cam.behavior == 3:
        #     print('adjust right')
        #     self.adjust_right()

        # elif cam.behavior == 4:
        #     print('right')
        #     self.right()
        
        # elif cam.behavior == 5:
        #     self.turn()

        if cam.video_blob_direction() == 0:
            print('left')
            self.left()

        elif cam.video_blob_direction() == 1:
            print('adjust left')
            self.adjust_left()

        elif cam.video_blob_direction() == 2:
            print('move forward')
            self.move_forward()

        elif cam.video_blob_direction() == 3:
            print('adjust right')
            self.adjust_right()

        elif cam.video_blob_direction() == 4:
            print('right')
            self.right()

        elif cam.video_blob_direction() == 5:
            print('turn')
            self.turn()

        else:
            print(' no action')
            return None

    def move(self, lin, ang, dur):
        print('in move')
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.publish(msg)
        print(f'msg = {msg}')
        rospy.sleep(dur)

    
if __name__ == '__main__':
    rospy.init_node('FollowBlob', anonymous=False)
    print( " === Starting Program === " )
    fb = FollowBlob()
    for _ in range(10):
        cam = camera.Camera()
        cam.video_blob_direction()
        fb.decideBehavior(cam)
        # cam = camera.Camera(cv2.VideoCapture(1,cv2.CAP_DSHOW))
        # cv2.VideoCapture(1,cv2.CAP_DSHOW)
        # fb.decideBehavior(cam)