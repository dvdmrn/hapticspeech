"""
	Voicing Filter
	Returns true or false if a segment is voiced.
	Voicing is determined on the basis of whether or not there is more power
	below 1kHz relative to above it.
"""
from pylab import *
from scipy.io import wavfile

sampFreq, snd = wavfile.read('stimuli/male/stops/120_bought_vs_m.wav')

THRESHOLD_CUTOFF = 2.5 #in kHz


snd = snd/(2.**15) # convert to floating point from -1 to 1
				   # because 16 bit ranges from -2^15:2^15

# ========================================

def fftAnalyze(data,chunkStart,chunkEnd):
	"""
		Returns a tuple (x,y) where
			x := frequency array
			y := sound samples (magnitude)
	"""
	# print chunkStart
	# print chunkEnd
	if chunkEnd > len(data):
		return ([0],[0])
	n = len(data[chunkStart:chunkEnd])
	p = fft(data[chunkStart:chunkEnd]) # number of points 

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

	return (freqArray,p)



def processWaveChunk(data,size):
	"""
		data : an array?
		size : an int
	"""
	theTuple = fftAnalyze(data,0,len(data))
	freqArray = theTuple[0]
	p = theTuple[1]
	p = [cleanZeroes(v) for v in p]
	clf()
	
	cat = thresholdCategorization(p,freqArray,THRESHOLD_CUTOFF)
	return cat

	# ---- legacy ----
	# chunksSoFar = 0
	# while(chunksSoFar<len(snd)):
	# 	theTuple = fftAnalyze(snd,chunksSoFar,CHUNK)
	# 	freqArray = theTuple[0]
	# 	p = theTuple[1]
	# 	clf()
		
	# 	thresholdCategorization(p,freqArray,1) # <1kHz
	# 	#  -- plotting --
	# 	# plot(array(freqArray/1000), 10*log10(p), color='k')
	# 	# # log10(p) because dB
	# 	# # freqArray/1000 converts to kHz
	# 	# xlabel('Frequency (kHz)')
	# 	# ylabel('Power (dB)')
	# 	# show()
	# 	chunksSoFar += CHUNK


# def sumBuckets(magnitudes, frequencies, subsampleWidth, subsampleDifference):
# 	"""
# 	magnitudes: an array
# 	frequencies: an array
# 	subsampleWidth: number of magnitudes to sample
# 	subsampleDifference: difference between current sample and next
# 	"""
# 	i = 0
# 	means = []
# 	while i < len(magnitudes):		
# 		means.append(mean(magnitudes[i:i+subsampleWidth]))
# 		i += subsampleDifference
# 	return means

def thresholdCategorization(magnitudes, frequencies, threshold):
	if(len(magnitudes) > 1): # ensure a valid list of magnitudes
		logMagnitudes = 10*log10(magnitudes)
		# print frequencies
		HzArray = map(lambda x: x/float(1000), frequencies)
		# print HzArray
		dataTupledList = []
		for i in xrange(0,len(magnitudes)-1):
			dataTupledList.append((HzArray[i],logMagnitudes[i]))
		dataTupled = array(dataTupledList)
		return aveDiff(dataTupled,threshold)
		# dataTupled = array([(HzArray[i],frequencies[i]) for i in xrange(0,len(magnitudes)-1)])	
		# print dataTupled


def aveDiff(inputSequence, threshold):
	"""
	the relative difference between everything
	below the threshold, vs everything beyond.
	Returns true when everything there is a large difference between
	the two values. The difference is set at 15 and was determined
	through trial and error.

	Why just a 'large difference' and not verifying if - or + (thereby
	knowing if everything below the threshold is larger or not?)
	Noise above the threshold seems to 
	"""
	# take average of everything < threshold
	# take average of everything > threshold
	# if < threshold ave is larger, return true

	withinThreshold = []
	beyondThreshold = []

	for e in inputSequence:
		# e[0] := frequency
		# e[1] := magnitude
		if e[0] < threshold:
			withinThreshold.append(e[1])
		else:
			beyondThreshold.append(e[1])
	
	thresholdMean = mean(withinThreshold)
	beyondMean =  mean(beyondThreshold)
	difference = thresholdMean - beyondMean
	

	# print ("difference: ",difference,"threshold: ",thresholdMean, "beyond: ",beyondMean)

	if(difference > 17): 
		# print ("difference:",difference," | thresholdMean: ",thresholdMean," | beyondMean: ",beyondMean," [+V]")
		return True
		# print ("threshold mean: ",thresholdMean)
		# print ("beyond mean: ",beyondMean)
	else:
		# print ("difference:",difference," | thresholdMean: ",thresholdMean," | beyondMean: ",beyondMean)
		return False
		# print ("threshold mean: ",thresholdMean)
		# print ("beyond mean: ",beyondMean)


def cleanZeroes(n):
	if n < 1:
		return 1
	else:
		return n