##

"""
Augmented Reality Drumset Main Script
"""

## Imports

import cv2
import numpy as np
import time
import pyaudio
import wave
from array import array
from struct import pack
import os
import threading

##

DRUMSOUNDSFOLDER = "drumFiles"

## Playing Drum Sounds

#threads the play function
def drumThreadCreator(file):
    drumThread = threading.Thread(target = play, args = (file,))
    drumThread.start()

#plays the sound of given .wav file
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

#plays drum given specified drum sound index
def playDrum(i):
    global DRUMSOUNDSFOLDER
    if i == 0:
        drumThreadCreator(DRUMSOUNDSFOLDER+"/snare.wav")
    elif i == 1:
        drumThreadCreator(DRUMSOUNDSFOLDER+"/rack tom.wav")
    elif i == 2:
        drumThreadCreator(DRUMSOUNDSFOLDER+"/tom.wav")
    elif i == 3:
        drumThreadCreator(DRUMSOUNDSFOLDER+"/kick.wav")
    elif i == 4:
        drumThreadCreator(DRUMSOUNDSFOLDER+"/closed hat.wav")

## 

#returns the drum shape and location on screen
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
    drumParas = [cir1,cir2,cir3,cir4,cir5]
    return drumParas[i]
    
#check if drumstick is detected in any drums
def checkDrum(res, k):
    threshold = (10,10,10)
    point, radius, _, _ = getDrum(k)
    counter = False
    for line in range(point[1] - radius//2, point[1] + (radius*2//3), 20):
        for char in range(point[0] - radius//2, point[0] + radius//2, 20):
            for i in range(3):
                if res[line][char][i] >= threshold[i]:
                    counter = True
                    return counter

#gives color range to be detected
def getColorRange():
    #range of color
    #Current Color: Red
    colorLower1 = np.array([0, 120, 70], np.uint8)
    colorUpper1 = np.array([10, 255, 255], np.uint8)
    colorLower2 = np.array([170, 120, 70], np.uint8)
    colorUpper2 = np.array([180, 255, 255], np.uint8)
    return colorLower1, colorUpper1, colorLower2, colorUpper2

#apply filters and mask on frame for contouring
def filterFrame(frame):
    
    #apply blur
    kernel = np.ones((5,5), 'uint8')
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    blurred = cv2.erode(blurred, kernel, iterations = 5)
    blurred = cv2.dilate(blurred, kernel, iterations = 5)
    
    #apply mask on hsv image
    cLow1, cUp1, cLow2, cUp2 = getColorRange()
    frameHSV = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    colorMask1 = cv2.inRange(frameHSV, cLow1, cUp1)
    colorMask2 = cv2.inRange(frameHSV, cLow2, cUp2)
    colorMask = colorMask1 + colorMask2
    res = cv2.bitwise_and(frame, frame, mask = colorMask)
    
    #grayscale and return
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    
    return gray, res

#resize and mirror frames for more natural drum experience
def rescaleFrame(frame):
    frame = cv2.resize(frame, (0,0), fx = 1, fy = 1)
    frame = cv2.flip(frame, +1)
    return frame

#finds contours around the filtered frame
def contourFilteredFrame(frame):
    thresh = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

#draws a circle with a dot for detected objects
def drawContours(contours):
    minRad = 30
    maxContours = 10
    contourList = []
    count = 0
    for contour in contours:
        count += 1
        ((x,y), radius) = cv2.minEnclosingCircle(contour)
        #remove contours that are too small
        if radius < minRad:
            continue
        #get center point
        M = cv2.moments(contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        contourList.append((x,y,radius,center))
        if count > maxContours:
            break
    return contourList

#Reduce Timer Count By 1
def timerLoopCount(drums):
    for i in range(len(drums)):
        if drums[i] > 0:
            drums[i] -= 1
    return drums
## Main

#main run function for program
def main():
    #parameters
    drumNum = 5
    
    drums = [0] * drumNum
    inDrums = [False] * drumNum
    #set up video
    cap = cv2.VideoCapture(0)
    #buffer to load video
    time.sleep(2.0)
    #main cv2 video loop
    while(True):
        #read frames
        _, frame = cap.read()
        frame = rescaleFrame(frame)
        filteredFrame, res = filterFrame(frame)
        contours = contourFilteredFrame(filteredFrame)
        contourList = drawContours(contours)
        for x,y,radius,center in contourList:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        # Reduce timer count by 1
        drums = timerLoopCount(drums)
        
        #loops through all drums
        for i in range(drumNum):
            #draws drum
            point, radius, color, lineWidth = getDrum(i)
            cv2.circle(frame,point,radius,color,lineWidth)
            #when drum has finished its timer period
            timer = drums[i]
            if timer == 0:
                #check if drum is hit
                isHit = checkDrum(res, i)
                if isHit == True and inDrums[i] == False:
                    playDrum(i)
                    cv2.circle(frame,point,radius,color,-1)
                    #reset timer to 5 loops
                    drums[i] = 5
                    inDrums[i] = True
                else:
                    inDrums[i] = False
        
        cv2.imshow("Drum AR", frame)
        
        #if condition is met, break out of loop
        ch = cv2.waitKey(1)
        if ch & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

main()