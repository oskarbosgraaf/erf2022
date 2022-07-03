#!/usr/bin/env python

import rospy
import actionlib
import math
from smach import State,StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from corridor import Corridor
import tf



o = []
# List of waypoints, hardcoded but can be generated if desired
points = [[1.619999885559082, 0.6499996781349182],
 [2.242051601409912, 4.6637749671936035],
  [3.0699996948242188, 5.850000858306885],
 [2.989999771118164, 7.790000915527344], 
[0.7000000476837158, 7.820000648498535],
[-0.5900008082389832, 0.9100019931793213],
 [-0.420043408870697, -0.5402257442474365],
 [2.460049867630005, 4.287151336669922]]

# calculate orientation from one point to the next
# provides fluid movement from 2 consecutive points
for i in range(len(points)):
    if i != 7:
        x1 = points[i][0]
        y1 = points[i][1]
        x2 = points[i+1][0]
        y2 = points[i+1][1]
        heading = math.atan2(y2 - y1, x2 - x1) #* (180 / math.pi)

        yaw = heading
        print(heading)
        roll = 0.0
        pitch = 0.0
        a, b, c, d = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
        o.append([a,b,c,d])

# waypoint formatting for the FSM
waypoints = [
    ['one', (points[0][0], points[0][1]), (o[0][0], o[0][1], o[0][2], o[0][3])],
    ['two', (points[1][0], points[1][1]), (o[1][0], o[1][1], o[1][2], o[1][3])],
    ['three', (points[2][0], points[2][1]), (o[2][0], o[2][1], o[2][2], o[2][3])],
    ['four', (points[3][0], points[3][1]), (o[3][0], o[3][1], o[3][2], o[3][3])],
    ['five', (points[4][0], points[4][1]), (o[4][0], o[4][1], o[4][2], o[4][3])],
    ['six', (points[5][0], points[5][1]), (o[5][0], o[5][1], o[5][2], o[5][3])],
    ['seven', (points[6][0], points[6][1]), (o[6][0], o[6][1], o[6][2], o[6][3])],
    ['eight', (points[7][0], points[7][1]), (0.0, 0.0, -0.10694790223400114, 0.9942646258455273)]
]


# FSM class
class Waypoint(State):
    def __init__(self, position, orientation):
        State.__init__(self, outcomes=['success'])

        # Get an action client
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

        # Define the goal
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]

    # send goal to robot
    def execute(self, userdata):
        self.client.send_goal(self.goal)
        self.client.wait_for_result()
        return 'success'

# main loop
if __name__ == '__main__':
    rospy.init_node('patrol')

    # corridor check for communication
    corridor = Corridor()

    # initialize FSM
    patrol = StateMachine('success')
    with patrol:
        for i,w in enumerate(waypoints):
            print(i)
            print(w[1])
            print(w[2])
            StateMachine.add(w[0],
                             Waypoint(w[1], w[2]),
                             transitions={'success':waypoints[(i + 1) % \
                             len(waypoints)][0]})

    # execute FSM
    patrol.execute()