#!/usr/bin/env python
# Wall Following
# Algorithmic Robotics Project 2017
# by Sinclair Gurny

import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from corridor import Corridor
from std_msgs.msg import Bool
import serial
import time



class WallFollow:
    def __init__( self ):
        print('in init')
        self.name = "Wall_Follow_Node"

        # self.pubber = rospy.Publisher("/client/cmd_vel", Twist, queue_size=10)
        # self.sub = rospy.Subscriber('client_scan/scan', LaserScan, self.LaserToSonar)

        self.ser = serial.Serial('/dev/ttyACM0', 9800, timeout=1)

        # self.left = None
        self.front = None
        self.right = None

        self.mode = False # True - following, False - picking behavior
        self.wall = -1 #-1 - no wall, 1 - left, 2 - right

        self.distF = 0.55
        self.min_dist = 0.3
        self.max_dist = 0.5
        self.last_right = 0
        self.right = 0

        self.front = 2
        self.lastfront = 2

        self.follow_right = True # follow right wall

        self.backward_done = False
        self.countdown = 60

        self.data = [0,0,0]

    def read(self):
        try:
            line = self.ser.readline()   # read a byte
            if line:
                self.data = [int(word) for word in line.split() if word.isdigit()]
                if len(self.data) != 3:
                    return self.read()
                print(self.data)
        except:
            print( "error in message: converting" )
            return self.read() # try again
        # if corridor.act and self.backward_done == False:
        #     self.move_backward()
        # elif corridor.act and self.backward_done:
        #     self.stop()
        if corridor.other_in_corridor:
            self.stop
        elif self.follow_right:
            self.follow_wall_r()
        else:
            self.follow_wall_l()
        
 
    def follow_wall_r(self):
        self.last_right = self.right
        self.lastfront = self.front
        self.front = self.data[0]
        self.right =self.data[1]
        self.left = self.data[2]

        F_plus = self.data[0] > self.distF
        F_min = self.data[0] < self.distF

        R_plus = self.data[1] > self.max_dist and self.data[1] < 0.7
        R_plusplus = self.data[1] > self.max_dist and self.data[1] > 0.7
        R_min = self.data[1] < self.min_dist
        R = (self.data[1] < self.max_dist) and (self.data[1] > self.min_dist)

        # if self.lastfront == 0 and self.front == 0:
        #     print('move backward')
        #     self.move(-0.2, 0.1, 0.4)

        # if (self.data[1] + self.data[2]) < 1:
        #     print('in corridor')
        
        if R_plus and F_plus:
            print('Muur net iets te ver')
            # self.move(0.13, -1, 0.1)
            self.move(0.2, -0.5, 0.13) # adjust left

        if R_plusplus and F_plus:
            print('Geen voorkant, geen muur')
            print('Adjust right')
            self.move(0.13, -1.5, 0.25) # adjust right
            #self.move(0.1, 0 , 0.1)

        elif (R_plus and F_min) or (R_plusplus and F_min):
            print('Voor een voorkant')
            print('Turn left')
            self.move(0.1, 2, 0.1) # adjust left

        elif R and F_plus:
            print('perfect')
            print('Move ahead')
            # print(f'last right: {self.last_right}')
            # print(f'right: {self.right}')
            self.move(0.15, 0, 0.2) # move ahead

            # make sure to drive straight
            if (self.right - self.last_right) > 0.001:
                print('not straight: adjust right')
                self.move(0.15, -0.18, 0.1)
            if (self.last_right - self.right) > 0.001:
                print('not straight: adjust left')
                self.move(0.15, 0.18, 0.1)

        elif R and F_min:
            print('In hoek')
            print('Turn left')
            self.move(0.2, 1.8, 0.2) # adjust left

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

        # if (self.data[1] + self.data[2]) < 1:
        #     print('in corridor')

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
        print(dur)
        rospy.sleep(dur)

    def stop(self):
        self.move(0,0,1)

    def move_backward(self):
        while self.countdown > 0:
            self.move(-0.13, 0, 0.1)
            self.countdown -= 1
        self.backward_done = True

if __name__ == '__main__':
    # rospy.init_node('wall_follow_sonar', anonymous=False)
    print( " === Starting Program === " )
    corridor = Corridor()
    wf = WallFollow()
    wf.read()
    # rospy.spin()
