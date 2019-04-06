import cv2
import numpy as np
import time

## Main Video Code
def checkDrum(res):
    counter = False
    for line in range(720, 1080):
        for character in (0,640):
            for i in range(3):
                if res[line][character][i] != 0:
                    counter = True
    return counter

#range of color
colorLower = np.array([110, 50, 50], np.uint8)
colorUpper = np.array([130, 255, 255], np.uint8)
print(colorLower, colorUpper)

#get the default/first camera
cap = cv2.VideoCapture(0)
hitTimer = 0


while(True):
    if hitTimer > 0:
        hitTimer -= 1
    #ret=True if frame is available, frame will actually capture the frame
    ret, frame = cap.read()

    frame = cv2.resize(frame, (0,0), fx = 2, fy = 2)
    #print(len(frame), len(frame[0])) #1440, 2560
    frame = cv2.flip(frame, +1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #range of color
    colorLower = np.array([lh, ls, lv], np.uint8)
    colorUpper = np.array([uv, us, uh], np.uint8)
    
    colorMask = cv2.inRange(frameHSV, colorLower, colorUpper)
    res = cv2.bitwise_and(frame, frame, mask = colorMask)
    
    isHit = checkDrum(res)
    if isHit == True and hitTimer == 0:
        print("hi")
        hitTimer = 20
    else:
        print("bye")

    #creating a frame
    cv2.imshow("Hello", res)
    cv2.imshow("Drum AR", frame)
        
    #if condition is met, break out of loop at keyPress "q"
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


        
## Tkinter