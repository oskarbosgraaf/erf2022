
import numpy as np
import math

import rospy
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from controller import PID
from std_msg.msg import Bool

COM_TOPIC_CM = "client_master"
COM_TOPIC_MC = "master_client"


if master: 
    rospy.init_node('wall_follower_master')
if client:
    rospy.init_node('wall_follower_client')

def CommunicationCB(msg):
    while True:
        print(f'received message: {msg.data}')
        if client: 
            com_pub.publish(True)

if master:
    rospy.Subscriber(COM_TOPIC_CM, Bool, CommunicationCB)
    com_pub = rospy.Publisher(COM_TOPIC_MC, Bool, queue_size = 10)

if client:
    rospy.Subscriber(self.COM_TOPIC_MC, Bool, CommunicationCB)
    com_pub = rospy.Publisher(COM_TOPIC_CM, Bool, queue_size = 10)



