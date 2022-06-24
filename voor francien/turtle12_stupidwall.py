#!/usr/bin/env python
# Wall Following
# Algorithmic Robotics Project 2017
# by Sinclair Gurny

import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32

# # print with timestamp
# def print2( stuff ):
#     fulltime = str(datetime.datetime.now())
#     dateandtime = fulltime.split( '.', 1)[0]
#     time = dateandtime.split(' ', 1)[1]
    # print( str(time) + " " + str(stuff) )

class WallFollow:
    def __init__( self ):
        print('in init')
        self.name = "Wall_Follow_Node"

        # make publisher & subscriber
        rospy.Subscriber('/scan', LaserScan, self.LaserToSonar)
        self.pubber = rospy.Publisher("cmd_vel", Twist, queue_size=10)

        # subscription for sonar
        """
        rospy.Subscriber('/sonar_dist2',Float32, self.read_f)
        rospy.Subscriber('/sonar_dist3',Float32, self.read_r)
        """

        # self.left = None
        self.front = None
        self.right = None

        self.mode = False # True - following, False - picking behavior
        self.wall = -1 #-1 - no wall, 1 - left, 2 - right

        self.distF = 0.5
        self.min_dist = 0.2
        self.max_dist = 0.5
        self.last_right = 0
        self.right = 0

        self.follow_right = True # follow right wall

        # rospy.on_shutdown(self.stop)
    
    def LaserToSonar(self, msg):
        print('in laser scanner')
        self.last_right = self.right
        self.data = [msg.ranges[0], msg.ranges[270], msg.ranges[90]]
        self.right = msg.ranges[270]
        self.left = msg.ranges[90]
        print(f'data: {self.data}')
        if self.follow_right:
            self.follow_wall_r()
        else:
            self.follow_wall_l()

    # read the sonar distances
    """
    def read_l(self, msg):
        self.left = msg.data

    def read_f(self, msg):
        self.front = msg.data
    
    def read_r(self, msg):
        self.right = msg.data
    """

    def follow_wall_r(self):
        F_plus = self.data[0] > self.distF
        F_min = self.data[0] < self.distF

        R_plus = self.data[1] > self.max_dist
        R_min = self.data[1] < self.min_dist
        R = (self.data[1] < self.max_dist) and (self.data[1] > self.min_dist)

        if (self.data[1] + self.data[2]) < 1:
            print('in corridor')

        if R_plus and F_plus:
            print('Geen voorkant, geen muur')
            print('Adjust right')
            self.move(0.1, -2, 0.25) # adjust right
            self.move(0.1, 0 , 0.1)

        elif R_plus and F_min:
            print('Voor een voorkant')
            print('Turn left')
            self.move(0.1, 2, 0.1) # adjust left

        elif R and F_plus:
            print('perfect')
            print('Move ahead')
            self.move(0.15, 0, 0.2) # move ahead

            # make sure to drive straight
            if self.right - self.last_right > 0:
                self.move(0.15, 0.1, 0.1)
            if self.right - self.last_right < 0:
                self.move(0.15, -0.1, 0.1)

        elif R and F_min:
            print('In hoek')
            print('Turn left')
            self.move(0.1, 2, 0.1) # adjust left

        elif R_min and F_plus:
            print('te dicht bij muur')
            print('Adjust left')
            self.move(0.15, 0.5, 0.1) # adjust left

        elif R_min and F_min:
            print('in een hoek + te dicht bij muur')
            print('Turn left')
            self.move(0.1, 2, 0.1) # adjust left

        self.move(0,0,0)
    
    def follow_wall_l(self):
        F_plus = self.data[0] > self.distF
        F_min = self.data[0] < self.distF

        L_plus = self.data[2] > self.max_dist
        L_min = self.data[2] < self.min_dist
        L = (self.data[2] < self.max_dist) and (self.data[2] > self.min_dist)

        if (self.data[1] + self.data[2]) < 1:
            print('in corridor')

        if L_plus and F_plus:
            print('Geen voorkant, geen muur')
            print('Adjust left')
            self.move(0.1, 2, 0.25) # adjust left
            self.move(0.1, 0 , 0.1)

        elif L_plus and F_min:
            print('Voor een voorkant')
            print('Turn right')
            self.move(0.3, -1.2, 0.1) # adjust right

        elif L and F_plus:
            print('perfect')
            print('Move ahead')
            self.move(0.15, 0, 0.2) # move ahead

            # make sure to drive straight
            if self.right - self.last_right > 0:
                self.move(0.15, -0.1, 0.1)
            if self.right - self.last_right < 0:
                self.move(0.15, 0.1, 0.1)

        elif L and F_min:
            print('In hoek')
            print('Turn right')
            self.move(0.1, -1, 0.1) # adjust right

        elif L_min and F_plus:
            print('te dicht bij muur')
            print('Adjust right')
            self.move(0.15, -0.5, 0.1) # adjust right

        elif L_min and F_min:
            print('in een hoek + te dicht bij muur')
            print('Turn right')
            self.move(0.15, -0.5, 0.1) # adjust right

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
    print( " === Starting Program === " )
    wf = WallFollow()
    rospy.spin()

    # wf.run()
