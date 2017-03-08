#!usr/bin/env python  
#coding=utf-8  

import pyaudio  
import wave  
import struct
import math


# ----------------------------------------------
# settings for sine wave
# ----------------------------------------------

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
bitrate = 16000 #number of frames per second/frameset.      

freq = 500 #Hz, waves per second, 261.63=C4-note.
length = 1 #seconds to play sound

amplitude = 1	# must be between 0-1

frameNum = 0

if freq > bitrate:
    bitrate = freq+100

numberofframes = int(bitrate * length)
restframes = numberofframes % bitrate
wavedata = ''

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
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
#read data  
data = f.readframes(chunk)

def rms( data ):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
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

for frame in data:
	data = f.readframes(chunk)
	frameNum += 1
	rmsAmp = mapRange(rms(data), 0,0.01,0,1)
	print rmsAmp
	wavedata = wavedata+chr(int(rmsAmp*math.sin(1/((bitrate/freq)/math.pi))*127+128))

for x in xrange(restframes): 
 wavedata = wavedata+chr(128)    

#play stream  
while data:  
    # print mapRange(rms(data), 0,0.01,0,1)
    data = f.readframes(chunk)
    stream.write(data)

    stream.write(wavedata)
#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()  