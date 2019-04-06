import cv2
import numpy as np

## Main Video Code

#range of color
colorLower = np.array([22, 60, 200], np.uint8)
colorUpper = np.array([60, 255, 255], np.uint8)

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0,0), fx = 2, fy = 2)
    frame = cv2.flip(frame, +1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("Drum AR", frame)
    
    #if condition is met, break out of loop
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

