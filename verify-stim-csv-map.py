from __future__ import print_function
from os import listdir, walk
from os.path import isfile, join
import random
import re
import csv
import tqdm


def getMinPairAudioFiles(path):
	print("in get_minpairs")
	male_files = []
	female_files = []
	wavfiles = []
	minPairs = []
	playListAmp = []
	playListCtrl = []
	minPairMap = []

	# get mappings of minpairs
	with open(join(path,"minpairmap.csv")) as mpmap:
	    reader = csv.DictReader(mpmap)
	    for row in reader:
	        # print("appending row",row)
	        minPairMap.append(row)

	temp_wavfiles = listdir(path)
	# print("temp_wavfiles",temp_wavfiles)

	if '.DS_Store' in temp_wavfiles:
	    temp_wavfiles.remove('.DS_Store')


	# look for minpair ID match ------------------------------

 	for row in minPairMap:
	    # makes mp sets such that:
	    # {"mpID":["wave1.wav","wave2.wav", ..."waveN.wav"]}
	    mpSet = {}
	    idToFind = str(row["ID"])
	    mpsToAdd = [] # list of paths that match mpID

	    # search all subdirectories for matching IDs

	    for root, subFolders, files in walk(path):  
	      for f in files:
	        idMatch = re.findall(r'\d+', f)
	        try:
	            idStr = idMatch[0]
	        except:
	            idStr = "NO"
	        # TODO: strong match
	        # because 7 in 127 so .*7.* counts :'(
	        if idToFind == idStr:
	            # print("FOUND MATCH:",idToFind,f)
	            verifyID(f,row,idStr)
	            mpsToAdd.append(join(root,f))

	    # for filename in temp_wavfiles:
	    #     if idToFind in filename:
	    #         print("FOUND MATCH:",idToFind,filename)
	    mpSet["ID"] = idToFind
	    mpSet["DATA"] = mpsToAdd

def verifyID(file,row,id):
	if not ((row["p0"] in file) or (row["p1"] in file)):
		print("could not find congruent word for id: ",id)
		print("    wav: ",file," pairs in csv: ",row["p0"],"/",row["p1"])



getMinPairAudioFiles("stimuli/")