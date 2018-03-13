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
import playback_voicingrms as playback
import pygame_textinput
import csv
import os
import re

# init pygame
ID = str(input("Participant ID: "))
participantResponseRootFilePath = ("responses/"+ID)

if not os.path.exists(participantResponseRootFilePath):
    os.makedirs(participantResponseRootFilePath)

pygame.init()


# typefaces ------------\
titleText = pygame.font.Font('UbuntuMono-R.ttf',40)
bodyText = pygame.font.Font('UbuntuMono-R.ttf', 32)
answerText = pygame.font.Font('UbuntuMono-R.ttf', 60)

# inputFont = pygame.font.Font('UbuntuMono-R', 32)
# ----------------------/


# state control --------\
drawn = False
recording = False
endoftrial = False
# ----------------------/

phrases = util.get_wavfiles("stimuli/phrases/")
words = util.get_wavfiles("stimuli/words/")
minpairs = util.get_minpairs("stimuli/minpairs/")
minPairMap = [] # will be populated with minpair IDs and tokens

file_index = 0

# a hack ---------------\
# look the other way
currentFilePath = ""
currentCsvPath = ""
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

# setup input text
textinput = pygame_textinput.TextInput("UbuntuMono-R.ttf",30)
textinput.set_text_color(p.PINK)
textinput.set_cursor_color(p.PINK)

# ============================================================================================
# Functions
# ============================================================================================

# ----------------------------------------------
# Welcome Screen
# ----------------------------------------------

def  welcomeScreen():
    global drawn
    welcomeTitle= "Welcome to the Haptic Speech Experiment!"
    welcomeDescriptor= "During the experiment you will hear a series of words and phrases. Thereafter, you will be prompted to write what you've heard.You will feel slight vibrations.\n\nWhen you are ready to begin, press the ENTER/RETURN key to continue."
    complete = False
    exitWindow = False
    while not complete:

        if not drawn:
            screenDisplay.fill(p.BG)
            txt.textLine(screenDisplay, welcomeTitle,"top", titleText, p.PINK)
            txt.textWrap(screenDisplay, welcomeDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.OFFWHITE, p.BG, 1) 

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
    global currentFilePath


    if not drawn:
        num_of_files = len(files)
            
        print("file index: "+str(file_index))
        print("wave file: "+str(files[file_index]))
        # print("files: "+str(files))

        screenDisplay.fill(p.BG)
        pygame.display.update()
        currentFilePath = util.constructPath(path,files[file_index])
        print("calling haptic_playback")
        playback.haptic_playback(currentFilePath)
        drawn = True
    

