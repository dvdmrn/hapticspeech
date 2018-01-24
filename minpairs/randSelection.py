from random import *
import csv

toWrite = []




def writeCSV(listOfDicts):

	with open("pairstospeak.csv", "wb") as csvfile:
		
		fieldnames = ["ID", "p0", "p1"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
		writer.writeheader()
		writer.writerows(listOfDicts)

with open('minimalpairs.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	rows = list(reader)
	numOfRows = len(rows)

	for i in range(0,100):
		selection = randint(1,numOfRows)
		print "selecting "+str(rows[selection])
		toWrite.append(rows[selection])
	writeCSV(toWrite)

# print randint(0,100)
# print randint(0,100)
# print randint(0,100)
# print randint(0,100)