from __future__ import division
import os
import csv
import random
import utilities as util
import playback
#----------------------------------------------------------------------
csvpath = 'calibrationLogs.csv'

consoleSys = 'windows' # set to 'windows' or 'unix'

wordspath = "stimuli/calibrationassist/words/"
phrasespath = "stimuli/calibrationassist/phrases/"

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# main function
# returns: nothing
def main():
	calibrated = False #for main loop
	#check os for console formatting
	wavpath = ""
	if consoleSys == 'windows':
		clear = 'cls'

	# Intro setup
	# determine whether use is calibrating words or phrases
	correct_Entry = False
	typeOfCal = raw_input("Are you calibrating words or phrases? \n")
	while correct_Entry == False:
		if typeOfCal == "Words" or typeOfCal == "words":
			correct_Entry = True
			wavfiles = util.get_wavfiles(wordspath)
			# implement the set of words later
			# run the calibration loop for words
			main_loop(calibrated, clear, wordspath, wavfiles)
		elif typeOfCal == "Phrases" or typeOfCal == "phrases":
			correct_Entry = True
			wavfiles = util.get_wavfiles(phrasespath)
			# run the calibration loop for phrases
			main_loop(calibrated, clear, phrasespath, wavfiles)
		else:
			typeOfCal = raw_input("Please enter 'words' or 'phrases': \n")

#----------------------------------------------------------------------
# main loop for phrases as a function
#
# Boolean, Dict
# returns : None
# def main_phrases(calibrated, phrases):
# 	clear = 'clear' 
# 	correctResponses = 0
# 	sumOfScores = 0
# 	trialNumber = 0
# 	blockNumber = 1 
# 	participantID = 0

# 	participantID = raw_input("participant ID: \n")
# 	print "Callibrate accuracy to ~33%\n"
# 	print("Input the number of lexical category items that the subject identifies \ncorrectly as the score")
# 	print("")

# 	for i in phrases:
# 		trialNumber+=1
# 		print("Phrase: " + i)
# 		print("Lexical Words: " + str(phrases[i]))
# 		var = raw_input("Score: ")
		
# 		# score
# 		if var=="0" or var=="1" or var=="2" or var=="3":
# 			os.system(clear) #refresh screen
# 			correctResponses = int(var)
# 			sumOfScores += int(var)/phrases[i]
# 			accuracy = calcAverage(sumOfScores,trialNumber)
# 			print " _________\n| block "+str(blockNumber)+" |\n------------------------------------"
# 			print accuracyFormatting(accuracy)
# 			print "| trial score: "+str(correctResponses)+" out of "+str(phrases[i])+"| trial n: "+str(trialNumber)+"\n"
			
# 		#new block
# 		if var=="new":
# 			os.system(clear)
# 			correctResponses = 0
# 			trialNumber = 0
# 			blockNumber +=1
# 			print " _________\n| block "+str(blockNumber)+" |\n------------------------------------\n\nNew block!"
		
# 		#exit program
# 		if var == "done" or var == "exit":
# 			exit()

# 		#resets vars
# 		if var == "reset":
# 			os.system(clear)
# 			trialNumber = 0
# 			correctResponses = 0
# 			accuracy = 0
# 			print " _________\n| block "+str(blockNumber)+" |\n------------------------------------"
# 			print("| accuracy: "+str(accuracy))
# 			print "| trial score: "+str(correctResponses)+"| trial n: "+str(trialNumber)+"\n"
# 			print("block settings reset!")

# 		#start again
# 		if var == "nuclear option":
# 			confirm = raw_input("Will completely wipe history, are you sure? (y/n): ")
# 			if (confirm=="y"):
# 				os.system(clear)
# 				trialNumber = 0
# 				correctResponses = 0
# 				blockNumber = 0
# 				accuracy = 0
# 				print " _________\n| block "+str(blockNumber)+" |\n------------------------------------"
# 				print("| accuracy: "+str(accuracy))
# 				print "| trial score: "+str(correctResponses)+"| trial n: "+str(trialNumber)+"\n"
# 				print("Complete reset!")

# 		#exports csv
# 		if var == "export":
# 			noiseLevels = raw_input("noise level: ")
# 			signalLevels = raw_input("signal level: ")
# 			placement = raw_input("actuator placement: ")
# 			confirm = raw_input("confirm? (y/n): ")

# 			if confirm == "y":
# 				print "    writing to file: `"+csvpath+"`..."
# 				writeCSV(participantID,noiseLevels,signalLevels,placement)
# 				print "    Complete!"
		
# 		#user help
# 		if var == "...":
# 			print "    commands:\n        y: correct response\n        n: incorrect response\n        new: initiate new block\n        export: export .csv\n        reset: reset the current block (if you made a mistake)\n        nuclear option: complete reset (start again from block 1)\n        exit: exit program"

#----------------------------------------------------------------------
# main loop for words as a function
#
# Boolean
# returns : None

