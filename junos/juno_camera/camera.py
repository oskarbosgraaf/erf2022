import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import follow_blob
from camera_corridor import Corridor
import sys
fb = follow_blob.FollowBlob()

corridor = Corridor()

class Camera:
    def __init__(self):
        self.video = 0
        self.width = 0
        self.behavior = 2
        self.centerX = 320

    def show_RGB_to_HSV(self, image):
        img_HSV = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        plt.imshow(img_HSV)
        plt.show()

    def one_big_rect(self, color_string, image):
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

        # UNCOMMENT IF TIME LEFT

        # if color_string == 'green' and size_blob > 1382000:
        #     # stop
        #     self.behavior = 8
            # fb.decideBehavior(self.behavior)
            # print("JUNO CLOSE")
            # print(size_blob)

        #########

        distanceX = (960/(right-left)) * 60
        self.centerX = (x+(0.5*w))
        RGB_result = result
        return RGB_result, self.centerX

    def video_blob_direction(self):
        # 0 voor ubuntu logitech camera (Sien)
        # 1, error vindt niet
        # 0 webcam lap
        # -1 webcam lap
        # 4 op laptop jurgens
        self.video = cv2.VideoCapture(4,cv2.CAP_V4L2)

        # voor thijmens laptop
        # self.video = cv2.VideoCapture(0)

        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)

        blue_counter = 0
        no_blue_counter = 0
        last_blue = False

        while(self.video.isOpened()):
            ret, frame = self.video.read()
            if ret == True:
                frame_green, self.centerX = self.one_big_rect('green', frame)
                frame_blue, self.centerX_blue = self.one_big_rect('blue', frame)

                ### UNCOMMENT IF TIME

                if frame_blue is None:
                    # reset blue counter
                    print('no blue')
                    no_blue_counter += 1
                

                    if no_blue_counter > 5 and last_blue:
                        no_blue_counter = 0
                        blue_counter = 0 
                        last_blue = False
                        print("LIGHTS OFF")
                        self.behavior = 11
                        fb.decideBehavior(11)
                else: 
                    blue_counter += 1
                    no_blue_counter = 0
                    # frame_blue_last = True
                    print('blue')

                    if blue_counter > 5 and not last_blue:
                        blue_counter = 0
                        no_blue_counter = 0
                        last_blue = True
                        print("LIGHTS ON")
                        self.behavior = 10
                        fb.decideBehavior(self.behavior)

                ###### 
                
                if frame_green is not None:
                    cv2.imshow('Frame',frame_green)
                    # cv2.imshow('Frame', frame)
            
                    cv2.waitKey(20)

                elif frame_blue is not None:
                    cv2.imshow('Frame',frame_blue)
                    # cv2.imshow('Frame', frame)
            
                    cv2.waitKey(20)
                    continue

                else:
                    
                    cv2.imshow('Frame', frame)
                    cv2.waitKey(20)
                    # print('no green: turn')
                    # self.behavior = 5
                    # if corridor.other_in_corridor:
                    #     fb.wait()
                    # else:
                    #     fb.decideBehavior(self.behavior)
                    
                    continue


            else:
                print('ret is false')
                return None

            if self.centerX < ((1/5)*self.width):
                # print('left')
                self.behavior = 0


            if (self.centerX > (1/5)*self.width) and (self.centerX < (2/5)*self.width):
                # print('adjust left')
                self.behavior = 1


            if (self.centerX > (2/5)*self.width) and (self.centerX < (3/5)*self.width):
                # print('forward')
                self.behavior = 2



            if (self.centerX > (3/5)*self.width) and (self.centerX < (4/5)*self.width):
                # print('adjust right')
                self.behavior = 3


            if (self.centerX > ((4/5)*self.width)):
                # print('right')
                self.behavior = 4

            # if corridor.other_in_corridor:
            #     fb.wait()
            # else:
            #     fb.decideBehavior(self.behavior)

        self.video.release()
