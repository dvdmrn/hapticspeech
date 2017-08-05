from pylab import *
from scipy.io import wavfile
import matplotlib.pyplot as plt

sampFreq, snd = wavfile.read('../stimuli/phrases/PHRASE_imagination_male.wav')

CHUNK = 512


snd = snd/(2.**15) # convert to floating point from -1 to 1
				   # because 16 bit ranges from -2^15:2^15

numOfSamples = snd.shape[0] # .shape gives us

# time array is a series of time points
timeArray = arange(0,numOfSamples,1) # an array of the length of the num of samples
timeArray = timeArray/float(sampFreq) # normalizes time array as ratio of our sample freq
timeArray = timeArray*1000 # scale to milliseconds

# ========================================


def fftAnalyze(data,chunkSize):
	n = len(snd[:CHUNK])
	p = fft(snd[:CHUNK]) # number of points 

	nUniquePoints = int(ceil((n+1)/2.0)) 
	p = p[0:nUniquePoints] 
	p = abs(p)

	p = p/float(n) # scaling my num of points 
	p = p**2

	# for Nyquist point {in/ex}clusion
	if n%2 > 0: # odd num. of points
		p[1:len(p)] = p[1:len(p)] * 2
	else: # even num. of points
		p[1:len(p)-1] = p[1:len(p)-1] * 2

	freqArray = arange(0, nUniquePoints, 1.0) * (sampFreq / n)

plotLoop()

clf()
plot(array(freqArray/1000), 10*log10(p), color='k') 
# log10(p) because dB
# freqArray/1000 converts to kHz
xlabel('Frequency (kHz)')
ylabel('Power (dB)')















show()
