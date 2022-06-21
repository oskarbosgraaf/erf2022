from rcply.qos import qos_profile_sensor_data, QoSProfile
from sensor_msgs.msg import LaserScan
import rclpy

def test(msg):
    print(msg.ranges)
    print(f'value at 0 {msg.ranges[0]}')
    print(f'value at 15 {msg.ranges[15]}')

def main():
    rclpy.init()
    # qos = QoSProfile(depth=10)
    node = rclpy.create_node('scan_listener')
    sub = node.create_subscription(LaserScan, 'scan', test, qos_profile = qos_profile_sensor_data)

    try:
        while True:
            rclpy.spin_once(node)
    
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    print('start run')
    main()
    print('done')
