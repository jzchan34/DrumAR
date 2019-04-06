import cv2
import numpy as np
import time

## Main Video Code

def checkDrum(res):
    counter = False
    for line in range(720, 960,20): #check every 20 px
        for character in (0,640,20):
            for i in range(3):  
                if res[line][character][i] != 0:
                    counter = True
    return counter

#range of color
colorLower = np.array([110, 50, 50], np.uint8)
colorUpper = np.array([130, 255, 255], np.uint8)
print(colorLower, colorUpper)
cap = cv2.VideoCapture(0)
hitTimer = 0

def drawDrums(frame):
    #draw drums
    color = (0,255,0)
    lineWidth = 2
    radius1, radius2, radius3 = 100, 150, 200
    point1, point2, point3, point4 = (250,350), (460,530), (830,530), (1050,350)
    cv2.circle(frame,point1,radius1,color,lineWidth)
    cv2.circle(frame,point2,radius2,color,lineWidth)
    cv2.circle(frame,point3,radius2,color,lineWidth)
    cv2.circle(frame,point4,radius1,color,lineWidth)

while(True):
    if hitTimer > 0:
        hitTimer -= 1
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0,0), fx = 2, fy = 2)
    
    drawDrums(frame)
    
    #print(len(frame), len(frame[0])) #1440, 2560
    frame = cv2.flip(frame, +1)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    colorMask = cv2.inRange(frameHSV, colorLower, colorUpper)
    
    res = cv2.bitwise_and(frame, frame, mask = colorMask)
    isHit = checkDrum(res)
    
    if isHit == True and hitTimer == 0:
        print("hi")
        hitTimer = 20
    else:
        print("bye")
    
    cv2.imshow("Hello", res)
    cv2.imshow("Drum AR", frame)
    #if condition is met, break out of loop
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


        
## Tkinter