from struct import pack, unpack
from math import sin, pi
import wave
import random
import pyaudio  

RATE=44100
chunk = 1024

## GENERATE MONO FILE ##
wv = wave.open('test_mono.wav', 'w')
wv.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
maxVol=2**15-1.0 #maximum amplitude
wvData=""



for i in range(0, RATE*3):
	wvData+=pack('h', maxVol*sin(i*500.0/RATE)) #500Hz
wv.writeframes(wvData)
wv.close()



def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

f = wave.open(r"PHRASE_dramatist_female_edited.wav","rb")  
data = f.readframes(chunk)
## GENERATE STEREO FILE ##
wv = wave.open('test_stereo.wav', 'w')
wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
maxVol=10 # maximum amplitude
wvData=""
i = 0

for i in range(0, f.getnframes()):
	frameSample = f.readframes(1)
	if len(frameSample):
		data = unpack('h',f.readframes(1))
	else:
		data = 0
	# print data 
	if data:
		# print "sinewave: "+str(maxVol*sin(i*400.0/RATE))
		wvData+=pack('h', data[0])
		wvData+=pack('h', maxVol*sin(i*400.0/RATE)) #200Hz right
	else:
		wvData+=pack('h', 0)
		wvData+=pack('h', maxVol*sin(i*400.0/RATE)) #200Hz right

print f.getframerate()
wv.setframerate(f.getframerate()/2)
wv.writeframes(wvData)
wv.close()