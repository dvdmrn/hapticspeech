import random
import math
import time

totalTrials = 1
responsesSoFar = 0
score = 0
block = 0
selected = []

# def newBlock():
#     global responsesSoFar
#     global score
#     responsesSoFar = 0
#     score = 0

# def calcuateAccuracy(score,responsesSoFar):
#     return score/float(responsesSoFar)

# def c_response(file_index,files,path):
#     """
#     draws main record screen for a given file_index
#     file_index : an int

#     LEFT response = mp0
#     RIGHT response = mp1
#     """

#     global drawn
#     global ID
#     endoftrial = False
#     complete = False
#     exitWindow = False
#     recordDescriptor="Select the word you heard using the arrow keys:"
#     print "----\nAwaiting input for: "+str(files[file_index])
#     mpIDpattern = re.search("[0-9]+_",str(files[file_index])) # match ID
#     tokenName = re.search("\_\w+\_",str(files[file_index]))
#     token = tokenName.group(0)[1:-1]
#     mpID = mpIDpattern.group(0)[:-1]
#     print("minpair ID: "+str(mpID))
#     mp = searchForMinPair(mpID)
#     print("minpair: ",mp)
#     mp0 = mp[0]
#     mp1 = mp[1]

#     answers = "<- "+mp0+" | "+mp1+" ->"
#     print(mp0,mp1,"token: ",token)
    


#     # event loop -- 
#     """
#         SPACE: record
#         ESC: quit
#         RETURN: next
#     """
#     while not complete:
#         screenDisplay.fill(p.BG)
#         events = pygame.event.get()
#         textLineHeight = 40
#         inputTextPadding = 5
        
#         # descriptor text
#         txt.textWrap(screenDisplay, recordDescriptor, bodyText, pygame.Rect((40,40,p.screen_width, p.recBarWidth)), p.OFFWHITE, p.BG, 1) 
#         txt.textLine(screenDisplay,answers, "mid", answerText, p.OFFWHITE,)

#         pygame.display.update()

#         if not drawn:
#             # text input --
#             drawn = True

#         if exitWindow:
#             pygame.quit()
#             quit()

#         for event in events :
#             if event.type == pygame.QUIT: 
#                 exitWindow = True

#             # KEYDOWN events ---------------
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     print("Escape pressed!")
#                     exitWindow = True
                
#                 # move on 
#                 if event.key == pygame.K_LEFT:
#                     # left key input
#                     # p0
#                     complete = True
#                     evaluate_response(mp0,token)

#                 if event.key == pygame.K_RIGHT:
#                     # right key input
#                     # p1
#                     complete = True
#                     evaluate_response(mp1,token)
                
#             clock.tick(30)

#     drawn = False

# def evaluate_response(response,token):
#     global responsesSoFar
#     global score
#     global totalTrials

#     m = re.findall(r'[A-Za-z]+',token)
#     formattedToken = m[0]
#     formattedContrast = m[1]

#     correct = 0
#     if answer == formattedToken:
#         correct = 1

#     responsesSoFar += 1
#     score += correct
#     totalTrials += 1
#     accuracy = calcuateAccuracy(score,responsesSoFar)
#     return accuracy


def heuristic_calibration(i,minpairs):
    global responsesSoFar
    global totalTrials
    global score
    global block
    adj_factor = 0.8
    index_mem = set()

    # selects a unique random minpair --
    for j in range(0,len(minpairs)):
        i = int(math.floor(random.random()*len(minpairs)))
        while i in index_mem:
            i = int(math.floor(random.random()*len(minpairs)))
        index_mem.add(i)
        print "evaluating: "+str(minpairs[i])
        totalTrials += 1
        if block == 0:
            block_0(minpairs[i])
        else:
            block_n(minpairs[i])


    calibrated = False


def block_0(path):
        # play_stim(path)
        # correct = get_response(path)
        if not correct:
            adjustVolume(adj_factor)

def block_n(path):
        # play_stim()


heuristic_calibration(0,range(0,100))