"""
    use the -w flag for windowed mode

    notes:

    gets files in stim based off minpairmappings.csv. Randomly populates an array called "files"

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
import playback_rms
# import playback_lowfi
import pygame_textinput
import csv
import os
import re
import math, random
# import autocalibration

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

# phrases = util.get_wavfiles("stimuli/phrases/")
# words = util.get_wavfiles("stimuli/words/")
minpairs = util.get_minpairs("stimuli/")
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




# refactor the following? (music)

# init babble track in L channel
# channel0 := babbletrack
# channel1 := pure speech

babbletrack = pygame.mixer.Sound('stimuli/MT_babble.wav')
channel0 = pygame.mixer.Channel(0)
channel1 = pygame.mixer.Channel(1)
channel0.play(babbletrack,-1)
BASE_VOLUME = 0.2
babbletrack.set_volume(BASE_VOLUME)
channel0.set_volume(1, 0.0) # 1st arg = left; 2nd arg = right

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
    welcomeDescriptor= "During the experiment you will hear a series of words. You will be prompted to identify each word in a multiple choice manner. Select the LEFT word with the left arrow key [<-], and the RIGHT word with the right arrow key [->]. \nThe experiment will begin with a calibration phase. Afterwards, you will be asked to notify a researcher to assist you with the vibrator.\n\nWhen you are ready to begin, press the ENTER/RETURN key to continue."
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
        playback_rms.haptic_playback(currentFilePath)
        drawn = True
    

# ----------------------------------------------
#  Recording  Screen
# ----------------------------------------------
def recordScreen(file_index,files,path):
    """
    draws main record screen for a given file_index
    file_index : an int

    LEFT response = mp0
    RIGHT response = mp1
    """

    global drawn
    global ID
    endoftrial = False
    complete = False
    exitWindow = False
    recordDescriptor="Select the word you heard using the arrow keys:"
    print "----\nAwaiting input for: "+str(files[file_index])
    mpIDpattern = re.search("[0-9]+_",str(files[file_index])) # match ID
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
                
                # move on 
                if event.key == pygame.K_LEFT:
                    # left key input
                    # p0
                    complete = True
                    appendToAnswerSheet(mp0,token)

                if event.key == pygame.K_RIGHT:
                    # right key input
                    # p1
                    complete = True
                    appendToAnswerSheet(mp1,token)
                
            clock.tick(30)

    drawn = False



def breakScreen(breakDescriptor):

    global drawn
    exitWindow = False
    complete = False

    
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
    """
    play & rec a token

    file_index := an int
    files := a list of files
    """

    print files

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
    global minpairs

    with open("stimuli/minpairmap.csv") as mpmap:
        reader = csv.DictReader(mpmap)
        for row in reader:
            minPairMap.append(row)

    welcomeScreen()
    heuristic_calibration(0,minpairs)
    breakScreen("Calibration Complete!\nPlease notify a researcher.")
    random.shuffle(minpairs)
    initCsv("minpair")
    numOfTokens = len(minpairs)
    halfTokens = numOfTokens/2
    for file in xrange(0,halfTokens):
        trial(file_index,minpairs,p.minpairs)
        file_index+=1
    
    breakScreen("You're halfway through\nPlease notify a researcher to assist with vibrator placement.")

    for file in xrange(halfTokens,numOfTokens):
        trial(file_index,minpairs,p.minpairs)
        file_index+=1
    breakScreen("Complete! Thank-you!")

def appendToAnswerSheet(answer,token):
    """
    
    """
    with open(currentCsvPath,'ab') as csvFile:
        evaluate_response(answer,token,csvFile)
        

def evaluate_response(answer,token, csvFile=None):
    m = re.findall(r'[A-Za-z]+',token)
    formattedToken = m[0]
    formattedContrast = m[1]

    correct = 0
    if answer == formattedToken:
        correct = 1

    if csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow([answer,formattedToken,correct,formattedContrast])
    
    return correct


def initCsv(type):
    """
    writes the csv file of participant responses
    type:= a string

    CSV format:

        response | token | correct | contrast
        -----------------------------
        p0       | p0    | 1       | vf
        p0       | p1    | 0       | Vh
        p1       | p1    | 1       | Vh
        ...        ...     ...

    """
    global ID
    global currentCsvPath
    currentCsvPath = participantResponseRootFilePath+"/"+ID+"_"+type+"_responses.csv"
    with open(currentCsvPath, 'wb') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["response","token","correct","contrast"])

def searchForMinPair(id):
    for row in minPairMap:
        if row["ID"] == id:
            return [row["p0"],row["p1"]]

    return ["NO_PAIR_FOUND","NO_PAIR_FOUND"]













# ============[calibration]==========================

def heuristic_calibration(i,minpairs):
    cTrials = 0
    score = 0
    block = 0
    adj_factor = 0.8
    index_mem = set()
    ave = 0

    # selects a unique random minpair --
    for j in range(0,len(minpairs)):
        i = int(math.floor(random.random()*len(minpairs)))
        while i in index_mem:
            i = int(math.floor(random.random()*len(minpairs)))
        index_mem.add(i)
        print "evaluating: "+str(minpairs[i])
        cTrials += 1

        # --- very aggressive calibration --------
        if block == 0:
            correct = eval_token(minpairs[i],i)
            if not correct:
                adj_volume(adj_factor*-1)
                adj_factor = math.log10(11-cTrials)
            else:
                adj_volume(adj_factor)
                adj_factor = math.log10(11-cTrials)
            if cTrials > 4:
                block += 1
                cTrials = 0

        # --- looks for averages in blocks of 10 ----
        else:
            correct = eval_token(minpairs[i],i)
            adj_factor = max(0.1,math.log10(4+block))
            if not correct:
                cTrials += 1
                ave = runningAverage(score,cTrials)
            else:
                cTrials += 1
                score += 1
                ave = runningAverage(score,cTrials)
            if cTrials > 10:
                if (ave > 0.22) and (ave < 0.38):
                    print("calibrated with ave:",ave,"| volume: ",babbletrack.get_volume())
                    with open(participantResponseRootFilePath+"/"+ID+"_calibrationSettings.txt","w") as txt:
                        txt.write("volume: "+str(babbletrack.get_volume())+"\naccuracy: "+str(ave))
                    return

                if ave > 0.38:
                    adj_volume(adj_factor*-1)
                    cTrials = 0
                    score = 0
                    block += 1
                if ave < 0.22:
                    adj_volume(adj_factor)
                    cTrials = 0
                    score = 0
                    block += 1
                

        #     block_n(minpairs[i])


    calibrated = False

def runningAverage(score,trialsSoFar):
    ave = score/float(trialsSoFar)
    print(ave)
    return ave

def adj_volume(factor):
    global BASE_VOLUME
    BASE_VOLUME = min(BASE_VOLUME+factor,1)
    babbletrack.set_volume(factor)
    print "volume adjusted to: "+str(factor)

def eval_token(path,index):
        print "block_0"
        speech = pygame.mixer.Sound(path)
        channel1.play(speech)
        # play_stim(path)1
        correct = get_calibration_response(index,minpairs,p.minpairs)
        return correct


def get_calibration_response(file_index,files,path):
    """
    draws main record screen for a given file_index
    file_index : an int

    LEFT response = mp0
    RIGHT response = mp1
    """

    global drawn
    global ID
    endoftrial = False
    complete = False
    exitWindow = False
    correct = 0

    recordDescriptor="Select the word you heard using the arrow keys:"
    print "----\nAwaiting input for: "+str(files[file_index])
    mpIDpattern = re.search("[0-9]+_",str(files[file_index])) # match ID
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
                
                # move on 
                if event.key == pygame.K_LEFT:
                    # left key input
                    # p0
                    complete = True
                    correct = evaluate_response(mp0,token)

                if event.key == pygame.K_RIGHT:
                    # right key input
                    # p1
                    complete = True
                    correct = evaluate_response(mp1,token)
                
            clock.tick(30)

    drawn = False
    return correct
# =============================================================





def main():
    setup()
    pygame.init()
    experimentCtrlFlow()


# main()
experimentCtrlFlow()
pygame.quit()
quit()
