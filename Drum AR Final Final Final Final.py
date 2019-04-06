import cv2
import numpy as np
import time
import pyaudio
import wave
from array import array
from struct import pack
import os
import threading
import sys
from collections import deque
from imutils.video import VideoStream
import argparse
import imutils

##Sound
    
def drumThreadCreator(file):
    drumThread = threading.Thread(target = play, args = (file,))
    drumThread.start()

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

## Main Video Code


def playDrum(i):
    if i == 0:
        drumThreadCreator("Other/snare.wav")
    elif i == 1:
        drumThreadCreator("Other/rack tom.wav")
    elif i == 2:
        drumThreadCreator("Other/tom.wav")
    elif i == 3:
        drumThreadCreator("Other/kick.wav")
    elif i == 4:
        drumThreadCreator("Other/closed hat.wav")

def getDrum(i):
    color = (0,255,0)
    lineWidth = 2
    radius1, radius2, radius3, radius4 = 100, 120, 140, 100
    point1, point2, point3, point4, point5 = (300,550), (580,500), (820,500), (1100,550), (150,300)
    cir1 = (point1,radius2,color,lineWidth)
    cir2 = (point2,radius1,color,lineWidth)
    cir3 = (point3,radius1,color,lineWidth)
    cir4 = (point4,radius3,color,lineWidth)
    cir5 = (point5,radius4,color,lineWidth)
    ##Change based on System Mac or Windows
    drumParas = [cir1,cir2,cir3,cir4,cir5]
    return drumParas[i]

def main():
    hRange = (550, 650)
    splitRange = 320
    drumNum = 5
    threshold = (10,10,10)
    def checkDrum(res, k):
        point, radius, _, _ = getDrum(k)
        counter = False
        for line in range(point[1] - radius//2, point[1] + (radius*2//3), 20):
            for char in range(point[0] - radius//2, point[0] + radius//2, 20):
                for i in range(3):
                    if res[line][char][i] >= threshold[i]:
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
    drums = [0] * drumNum
    inDrums = [False] * drumNum
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)
    drumStatus = [0] * drumNum
    while(True):
        for i in range(len(drums)):
            if drums[i] > 0:
                drums[i] -= 1
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0,0), fx = 1, fy = 1)
        #print(len(frame), len(frame[0])) #1440, 2560, 720, 1280
        frame = cv2.flip(frame, +1)
        blurred = cv2.GaussianBlur(frame, (11,11), 0)
        frameHSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        frameHSV = cv2.erode(frameHSV, kernal, iterations = 5)
        frameHSV = cv2.dilate(frameHSV, kernal, iterations = 5)
        cv2.imshow("hsv", frameHSV)
        colorMask0 = cv2.inRange(frameHSV, colorLower, colorUpper)
        colorMask1 = cv2.inRange(frameHSV, colorLower1, colorUpper1)
        colorMask = colorMask0 + colorMask1
        
        res = cv2.bitwise_and(frame, frame, mask = colorMask)
        cv2.imshow("Before",res)
        
        
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        cv2.imshow("After", res)
        
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        for i in contours:
            count += 1
            ((x,y), radius) = cv2.minEnclosingCircle(i)
            if radius < 20:
                continue
            M = cv2.moments(i)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        for i in range(len(drums)):
            timer = drums[i]
            point, radius, color, lineWidth = getDrum(i)
            cv2.circle(frame,point,radius,color,lineWidth)
            if timer == 0:
                isHit = checkDrum(res, i)
                if isHit == True and inDrums[i] == False:
                    drumStatus[i] = 1
                    cv2.circle(frame,point,radius,color,-1)
                    drums[i] = 5
                    inDrums[i] = True
                else:
                    inDrums[i] = False
        for i in range(len(drumStatus)):
            if drumStatus[i] == 1:
                playDrum(i)
                drumStatus[i] = 0
        cv2.imshow("Hello", res)
        cv2.imshow("Drum AR", frame)
        #if condition is met, break out of loop
        ch = cv2.waitKey(1)
        if ch & 0xFF == ord('q'):
            break
    cap.release
    cv2.destroyAllWindows()

main()
        
## Tkinter