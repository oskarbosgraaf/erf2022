import rospy
from geometry_msgs import Twist

rospy.init_node('Test', anonymous=False)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

msg = Twist()
msg.linear.x = 0.2
msg.angular.z = 0.15
pub.publish(msg)
rospy.sleep(0.2)


msg = Twist()
msg.linear.x = 0.2
msg.angular.z = -0.15
pub.publish(msg)
rospy.sleep(0.2)