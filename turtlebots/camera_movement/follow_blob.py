import rospy
from geometry_msgs.msg import Twist
# import camera
import cv2


class FollowBlob():

    def __init__(self):
        rospy.init_node('FollowBlob', anonymous=False)
        self.pub = rospy.Publisher("/client/cmd_vel", Twist, queue_size=10)
        msg = Twist()
        msg.linear.x = 0.2
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
        self.move(0, -0.5, 0.1)
    
    def decideBehavior(self, behavior):
        # print(f'video blob direction {cam.video_blob_direction()}' )
        # print(f'video blob direction {type(cam.video_blob_direction())}' )
        
        if behavior == 0:
            print(('left'), 0.1)
    
    def decideBehavior(self, behavior):
        # print(f'video blob direction {cam.video_blob_direction()}' )
        # print(f'video blob direction {type(cam.video_blob_direction())}' )
        
        if behavior == 0:
            print('left')
            self.left()
        
        elif behavior == 1:
            print('adjust left')
            self.adjust_left()
        
        elif behavior == 2:
            print('move forward')
            self.move_forward()

        elif behavior == 3:
            print('adjust right')
            self.adjust_right()

        elif behavior == 4:
            print('right')
            self.right()
        
        elif behavior == 5:
            self.turn()

        # if cam.video_blob_direction() == 0:
        #     print('left')
        #     self.left()

        # elif cam.video_blob_direction() == 1:
        #     print('adjust left')
        #     self.adjust_left()

        # elif cam.video_blob_direction() == 2:
        #     print('move forward')
        #     self.move_forward()

        # elif cam.video_blob_direction() == 3:
        #     print('adjust right')
        #     self.adjust_right()

        # elif cam.video_blob_direction() == 4:
        #     print('right')
        #     self.right()

        # elif cam.video_blob_direction() == 5:
        #     print('turn')
        #     self.turn()

        else:
            print(' no action')
            return None

    def move(self, lin, ang, dur):
        print('in move')
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.pub.publish(msg)
        # print(f'msg = {msg}')
        rospy.sleep(dur)