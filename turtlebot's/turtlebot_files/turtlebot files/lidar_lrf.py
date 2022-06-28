#!/usr/bin/env python
# Wall Following
# Algorithmic Robotics Project 2017
# by Sinclair Gurny

import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32

# # print with timestamp
# def print( stuff ):
#     fulltime = str(datetime.datetime.now())
#     dateandtime = fulltime.split( '.', 1)[0]
#     time = dateandtime.split(' ', 1)[1]
#     print( str(time) + " " + str(stuff) )

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

        # self.distF = 0.6
        # self.min_dist = 0.3
        # self.max_dist = 0.5

        self.required_distance = 0.4

        # rospy.on_shutdown(self.stop)
    
    def LaserToSonar(self, msg):
        print('in laser scanner')
        #print(msg.ranges)
        self.data = [msg.ranges[0], msg.ranges[270], msg.ranges[90]]
        print(f'data: {self.data}')
        self.follow_wall()

        print( " ====================== " )

        if self.mode:
            # Following wall
            print( " === Following Wall === " )
            self.follow_wall()
        else:
            # Find wall
            print( " === Picking === " )
            self.pick_wall()

 
    # read the sonar distances
    """
    def read_l(self, msg):
        self.left = msg.data

    def read_f(self, msg):
        self.front = msg.data
    
    def read_r(self, msg):
        self.right = msg.data
    """

    def follow_wall(self):
        #check if wall is still visible
        if self.data[0] < 0.2:
            print( "Obstacle Found" )
            self.mode = False
            self.wall = -1
            return
        if self.data[self.wall] > 0.6:
            print( "Wall gone" )
            self.mode = False
            self.wall = -1
            return
        too_far = self.data[self.wall] > 0.5
        too_close = self.data[self.wall] < 0.3
        val = -1 if self.wall == 1 else 1

        if too_close:
            print( "too close to wall" )
            self.move( 0.2, -1*val * 2.5, 0.2 )
        elif too_far:
            print( "too far from wall" )
            self.move( 0.2, val * 2.5, 0.2 )
        else:
            print( "following wall..." )
            self.move( 0.2, 0, 0.1 )
        self.move(0,0,0)


    def pick_wall(self):
        F = (self.data[0] != 0 and self.data[0] < self.required_distance)
        R = (self.data[1] != 0 and self.data[1] < self.required_distance)
        L = (self.data[2] != 0 and self.data[2] < self.required_distance)
       
        if F and L and R: # dead end
            print( "turning back" )
            self.move( 0, 3, 0.4 )
        elif (not F) and (not L) and (not R): # can't see anything
            print( "driving straight" )
            self.move( 0.2, 0, 0.2 )
        elif F and L and (not R): # corner
            print( "turning right" )
            self.move( 0.0, 2.5, 0.2 ) #turn_right()
        elif F and R and (not L): # corner
            print( "turning left" )
            self.move( 0.0, -2.5, 0.2 ) #turn_left()
        elif L and R and (not F): # hallway
            print( "pick a wall" )
            if self.data[1] < self.data[2]:
                self.wall = 1
                self.mode = True
                print( "right wall" )
            else:
                self.wall = 2
                self.mode = True
                print( "left wall" )
        elif F and (not L) and (not R):
            print( "Wall block" )
            self.move( 0, -2.5, 0.2 )
        elif R: # wall
            print( "pick right" )
            self.wall = 2
            self.mode = True
        elif L: # wall
            print( "pick left" )
            self.wall = 1
            self.mode = True

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
