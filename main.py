"""

     _   _             _   _      _____                      _     
    | | | |           | | (_)    /  ___|                    | |    
    | |_| | __ _ _ __ | |_ _  ___\ `--. _ __   ___  ___  ___| |__  
    |  _  |/ _` | '_ \| __| |/ __|`--. \ '_ \ / _ \/ _ \/ __| '_ \ 
    | | | | (_| | |_) | |_| | (__/\__/ / |_) |  __/  __/ (__| | | |
    \_| |_/\__,_| .__/ \__|_|\___\____/| .__/ \___|\___|\___|_| |_|
                | |                    | |                         
                |_|                    |_|                         
    
    ===================================================================
    -------------------------------------------------------------------
    ...................................................................


    Labs: -------------------------------------------------------------

         _______..______    __  .__   __.
        /       ||   _  \  |  | |  \ |  |
       |   (----`|  |_)  | |  | |   \|  |
        \   \    |   ___/  |  | |  . `  |
    .----)   |   |  |      |  | |  |\   |
    |_______/    | _|      |__| |__| \__|
                                         
    Sensory Perception and Interaction Lab

    ________/\\\\\\\\\________________/\\\\\\\\\\\\_____/\\\_____________        
     _____/\\\////////________________\/\\\////////\\\__\/\\\_____________       
      ___/\\\/_________________________\/\\\______\//\\\_\/\\\_____________      
       __/\\\_________________/\\\\\____\/\\\_______\/\\\_\/\\\_____________     
        _\/\\\_______________/\\\///\\\__\/\\\_______\/\\\_\/\\\_____________    
         _\//\\\_____________/\\\__\//\\\_\/\\\_______\/\\\_\/\\\_____________   
          __\///\\\__________\//\\\__/\\\__\/\\\_______/\\\__\/\\\_____________  
           ____\////\\\\\\\\\__\///\\\\\/___\/\\\\\\\\\\\\/___\/\\\\\\\\\\\\\\\_ 
            _______\/////////_____\/////_____\////////////_____\///////////////__

    Communications Dynamics Lab

    _________ _______  _______  _       
    \__   __/(  ____ \(  ____ )( \      
       ) (   | (    \/| (    )|| (      
       | |   | (_____ | (____)|| |      
       | |   (_____  )|     __)| |      
       | |         ) || (\ (   | |      
    ___) (___/\____) || ) \ \__| (____/\
    \_______/\_______)|/   \__/(_______/
                                       
    Interdisciplinary Speech Research Lab
    
    
    Researchers: ----------------------------------------------------
    PIs: Karon MacLean, Bryan Gick, Eric Vatikiotis-Bateson 
    RAs: David Marino, Hannah Elbaggari, Andrew Yang, Tamara Lottering



    About: -----------------------------------------------------------
    
    + Experimental software designed to evaluate the efficacy of 
      haptic enhancement of speech in noisy conditions.

    + Converts speech to a haptic signal (L channel)

    + use the `-w` flag for windowed mode
    
    + use the `-nc` (no calibration) flag to skip calibration

    notes:
    - gets files in stim based off minpairmappings.csv. 
    - Randomly populates an array called "files"

"""
from __future__ import print_function
print(" _   _             _   _      _____                      _     \n| | | |           | | (_)    /  ___|                    | |    \n| |_| | __ _ _ __ | |_ _  ___\ `--. _ __   ___  ___  ___| |__  \n|  _  |/ _` | '_ \| __| |/ __|`--. \ '_ \ / _ \/ _ \/ __| '_ \ \n| | | | (_| | |_) | |_| | (__/\__/ / |_) |  __/  __/ (__| | | |\n\_| |_/\__,_| .__/ \__|_|\___\____/| .__/ \___|\___|\___|_| |_|\n            | |                    | |                         \n            |_|                    |_|                         \n\nImporting modules...")
import pygame
import time
import pyaudio
import wave
import sys
import textdisplay as txt
import utilities as util
import parameters as p
import record
import playback
# import playback_lowfi
import pygame_textinput
import csv
import os
import re
import math, random

# -- globals ------------------------\\
STIM_VOLUME = 1.0 # 1 = max
ACCURACY_TARGET = 62.0 # % of correct scores needed
PADDING = 5.0 # +/- padding
# =====================================

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

minpairs = util.get_minpairs("stimuli/")
minPairMap = [] # will be populated with minpair IDs and tokens

file_index = 0

# a hack ---------------\
# look the other way
currentFilePath = ""
currentCsvPath = ""
includeCalibration = True
# ----------------------/

# pygame setup ---------\

