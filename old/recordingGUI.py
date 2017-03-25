"""
    use the -w flag for windowed mode
"""

import pygame
import time
# import textwrap
import pyaudio
import wave
import sys
import textdisplay as txt
import utilities as util
import parameters as p
import record

# init pygame
pygame.init()

# typefaces ------------\
titleText = pygame.font.Font('freesansbold.ttf',40)
bodyText = pygame.font.Font('freesansbold.ttf', 32)
# ----------------------/


# state control --------\
drawn = False
recording = False
# ----------------------/

# pygame setup ---------\

# accepts CL input `-w` for windowed mode
if (len(sys.argv)>1):
    if (sys.argv[1]=="-w"):
        screenDisplay= pygame.display.set_mode((p.screen_width,p.screen_height))
        pygame.display.set_caption( ' Haptic Speech Experiment ')
        clock = pygame.time.Clock()
        print "window mode"
else:
    screenDisplay= pygame.display.set_mode((p.screen_width,p.screen_height),pygame.FULLSCREEN )
    pygame.display.set_caption( ' Haptic Speech Experiment ')
    clock = pygame.time.Clock()
# ----------------------/

# ============================================================================================
# Functions
# ============================================================================================

# ----------------------------------------------
# Welcome Screen
# ----------------------------------------------

def  welcomeScreen():
    global drawn
    welcomeTitle= "Welcome to the Haptic Speech Experiment!"
    welcomeDescriptor= "During the experiment you will hear a series of words and phrases. Thereafter, you will be prompted to record yourself repeating what you've heard. Ocassionally you will feel a slight vibration.\n\nWhen you are ready to begin, press the ENTER/RETURN key to continue."


    if not drawn:
        screenDisplay.fill(p.GREY)
        txt.textLine(screenDisplay, welcomeTitle,"top", titleText)

        txt.textWrap(screenDisplay, welcomeDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.BLACK, p.GREY, 1) 

        drawn = True

# ----------------------------------------------
#  Stimulus Play Screen
# ----------------------------------------------    
def stimulusPlayScreen():
    # blank screen while stimuli plays
    # how move to next screen????
    return

# ----------------------------------------------
#  Recording  Screen
# ----------------------------------------------
def recordScreen():
    """
    draws main record screen
    """
    global drawn
    recordDescriptor="Now you will record yourself saying what you have just heard!\nYou are allowed to make as many recordings as you like.\nWhen you are ready to begin press and hold the SPACE bar."

    if not drawn:

        screenDisplay.fill(p.GREY)
        txt.textWrap(screenDisplay, recordDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.BLACK, p.GREY, 1) 

        drawn = True

# # ----------------------------------------------
# #  Render Timer
# #      - draws the timer bar
# # ----------------------------------------------

# def renderTimer(i,maxLength):
#     """
#     maxLength: an int of the number of samples in our wave file
#     i: current index of the wave file we are writing
#     """
#     currentIndex = int(util.translate(i, 0, maxLength, 0, p.recBarWidth)) +1
    
#     # if recording length is maxed out exit
#     if(maxLength-i <= 1):
#         pygame.display.update()
#         print "render complete"
#         return
#     # renders the timer bar
#     else:
#         pygame.draw.rect(screenDisplay,p.DARKGREY, pygame.Rect((p.screen_width-320,p.cornerPadding),(p.recBarWidth,p.recBarHeight)))
#         pygame.draw.rect(screenDisplay,p.PINK, pygame.Rect((p.screen_width-320,p.cornerPadding),(p.recBarWidth-currentIndex,p.recBarHeight)))
#         txt.textLine(screenDisplay,"recording!","custom", bodyText,p.screen_width-(p.recBarWidth/2)-p.cornerPadding,p.recBarHeight+p.cornerPadding+30)

#         pygame.display.update()

# # ----------------------------------------------
# #  Record
# #      - handles wave recording
# # ----------------------------------------------
# def record():

#     global recording 

#     if not recording:
#         # set recording to True at the beginning
#         # insert recorder.py
#         # render timer

#         recording = True

#         #start of wave recording---------------------------------------------------------------------------------------

#         FORMAT = pyaudio.paInt16
#         CHANNELS = 2
#         RATE = 44100
#         CHUNK = 1024
#         RECORD_SECONDS = 4

#         currentFile = "PHRASE_"
#         participantID = "1337"
#         WAVE_OUTPUT_FILENAME = participantID+"_"+currentFile+"_RESPONSE.wav"
#         savepath = "responses/"+participantID+"/"

         
#         audio = pyaudio.PyAudio()
         
#         # start Recording
#         stream = audio.open(format=FORMAT, channels=CHANNELS,
#                         rate=RATE, input=True,
#                         frames_per_buffer=CHUNK)
#         print "recording..."
#         frames = []

#         maxLength = int(RATE / CHUNK * RECORD_SECONDS)
#         for i in range(0, maxLength):
#             data = stream.read(CHUNK)
#             frames.append(data)
#             renderTimer(i, maxLength)
#         print "finished recording"
         
         
#         # stop Recording
#         stream.stop_stream()
#         stream.close()
#         audio.terminate()
         
#         waveFile = wave.open(savepath+WAVE_OUTPUT_FILENAME, 'wb')
#         waveFile.setnchannels(CHANNELS)
#         waveFile.setsampwidth(audio.get_sample_size(FORMAT))
#         waveFile.setframerate(RATE)
#         waveFile.writeframes(b''.join(frames))
#         waveFile.close()

#         #end of wave recording-------------------------------------------------------------------------------------------

def main_loop() :
    global drawn
    # event handling loop
    exitWindow = False  


    while not exitWindow:

        for event in pygame.event.get() :
            if event.type == pygame.QUIT: 
                exitWindow = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("right key pressed!")
                    exitWindow = True
                
                if event.key == pygame.K_SPACE:
                    if not record.recording:
                        record.rec(screenDisplay,bodyText)
                        drawn = False
                    print "space bar pressed!"
            # if event.type == pygame.KEYUP:
            #         if event.key == pygame.K_SPACE:
            #             record.stopRec()
            #             print "key up event!"


                

        recordScreen()


        
        pygame.display.update()  
        
        clock.tick(60)
        

    pygame.quit()
    quit()


main_loop()
print("exited game loop")
pygame.quit()
print("called pygame quit")
quit()
print("should've quit by now")