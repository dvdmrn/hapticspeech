from struct import pack, unpack
from math import sin, pi
import wave
import random
import pyaudio  
import math

RATE=44100
chunk = 1024

filepath = r"PHRASE_dramatist_female_edited.wav"

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

f = wave.open(filepath,"rb")  
print "opening: "+filepath
print "samplerate: "+str(f.getframerate())
print "frames: "+str(f.getnframes())
print "channels: "+str(f.getnchannels())
print "sample width: "+str(f.getsampwidth())


## GENERATE STEREO FILE ##
wv = wave.open('temp.wav', 'w')
wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
maxVol=2**14-1.0 #maximum amplitude
wvData=""
i = 0
tick = True

for i in range(0, f.getnframes()):
	if tick:
		tick = not tick
		frameSample = f.readframes(1)
		if len(frameSample):
			data = unpack('h',f.readframes(1))
		else:
			data = 0
		if data:
			amp = math.sqrt(data[0]**2)
			wvData+=pack('h', data[0])
			wvData+=pack('h', amp*sin(i*800.0/RATE)) #200Hz right
		else:
			break
	else:
		tick = not tick
		
		# print data 
		if data:
			# print "sinewave: "+str(maxVol*sin(i*400.0/RATE))
			wvData+=pack('h', data[0])
			wvData+=pack('h', amp*sin(i*800.0/RATE)) #200Hz right
		else:
			break

# wv.setframerate(f.getframerate())
wv.writeframes(wvData)
wv.close()

print "processed file!"


# --------------------------------------------------------
# playback processed audio
# --------------------------------------------------------

#open a wav format music  
f = wave.open(r"temp.wav","rb")  
#instantiate PyAudio  
p = pyaudio.PyAudio()  
#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()), 
                channels = 2,  
                rate = f.getframerate(),  
                output = True)  
#read data  
data = f.readframes(chunk)

print "playback initialized!"

while data:
    stream.write(data)
    data = f.readframes(chunk)

#stop stream  
stream.stop_stream()  
stream.close()  

print "playback ended."
#close PyAudio  
p.terminate()  