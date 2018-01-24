import re
import getpages
import csv

file = open("source.html","r")
identifier = 0
dataToWrite = []
matches = []

def findLink(s):
	match = re.findall('A HREF="\w+.html">[0-9]+</A></TD>', s)
	if match:
		return match

def findHtml(s):
	match = re.findall('[a-z]+.html', s)
	if match:
		return match

def compileData(minPairs):
	global identifier
	for element in minPairs:
		if not element:
			break
		pairs = element.split(" ")
		if len(pairs) < 2:
			break
		entry = {}
		entry["ID"] = identifier
		entry["p0"] = pairs[0]
		entry["p1"] = pairs[1]
		print "adding: "+str(entry)
		dataToWrite.append(entry)
		identifier += 1

	return dataToWrite

def writeCSV(listOfDicts):

	with open("minimalpairs.csv", "wb") as csvfile:
		
		fieldnames = ["ID", "p0", "p1"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
		writer.writeheader()
		writer.writerows(listOfDicts)

for line in file:

	match = findLink(line)
	if match:
		matches.append(match)

toSearch = []
for html in matches:
	match = findHtml(html[0])
	if match:
		toSearch.append("http://www.minpairs.talktalk.net/"+match[0])

txtToWrite = ""

acc = 0

print("number of items to search: ",len(toSearch))
for url in toSearch:
	acc += 1
	print "searching: "+url
	minPairs = getpages.getMinPairs(url)
	dataToWrite = compileData(minPairs)

# minPairs = getpages.getMinPairs("http://www.minpairs.talktalk.net/conway.html")
# dataToWrite = compileData("http://www.minpairs.talktalk.net/conway.html")



writeCSV(dataToWrite)
