import pyaudio
import wave
from struct import pack, unpack
from math import sin, pi, sqrt
import os
import parameters as p

def haptic_playback(filepath):
    """
        processes a wavfile so the left channel is sinewave output and right channel is raw wave data
        and then outputs to speakers
    """
    RATE=44100
    chunk = 1024

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
    i = 0

    for i in range(0, f.getnframes()):
    
        frameSample = f.readframes(1)
        # print len(frameSample)
        if len(frameSample):
            try:
                data = unpack('h',frameSample)
            except:
                print ("Unpacking error, may be from an invalid frameSample")
                print ("frame sample length: "+str(len(frameSample)))
                print ("frame sample string: "+frameSample)
            
        else:
            data = 0
        if data:
            amp = sqrt(data[0]**2)
            wvData+=pack('h', data[0])
            wvData+=pack('h', amp*sin(i*800.0/RATE)) #200Hz right
        else:
            break
    wv.writeframes(wvData)
    wv.close()

    print("processed file!")


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