import math
import pyaudio

#sudo apt-get install python-pyaudio

PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 16000 #number of frames per second/frameset.      

FREQUENCY = 500 #Hz, waves per second, 261.63=C4-note.
LENGTH = 1 #seconds to play sound

amplitude = 1	# must be between 0-1

if FREQUENCY > BITRATE:
    BITRATE = FREQUENCY+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''    

# --------------------------------------------------------
#  This is where the RMS analysis stuff should go \/
#---------------------------------------------------------
for x in xrange(NUMBEROFFRAMES):
 WAVEDATA = WAVEDATA+chr(int(amplitude*math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))
     

for x in xrange(RESTFRAMES): 
 WAVEDATA = WAVEDATA+chr(128)
 

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)

stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()