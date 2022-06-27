
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import follow_blob
import warnings
import rospy

# from turtlebot.camera_movement.main import FollowBlob

fb = follow_blob.FollowBlob()
warnings.filterwarnings('ignore')

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

    def one_big_rect(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        orange = cv2.inRange(hsv,(0, 100, 20), (25, 200, 255))
        orange = cv2.medianBlur(orange, 5)
        result = image.copy()
        contours = cv2.findContours(orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
        distanceX = (960/(right-left)) * 60
        self.centerX = (x+(0.5*w))
        RGB_result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return RGB_result, self.centerX

    # img = cv2.imread("blob_images/donald.jpg")
    # input, _ = one_big_rect(img)
    # plt.imshow(input)
    # plt.show()

    def show_video_blob(self):
        self.video = cv2.VideoCapture(1)

        while(self.video.isOpened()):
            ret, frame = self.video.read()
            if ret == True:
                frame, _ = self.one_big_rect(frame)
                cv2.imshow('Frame',frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        self.video.release()
        cv2.destroyAllWindows()

    # Onderstaande is de functie is voor blob detection en welke kant hij opgestuurd moet worden

    def video_blob_direction(self):
        # 0 voor ubuntu logitech camera (Sien)
        self.video = cv2.VideoCapture(0,cv2.CAP_V4L2)
        # print('thanks')
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # print('width and height')
        # print(width, height)

        while(self.video.isOpened()):
            print("2")
            # print('in video direction while')
            ret, frame = self.video.read()
            # print(f'frame shape = {frame.shape}')
            # print(f'frame = {frame}')
            if ret == True:
                frame, self.centerX = self.one_big_rect(frame)
                # print(f'centerX = {centerX}')
                # print(f'frame shape = {frame.shape}')
                if frame is None:
                    print('no orange: turn')
                    self.behavior = 5
                    fb.decideBehavior(self.behavior)
                    continue

                else:
                    cv2.imshow('Frame',frame)
                
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            else:
                print('ret is false')
                return None
            # print(f'width = {self.width}')
            print(f'centerx = {self.centerX}')
            print(f'widt = {self.width}')
            if self.centerX < ((1/5)*self.width):
                print('cam left')

                self.behavior = 0
                # return 0
            
            if (self.centerX > (1/5)*self.width) and (self.centerX < (2/5)*self.width):
                print('cam adjust left')
                self.behavior = 1
                # return 1

            if (self.centerX > (2/5)*self.width) and (self.centerX < (3/5)*self.width):
                print('cam move forward')
                self.behavior = 2
                # return 2

            if (self.centerX > (3/5)*self.width) and (self.centerX < (4/5)*self.width):
                print('cam adjust right')
                self.behavior = 3
                # return 3

            if (self.centerX > ((4/5)*self.width)):
                print('cam right')
                self.behavior = 4
                # return 4
            
            fb.decideBehavior(self.behavior)

        self.video.release()

        # cv2.destroyAllWindows()

if __name__ == '__main__':
    # rospy.init_node('FollowBlob', anonymous=False)
    print( " === Starting Program === " )
    
    # fb = FollowBlob()
    cam = Camera()
    cam.video_blob_direction()
        # fb.decideBehavior(cam)fb



