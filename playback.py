"""
    VoicingRMS playback
    Takes a wavefile and constructs a new wavefile and plays it such that:
        - The right channel is the content of the original wavefile
        - The left channel is a sinewave, where:
            - if at a given time the source wavefile is -voice, 
              the sinewave's amplitude is 0 
            - if at a given time the source wavefile is +voice,
              the sinewave's amplitude is coupled to the RMS amplitude of 
              the source wavefile. 
"""

# 2018/07/09 TODO:
# deal with positive/negative offsets 



import pyaudio
import wave
from struct import pack, unpack
from math import sin, pi, sqrt, floor
import os
import parameters as p
import voicingfilter
from pygame import mixer 
import time
import pprint
import array
import numpy as np

SHORT_MAX = 32767
GAIN = 2
AMP_THRESHOLD = 0

pp = pprint.PrettyPrinter()
def rms_playback(filepath, offset):
    
    """
        processes a wavfile so the left channel is sinewave output and right channel is raw wave data
        and then outputs to speakers.
        The sinewave amplitude = source amplitude, and only is present if the source file is +voice

        TODO: packs the voice file fine but not the sinewave. Why is this?
        Maybe instead of iterating in chunks try iterating continuously like before but just keep track
        when samplesSoFar%chunk = 0 so we know to restart our amp analysis

    """
    RATE= 44100
    chunk = 1024 # previously 512
    secondsoffset = sqrt((float(offset) /1000)**2)
    samplesoffset = int( floor(secondsoffset * RATE))  
    insertZeros = [0]* samplesoffset

    f = wave.open(filepath,"rb")  
    print("\n  opening: "+filepath)
    print("  samplerate: "+str(f.getframerate()))
    print("  frames: "+str(f.getnframes()))
    print("  channels: "+str(f.getnchannels()))
    print("  sample width: "+str(f.getsampwidth()))

    ## GENERATE STEREO FILE ##
    wv = wave.open('temp.wav', 'w')
    wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
    maxVol=2**14-1.0 #maximum amplitude
    wvData=""
    lData = [] # source wav
    rData = [] # sine wave
    ampData = []
    amp = 0
    i = 0
    t = 0
     
    



    for i in range(0, f.getnframes()):
        # populate lData with f sample data

        

        if (i%chunk == 0):
            # get amplitude data -----------
            # for every 512 samples of 
            startChunk = i
            endChunk = i+chunk
            for s in range(0,chunk):
                try:
                    frameSample = f.readframes(1)     
                    shortSample = unpack('h',frameSample)
                    lData.append(shortSample[0])
                except:
                    lData.append(0)

            try:
                subsamples = lData[startChunk:endChunk]
            except:
                # out of index range, so we are at the end
                subsamples = lData[startChunk:len(f.getnframes()-1)]
            print("amp data: ",RMS(subsamples))
            voiced = voicingfilter.processWaveChunk(subsamples,chunk)

            # amp = RMS(subsamples)

            if voiced > 0.25:
                amp = RMS(subsamples)
            else:
                amp = 0 
        ampData.append(amp)
            # print("amp: ",amp)

            # for sampleIndex in range(0,chunk):
            #     # write sine wave
            #     rData.append()
            #     t += 1

    print ("ampData len: ",len(ampData),"lData len",len(lData))

    sinewaveDataArray = np.zeros(len(ampData) + samplesoffset) 

    print "writing sine wave" 
    for k in xrange(0,len(ampData)):
        
        sine = GAIN*ampData[k]*sin(t*2*pi*(180.0/RATE))
        if sine < 0:
            sine = max(sine,(SHORT_MAX-1)*-1)
        if sine > 0:
            sine = min(sine,(SHORT_MAX-1))
        t += 1
        
        if offset > 0: #positive offset
            sinewaveDataArray [samplesoffset + k] = sine 
        else: #negative offset 
            sinewaveDataArray [k] = sine 



    print "adjust ampData/lData with 0 padding"
    
    if offset < 0: #negative offset 
        print "neg offset : appending 0 to front"
        ampDataArray = np.zeros([samplesoffset + len(ampData)])
        lDataArray = np.zeros([samplesoffset + len(lData)])

        for i in xrange (0,len(ampData)):
            ampDataArray [i + samplesoffset] = ampData [i] 
            # copying array but with the length of the offset 
            lDataArray [i + samplesoffset] = lData [i] 


        ampData = ampDataArray #abstraction 
        lData = lDataArray 

    else: #positive offset 
        # print "pos offset : appending 0 to back"
        for sample in  xrange(0,samplesoffset):    
            lData.append (0)
            ampData.append (0) 


        


    print ("ampData len2: ",len(ampData),"lData len2",len(lData))


    
    

       # sinewaveDataArray = np.append (sinewaveDataArray, sine)



    #print "inserting 0 to sinewaveData"    
    #   for i in xrange(0, samplesoffset): 
    #   sinewaveDataArray [i] = 0
    # sinewaveDataArray = np.insert (sinewaveDataArray,0,np.zeros(samplesoffset))
   
    print "sinewaveDataArray length :" + str(len(sinewaveDataArray))
    print "lData length :" + str(len(lData))
    print "ampData length :"+  str(len(ampData))
   # assert len(sinewaveDataArray) == len(lData) == len(ampData)


    print "packing sinewaveData"
    for s in xrange(0,len(sinewaveDataArray)):
        # -- write source wav file in left channel
        wvData += pack('h', lData[s])
        # -- write sine wave in right channel
        wvData += pack('h', sinewaveDataArray[s]) #200Hz right
    


        
   
    wv.writeframes(wvData)
    wv.close()

    # --------------------------------------------------------
    # playback processed audio
    # --------------------------------------------------------

    playProcessedAudio()




def playProcessedAudio():
    stim = mixer.Sound('temp.wav')
    channel2 = mixer.Channel(2)
    channel2.set_volume(1.0, 1.0) # 1st arg = left; 2nd arg = right
    channel2.play(stim)
    time.sleep(stim.get_length())


def RMS(dataArray):
    sum = 0
    for d in dataArray:
        sum += d**2
    mean = sum/float(len(dataArray))
    return sqrt(mean)


def voicingRMS(dataArray, chunk):
    """
        returns rms if dataArray is +V
        returns 0 if dataArray is -V
    """
    segmentIndex = 0
    segmentMax = len(dataArray) / chunk + 1
    # for i in xrange(0,segmentMax):
    #     try:
    #         toAnalyze = dataArray[segmentIndex:chunk]
    #     except:
    #         toAnalyze = dataArray[segmentIndex:len(dataArray-1)]
    #         chunk = len(dataArray)
    #     voiced = voicingfilter.processWaveChunk(toAnalyze,chunk)
    voiced = voicingfilter.processWaveChunk(dataArray[0],1)

    if(voiced):
        return sqrt(toAnalyze**2)
    else:
        return 0
    # sum = 0.0
    # for v in dataArray:
    #     sum += v**2
    # mean = sum/len(dataArray)
    # return sqrt(mean)


def normal_playback(filepath):
    """
        plays the wavfile specified by filepath
    """
    #define stream chunk   
    chunk = 2048  

    #open a wav format music  
    f = wave.open(filepath,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()  