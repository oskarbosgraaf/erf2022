import cv2
import numpy as np

# video=cv2.VideoCapture(0,cv2.CAP_DSHOW)
video=cv2.VideoCapture(0)

hype = True

while(hype):
    ret,frame=video.read()
    img=cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
    # gb = cv2.GaussianBlur(img, (5, 5), 100)

    edge=cv2.Canny(img, 100, 200)
    lines=cv2.HoughLinesP(edge,rho=1,theta=1*np.pi/180,threshold=100,minLineLength=100,maxLineGap=50)
    if lines is not None:
        for i in lines:
            x1,x2,y1,y2=i[0]
            cv2.line(img,(x1,x2), (y1,y2),(0,255,0),3)
    cv2.imshow("window", img)
    key=cv2.waitKey(1)
    # if(key==1000):
    #     break
# video.release()
cv2.destroyAllWindows()