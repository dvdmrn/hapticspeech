from os import listdir
from os.path import isfile, join
import os

import random

import pygame
import time

# basic settings
pygame.init()

width = 800
height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Haptic Speech Experiment')
clock = pygame.time.Clock()

wavpath = "../processing_hapticspeech/data"

"""============================================================="""
# # creates text boxes
# def text_objects(text, font):
# 	textSurface = font.render(text, True, black)
# 	return textSurface, textSurface.get_rect()

# # displays text in a textbox
# def message_display(text):
# 	largeText = pygame.font.Font('freesansbold.ttf',115)
# 	TextSurf, TextRect = text_objects(text, largeText)
# 	TextRect.center = ((display_width/2),(display_height/2))
# 	gameDisplay.blit(TextSurf, TextRect)

# 	pygame.display.update()

# 	time.sleep(2)
	
# 	game_loop()

# grabs a song from directory and plays it
def play_wavfile(filename):
	print "inside play_wavfile"
	fullname = os.path.join(wavpath, filename)
	sound = pygame.mixer.Sound(fullname)
	sound.play()

# returns a randomized list of songs in the directory
def get_wavfiles():
	path = "../processing_hapticspeech/data"
	# put names of wavfiles in a list
	wavfiles = [f for f in listdir(path) if isfile(join(path, f))]
	if '.DS_Store' in wavfiles:
		wavfiles.remove('.DS_Store')
	random.shuffle(wavfiles)
	return wavfiles
"""============================================================="""

def game_loop():

	wavfiles = get_wavfiles()

	gameExit = False
	num_of_files = len(wavfiles)
	file_index = 0

	play_wavfile(wavfiles[file_index])

	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if file_index == 0:
						pass
					else:
						file_index -= 1
						pygame.mixer.stop()
						play_wavfile(wavfiles[file_index])

				if event.key == pygame.K_RIGHT:
					if file_index == num_of_files:
						pass
					else:
						file_index += 1
						pygame.mixer.stop()
						play_wavfile(wavfiles[file_index])
						print "file index: "+str(file_index)
						print "wave file: "+str(wavfiles[file_index])
						break

			# may not need this part
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					pass

		gameDisplay.fill(white)
		pygame.display.update()
		clock.tick(60)


game_loop()
pygame.quit()
quit()