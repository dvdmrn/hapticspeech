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

"""============================================================="""
def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText = pygame.font.Font('freesansbold.ttf',115)
	TextSurf, TextRect = text_objects(text, largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	pygame.display.update()

	time.sleep(2)
	
	game_loop()

def playwav(index):
	"""load the sound file from the given directory"""
	fullname = os.path.join(wavpath, wavfiles[index])
	sound = pygame.mixer.Sound(fullname)
	sound.play()
	message_display("You are playing: " + wavfiles[index])

def get_wavfiles():
	path = "../processing_hapticspeech/data"
	# put names of wavfiles in a list
	wavfiles = [f for f in listdir(path) if isfile(join(path, f))]
	wavfiles.remove('.DS_Store')
	random.shuffle(wavfiles)
	return wavfiles
"""============================================================="""

wavpath = "../processing_hapticspeech/data"
wavfiles = get_wavfiles()

def game_loop():

	gameExit = False
	num_of_files = len(wavfiles)
	file_index = 0

	playwav(file_index)

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
						playwav(file_index)

				if event.key == pygame.K_RIGHT:
					if file_index == num_of_files:
						pass
					else:
						file_index += 1
						playwav(file_index)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					pass

		gameDisplay.fill(white)
		pygame.display.update()
		clock.tick(60)

game_loop()
pygame.quit()
quit()