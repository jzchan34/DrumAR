##

"""
Drum Sound Files Testing Script
Input Number For Drum Sound
1: Kick
2: Tom
3: Snare
4: Rack Tom
5: Closed Hat
6: Crash
7: Ride
8: Splash
9: Chinese Cymbal
"""

## 

import pyaudio
import wave
from array import array
from struct import pack
import os

##

#root folder for drum sounds
rootFile = "drumFiles"

##

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

#prompts input and tests drum
def playDrumRecord(rootFile):
    run=True
    while run==True:
        drum=input("What drum?-->")
        if drum=='1':
            #kick
            play(rootFile+"/kick.wav")
        elif drum=='2':
            #floor tom
            play(rootFile+"/tom.wav")
        elif drum=='3':
            #snare drum
            play(rootFile"/snare.wav")
        elif drum=='4':
            #hanging toms
            play(rootFile"/rack tom.wav")
        elif drum=='5':
            #hi-hat
            play(rootFile+"/closed hat.wav")
        elif drum=='6':
            #crash cymbal
            play(rootFile+"/crash.wav")
        elif drum=='7':
            #ride cymbal
            play(rootFile"/ride.wav")
        elif drum=='8':
            #splash cymbal
            play(rootFile"/splash.wav")
        elif drum=='9':
            #china cymbal
            play(rootFile+"/chinese.wav")
        else:
            run=False
    return run

playDrumRecord(rootFile)