# accepts CL input `-w` for windowed mode
if (len(sys.argv)>1):
    if (sys.argv[1]=="-w"):
        screenDisplay= pygame.display.set_mode((p.screen_width,p.screen_height))
        pygame.display.set_caption( ' Haptic Speech Experiment ')
        clock = pygame.time.Clock()
        print ("window mode")
    if (sys.argv[1]=="-nc"):
        screenDisplay= pygame.display.set_mode((p.screen_width,p.screen_height))
        pygame.display.set_caption( ' Haptic Speech Experiment [NO CALIBRATION] ')
        clock = pygame.time.Clock()
        print ("window mode: NO CALIBRATION")
        includeCalibration = False
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
def playbackScreen(file_index,files,path, ctrl= False):
    """
    Renders the screen for signal playback
    @param file_index: an int
    """

    global drawn
    global currentFilePath

    print ("\n\n\n!!!",files[file_index])

    if not drawn:
        num_of_files = len(files)
            
        print("file index: "+str(file_index))
        print("wave file: "+str(files[file_index]["file"]))
        # print("files: "+str(files))

        screenDisplay.fill(p.BG)
        pygame.display.update()
        currentFilePath = util.constructPath(path,files[file_index]["file"])
        print("calling haptic_playback")
        if ctrl:
            playFile(currentFilePath, STIM_VOLUME, "left")
        else :
            playback.rms_playback(currentFilePath)
            


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
    print("----\nAwaiting input for: "+str(files[file_index]["file"]))
    mpIDpattern = re.search("[0-9]+_",str(files[file_index]["file"])) # match ID
    tokenName = re.search("\_\w+\_",str(files[file_index]["file"]))
    token = tokenName.group(0)[1:-1]
    mpID = mpIDpattern.group(0)[:-1]
    mp = searchForMinPair(mpID)
    mp0 = mp[0]
    mp1 = mp[1]

    answers = "<- "+mp0+" | "+mp1+" ->"
    


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
                    print("selected: ",mp0)
                    complete = True
                    appendToAnswerSheet(mp0,token,files[file_index]["vib_style"])

                if event.key == pygame.K_RIGHT:
                    # right key input
                    # p1
                    complete = True
                    print("selected: ",mp1)
                    appendToAnswerSheet(mp1,token,files[file_index]["vib_style"])
                
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

    print("\n\n==============================")
    global drawn 
    global endoftrial
    playbackScreen(file_index,files,path,True)
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

    if includeCalibration:
        heuristic_calibration(minpairs) 
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

def appendToAnswerSheet(answer,token,vib_style):
    """
    
    """
    with open(currentCsvPath,'ab') as csvFile:
        evaluate_response(answer,token,csvFile,vib_style)
        

def evaluate_response(answer,token, csvFile=None, vibStyle=""):
    m = re.findall(r'[A-Za-z]+',token)
    formattedToken = m[0]
    formattedContrast = m[1]

    correct = 0
    if answer == formattedToken:
        correct = 1

    if csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow([answer,formattedToken,correct,formattedContrast,vibStyle])
    
    return correct


def initCsv(type):
    """
    writes the csv file of participant responses
    type:= a string

    CSV format:

        response | token | correct | contrast  | vib style
        ------------------------------------------
        p0       | p0    | 1       | vf        | amp
        p0       | p1    | 0       | Vh        | lowfi
        p1       | p1    | 1       | Vh        | ctrl
        ...        ...     ...       ...

    """
    global ID
    global currentCsvPath
    currentCsvPath = participantResponseRootFilePath+"/"+ID+"_"+type+"_responses.csv"
    with open(currentCsvPath, 'wb') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["response","token","correct","contrast","vib_style"])

def searchForMinPair(id):
    for row in minPairMap:
        if row["ID"] == id:
            return [row["p0"],row["p1"]]

    return ["NO_PAIR_FOUND","NO_PAIR_FOUND"]













# ============[calibration]==========================

