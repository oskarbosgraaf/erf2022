#!/usr/bin/env python
# Wall Following
# Algorithmic Robotics Project 2017
# by Sinclair Gurny

import rospy, serial, sys, datetime
from duckietown_msgs.msg import Twist2DStamped


import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
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
        self.pubber = rospy.Publisher("/pi/dagu_car/vel_cmd", Twist2DStamped, queue_size=1)
        # make serial port to arduino
        try:
            self.arduino = serial.Serial("/dev/ttyACM0", 9600)
            break
        except:
            print( "Could not open Serial Port ACM0" )
            num += 1
            if num > 9:
                sys.exit(0)

        # variables
        self.mode = False # True - following, False - picking behavior
        self.wall = -1 #-1 - no wall, 1 - left, 2 - right
        rospy.on_shutdown( self.stop )

    def read( self ):
        try:
            line = self.arduino.readline();
            data = line.split(" ")
            # error in message
            if len( data ) != 7:
                print( "incomplete message error" )
                return self.read()
            # convert to ints
            ans = [0, 0, 0, 0, 0]
            for i in range( 0, 5 ):
                ans[i] = int( data[i+1] )
                #print( ans )
            return ans
        except:
            print( "error in message: converting" )
            return self.read() # try again

    def run( self ):
        print( " ====================== " )
        while not rospy.is_shutdown():
            data = self.read()
            print2( data )
            if self.mode:
                # Following wall
                print2( " === Following Wall === " )
                self.follow_wall( data )
            else:
                # Find wall
                print2( " === Picking === " )
                self.pick_wall( data)

    def pick_wall( self, data ):
        F = (data[0] != -2 and data[0] < 40)
        L = (data[1] != -2 and data[1] < 40) and (data[3] != -2 and data[3] < 60)
        R = (data[2] != -2 and data[2] < 40) and (data[4] != -2 and data[4] < 60)

        if F and L and R: # dead end
            print2( "turning back" )
            self.move( 0, 3, 0.4 )
        elif (not F) and (not L) and (not R): # can't see anything
            print2( "driving straight" )
            self.move( 0.2, 0, 0.2 )
        elif F and L and (not R): # corner
            print2( "turning right" )
            self.move( 0.0, 2.5, 0.2 ) #turn_right()
        elif F and R and (not L): # corner
            print2( "turning left" )
            self.move( 0.0, -2.5, 0.2 ) #turn_left()
        elif L and R and (not F): # hallway
            print2( "pick a wall" )
            if data[1] < data[2]:
                self.wall = 1
                self.mode = True
                print2( "right wall" )
            else:
                self.wall = 2
                self.mode = True
                print2( "left wall" )
        elif F and (not L) and (not R):
            print2( "Wall block" )
            self.move( 0, -2.5, 0.2 )
        elif R: # wall
            print2( "pick right" )
            self.wall = 2
            self.mode = True
        elif L: # wall
            print2( "pick left" )
            self.wall = 1
            self.mode = True
        self.move(0,0,0)

    def follow_wall( self, data ):
        #check if wall is still visible
        if data[0] < 30:
            print2( "Obstacle Found" )
            self.mode = False
            self.wall = -1
            return
        if data[self.wall] > 60:
            print2( "Wall gone" )
            self.mode = False
            self.wall = -1
            return
        too_far = (data[self.wall] > 30) and (data[self.wall+2] > 60)
        too_close = (data[self.wall] < 10) or (data[self.wall+2] < 30)
        val = -1 if self.wall == 1 else 1
        if too_close:
            print2( "too close to wall" )
            self.move( 0.2, -1*val * 2.5, 0.2 )
        elif too_far:
            print2( "too far from wall" )
            self.move( 0.2, val * 2.5, 0.2 )
        else:
            print2( "following wall..." )
            self.move( 0.2, 0, 0.1 )
        self.move(0,0,0)

    def move( self, lin_vel, ang_vel, dur ):
        cmd1 = Twist2DStamped(v=lin_vel, omega=-ang_vel)
        self.pubber.publish( cmd1 )
        rospy.sleep( dur )

    def stop( self ):
        self.move(0,0,0.1)

if __name__ == '__main__':
    rospy.init_node('wall_follow', anonymous=False)
    wf = WallFollow()
    print2( " === Starting Program === " )
    wf.run()
