#!usr/bin/env python  
#coding=utf-8  

import pyaudio  
import wave  
import struct
import math
from struct import pack
from math import sin, pi
# ----------------------------------------------
# settings for sine wave
# ----------------------------------------------

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
bitrate = 16000 #number of frames per second/frameset.      

freq = 500 #Hz, waves per second, 261.63=C4-note.
length = 1 #seconds to play sound

amplitude = 1   # must be between 0-1

frameNum = 0

if freq > bitrate:
    bitrate = freq+100

numberofframes = int(bitrate * length)
restframes = numberofframes % bitrate
wavedata = ''

rmsVals = []


# for x in xrange(numberofframes):
#  wavedata = wavedata+chr(int(amplitude*math.sin(x/((bitrate/freq)/math.pi))*127+128))
     

# for x in xrange(restframes): 
#  wavedata = wavedata+chr(128)    


# ----------------------------------------------
# load and read wav file
# ----------------------------------------------

#define stream chunk   
chunk = 1024  

#open a wav format music  
f = wave.open(r"PHRASE_dramatist_female_edited.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()  
#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = 1,  
                rate = f.getframerate(),  
                output = True)  
#read data  
data = f.readframes(chunk)

def rmsAnalysis( data ):
    if len(data)<1:
        return 0
    else:
        count = len(data)/2
        # if count < 1:
        #   count = 2048
        
        format = "%dh"%(count)
        shorts = struct.unpack( format, data )
        sum_squares = 0.0
        for sample in shorts:
            n = sample*(1.0/len(data))
            sum_squares += n*n
        return math.sqrt( sum_squares / count )
# maps a value between leftMin-leftMax => rightMin-rightMax
# e.g. 0-1 => 1-100
def mapRange(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

#load up rmsVals
while data:
    data = f.readframes(chunk)
    rmsVals.append(rmsAnalysis(data))
    # stream.write(data)


# reopen wav  
f = wave.open(r"PHRASE_dramatist_female_edited.wav","rb")  
data = f.readframes(chunk)

print "yo"

# wv = wave.open('PHRASE_dramatist_female_edited.wav', 'w')
# wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
# maxVol=2**15-1.0 #maximum amplitude
i = 0
while data:
    wvData=""
    i += 1
    maxVol=2**15-1.0 #maximum amplitude
    wvData+=f.readframes(chunk) # left
    # print sample
    wvData+=pack('h', maxVol*sin(i*200.0/f.getframerate())) #200Hz right
    stream.write(wvData)


# # print rmsVals
# while data:
#     print "in second while"  
#     data = f.readframes(chunk)
#     stream.write(data)
    # print "data: "+str(map(ord,data))+"\n----------------------------------"
    # print(rmsAnalysis(data))
    


#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  