def heuristic_calibration(minpairs):
    # todo: once adjust stim volume, make sure stim in main block playback @ that vol.
    minpairs = util.getFilePaths(minpairs)
    global STIM_VOLUME
    cTrials = 0
    score = 0
    block = 0
    adj_factor = math.log10(9-cTrials)
    ave = 0
    lowerBound = (ACCURACY_TARGET-PADDING)/float(100)
    upperBound = (ACCURACY_TARGET+PADDING)/float(100)

    for j in range(0,len(minpairs)):
        # i = int(math.floor(random.random()*len(minpairs)))
        # while i in index_mem:
        #     i = int(math.floor(random.random()*len(minpairs)))
        # index_mem.add(i)
        print("evaluating: ",str(minpairs[j]))
        cTrials += 1

        # --- very aggressive calibration --------
        if block == 0:
            print("\n\n====\nAGGRESSIVE CALIBRATION")
            correct = eval_token(minpairs[j],j,STIM_VOLUME)
            if not correct:
                adj_volume(adj_factor*-1)
                adj_factor = math.log10(9-cTrials)
            else:
                adj_volume(adj_factor)
                adj_factor = math.log10(9-cTrials)
            if cTrials >= 7:
                print("On 8th trial: aggressive calibration complete")
                block += 1
                cTrials = 0

        # --- looks for averages in blocks of 12 ----
        else:
            correct = eval_token(minpairs[j],j,STIM_VOLUME)
            y = 2 - (block**2/float(block**2+3)) # a decreasing value from 2->1
            adj_factor = max(0.1,math.log10(y))
            if correct:
                score += 1
            if cTrials >= 12: # if number of trials greater than 12
                print("calibration trial: ",cTrials,"blocks: ",block)
                ave = runningAverage(score,cTrials)
                cTrials = 0
                score = 0
                # in right range
                print("lowerBound: ",lowerBound,"ave: ",ave)
                print("is ave < upperbound?",ave<upperBound,"is ave > lowerbound?",ave > lowerBound)
                
                # they are accurate enough yay
                if (ave < upperBound) and (ave > lowerBound):
                    if block > 1:
                        print("calibrated with ave:",ave,"| volume: ",babbletrack.get_volume())

                        # write .txt file with calibration settings
                        with open(participantResponseRootFilePath+"/"+ID+"_calibrationSettings.txt","w") as txt:
                            txt.write("volume: "+str(babbletrack.get_volume())+"\naccuracy: "+str(ave))
                        return
                    else:
                        block += 1

                # too accurate, make noise harder
                if ave > upperBound:
                    print("too accuracte, adjusting by: ",adj_factor)
                    if ave > 0.7:
                        print("way too accurate")
                        # give it a little extra
                        adj_factor += 0.10
                        print("new adj factor: ",adj_factor)
                    adj_volume(adj_factor)
                    block += 1

                # not accurate enough, pump it up
                if ave < lowerBound:
                    f = adj_factor*-1
                    if ave < 0.5:
                        # v. bad, pump it up
                        adj_factor -= 0.10
                        print("vey under lowerBound, new adj factor: ",adj_factor)

                    adj_volume(f)
                    block += 1
                

        #     block_n(minpairs[j])


    calibrated = False

def runningAverage(score,trialsSoFar):
    ave = score/float(trialsSoFar)
    print("accuracy: ",ave,"calibration trials: ",trialsSoFar,"score: ",score)
    return ave

def adj_volume(factor):
    global BASE_VOLUME
    BASE_VOLUME = min(BASE_VOLUME+factor,1)
    prevVolume = babbletrack.get_volume()
    print("prev vol.:",prevVolume)
    toSet = min(prevVolume+factor,1)
    babbletrack.set_volume(toSet)
    print("volume adjusted by: "+str(factor)+" current volume: ",babbletrack.get_volume())

def eval_token(path,index,gain):

        playFile(path,gain)

        screenDisplay.fill(p.BG)
        pygame.display.update()

        correct = get_calibration_response(index,minpairs,p.minpairs)
        return correct

def playFile(path,gain,channel=""):
        """
        plays a sound file, and also pauses for the duration of that file.
        """
        speech = pygame.mixer.Sound(path)
        if channel=="left":
            channel1.set_volume(gain,0)
        else:
            channel1.set_volume(gain,gain)
        channel1.play(speech)
        time.sleep(speech.get_length())
    


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
    print("\nAwaiting input for: "+str(files[file_index]))
    mpIDpattern = re.search("[0-9]+_",str(files[file_index])) # match ID
    tokenName = re.search("\_\w+\_",str(files[file_index]))
    token = tokenName.group(0)[1:-1]
    mpID = mpIDpattern.group(0)[:-1]
    mp = searchForMinPair(mpID)
    mp0 = mp[0]
    mp1 = mp[1]

    answers = "<- "+mp0+" | "+mp1+" ->"
    


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
                    print("selected: ",mp0,"correct:",token)
                    complete = True
                    correct = evaluate_response(mp0,token)

                if event.key == pygame.K_RIGHT:
                    # right key input
                    # p1
                    print("selected: ",mp1,"correct:",token)
                    complete = True
                    correct = evaluate_response(mp1,token)
                
            clock.tick(30)

    drawn = False
    return correct
# =============================================================





# def main():
#     setup()
#     pygame.init()
#     experimentCtrlFlow()


# main()
experimentCtrlFlow()
pygame.quit()
quit()
