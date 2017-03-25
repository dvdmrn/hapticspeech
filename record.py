import pygame
import pyaudio
import wave
import utilities as util
import parameters as p
import textdisplay as txt


recording = False
stop = False

def stopRec():
    global stop
    stop = True

# ----------------------------------------------
#  Render Timer
#      - draws the timer bar
# ----------------------------------------------

def renderTimer(surface,i,maxLength,font):
    """
    maxLength: an int of the number of samples in our wave file
    i: current index of the wave file we are writing
    """
    currentIndex = int(util.translate(i, 0, maxLength, 0, p.recBarWidth)) +1
    
    # if recording length is maxed out exit
    if(maxLength-i <= 1):
        pygame.display.update()
        print "render complete"
        return
    # renders the timer bar
    else:
        pygame.draw.rect(surface,p.DARKGREY, pygame.Rect((p.screen_width-320,p.cornerPadding),(p.recBarWidth,p.recBarHeight)))
        pygame.draw.rect(surface,p.PINK, pygame.Rect((p.screen_width-320,p.cornerPadding),(p.recBarWidth-currentIndex,p.recBarHeight)))
        txt.textLine(surface,"recording!","custom", font,p.screen_width-(p.recBarWidth/2)-p.cornerPadding,p.recBarHeight+p.cornerPadding+30)

        pygame.display.update()

# ----------------------------------------------
#  Record
#      - handles wave recording
# ----------------------------------------------
def rec(surface,font):

    global recording, stop

    if not recording:
        # set recording to True at the beginning
        # insert recorder.py
        # render timer

        recording = True

        #start of wave recording---------------------------------------------------------------------------------------

        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 4

        currentFile = "PHRASE_"
        participantID = "1337"
        WAVE_OUTPUT_FILENAME = participantID+"_"+currentFile+"_RESPONSE.wav"
        savepath = "responses/"+participantID+"/"

         
        audio = pyaudio.PyAudio()
         
        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print "recording..."
        frames = []

        maxLength = int(RATE / CHUNK * RECORD_SECONDS)
        breakFor = False
        for i in range(0, maxLength):
            # key up to stop recording
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        breakFor = True
                        break
            # for some reason break doesn't work in that scope
            # so we defer the break function in the logic below
            # and I'm too lazy to make this prettier
            if breakFor:
                break
            data = stream.read(CHUNK)
            frames.append(data)
            renderTimer(surface, i, maxLength,font)
        print "finished recording"

         
        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
         
        waveFile = wave.open(savepath+WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        recording = False

        #end of wave recording-------------------------------------------------------------------------------------------