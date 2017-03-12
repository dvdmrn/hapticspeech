import math
import pyaudio

#sudo apt-get install python-pyaudio

PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
bitrate = 16000 #number of frames per second/frameset.      

freq = 500 #Hz, waves per second, 261.63=C4-note.
length = 1 #seconds to play sound

amplitude = 1	# must be between 0-1

if freq > bitrate:
    bitrate = freq+100

numberofframes = int(bitrate * length)
restframes = numberofframes % bitrate
wavedata = ''    

# --------------------------------------------------------
#  This is where the RMS analysis stuff should go \/
#---------------------------------------------------------
for x in xrange(numberofframes):
 print x
 wavedata = wavedata+chr(int(amplitude*math.sin(x/((bitrate/freq)/math.pi))*127+128))
     

for x in xrange(restframes): 
 wavedata = wavedata+chr(128)
 

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = bitrate, 
                output = True)

stream.write(wavedata)
stream.stop_stream()
stream.close()
p.terminate()