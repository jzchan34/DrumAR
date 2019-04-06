import cv2
import numpy as np

## Main Video Code

#get the default/first camera
cap = cv2.VideoCapture(0)

def doNothing(x):
    pass

cv2.namedWindow("Tracking")
cv2.createTrackbar("lowerHue", "Tracking", 0, 255, doNothing)
cv2.createTrackbar("lowerSaturation", "Tracking", 0, 255, doNothing)
cv2.createTrackbar("lowerValue", "Tracking", 0, 255, doNothing)
cv2.createTrackbar("upperHue", "Tracking", 255, 255, doNothing)
cv2.createTrackbar("upperSaturation", "Tracking", 255, 255, doNothing)
cv2.createTrackbar("upperValue", "Tracking", 255, 255, doNothing)

while(True):
    #ret=True if frame is available, frame will actually capture the frame
    ret, frame = cap.read()

    frame = cv2.resize(frame, (0,0), fx = 2, fy = 2)
    frame = cv2.flip(frame, +1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    #customizable HSV
    lh = cv2.getTrackbarPos("lowerHue", "Tracking")
    ls = cv2.getTrackbarPos("lowerSaturation", "Tracking")
    lv = cv2.getTrackbarPos("lowerValue", "Tracking")
    
    uh = cv2.getTrackbarPos("upperHue", "Tracking")
    us = cv2.getTrackbarPos("upperSaturation", "Tracking")
    uv = cv2.getTrackbarPos("upperValue", "Tracking")

    #range of color
    colorLower = np.array([lh, ls, lv], np.uint8)
    colorUpper = np.array([uv, us, uh], np.uint8)
    
    colorMask = cv2.inRange(frameHSV, colorLower, colorUpper)
    res = cv2.bitwise_and(frame, frame, mask = colorMask)

    #creating a frame
    cv2.imshow("Hello", res)
    cv2.imshow("Drum AR", frame)
        
    #if condition is met, break out of loop at keyPress "q"
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

