#!/usr/bin/env python
import time
import rospy
import rosservice
import signal
import sys
import math
import atexit

# TODO: check if we need the telemetrix version of this?
#sys.path.append('/usr/local/lib/python2.7/dist-packages/PyMata-2.20-py2.7.egg')  # Needed for jupyter notebooks
#sys.path.append('/usr/local/lib/python2.7/dist-packages/pyserial-3.4-py2.7.egg')

import message_filters
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from std_msgs.msg import String
from std_msgs.msg import Empty
from mirte_msgs.msg import *

from mirte_msgs.srv import *
from std_srvs.srv import *

mirte = {}

class Robot():
    """ Robot API

        This class allows you to control the robot from Python. The getters and setters
        are just wrappers calling ROS topics or services.
    """


    def __init__(self):
        # Stop robot when exited
        atexit.register(self.stop)

        self.PWM = 3 #PrivateConstants.PWM when moving to Python3
        self.INPUT = 0
        self.OUTPUT = 1
        self.PULLUP = 11
        self.ANALOG = 2

        # Start timing
        self.begin_time = time.time()
        self.last_call = 0

        # Call /stop and /start service to disable/enable the ROS diff_drive_controller
        # By default this class will control the rbot though PWM (controller stopped). Only in case
        # the controller is needed, it will be enabled.
        self.stop_controller_service = rospy.ServiceProxy('stop', Empty, persistent=True)
        self.start_controller_service = rospy.ServiceProxy('start', Empty, persistent=True)
        #self.stop_controller_service()

        # Service for motor speed
        self.motors = {}
        if rospy.has_param("/mirte/motor"):
            self.motors = rospy.get_param("/mirte/motor")
            self.motor_services = {}
            for motor in self.motors:
                self.motor_services[motor] = rospy.ServiceProxy('/mirte/set_' + self.motors[motor]["name"] + '_speed', SetMotorSpeed, persistent=True)

        # Service for motor speed
        if rospy.has_param("/mirte/servo"):
            servos = rospy.get_param("/mirte/servo")
            self.servo_services = {}
            for servo in servos:
                self.servo_services[servo] = rospy.ServiceProxy('/mirte/set_' + servos[servo]["name"] + '_servo_angle', SetServoAngle, persistent=True)

        rospy.init_node('mirte_python_api', anonymous=False)

        ## Sensors
        ## The sensors are now just using a blocking service call. This is intentionally
        ## since one first needs to learn to program in a synchronous way without events.
        ## Event based programming is already possible using the ROS topics for the
        ## same sensors. At a later stage we will expose this as well to this API and
        ## maybe even to blockly.

        # Services for distance sensors
        if rospy.has_param("/mirte/distance"):
            distance_sensors = rospy.get_param("/mirte/distance")
            self.distance_services = {}
            for sensor in distance_sensors:
               self.distance_services[sensor] = rospy.ServiceProxy('/mirte/get_distance_' + distance_sensors[sensor]["name"], GetDistance, persistent=True)

        if rospy.has_param("/mirte/oled"):
            oleds = rospy.get_param("/mirte/oled")
            self.oled_services = {}
            for oled in oleds:
               self.oled_services[oled] = rospy.ServiceProxy('/mirte/set_' + oleds[oled]["name"] + '_image', SetOLEDImage, persistent=True)

        # Services for intensity sensors (TODO: how to expose the digital version?)
        if rospy.has_param("/mirte/intensity"):
            intensity_sensors = rospy.get_param("/mirte/intensity")
            self.intensity_services = {}

            # We can not get the types (analog and/or digital) of the intensity sensor
            # straight from the parameter server (it might be just set as the PCB without
            # explicit values. We can however deduct what is there by checking the
            # services.
            service_list = rosservice.get_service_list()
            for sensor in intensity_sensors:
                if "/mirte/get_intensity_" + intensity_sensors[sensor]["name"] in service_list:
                    self.intensity_services[sensor] = rospy.ServiceProxy('/mirte/get_intensity_' + intensity_sensors[sensor]["name"], GetIntensity, persistent=True)
                if "/mirte/get_intensity_" + intensity_sensors[sensor]["name"] + "_digital" in service_list:
                    self.intensity_services[sensor + "_digital"] = rospy.ServiceProxy('/mirte/get_intensity_' + intensity_sensors[sensor]["name"] + "_digital", GetIntensityDigital, persistent=True)


        # Services for encoder sensors
        if rospy.has_param("/mirte/encoder"):
            encoder_sensors = rospy.get_param("/mirte/encoder")
            self.encoder_services = {}
            for sensor in encoder_sensors:
                self.encoder_services[sensor] = rospy.ServiceProxy('/mirte/get_encoder_' + encoder_sensors[sensor]["name"], GetEncoder, persistent=True)

        # Services for keypad sensores
        if rospy.has_param("/mirte/keypad"):
            keypad_sensors = rospy.get_param("/mirte/keypad")
            self.keypad_services = {}
            for sensor in keypad_sensors:
                self.keypad_services[sensor] = rospy.ServiceProxy('/mirte/get_keypad_' + keypad_sensors[sensor]["name"], GetKeypad, persistent=True)

        self.get_pin_value_service = rospy.ServiceProxy('/mirte/get_pin_value', GetPinValue, persistent=True)
        self.set_pin_value_service = rospy.ServiceProxy('/mirte/set_pin_value', SetPinValue, persistent=True)


        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def getTimestamp(self):
        """Gets the elapsed time in seconds since the initialization fo the Robot.

        Returns:
            float: Time in seconds since the initialization of the Robot. Fractions of a second may be present if the system clock provides them.
        """

        return time.time() - self.begin_time

    def getTimeSinceLastCall(self):
        """Gets the elapsed time in seconds since the last call to this function.

        Returns:
            float: Time in seconds since last call to this function. Fractions of a second may be present if the system clock provides them.
        """

        last_call = self.last_call
        self.last_call = time.time()
        if last_call == 0:
           return 0
        else:
           return time.time() - last_call

    def getDistance(self, sensor):
        """Gets data from a HC-SR04 distance sensor: calculated distance in meters.

        Parameters:
            sensor (str): The name of the sensor as defined in the configuration.

        Returns:
            int: Range in meters measured by the HC-SR04 sensor.

        Warning:
            A maximum of 6 distance sensors is supported.
        """


        dist = self.distance_services[sensor]()
        return dist.data

    def getIntensity(self, sensor, type="analog"):
        """Gets data from an intensity sensor.

        Parameters:
            sensor (str): The name of the sensor as defined in the configuration.
            type (str): The type of the sensor (either 'analog' or 'digital').

        Returns:
            int: Value of the sensor (0-255 when analog, 0-1 when digital).
        """
        if type == "analog":
           value = self.intensity_services[sensor]()
        if type == "digital":
           value = self.intensity_services[sensor + "_digital"]()
        return value.data

    def getEncoder(self, sensor):
        """Gets data from an encoder: every encoder pulse increments the counter.

        Parameters:
            sensor (str): The name of the sensor as defined in the configuration.

        Returns:
            int: Number of encoder pulses since boot of the robot.
        """

        value = self.encoder_services[sensor]()
        return value.data

    def getKeypad(self, keypad):
        """Gets the value of the keypad: the button that is pressed.

        Parameters:
            keypad (str): The name of the sensor as defined in the configuration.

        Returns:
            str: The name of the button ('up', 'down', 'left', 'right', 'enter').
        """


        value = self.keypad_services[keypad]()
        return value.data

    def getAnalogPinValue(self, pin):
        """Gets the input value of an analog pin.

        Parameters:
            pin (str): The pin number of an analog pin as printed on the microcontroller.

        Returns:
            int: Value between 0-255.
        """

        value = self.get_pin_value_service(str(pin), "analog")
        return value.data

    def setAnalogPinValue(self, pin, value):
        """Sets the output value of an analog pin (PWM).

        Parameters:
            pin (str): The pin number of an analog pin as printed on the microcontroller.
            value (int): Value between 0-255.
        """

        value = self.set_pin_value_service(str(pin), "analog", value)
        return value.status

    def setOLEDText(self, oled, text):
        """Shows text on the OLED.

        Parameters:
            oled (str): The name of the sensor as defined in the configuration.
            text (str): String to be shown on the 128x64 OLED.
        """
        value = self.oled_services[oled]('text', str(text))
        return value.status

    def setOLEDImage(self, oled, image):
        """Shows image on the OLED.

        Parameters:
            oled (str): The name of the sensor as defined in the configuration.
            image (str): Image name as defined in the images folder of the mirte-oled-images repository (excl file extension).
        """

        value = self.oled_services[oled]('image', image)
        return value.status

    def setOLEDAnimation(self, oled, animation):
        """Shows animation on the OLED.

        Parameters:
            oled (str): The name of the sensor as defined in the configuration.
            animation (str): Animation (directory) name as defined in the animations folder of the mirte-oled-images repository.
        """

        value = self.oled_services[oled]('animation', animation)
        return value.status

    def getDigitalPinValue(self, pin):
        """Gets the input value of a digital pin.

        Parameters:
            pin (str): The pin number of an analog pin as printed on the microcontroller.

        Returns:
            bool: The input value.
        """

        value = self.get_pin_value_service(str(pin), "digital")
        return value.data

    def setServoAngle(self, servo, angle):
        """Sets the angle of a servo.

        Parameters:
            servo (str): The name of the sensor as defined in the configuration.
            angle (int): The angle of the servo (range [0-360], but some servos
                         might be hysically limited to [0-180].

        Returns:
            bool: True if set successfully.

        Warning:
            The servo uses the Servo library from Arduino (through Telemetrix). This also
            means that, when a servo is used and the library is enabled, the last timer on
            the MCU will be used for timing of the servos. This timer therefore can not be
            used for PWM anymore. For Arduino Nano/Uno this means pins D9 and D10 will not
            have PWM anymore. For the SMT32 this means pins A1, A2, A3, A15, B3, B10, and B11
            will not have PWM anymore.

        Warning:
            A maximum of 12 servos is supported.
        """

        value = self.servo_services[servo](angle)
        return value.status

    def setDigitalPinValue(self, pin, value):
        """Sets the output value of a digital pin.

        Parameters:
            pin (str): The pin number of an analog pin as printed on the microcontroller.
            value (bool): Value to set.
        """
        value = self.set_pin_value_service(str(pin), "digital", value)
        return value.status

    def setMotorSpeed(self, motor, value):
        """Sets the speed of the motor.

        Parameters:
            motor (str): The name of the sensor as defined in the configuration.
            value (int): The 'directional duty cycle' (range [-100, 100]) of the PWM 
                         signal (-100: full backward, 0: stand still, 100: full forward).

        Returns:
            bool: True if set successfully.
        """

        motor = self.motor_services[motor](value)
        return motor.status

    def stop(self):
        """Stops all DC motors defined in the configuration

        Note:
            This function is always called when a script exits (either by the user
            or when it finished.

        """

        for motor in self.motors:
           self.setMotorSpeed(self.motors[motor]["name"], 0)

    def _signal_handler(self, sig, frame):
        self.stop()
        sys.exit()

# We need a special function to initiate the Robot() because the main.py need to call the
# init_node() (see: https://answers.ros.org/question/266612/rospy-init_node-inside-imported-file/)
def createRobot():
    """Creates and return instance of the robot class.

    Returns:
       Robot: The initialize Robot class.
    """

    global mirte
    mirte = Robot()
    return mirte