# ----------------------------------------------
#  Recording  Screen
# ----------------------------------------------
def recordScreen(file_index,files,path):
    """
    draws main record screen for a given file_index
    file_index : an int
    """

    global drawn
    global ID
    endoftrial = False
    complete = False
    exitWindow = False
    recordDescriptor="Select the word you heard using the arrow keys:"
    print "----\nAwaiting input for: "+str(files[file_index])
    mpIDpattern = re.match("[0-9]+_",str(files[file_index]))
    tokenName = re.search("\_\w+\_",str(files[file_index]))
    token = tokenName.group(0)[1:-1]
    mpID = mpIDpattern.group(0)[:-1]
    print("minpair ID: "+str(mpID))
    mp = searchForMinPair(mpID)
    print("minpair: ",mp)
    mp0 = mp[0]
    mp1 = mp[1]

    answers = "<- "+mp0+" | "+mp1+" ->"
    print(mp0,mp1,"token: ",token)
    


    # event loop -- 
    """
        SPACE: record
        ESC: quit
        RETURN: next
    """
    while not complete:
        screenDisplay.fill(p.BG)
        events = pygame.event.get()
        textLineHeight = 40
        inputTextPadding = 5
        
        # descriptor text
        txt.textWrap(screenDisplay, recordDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.OFFWHITE, p.BG, 1) 
        txt.textLine(screenDisplay,answers, "mid", answerText, p.OFFWHITE,)

        # txt.textWrap(screenDisplay, mp0, bodyText, pygame.Rect((p.screen_width/4,40, 400, 40)), p.OFFWHITE, p.BG, 1) 
        # txt.textWrap(screenDisplay, mp1, bodyText, pygame.Rect((p.screen_width/2,40,400, 40)), p.OFFWHITE, p.BG, 1) 

        # textual input start --\\
        # pygame.draw.rect(screenDisplay,p.DARKGREY, pygame.Rect((p.cornerPadding,p.screen_height-p.cornerPadding-textLineHeight-200),(p.screen_width-2*p.cornerPadding,textLineHeight+inputTextPadding)))
        # textinput.update(events)
        # screenDisplay.blit(textinput.get_surface(), (p.cornerPadding+inputTextPadding, p.screen_height-p.cornerPadding-textLineHeight-200+inputTextPadding))
        # textual input end --//

        pygame.display.update()

        if not drawn:
            # text input --
            drawn = True

        if exitWindow:
            pygame.quit()
            quit()

        for event in events :
            if event.type == pygame.QUIT: 
                exitWindow = True

            # KEYDOWN events ---------------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape pressed!")
                    exitWindow = True
                
                # record -- legacy code: uncomment for audio recording.
                #           also uncomment the if block marked with ***

                # if event.key == pygame.K_SPACE:
                #     if not record.recording:
                #         record.rec(screenDisplay,bodyText, files[file_index], ID)
                #         drawn = False
                #         endoftrial = True
                
                # move on 
                if event.key == pygame.K_LEFT:
                    # left key input
                    # p0
                    complete = True
                    # appendToAnswerSheet(...) , some stuff

                if event.key == pygame.K_RIGHT:
                    # right key input
                    # p1
                    complete = True
                    # appendToAnswerSheet(...)
                # if event.key == pygame.K_RETURN:
                #     print("\n\n\nINPUT TEXT: "+textinput.get_text())
                #     appendToAnswerSheet(textinput.get_text(),os.path.basename(currentFilePath))
                #     textinput.clear_text()
                #     complete = True

                    # *** uncomment the following if using audio recording, and comment out 
                    #     the complete = True statement above
                    # if endoftrial: 
                    #     print "end of trial clause"
                    #     complete = True


            clock.tick(30)

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
            screenDisplay.fill(p.BG)
            # render thing here
            txt.textWrap(screenDisplay, breakDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.OFFWHITE, p.BG, 1) 

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
    recordScreen(file_index,files,path)
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
    global minPairMap

    with open("stimuli/minpairmap.csv") as mpmap:
        reader = csv.DictReader(mpmap)
        for row in reader:
            minPairMap.append(row)

    welcomeScreen()

    initCsv("minpair")
    numOfTokens = len(minpairs)
    halfTokens = numOfTokens/2
    for file in xrange(0,halfTokens):
        trial(file_index,minpairs,p.minpairs)
        file_index+=1
    breakScreen()
    for file in xrange(halfTokens+1,numOfTokens):
        trial(file_index,minpairs,p.minpairs)
        file_index+=1
    breakScreen()

def appendToAnswerSheet(answer,token):
    with open(currentCsvPath,'ab') as csvFile:
        # we format the filepath so we don't have an ugly /.../.../... .wav name
        m = re.search('\_.*\_', token) # finds stuff that looks like _this_
        formattedToken = m.group(0)[1:-1] # strips the _'s
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow([answer,formattedToken])

def initCsv(type):
    """
    writes the csv file of participant responses
    type: a string
    """
    global ID
    global currentCsvPath
    currentCsvPath = participantResponseRootFilePath+"/"+ID+"_"+type+"_responses.csv"
    with open(currentCsvPath, 'wb') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["Response","Token"])

def searchForMinPair(id):
    for row in minPairMap:
        if row["ID"] == id:
            return [row["p0"],row["p1"]]

    return ["NO_PAIR_FOUND","NO_PAIR_FOUND"]

def main():
    setup()
    pygame.init()
    experimentCtrlFlow()


# main()
experimentCtrlFlow()
pygame.quit()
quit()
