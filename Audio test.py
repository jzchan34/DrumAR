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


play("./musicradar-drum-samples"+os.sep+"CYCdh_K1close_ClHat-01.wav")