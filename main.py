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
import playback
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

wavfiles = util.get_wavfiles()



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
def playbackScreen():
    global drawn

    if not drawn:
        # gameExit = False
        num_of_files = len(wavfiles)
        file_index = 0
        print("file index: "+str(file_index))
        print("wave file: "+str(wavfiles[file_index]))
        print("files: "+str(wavfiles))

        screenDisplay.fill(p.GREY)
        pygame.display.update()
        filepath = util.constructPath(p.wavpath,wavfiles[file_index])
        playback.play_wavfile(filepath)
        drawn = True


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


                

        playbackScreen()
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