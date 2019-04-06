import cv2
import numpy as np
import time

## Main Video Code
def main():
    hRange = (1100, 1300)
    splitRange = 640
    drumNum = 4
    threshold = (10,10,10)
    def checkDrum(res, k):
        mrg = 150
        counter = False
        for line in range(hRange[0], hRange[1], 20):
            for character in range(k * splitRange + mrg, (k + 1)*splitRange - mrg, 20):
                for i in range(3):
                    if res[line][character][i] >= threshold[i]:
                        counter = True
        return counter
    
    #range of color
    #colorLower = np.array([0, 50, 0], np.uint8)
    #colorUpper = np.array([45, 100, 100], np.uint8)
    colorLower = np.array([0, 120, 70], np.uint8)
    colorUpper = np.array([10, 255, 255], np.uint8)
    colorLower1 = np.array([170, 120, 70], np.uint8)
    colorUpper1 = np.array([180, 255, 255], np.uint8)
    
    cap = cv2.VideoCapture(0)
    drums = [0] * drumNum
    
    while(True):
        for timer in drums:
            if timer > 0:
                timer -= 1
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx = 2, fy = 2)
        #print(len(frame), len(frame[0])) #1440, 2560
        frame = cv2.flip(frame, +1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        colorMask0 = cv2.inRange(frameHSV, colorLower, colorUpper)
        colorMask1 = cv2.inRange(frameHSV, colorLower1, colorUpper1)
        colorMask = colorMask0 + colorMask1
        res = cv2.bitwise_and(frame, frame, mask = colorMask)
        for i in range(len(drums)):
            timer = drums[i]
            cv2.rectangle(frame,(i*splitRange,hRange[0]),((i+1)*splitRange,hRange[1]),(0,255,0),3)
            if timer == 0:
                isHit = checkDrum(res, i)
                if isHit == True:
                    
                    print("Drum", i+1, "hi")
                    cv2.rectangle(frame,(i*splitRange,hRange[0]),((i+1)*splitRange,hRange[1]),(0,255,0),-1)
                    timer = 20
                else:
                    print("Drum", i+1, "bye")
        
        cv2.imshow("Hello", res)
        cv2.imshow("Drum AR", frame)
        #if condition is met, break out of loop
        ch = cv2.waitKey(1)
        if ch & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

main()
        
## Tkinter