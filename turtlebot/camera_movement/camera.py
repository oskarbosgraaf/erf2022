
import cv2
from matplotlib import pyplot as plt
import numpy as np
import time

class Camera:
    def __init__(self, video):
        self.video = video

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
        left, top = np.min(boxes, axis=0)[:2]
        right, bottom = np.max(boxes, axis=0)[2:]
        cv2.rectangle(result, (left,top), (right,bottom), (255, 0, 0), 2)
        distanceX = (960/(right-left)) * 60
        centerX = (x+(0.5*w))
        RGB_result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return RGB_result, centerX

    img = cv2.imread("blob_images/donald.jpg")
    input, _ = one_big_rect(img)
    plt.imshow(input)
    plt.show()

    def show_video_blob(self):
        # cap = cv2.VideoCapture(1)

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

    def video_blob_direction(self, method):
        # cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        while(self.video.isOpened()):
            ret, frame = self.video.read()
            if ret == True:
                frame, centerX = method(frame)
                cv2.imshow('Frame',frame)
                
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            if centerX < 460:
                return 'adjustright'
            elif centerX > 500:
                return 'adjustleft'

            else:
                return 'drivestraight'


                

        self.video.release()

        cv2.destroyAllWindows()