def main_loop(calibrated, platform,path,wavfiles):
	clear = platform 
	correctResponses = 0
	trialNumber = 0
	blockNumber = 1 
	participantID = 0

	fileIndex = -1

	participantID = raw_input("participant ID: \n")
	print "Callibrate accuracy to ~33%\n" 
	var = raw_input("input 'y' for correct, 'n' for incorrect, and 'new' to initiate a new block\n>")

	#main loop---------------------------------------------------
	while calibrated==False:
		trialNumber += 1
		fileIndex += 1
		if (len(wavfiles)<fileIndex+1):
			exit()

		#correct
		if var=="Y" or var=="y":
			os.system(clear) #refresh screen

			correctResponses+=1
			accuracy = calcAverage(correctResponses,trialNumber)
			 
			print " _________\n| block "+str(blockNumber)+" |\n------------------------------------"
			print accuracyFormatting(accuracy)
			print "| correct: "+str(correctResponses)+"| trial n: "+str(trialNumber)+"\n"
		#incorrect
		if var=="N" or var=="n":
			os.system(clear)
			accuracy = calcAverage(correctResponses,trialNumber)
			print " _________\n| block "+str(blockNumber)+" |\n------------------------------------"
			print accuracyFormatting(accuracy)
			print "| correct: "+str(correctResponses)+"| trial n: "+str(trialNumber)+"\n"
		
		#new block
		if var=="new":
			os.system(clear)
			correctResponses = 0
			trialNumber = 0
			blockNumber +=1
			print " _________\n| block "+str(blockNumber)+" |\n------------------------------------\n\nNew block!"
		
		#exit program
		if var == "done" or var == "exit":
			exit()

		#resets vars
		if var == "reset":
			os.system(clear)
			trialNumber = 0
			correctResponses = 0
			accuracy = 0
			print " _________\n| block "+str(blockNumber)+" |\n------------------------------------"
			print("| accuracy: "+str(accuracy))
			print "| correct: "+str(correctResponses)+"| trial n: "+str(trialNumber)+"\n"
			print("block settings reset!")

		#start again
		if var == "nuclear option":
			confirm = raw_input("Will completely wipe history, are you sure? (y/n): ")
			if (confirm=="y"):
				os.system(clear)
				trialNumber = 0
				correctResponses = 0
				blockNumber = 0
				accuracy = 0
				print " _________\n| block "+str(blockNumber)+" |\n------------------------------------"
				print("| accuracy: "+str(accuracy))
				print "| correct: "+str(correctResponses)+"| trial n: "+str(trialNumber)+"\n"
				print("Complete reset!")

		#exports csv
		if var == "export":
			noiseLevels = raw_input("noise level: ")
			signalLevels = raw_input("signal level: ")
			placement = raw_input("actuator placement: ")
			confirm = raw_input("confirm? (y/n): ")

			if confirm == "y":
				print "    writing to file: `"+csvpath+"`..."
				writeCSV(participantID,noiseLevels,signalLevels,placement)
				print "    Complete!"
		
		#user help
		if var == "...":
			print "    commands:\n        y: correct response\n        n: incorrect response\n        new: initiate new block\n        export: export .csv\n        reset: reset the current block (if you made a mistake)\n        nuclear option: complete reset (start again from block 1)\n        exit: exit program"

		print "------------------------------------\n    playing: "+wavfiles[fileIndex]+"\n"
		playback.normal_playback(path+wavfiles[fileIndex])
		var = raw_input("[y | n | new | export | ...]\n> ")


#----------------------------------------------------------------------
# calcAverage
# calculates a mean.
#
# Int correct
# Int trials
# returns: Float
def calcAverage(correct,trials):
	return correct/trials

#----------------------------------------------------------------------
# writeCSV
# Writes a CSV file
#
# String pID (participant ID)
# String noise (noise level)
# String signal (signal level)
# String placement (placement)
# returns: nothing
def writeCSV(pID,noise,signal,placement):
	prevCSV = readCSV(csvpath)
	with open(csvpath, 'wb') as csvfile:
	    writer = csv.writer(csvfile, delimiter=',',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    for row in prevCSV:
	    	writer.writerow(row)
	    writer.writerow([pID,noise,signal,placement])

#----------------------------------------------------------------------
# readCSV
# Gets contents of a csv
#
# String csvpath (path to .csv)
# Returns: List
def readCSV(csvpath):
	csvSoFar = []
	with open(csvpath) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			csvSoFar.append(row)
		return csvSoFar
#----------------------------------------------------------------------
# accuracyFormatting
# pretty formatting if within a certain scope
#
# Float accuracy
# returns: String
def accuracyFormatting(accuracy):
	if accuracy > 0.29 and accuracy < 0.4:
		return "| accuracy: *~"+str(accuracy)+"~*"
	else:
		return "| accuracy: "+str(accuracy)

#----------------------------------------------------------------------
# read CSV file for phrases and store in a dictionary
# order of phrases in the dictionary is randomized
#
# String csv path
# returns: dictionary
def readCSV_Phrases(csvPath):
	# reads the csv and stores items in each row as a 
	# list element in a list
	listOfPhrases = readCSV(csvPath)
	# get rid of the first element ['phrase', 'lexicalCount']
	listOfPhrases.pop(0)
	# randomize the order of the phrases
	random.shuffle(listOfPhrases)
	# find out how many phrases there are
	numOfPhrases = len(listOfPhrases)
	phrases = {}
	# store each row as a key:value pair in a dictionary
	for i in range(numOfPhrases):
		phrases[listOfPhrases[i][0]] = int(listOfPhrases[i][1])
	return phrases

#----------------------------------------------------------------------


main()


