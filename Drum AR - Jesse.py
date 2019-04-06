import cv2
import numpy as np
import time

## Main Video Code
def main():
    hRange = (400, 650)
    splitRange = 300
    threshold = (10,10,10)
    def checkDrum(res, k):
        mrg = 90
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
    drumNum = 4
    drums = [0] * drumNum
    
    while(True):
        for timer in drums:
            if timer > 0:
                timer -= 1
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx = 2, fy = 2)
            
        #drum parameters
        color = (0,255,0)
        lineWidth = 2
        radius1, radius2, radius3 = 100, 130, 170
        point1, point2, point3, point4 = (200,530), (480,560), (740,560), (1060,500)
        cir1 = (frame,point1,radius2,color,lineWidth)
        cir2 = (frame,point2,radius1,color,lineWidth)
        cir3 = (frame,point3,radius1,color,lineWidth)
        cir4 = (frame,point4,radius3,color,lineWidth)
        drumParas = [cir4,cir3,cir2,cir1]
        
        #print(len(frame), len(frame[0])) #1440, 2560
        frame = cv2.flip(frame, +1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        colorMask0 = cv2.inRange(frameHSV, colorLower, colorUpper)
        colorMask1 = cv2.inRange(frameHSV, colorLower1, colorUpper1)
        colorMask = colorMask0 + colorMask1
        res = cv2.bitwise_and(frame, frame, mask = colorMask)
        for i in range(len(drums)):
            timer = drums[i]
            #retrieve the drum parameters
            frame,point1,radius2,color,lineWidth = drumParas[i]
            cv2.circle(frame,point1,radius2,color,3)
            #here
            if timer == 0:
                isHit = checkDrum(res, i)
                if isHit == True:
                    
                    print("Drum", i+1, "hi")
                    cv2.circle(frame,point1,radius2,color,-1)
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