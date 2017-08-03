from pylab import *
from scipy.io import wavfile

sampFreq, snd = wavfile.read('../stimuli/phrases/PHRASE_imagination_male.wav')

snd = snd/(2.**15)

numOfSamples = snd.shape[0]

timeArray = arange(0,numOfSamples,1)
timeArray = timeArray/float(sampFreq)
timeArray = timeArray*1000 # scale to milliseconds

# plot(timeArray, snd, color='k')
# ylabel('Amplitude')
# xlabel('Time (ms)')
# show()

n = len(snd)
p = fft(snd)

nUniquePoints = int(ceil((n+1)/2.0))
p = p[0:nUniquePoints]
p = abs(p)

p = p/float(n) # scaling my num of points 
p = p**2

if n%2 > 0: # odd num. of points
	p[1:len(p)] = p[1:len(p)] * 2
else: # even num. of points
	p[1:len(p)-1] = p[1:len(p)-1] * 2

freqArray = arange(0, nUniquePoints, 1.0) * (sampFreq / n)

plot(freqArray/1000, 10*log10(p), color='k') # log10(p) because dB
xlabel('Frequency (kHz)')
ylabel('Power (dB)')
show()
