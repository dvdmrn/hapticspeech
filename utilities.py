from os import listdir
from os.path import isfile, join
import random
import re
import csv


minpairMap = []

def translate(value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

def get_wavfiles(path):
    """
        Populates a list of wavfiles and randomizes for gender.
    """

    temp_wavfiles = listdir(path)
    if '.DS_Store' in temp_wavfiles:
        temp_wavfiles.remove('.DS_Store')
    
    male_files = []
    female_files = []
    wavfiles = []
 
    for f in temp_wavfiles:
        if 'female' in f:
            female_files.append(f)
        else:
            male_files.append(f)

    for f in female_files:
        if bool(random.getrandbits(1)):
            wavfiles.append(f)
        else:
            m = f.replace('female', 'male')
            if m in male_files:
                wavfiles.append(m)
            else:
                wavfiles.append(f)

    del male_files
    del female_files
    random.shuffle(wavfiles)
    return wavfiles

def get_minpairs(path):
    """
        Populates a list of wavfiles and randomizes for gender.
    """
    print("in get_minpairs")
    male_files = []
    female_files = []
    wavfiles = []
    minPairs = []
    playList = []
    global minpairMap

    with open("stimuli/minpairmap.csv") as mpmap:
        reader = csv.DictReader(mpmap)
        for row in reader:
            minpairMap.append(row)

    temp_wavfiles = listdir(path)
    if '.DS_Store' in temp_wavfiles:
        temp_wavfiles.remove('.DS_Store')
    
    for row in minpairMap:
        mpSet = {}
        idToFind = str(row["ID"])
        mpsToAdd = []
        for filename in temp_wavfiles:
            if idToFind in filename:
                print("FOUND MATCH:",idToFind,filename)
                mpsToAdd.append(filename)
        mpSet["ID"] = idToFind
        mpSet["DATA"] = mpsToAdd
        if mpSet["DATA"]:
            minPairs.append(mpSet)
    print minPairs

    for e in minPairs:
        random.shuffle(e["DATA"])
        playList.append(e["DATA"][0])
    # for f in temp_wavfiles:
    #     m = re.search('\_.*\_', token) # finds stuff that looks like _this_
    #     formattedToken = m.group(0)[:-1] # strips the _'s
    #     idList.append(formattedToken)
    # idList = set(idList) # gets rid of duplicates
    # idList = list(idList) # converts back to list so it's indexable

    # for f in temp_wavfiles:
    #     if 'female' in f:
    #         female_files.append(f)
    #     else:
    #         male_files.append(f)

    # for f in female_files:
    #     if bool(random.getrandbits(1)):
    #         wavfiles.append(f)
    #     else:
    #         m = f.replace('female', 'male')
    #         if m in male_files:
    #             wavfiles.append(m)
    #         else:
    #             wavfiles.append(f)

    # del male_files
    # del female_files
    # random.shuffle(wavfiles)
    return playList

def constructPath(path,filename):
	filepath = join(path, filename)
	return filepath

def get_token(filename):
    first = filename.index('_')
    second = filename.index('_', first + 1)
    return filename[first+1:second]