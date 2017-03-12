from struct import pack
from math import sin, pi
import wave
import random
import pyaudio
import math


RATE=44100
chunk = 1024

## GENERATE MONO FILE ##
# wv = wave.open('test_mono.wav', 'w')
# wv.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
# maxVol=2**15-1.0 #maximum amplitude
# wvData=""
# for i in range(0, RATE*3):
# 	wvData+=pack('h', maxVol*sin(i*500.0/RATE)) #500Hz
# wv.writeframes(wvData)
# wv.close()


f = wave.open(r"PHRASE_dramatist_female_edited.wav","rb")  
duration = f.getnframes() / float(f.getframerate())

# stats: 
print "\nnum frames: "+str(f.getnframes())+"\n"+str(f.getnchannels())+"\n"+str(f.getframerate())
print("duration: ",duration)
print("ceiling duration: ",int(math.ceil(duration)))


## GENERATE STEREO FILE ##
wv = wave.open('temp.wav', 'wb')
wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
maxVol=2**15-1.0 #maximum amplitude
wvData=""
for i in range(0, RATE*int(math.ceil(duration))):
	# wvData+=pack('h', maxVol*sin(i*500.0/RATE)) #500Hz left
	print f.readframes(f.getframerate())
	wvData+=f.readframes(f.getframerate())
	wvData+=pack('h', maxVol*sin(i*200.0/RATE)) #200Hz right
wv.writeframes(wvData)
wv.close()




# wv = wave.open(r'PHRASE_dramatist_female_edited.wav', 'rb')


# ----------- pyaudio ---------------

# p = pyaudio.PyAudio()  


# #open stream  
# stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
#                 channels = f.getnchannels(),  
#                 rate = f.getframerate(),  
#                 output = True)  

# data = wv.readframes(chunk)

# while data:
# 	stream.write(data)
# 	data = wv.readframes(chunk)

# # stop stream
# stream.stop_stream()
# stream.close()

# # close pyaudio
# p.terminate()

