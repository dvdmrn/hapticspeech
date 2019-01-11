import csv

inputFile = 'responses2.csv'

def gradeCSV(): 
	# Constructs a graded list of dicts
	# gives the list of dicts to writeCSV

	listOfDicts = []
	with open(inputFile) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			print (row ['Response'], row ['Token'])
			grade = row ['Response'] == row ['Token']

			row['Grade'] = grade

			listOfDicts.append(row)
			print listOfDicts

	writeCSV(listOfDicts)

def writeCSV(listOfDicts):
	
	outputFileName = inputFile[0:-4]+ '_graded.csv'

	with open(outputFileName, 'w') as csvfile:
		customheaders = ['Response', 'Token', 'Grade']
		writer = csv.DictWriter(csvfile, fieldnames = customheaders)

		writer.writeheader()

		for dictObject in listOfDicts:
			writer.writerow(dictObject)


gradeCSV()





		


