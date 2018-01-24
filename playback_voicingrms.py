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

# TODO: !!! 2017-11-28
    # writes a blank temp.wav file. I think it's because I unpack('h',...)
    # and then pack('h',...) but inbetween I strip it into an array so I 
    # may lose the short datatypeness of it all messing up the pack()

import pyaudio
import wave
from struct import pack, unpack
from math import sin, pi, sqrt
import os
import parameters as p
import voicingfilter

def haptic_playback(filepath):
    """
        processes a wavfile so the left channel is sinewave output and right channel is raw wave data
        and then outputs to speakers.
        The sinewave amplitude = source amplitude, and only is present if the source file is +voice

        TODO: packs the voice file fine but not the sinewave. Why is this?
        Maybe instead of iterating in chunks try iterating continuously like before but just keep track
        when samplesSoFar%chunk = 0 so we know to restart our amp analysis

    """
    print("in haptic_playback")
    RATE= 44100
    chunk = 512


    f = wave.open(filepath,"rb")  
    print("\n\nopening: "+filepath)
    print("samplerate: "+str(f.getframerate()))
    print("frames: "+str(f.getnframes()))
    print("channels: "+str(f.getnchannels()))
    print("sample width: "+str(f.getsampwidth()))

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

            voiced = voicingfilter.processWaveChunk(subsamples,chunk)

            amp = RMS(subsamples)

            if voiced:
                amp = RMS(subsamples)
                ampData.append(amp)
            else:
                amp = 0
        else:
            ampData.append(amp)
            # print("amp: ",amp)

            # for sampleIndex in range(0,chunk):
            #     # write sine wave
            #     rData.append()
            #     t += 1
            
    for k in xrange(0,len(ampData)):
        sine = ampData[k]*sin(t*2*pi*(180.0/RATE))
        # -- write source wav file in left channel
        wvData += pack('h', lData[k])
        # wvData += pack('h', sine) #200Hz right

        # -- write sine wave in right channel
        wvData += pack('h', sine) #200Hz right
        # print (lData[k],sine)
        t += 1
    # print("len data",len(lData),"len data / chunk", len(lData)/chunk)
   
    wv.writeframes(wvData)
    wv.close()




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

    print("playback initialized!")

    while data:
        stream.write(data)
        data = f.readframes(chunk)

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    print("playback ended.")
    #close PyAudio  
    p.terminate()  


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
    chunk = 1024  

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