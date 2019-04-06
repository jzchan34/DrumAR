import cv2
import numpy as np
import time
import pyaudio
import wave
from array import array
from struct import pack
import os


## Main Video Code

def play(file):
    CHUNK = 1024 #measured in bytes

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

def playDrum(i):
    if i == 0:
        play("Other/snare.wav")
    elif i == 1:
        play("Other/rack tom.wav")
    elif i == 2:
        play("Other/tom.wav")
    elif i == 3:
        play("Other/kick.wav")

def getDrum(i):
    color = (0,255,0)
    lineWidth = 2
    radius1, radius2, radius3 = 100, 130, 160
    point1, point2, point3, point4 = (200,530), (480,560), (740,560), (1060,500)
    cir1 = (point1,radius2,color,lineWidth)
    cir2 = (point2,radius1,color,lineWidth)
    cir3 = (point3,radius1,color,lineWidth)
    cir4 = (point4,radius3,color,lineWidth)
    ##Change based on System Mac or Windows
    drumParas = [cir1,cir2,cir3,cir4]
    return drumParas[i]
        
def main():
    hRange = (550, 650)
    splitRange = 320
    drumNum = 4
    threshold = (10,10,10)
    def checkDrum(res, k):
        mrg = 75
        counter = False
        for line in range(hRange[0], hRange[1], 30):
            for character in range(k * splitRange + mrg, (k + 1)*splitRange - mrg, 30):
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
    kernal = np.ones((5,5), 'uint8')
    cap = cv2.VideoCapture(0)
    drums = [0] * drumNum
    
    while(True):
        for timer in drums:
            if timer > 0:
                timer -= 1
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx = 1, fy = 1)
        #print(len(frame), len(frame[0])) #1440, 2560, 720, 1280
        frame = cv2.flip(frame, +1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frameHSV = cv2.erode(frameHSV, kernal, iterations = 5)
        frameHSV = cv2.dilate(frameHSV, kernal, iterations = 5)
        colorMask0 = cv2.inRange(frameHSV, colorLower, colorUpper)
        colorMask1 = cv2.inRange(frameHSV, colorLower1, colorUpper1)
        colorMask = colorMask0 + colorMask1
        res = cv2.bitwise_and(frame, frame, mask = colorMask)
        
        for i in range(len(drums)):
            timer = drums[i]
            point, radius, color, lineWidth = getDrum(i)
            cv2.circle(frame,point,radius,color,lineWidth)
            if timer == 0:
                isHit = checkDrum(res, i)
                if isHit == True:
                    playDrum(i)
                    cv2.circle(frame,point,radius,color,-1)
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