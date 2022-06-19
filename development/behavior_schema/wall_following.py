#! /usr/bin/env python

# https://github.com/ssscassio/ros-wall-follower-2-wheeled-robot/blob/master/catkin_ws/src/two-wheeled-robot-motion-planning/scripts/follow_wall.py

# ROS imports
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
#from tf import transformations
#from datetime import datetime

# Util imports
import random
import math
import time

class wallFollower:
    def __init__(self):
        self.detector = 'Laser'

        self.hz = 20                     # Cycle Frequency
        self.loop_index = 0              # Number of sampling cycles
        self.loop_index_outer_corner = 0 # Loop index when the outer corner is detected
        self.loop_index_inner_corner = 0 # Loop index when the inner corner is detected
        self.inf = 5                     # Limit to Laser sensor range in meters, all distances above this value are 
                                    #      considered out of sensor range
        self.wall_dist = 0.5             # Distance desired from the wall
        self.max_speed = 0.3             # Maximum speed of the robot on meters/seconds
        self.p = 15                      # Proportional constant for controller  
        self.d = 0                       # Derivative constant for controller 
        self.angle = 1                   # Proportional constant for angle controller (just simple P controller)
        self.direction = -1              # 1 for wall on the left side of the robot (-1 for the right side)
        self.e = 0                       # Diference between current wall measurements and previous one
        self.angle_min = 0               # Angle, at which was measured the shortest distance between the robot and a wall
        self.dist_front = 0              # Measured front distance
        self.diff_e = 0                  # Difference between current error and previous one
        self.dist_min = 0                # Minimum measured distance

        # Time when the last outer corner; direction and inner corner were detected or changed.
        self.last_outer_corner_detection_time = time.time()
        self.last_change_direction_time = time.time()
        self.last_inner_corner_detection_time = time.time()
        self.rotating = 0 
        self.pub_ = None
        # Sensor regions
        self.regions_ = {
                'bright': 0,
                'right': 0,
                'fright': 0,
                'front': 0,
                'left': 0,
        }
        self.last_kinds_of_wall=[0, 0, 0, 0, 0]
        self.index = 0

        self.state_outer_inner=[0, 0, 0, 0]
        self.index_state_outer_inner = 0

        self.bool_outer_corner = 0
        self.bool_inner_corner =0

        self.last_vel = [random.uniform(0.1,0.3),  random.uniform(-0.3,0.3)]
        self.wall_found =0

        #Robot state machines
        self.state_ = 0
        self.state_dict_ = {
            0: 'random wandering',
            1: 'following wall',
            2: 'rotating'
        }
    
    def clbk_laser(self, msg):
        """
        Read sensor messagens, and determine distance to each region. 
        Manipulates the values measured by the sensor.
        Callback function for the subscription to the published Laser Scan values.
        """
        # global self.regions_, self.e, self.angle_min, self.dist_front, self.diff_e, self.direction, self.bool_outer_corner, self.bool_inner_corner, self.index, self.last_kinds_of_wall
        size = len(msg.ranges)
        min_index = size*(self.direction+1)/4
        max_index = size*(self.direction+3)/4
        
        # Determine values for PD control of distance and P control of angle
        for i in range(min_index, max_index):
            if msg.ranges[i] < msg.ranges[min_index] and msg.ranges[i] > 0.01:
                min_index = i
        self.angle_min = (min_index-size/2)*msg.angle_increment
        self.dist_min = msg.ranges[min_index]
        self.dist_front = msg.ranges[size/2]
        self.diff_e = min((self.dist_min - self.wall_dist) - self.e, 100)
        self.e = min(self.dist_min - self.wall_dist, 100)

        # Determination of minimum distances in each region
        self.regions_ = {
            'bright':  min(min(msg.ranges[0:143]), self.inf),
            'right': min(min(msg.ranges[144:287]), self.inf),
            'fright':  min(min(msg.ranges[288:431]), self.inf),
            'front':  min(min(msg.ranges[432:575]), self.inf),
            'fleft':   min(min(msg.ranges[576:719]), self.inf),
            'left':   min(min(msg.ranges[720:863]), self.inf),
            'bleft':   min(min(msg.ranges[864:1007]), self.inf),
        }
        #rospy.loginfo(regions_)

        # Detection of Outer and Inner corner
        self.bool_outer_corner = self.is_outer_corner()
        self.bool_inner_corner = self.is_inner_corner()
        if self.bool_outer_corner == 0 and self.bool_inner_corner == 0:
            self.last_kinds_of_wall[self.index]=0
        
        # Indexing for last five pattern detection
        # This is latter used for low pass filtering of the patterns
        self.index = self.index + 1 #5 samples recorded to asses if we are at the corner or not
        if self.index == len(self.last_kinds_of_wall):
            self.index = 0
            
        self.take_action()

        return None

    def change_state(self):
        """
        Change state for the machine states in accordance with the active and inactive regions of the sensor.
                State 0 No wall found - all regions infinite - Random Wandering
                State 1 Wall found - Following Wall
                State 2 Pattern sequence reached - Rotating
        """
        #global self.regions_, self.index, self.last_kinds_of_wall, self.index_state_outer_inner, self.state_outer_inner, self.loop_index, self.loop_index_outer_corner
        
        #global self.wall_dist, self.max_speed, self.direction, self.p, self.d, self.angle, self.dist_min, self.wall_found, self.rotating, self.bool_outer_corner, self.bool_inner_corner

        regions = self.regions_
        msg = Twist()
        linear_x = 0
        angular_z = 0

        state_description = ''

        # Patterns for rotating
        rotate_sequence_V1 = ['I', 'C', 'C', 'C']
        rotate_sequence_V2 = [0, 'C', 'C', 'C']
        rotate_sequence_W = ['I', 'C', 'I', 'C']

        if self.rotating == 1:
            state_description = 'case 2 - rotating'
            self.change_state(2)
            if(regions['left'] < self.wall_dist or regions['right'] < self.wall_dist):
                rotating = 0
        elif regions['fright'] == self.inf and regions['front'] == self.inf and regions['right'] == self.inf and regions['bright'] == self.inf and regions['fleft'] == self.inf and regions['left'] == self.inf and regions['bleft'] == self.inf:
            state_description = 'case 0 - random wandering'
            self.change_state(0)
        elif (self.loop_index == self.loop_index_outer_corner) and (rotate_sequence_V1 == self.state_outer_inner or rotate_sequence_V2 == self.state_outer_inner or rotate_sequence_W == self.state_outer_inner):
            state_description = 'case 2 - rotating'
            self.change_direction()
            self.state_outer_inner = [ 0, 0,  0, 'C']
            self.change_state(2)
        else:
            state_description = 'case 1 - following wall'
            self.change_state(1)
        
        return None

    def random_wandering(self):
        """
        This function defines the linear.x and angular.z velocities for the random wandering of the robot.
        Returns:
                Twist(): msg with angular and linear velocities to be published
                        msg.linear.x -> [0.1, 0.3]
                        msg.angular.z -> [-1, 1]
        """
        #global self.direction, self.last_vel
        msg = Twist()
        msg.linear.x = max(min(self.last_vel[0] + random.uniform(-0.01,0.01),0.3),0.1)
        msg.angular.z= max(min(self.last_vel[1] + random.uniform(-0.1,0.1),1),-1)
        if msg.angular.z == 1 or msg.angular.z == -1:
            msg.angular.z = 0
        self.last_vel[0] = msg.linear.x
        self.last_vel[1] = msg.angular.z
        return msg 

    def following_wall(self):
        """
        PD control for the wall following state. 
        Returns:
                Twist(): msg with angular and linear velocities to be published
                        msg.linear.x -> 0; 0.5max_speed; 0.4max_speed
                        msg.angular.z -> PD controller response
        """
        #global self.wall_dist, self.max_speed, self.direction, self.p, self.d, self.angle, self.dist_min, self.dist_front, self.e, diff_e, angle_min
        msg = Twist()
        if self.dist_front < self.wall_dist:
            msg.linear.x = 0
        elif self.dist_front < self.wall_dist*2:
            msg.linear.x = 0.5*self.max_speed
        elif abs(self.angle_min) > 1.75:
            msg.linear.x = 0.4*self.max_speed
        else:
            msg.linear.x = self.max_speed
        msg.angular.z = max(min(self.direction*(self.p*self.e+self.d*self.diff_e) + self.angle*(self.angle_min-((math.pi)/2)*self.direction), 2.5), -2.5)
        #print 'Turn Left angular z, linear x %f - %f' % (msg.angular.z, msg.linear.x)
        return msg

    def change_direction(self):
        """
        Toggle direction in which the robot will follow the wall
            1 for wall on the left side of the robot and -1 for the right side
        """
        #global self.direction, self.last_change_direction_time, self.rotating
        print('Change direction!')
        elapsed_time = time.time() - self.last_change_direction_time # Elapsed time since last change direction
        if elapsed_time >= 20:
            last_change_direction = time.time()
            self.direction = -self.direction # Wall in the other side now
            self.rotating = 1

    def rotating(self):
        """
        Rotation movement of the robot. 
        Returns:
                Twist(): msg with angular and linear velocities to be published
                        msg.linear.x -> 0m/s
                        msg.angular.z -> -2 or +2 rad/s
        """
        #global self.direction
        msg = Twist()
        msg.linear.x = 0
        msg.angular.z = self.direction*2
        return msg


    def is_outer_corner(self):
        """
        Assessment of outer corner in the wall. 
        If all the regions except for one of the back regions are infinite then we are in the presence of a possible corner.
        If all the elements in last_kinds_of_wall are 'C' and the last time a real corner was detected is superior or equal to 30 seconds:
            To state_outer_inner a 'C' is appended and 
            The time is restart.
        Returns:
                bool_outer_corner: 0 if it is not a outer corner; 1 if it is a outer corner
        """
        #global self.regions_, self.last_kinds_of_wall, self.last_outer_corner_detection_time, self.index, state_outer_inner, self.index_state_outer_inner, self.loop_index, self.loop_index_outer_corner
        regions = self.regions_
        self.bool_outer_corner = 0
        if (regions['fright'] == self.inf and regions['front'] == self.inf and regions['right'] == self.inf and regions['bright'] < self.inf  and regions['left'] == self.inf and regions['bleft'] == self.inf and regions['fleft'] == self.inf) or (regions['bleft'] < self.inf and regions['fleft'] == self.inf and regions['front'] == self.inf and regions['left'] == self.inf and regions['right'] == self.inf and regions['bright'] == self.inf and regions['fright'] == self.inf):
            self.bool_outer_corner = 1 # It is a corner
            self.last_kinds_of_wall[self.index]='C'
            elapsed_time = time.time() - self.last_outer_corner_detection_time # Elapsed time since last corner detection
            if self.last_kinds_of_wall.count('C') == len(self.last_kinds_of_wall) and elapsed_time >= 30:
                self.last_outer_corner_detection_time = time.time()
                self.loop_index_outer_corner = self.loop_index
                self.state_outer_inner = self.state_outer_inner[1:]
                self.state_outer_inner.append('C')
                print('It is a outer corner')
        return self.bool_outer_corner

    def is_inner_corner(self):
        """
        Assessment of inner corner in the wall. 
        If the three front regions are inferior than the wall_dist.
        If all the elements in last_kinds_of_wall are 'I' and the last time a real corner was detected is superior or equal to 20 seconds:
            To state_outer_inner a 'I' is appended and 
            The time is restart.
        Returns:
                bool_inner_corner: 0 if it is not a inner corner; 1 if it is a inner corner
        """
        #global self.regions_, self.wall_dist, self.last_kinds_of_wall, self.last_inner_corner_detection_time, self.index, self.state_outer_inner, self.index_state_outer_inner, self.loop_index_inner_corner, self.loop_index
        regions = self.regions_
        self.bool_inner_corner = 0
        if regions['fright'] < self.wall_dist and regions['front'] < self.wall_dist and regions['fleft'] < self.wall_dist:
            self.bool_inner_corner = 1
            self.last_kinds_of_wall[self.index]='I'
            elapsed_time = time.time() - self.last_inner_corner_detection_time # Elapsed time since last corner detection
            if self.last_kinds_of_wall.count('I') == len(self.last_kinds_of_wall) and elapsed_time >= 20:
                self.last_inner_corner_detection_time = time.time()
                self.loop_index_inner_corner = self.loop_index
                self.state_outer_inner = self.state_outer_inner[1:]
                self.state_outer_inner.append('I')
                print('It is a inner corner')
        return self.bool_inner_corner

    def FollowWall(self):
        global pub_, active_, self.hz, self.loop_index
    
        rospy.init_node('reading_laser')
        
        pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, self.clbk_laser)
        
        print('Code is running')
        rate = rospy.Rate(self.hz)
        while not rospy.is_shutdown():
            self.loop_index = self.loop_index + 1
            msg = Twist()

            # State Dispatcher
            if self.state_ == 0:
                msg = self.random_wandering()
            elif self.state_ == 1:
                msg = self.following_wall()
            elif self.state_ == 2:
                msg = self.rotating()
            else:
                rospy.logerr('Unknown state!')
            
            pub_.publish(msg)
            
            rate.sleep()