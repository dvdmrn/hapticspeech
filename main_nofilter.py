"""
    use the -w flag for windowed mode
"""

import pygame
import time
import pyaudio
import wave
import sys
import textdisplay as txt
import utilities as util
import parameters as p
import record
import playback_nofilter

# init pygame
ID = str(input("Participant ID: "))
pygame.init()

# typefaces ------------\
titleText = pygame.font.Font('freesansbold.ttf',40)
bodyText = pygame.font.Font('freesansbold.ttf', 32)
# ----------------------/


# state control --------\
drawn = False
recording = False
endoftrial = False
# ----------------------/

phrases = util.get_wavfiles("stimuli/phrases/")
words = util.get_wavfiles("stimuli/words/")
file_index = 0


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
    complete = False
    exitWindow = False
    while not complete:

        if not drawn:
            screenDisplay.fill(p.GREY)
            txt.textLine(screenDisplay, welcomeTitle,"top", titleText)
            txt.textWrap(screenDisplay, welcomeDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.BLACK, p.GREY, 1) 

            drawn = True

        if exitWindow:
            pygame.quit()
            quit()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT: 
                exitWindow = True

            # KEYDOWN events ---------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape pressed!")
                    exitWindow = True
                
                # record
                if event.key == pygame.K_RETURN:
                    complete = True

            pygame.display.update()  
            clock.tick(60)
    drawn = False

# ----------------------------------------------
#  Stimulus Play Screen
# ----------------------------------------------    
def playbackScreen(file_index,files,path):
    """
    Renders the screen for signal playback
    @param file_index: an int
    """

    global drawn


    if not drawn:
        num_of_files = len(files)
            
        print("file index: "+str(file_index))
        print("wave file: "+str(files[file_index]))
        print("files: "+str(files))

        screenDisplay.fill(p.GREY)
        pygame.display.update()
        filepath = util.constructPath(path,files[file_index])
        playback_nofilter.haptic_playback(filepath)
        drawn = True
    

# ----------------------------------------------
#  Recording  Screen
# ----------------------------------------------
def recordScreen(file_index,files):
    """
    draws main record screen for a given file_index
    file_index : an int
    """

    global drawn
    global ID
    endoftrial = False
    complete = False
    exitWindow = False
    recordDescriptor="Now you will record yourself saying what you have just heard!\nYou are allowed to make as many recordings as you like. We will only use the last recording.\nWhen you are ready to begin press and hold the SPACE bar.\nWhen you are satisfied with your recording press ENTER to continue with the rest of the study."

    # event loop -- 
    """
        SPACE: record
        ESC: quit
        RETURN: next
    """
    while not complete:
        if not drawn:
            screenDisplay.fill(p.GREY)
            txt.textWrap(screenDisplay, recordDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.BLACK, p.GREY, 1) 
            pygame.display.update()
            drawn = True

        if exitWindow:
            pygame.quit()
            quit()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT: 
                exitWindow = True

            # KEYDOWN events ---------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape pressed!")
                    exitWindow = True
                
                # record
                if event.key == pygame.K_SPACE:
                    if not record.recording:
                        record.rec(screenDisplay,bodyText, files[file_index], ID)
                        drawn = False
                        endoftrial = True
                
                # move on 
                if event.key == pygame.K_RETURN:
                    if endoftrial: 
                        print "end of trial clause"
                        complete = True

            pygame.display.update()  
            clock.tick(60)

    drawn = False



def breakScreen():

    global drawn
    exitWindow = False
    complete = False
    breakDescriptor = "Take a break!\nPress C to continue the rest of the study."

    
    # event loop -- 
    """
    Press C to continue
    Press esc to quit
    """
    while not complete:

        if not drawn:
            screenDisplay.fill(p.GREY)
            # render thing here
            txt.textWrap(screenDisplay, breakDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.BLACK, p.GREY, 1) 

            pygame.display.update()
            drawn = True

        if exitWindow:
            pygame.quit()
            quit()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT: 
                exitWindow = True

            # KEYDOWN events ---------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape pressed!")
                    exitWindow = True
                
                # record
                if event.key == pygame.K_c:
                    complete = True

            pygame.display.update()  
            clock.tick(60)
    drawn = False



def trial(file_index,files,path):

    global drawn 
    global endoftrial
    playbackScreen(file_index,files,path)
    drawn = False
    recordScreen(file_index,files)
    drawn = False


def experimentCtrlFlow():

    """
    Main experiment control flow.
    The number of trials is based off how many stimuli are contained
    in `stimuli/words/` and `stimuli/phrases/`.
    Counterbalancing is conducted based off the participant ID.
    If the participant ID is even then we go phrases->words. If it is
    odd then we go words->phrases.
    """

    global file_index

    welcomeScreen()

    # if participant ID is even then go phrases->words
    # else go words->phrases
    if (int(ID)%2==0):
        print  "phrases->words"
        # phrases --
        for file in xrange(0,len(phrases)-1):
            trial(file_index,phrases,p.phrasepath)
            file_index+=1
        breakScreen()
        file_index=0
        # words --
        for file in xrange(1,len(words)-1):
            trial(file_index,words,p.wordpath)
            file_index+=1
    else: 
        # words --
        print  "words->phrases"
        for file in xrange(1,len(words)-1):
            trial(file_index,words,p.wordpath)
            file_index+=1
        breakScreen()
        file_index=0
        # phrases --
        for file in xrange(0,len(phrases)-1):
            trial(file_index,phrases,p.phrasepath)
            file_index+=1


def main():
    setup()
    pygame.init()
    experimentCtrlFlow()


# main()
experimentCtrlFlow()
pygame.quit()
quit()
