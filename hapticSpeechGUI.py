import pygame
import time

pygame.init()

screen_width = 1280  # how do ensure this fullscreen?? 
screen_height = 720

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (190, 190, 190)

screenDisplay= pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN )
pygame.display.set_caption( ' Haptic Speech Experiment ')
clock = pygame.time.Clock()

welcomeTitleSurf= "Welcome the Haptic Speech Experiment"
welcomeDescriptorSurf= "During the experiment, you will hear a series of words and phrases. Thereafter, you will be prompted to record yourself repeating what you've heard. Ocassionally, you will feel a slight vibration"
welcomeStartSurf = "When you are ready, press the ENTER/RETURN key to begin"

titleText = pygame.font.Font('freesansbold.ttf',40)

# ----------------------------------------------
# Welcome Screen
# ----------------------------------------------

def  welcomeScreen():
    text_display(welcomeTitleSurf,"top",30)
    
    # game_loop()

    # welcomeTitleFont = pygame.font.Font('freesansbold.ttf ', 100)
    # welcomeDescriptorFont = pygame.font.Font('freesansbold.ttf ', 50)
    # welcomeStartFont = pygame.font.Font('freesansbold.ttf ', 50)

    # incorporate key event to take user to stimulusPlayScreen()
    
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
    recordDescriptorSurf= recordDescriptorFont.render( "Now you will record yourself saying what you have just heard!", True, BLACK) #use the render_textrect()
    recordStartSurf =  recordStartFont.render(  'You are able to make as many recordings as you like.When you are ready to begin press and hold the SPACE bar', True, BLACK) 

# key event that takes them to 
    

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def text_display(text, height, fontsize):
    # font size: 10 is tiny, 115 is huge!

    division=1 # very top
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

    # time.sleep(2)
    # game_loop()
    


# def text_objects(text, font):
#     textSurface = font.render(text, True , BLACK)

#     largeText = pygame.font.Font ('freesansbold.ttf ', 115)
#     experimentTitle =  largeText.render (' Welcome to the Haptic Speech Experiment ' , 1 , BLACK)

#     screenDisplay.blit(experimentTitle, ( screen_width /2 ,  screen_height/2) )

#     pygame.display.update() 

#     time.sleep(2)
#     return textSurface, textSuface.get_rect()

#     game_loop()

def game_loop() :
    
    # event handling loop
    exitWindow = False  


    while not exitWindow:

        for event in pygame.event.get() :
            if event.type == pygame.QUIT: # when people exit out of the window by pressing red 'x' on window
                exitWindow = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("right key pressed!")
                    exitWindow = True
        
        screenDisplay.fill(GREY)
        print("exit window val: ",exitWindow)
        welcomeScreen()
        
        pygame.display.update()  # to update something in the next screen - like the text- just pass that parameter into  pygame.display.update()
        
        clock.tick(60)
        

    # game_loop()
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