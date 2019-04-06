import pyaudio
import wave
from array import array
from struct import pack
import os

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


def playDrumRecord():
    run=True
    while run==True:
        drum=input("What drum?-->")
        if drum=='1':
            #kick
            play("Other/kick.wav")
        elif drum=='2':
            #floor tom
            play("Other/tom.wav")
        elif drum=='3':
            #snare drum
            play("Other/snare.wav")
        elif drum=='4':
            #hanging toms
            play("Other/rack tom.wav")
        elif drum=='5':
            #hi-hat
            play("Other/closed hat.wav")
        elif drum=='6':
            #crash cymbal
            play("Other/crash.wav")
        elif drum=='7':
            #ride cymbal
            play("Other/ride.wav")
        elif drum=='8':
            #splash cymbal
            play("Other/splash.wav")
        elif drum=='9':
            #china cymbal
            play("Other/chinese.wav")
        else:
            run=False
    return run

playDrumRecord()
'''
#create commands list
a=[]
for i in range(1, 10):
    a.append(str(i))

def createDrumRecord():
    #create drums record with human input
    drumsList=[]
    while True:
        drum=input("What drum do you want to play?-->")
        if drum=='s' or drum=='S':
            break
        elif drum in a:
            drumsList.append(drum)
    return drumsList

def playDrumRecord(lst):
    for i in lst:
        if i=='1':
            #kick
            play("Other/kick.wav")
        elif i=='2':
            #floor tom
            play("Other/tom.wav")
        elif i=='3':
            #snare drum
            play("Other/snare.wav")
        elif i=='4':
            #hanging toms
            play("Other/rack tom.wav")
        elif i=='5':
            #hi-hat
            play("Other/closed hat.wav")
        elif i=='6':
            #crash cymbal
            play("Other/crash.wav")
        elif i=='7':
            #ride cymbal
            play("Other/ride.wav")
        elif i=='8':
            #splash cymbal
            play("Other/splash.wav")
        elif i=='9':
            #china cymbal
            play("Other/chinese.wav")

def playDrums():
    drumsList=createDrumRecord()
    playDrumRecord(drumsList)
    return

playDrums()
'''