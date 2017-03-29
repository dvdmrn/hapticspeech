from os import listdir
from os.path import isfile, join
import os
import random
from struct import pack, unpack
from math import sin, pi
import wave
import pyaudio
import math
import pygame
import time
import pygame
import time
import textwrap

# settings
pygame.init()

screen_width = 1280   
screen_height = 720

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (190, 190, 190)

screenDisplay = pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN)
pygame.display.set_caption('Haptic Speech Experiment')
clock = pygame.time.Clock()

welcomeTitle = "Welcome to the Haptic Speech Experiment!"
welcomeDescriptor = "During the experiment you will hear a series of words and phrases. Thereafter, you will be prompted to record yourself repeating what you've heard. Ocassionally you will feel a slight vibration.\n\nWhen you are ready to begin, press the ENTER/RETURN key to continue."

titleText = pygame.font.Font('freesansbold.ttf', 40)
bodyText = pygame.font.Font('freesansbold.ttf', 32)

drawn = False

wavpath = "stimuli/"

# ----------------------------------------------
# Welcome Screen
# ----------------------------------------------

def welcomeScreen():
    global drawn
    
    if not drawn:
        screenDisplay.fill(GREY)
        text_display(welcomeTitle, "top", 30)
        render_textrect(welcomeDescriptor, bodyText, pygame.Rect((40, 40, screen_width, 300)), BLACK, GREY, 1) 

        drawn = True


# ----------------------------------------------
# Text Display Functions
# ----------------------------------------------
class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException("Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]


    horizontal_center = (surface.get_rect().right - surface.get_rect().left)/2
    vertical_center = (surface.get_rect().bottom - surface.get_rect().top)/2
    screenDisplay.blit(surface, ((screen_width/2) - horizontal_center, (screen_height/2) - vertical_center+75)) 
    
    return surface

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def text_display(text, height, fontsize):
    # font size: 10 is tiny, 115 is huge!

    division = 1 # very top
    if height=="mid": # middle of screen
        division = 2
    if height=="top": # top 75% of screen
        division = 4
    if height=="bottom": # bot. 25% of the screen
        division = 4/float(3)        
    
    TextSurf, TextRect = text_objects(text, titleText)
    TextRect.center = ((screen_width/2),(screen_height/float(division)))
    screenDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


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
    recordDescriptorFont = pygame.font.Font('freesansbold.ttf ', 50)
    recordStartFont = pygame.font.Font('freesansbold.ttf ', 50)
    recordDescriptorSurf = recordDescriptorFont.render( "Now you will record yourself saying what you have just heard!", True, BLACK) #use the render_textrect()
    recordStartSurf =  recordStartFont.render(  'You are able to make as many recordings as you like.When you are ready to begin press and hold the SPACE bar', True, BLACK) 


# ----------------------------------------------
#  Playback
# ----------------------------------------------
# def play_wavfile(filename):
#     RATE=44100
#     chunk = 1024

#     filepath = os.path.join(wavpath, filename)

#     f = wave.open(filepath,"rb")  
#     print("\n\nopening: "+filepath)
#     print("samplerate: "+str(f.getframerate()))
#     print("frames: "+str(f.getnframes()))
#     print("channels: "+str(f.getnchannels()))
#     print("sample width: "+str(f.getsampwidth()))

#     ## GENERATE STEREO FILE ##
#     wv = wave.open('temp.wav', 'w')
#     wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
#     maxVol=2**14-1.0 #maximum amplitude
#     wvData=""
#     i = 0

#     for i in range(0, f.getnframes()):
    
#         frameSample = f.readframes(1)
#         # print len(frameSample)
#         if len(frameSample):
#             try:
#                 data = unpack('h',frameSample)
#             except:
#                 print ("Unpacking error, may be from an invalid frameSample")
#                 print ("frame sample length: "+str(len(frameSample)))
#                 print ("frame sample string: "+frameSample)
            
#         else:
#             data = 0
#         if data:
#             amp = math.sqrt(data[0]**2)
#             wvData+=pack('h', data[0])
#             wvData+=pack('h', amp*sin(i*800.0/RATE)) #200Hz right
#         else:
#             break
#     wv.writeframes(wvData)
#     wv.close()

#     print("processed file!")


#     # --------------------------------------------------------
#     # playback processed audio
#     # --------------------------------------------------------

#     #open a wav format music  
#     f = wave.open(r"temp.wav","rb")  
#     #instantiate PyAudio  
#     p = pyaudio.PyAudio()  
#     #open stream  
#     stream = p.open(format = p.get_format_from_width(f.getsampwidth()), 
#                     channels = 2,  
#                     rate = f.getframerate(),  
#                     output = True)  
#     #read data  
#     data = f.readframes(chunk)

#     print("playback initialized!")

#     while data:
#         stream.write(data)
#         data = f.readframes(chunk)

#     #stop stream  
#     stream.stop_stream()  
#     stream.close()  

#     print("playback ended.")
#     #close PyAudio  
#     p.terminate()  

# returns a randomized list of songs in the directory
# def get_wavfiles():
#     path = "stimuli/"
#     # put names of wavfiles in a list
#     wavfiles = [f for f in listdir(path) if isfile(join(path, f))]
#     if '.DS_Store' in wavfiles:
#         wavfiles.remove('.DS_Store')
#     random.shuffle(wavfiles)
#     return wavfiles

# def translate(value, leftMin, leftMax, rightMin, rightMax):
#     # Figure out how 'wide' each range is
#     leftSpan = leftMax - leftMin
#     rightSpan = rightMax - rightMin

#     # Convert the left range into a 0-1 range (float)
#     valueScaled = float(value - leftMin) / float(leftSpan)

#     # Convert the 0-1 range into a value in the right range.
#     return rightMin + (valueScaled * rightSpan)


# ----------------------------------------------
#  Playback Screen
# ----------------------------------------------
def playbackScreen():
    wavfiles = get_wavfiles()
    gameExit = False
    num_of_files = len(wavfiles)
    file_index = 0
    print("file index: "+str(file_index))
    print("wave file: "+str(wavfiles[file_index]))
    print("files: "+str(wavfiles))

    screenDisplay.fill(GREY)
    pygame.display.update()
    play_wavfile(wavfiles[file_index])


# ----------------------------------------------
#  Record Screen
# ----------------------------------------------
def recordScreen():
    text_display("Press space to record", "top", 30)
    pygame.display.update()


# ----------------------------------------------
#  Recording Screen
# ----------------------------------------------
def recordingScreen():
    screenDisplay.fill(GREY)
    text_display("Recording...", "top", 30)
    pygame.display.update() 


# ----------------------------------------------
#  Game Loop
# ----------------------------------------------
def game_loop() :
    
    # event handling loop
    exitWindow = False  
    

    while not exitWindow:

        for event in pygame.event.get() :
            if event.type == pygame.QUIT: 
                exitWindow = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC key pressed!")
                    exitWindow = True

                if event.key == pygame.K_RETURN:
                    print("Enter key pressed!")
                    playbackScreen()
                    recordScreen()

                if event.key == pygame.K_SPACE:
                    recordingScreen()
                    # implement record

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # implement stop recording?
                    pass
        
        welcomeScreen()
        
        pygame.display.update()  
        clock.tick(60)
        
    print("exited game loop")
    pygame.quit()
    print("called pygame quit")
    quit()


game_loop()
print("exited game loop")
pygame.quit()
print("called pygame quit")
quit()
print("should've quit by now")