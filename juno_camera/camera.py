
"""
Code for camera operation for the autonomous navigational robotics hackathon
from European Robotics Forum (ERF) 2022, implemented specifically for the Lely
Juno robot.
Team Unuversity of Amsterdam
Github: https://github.com/oskarbosgraaf/erf2022

Written and implemented by:
    Sjoerd Gunneweg
    Thijmen Nijdam
    Jurgen de Heus
    Francien Barkhof
    Oskar Bosgraaf
    Juell Sprott
    Sander van den Bent
    Derck Prinzhoorn

last updated: 1st of July, 2022
"""

import cv2
from matplotlib import pyplot as plt
import numpy as np
import follow_blob
from camera_corridor import Corridor
fb = follow_blob.FollowBlob()
from std.msgs.msg import Bool


class Camera:
    """All camera sensor in and output methods."""

    def __init__(self):
        self.video = 0
        self.width = 0
        self.behavior = 2
        self.centerX = 320
        self.pub_j = rospy.Publisher('other_detected', Bool, queue_size=10) #jurgen


    def show_RGB_to_HSV(self, image):
        """Show the current frame on screen."""
        img_HSV = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        plt.imshow(img_HSV)
        plt.show()


    def one_big_rect(self, color_string, image):
        """Generate blob detection and its center on the X-axis"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        result = image.copy()

        if color_string == 'green':
            sensitivity_g = 30
            color = cv2.inRange(hsv,(60 - sensitivity_g, 100, 100),(60 + sensitivity_g, 255, 255))

        if color_string == 'blue':
            color = cv2.inRange(hsv,(99, 115, 150),(120, 255, 255))

        contours = cv2.findContours(color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        boxes = []
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            if w > 10 and h > 10:
                boxes.append([x,y, x+w,y+h])

        result = image.copy()
        boxes = np.asarray(boxes)

        if len(boxes) == 0:
            return None, None
        left, top = np.min(boxes, axis=0)[:2]

        right, bottom = np.max(boxes, axis=0)[2:]
        cv2.rectangle(result, (left,top), (right,bottom), (255, 0, 0), 2)
        size_blob = (right - left) * (bottom - top)

        distanceX = (960/(right-left)) * 60
        self.centerX = (x+(0.5*w))
        RGB_result = result

        return RGB_result, self.centerX


    def video_blob_direction(self):
        """
        Driver code for sending hominig twist messages, based on the position
        of the green or blue blob in the field of vision.

        """
        self.video = cv2.VideoCapture(4,cv2.CAP_V4L2)
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)

        blue_counter = 0
        no_blue_counter = 0
        last_blue = False

        # continuous updates of camera frames
        while(self.video.isOpened()):
            ret, frame = self.video.read()

            # camera frame is valid
            if ret == True:
                frame_green, self.centerX = self.one_big_rect('green', frame)
                frame_blue, self.centerX_blue = self.one_big_rect('blue', frame)

                # blue is not detected
                if frame_blue is None:
                    no_blue_counter += 1

                    if no_blue_counter > 5 and last_blue:
                        # reset counters because behavior call later
                        no_blue_counter = 0
                        blue_counter = 0

                        last_blue = False

                        # activate behavior of turning lights off
                        self.behavior = 11
                        fb.decideBehavior(11)
                        self.pub_j.publish(False)
                # blue is detected
                else:
                    blue_counter += 1

                    if blue_counter > 5 and not last_blue:
                        # reset counters because behaviour call later
                        blue_counter = 0
                        no_blue_counter = 0

                        last_blue = True

                        # activate behavior of turning lights on
                        self.behavior = 10
                        fb.decideBehavior(self.behavior)
                        self.pub_j.publish(True)

                if frame_green is not None:
                    # show green blob detected in frame
                    cv2.imshow('Frame',frame_green)
                    cv2.waitKey(20)
                elif frame_blue is not None:
                    # show blue blob detected in frame
                    cv2.imshow('Frame',frame_blue)
                    cv2.waitKey(20)
                    continue
                else:
                    # behaviour call for turning if no blue or green blobs
                    cv2.imshow('Frame', frame)
                    cv2.waitKey(20)
                    self.behavior = 5
                    fb.decideBehavior(self.behavior)
                    continue
            # camera frame is invalid
            else:
                print('ret is false')
                return None

            # decide behavior to call for following blob direction
            print(self.centerX)
            if self.centerX < ((1/5)*self.width):
                self.behavior = 0

            if (self.centerX > (1/5)*self.width) and (self.centerX < (2/5)*self.width):
                self.behavior = 1

            if (self.centerX > (2/5)*self.width) and (self.centerX < (3/5)*self.width):
                self.behavior = 2

            if (self.centerX > (3/5)*self.width) and (self.centerX < (4/5)*self.width):
                self.behavior = 3

            if (self.centerX > ((4/5)*self.width)):
                self.behavior = 4

            fb.decideBehavior(self.behavior)

        self.video.release()
