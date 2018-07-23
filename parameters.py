import pygame.display as pd
# static parameters ----\

# dimensions --
# screen_width = 1280   
# screen_height = 720

screen_width = 1366   
screen_height = 768
recBarWidth = 300
recBarHeight = 30
cornerPadding = 20

# color --
BLACK = (0,0,0)
WHITE = (255, 255, 255)
OFFWHITE = (230,230,230)
GREY = (190, 190, 190)
BG = (30, 10, 20)

DARKGREY = (30,10,20)
# DARKGREY = (10,10,10)
PINK = (200,100,200)


titleSize = 40
bodySize = 32
answerSize = 60



# files --
wordpath = "stimuli/words/"
phrasepath = "stimuli/phrases/"
minpairs = ""

responsePath = "responses/"

# ----------------------/

# ULTRA HD MODE
def setUHD():
	global screen_width
	global screen_height
	global titleSize
	global bodySize
	global answerSize
	global recBarWidth
	global recBarHeight
	print("called uhd")
	screen_width = 3480
	screen_height = 2160
	titleSize = 80
	bodySize = 64
	answerSize = 80
	recBarWidth = 600
	recBarHeight = 300