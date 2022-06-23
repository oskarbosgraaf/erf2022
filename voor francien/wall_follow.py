#!/usr/bin/env python
# Wall Following
# Algorithmic Robotics Project 2017
# by Sinclair Gurny

import rospy, serial, sys, datetime
# from duckietown_msgs.msg import Twist2DStamped
from geometry_msg.msg import Twist
from std_msgs.msg import Float32

# print with timestamp
def print2( stuff ):
    fulltime = str(datetime.datetime.now())
    dateandtime = fulltime.split( '.', 1)[0]
    time = dateandtime.split(' ', 1)[1]
    print( str(time) + " " + str(stuff) )

class WallFollow:
    def __init__( self ):
        self.name = "Wall_Follow_Node"
        # make publisher
        self.pubber = rospy.Publisher("cmd_vel", Twist, queue_size=1)

        # subscribe to different sonar
        # rospy.Subscriber('/sonar_dist1',Float32, self.read_l)
        rospy.Subscriber('/sonar_dist2',Float32, self.read_f)
        rospy.Subscriber('/sonar_dist3',Float32, self.read_r)

        # self.left = None
        self.front = None
        self.right = None

        self.mode = False # True - following, False - picking behavior
        self.wall = -1 #-1 - no wall, 1 - left, 2 - right

        self.distF = 40
        self.min_dist = 20
        self.max_dist = 30

        rospy.on_shutdown(self.stop)
    
    # read the sonar distances
    def read_l(self, msg):
        self.left = msg.data

    def read_f(self, msg):
        self.front = msg.data
    
    def read_r(self, msg):
        self.right = msg.data


    def run( self ):
        print( " ====================== " )
        while not rospy.is_shutdown():
            data = [int(self.front), int(self.right)]
            print(f'current data = {data}')
            self.follow_wall(data)
            rospy.spin()

    def follow_wall(self, data):
        F_plus = data[0] > self.distF
        F_min = data[0] < self.distF

        R_plus = data[1] > self.max_dist
        R_min = data[1] < self.min_dist
        R = (data[1] < self.max_dist) and (data[1] > self.min_dist)

        if R_plus and F_plus:
            print('Adjust right')
            self.move(0.0, 2.5, 0.2) # adjust right

        elif R_plus and F_min:
            print('Adjust left')
            self.move(0.0, -2.5, 0.2) # adjust left

        elif R and F_plus:
            print('Move ahead')
            self.move( 0.2, 0, 0.2 ) # move ahead
        elif R and F_min:
            print('Adjust left')
            self.move(0.0, -2.5, 0.2) # adjust left

        elif R_min and F_plus:
            print('Adjust left')
            self.move(0.0, -2.5, 0.2) # adjust left

        elif R_min and F_min:
            print('Adjust left')
            self.move(0.0, -2.5, 0.2) # adjust left

        self.move(0,0,0)

    def move(self, lin_vel, ang_vel, dur):
        msg = Twist()
        msg.linear.x = lin_vel
        msg.angular.z = ang_vel
        # cmd1 = Twist2DStamped(v=lin_vel, omega=-ang_vel)
        self.pubber.publish(msg)
        rospy.sleep(dur)

    def stop(self):
        self.move(0,0,0.1)

if __name__ == '__main__':
    rospy.init_node('wall_follow_sonar', anonymous=False)
    wf = WallFollow()
    print2( " === Starting Program === " )
    wf.run()
