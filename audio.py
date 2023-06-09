import os
import Levenshtein as lev
import threading

from sys import byteorder
import pyfiglet as pyg  
from array import array
from struct import pack

import pyaudio
import wave

welcome=pyg.figlet_format("Welcome to the Voice Assistant")
print(welcome)

THRESHOLD = 900
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')
    print("Recording...", r)
    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            # print("big")
            snd_data.byteswap()
        if snd_started:
            r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            # print(".")
            num_silent += 1
        elif not silent and not snd_started:
            print("Recording")
            snd_started = True

        if snd_started and num_silent > 30:
            # print("Finished recording")
            # snd_started = False
            # num_silent = 0
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)
    file=open("newText.txt", 'w')
    file.write(str(data))
    # file.close()
    # wf = wave.open(path, 'wb')
    # wf.setnchannels(1)
    # wf.setsampwidth(sample_width)
    # wf.setframerate(RATE)
    # wf.writeframes(data)
    # wf.close()
    return data




isMatched=False

def audioMatch(file1, file2):
    global isMatched


    file=open(f'Dataset\my Data\{file1}','rb')
    a=str(file.read())


    b=str(file2)



    Ratio = lev.ratio(b.lower(), a.lower())
    # print(Ratio)


    if Ratio>=0.8:
        isMatched=True
        return True

def audioTest(data):
    print("start audioTest")
    for root, dirs, files in os.walk("Dataset\my Data"):
        for filename in files:
            # print(filename)
            if audioMatch(filename,data):
                if isMatched!=True:
                    break
    if isMatched:
        print("normal")
    else:
        print("Cheating Detected")

def checkVoice():
    print("start checkVoice")
    data=record_to_file("demo.wav")
    print("recorded")
    threadStart=threading.Thread(target=audioTest,args=(data,))
    newRecording=threading.Thread(target=checkVoice)
    threadStart.start()
    checkVoice()
    print("thread started")
    # newRecording.start()


checkVoice()