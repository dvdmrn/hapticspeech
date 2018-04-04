from os import listdir, walk
from os.path import isfile, join
import random
import re
import csv
import tqdm


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

        Randomly encodes vibration style

    """
    print("in get_minpairs")
    male_files = []
    female_files = []
    wavfiles = []
    minPairs = []
    playList = []
    global minpairMap

    # get mappings of minpairs
    print("constructing minpair mappings with minpairmap.csv")
    with open(join(path,"minpairmap.csv")) as mpmap:
        reader = csv.DictReader(mpmap)
        for row in reader:
            # print("appending row",row)
            minpairMap.append(row)

    temp_wavfiles = listdir(path)
    # print("temp_wavfiles",temp_wavfiles)
    
    if '.DS_Store' in temp_wavfiles:
        temp_wavfiles.remove('.DS_Store')
    
    print("searching subdirectories for matching IDs")
    for row in tqdm.tqdm(minpairMap):
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
                mpsToAdd.append(join(root,f))

        # for filename in temp_wavfiles:
        #     if idToFind in filename:
        #         print("FOUND MATCH:",idToFind,filename)
        mpSet["ID"] = idToFind
        mpSet["DATA"] = mpsToAdd
        if mpSet["DATA"]:
            minPairs.append(mpSet)
    print "MP len: "+str(len(minPairs))

    for e in minPairs:
        random.shuffle(e["DATA"])
        playList.append(e["DATA"][0])
   
    # print "playList: "+str(playList)

    minPairVibMap = [] # array of dicts [{"vib_style":lowfi,"file":file.wav}, ...]
    styleSegmentation = len(playList)/3 # assumes no. of supplied stim are divisible by 3

    random.shuffle(playList)
    namp = 0
    nlowfi = 0
    nctrl = 0
    for i in range(0,len(playList)):
        if i % 3 == 0:
            minPairVibMap.append({"vib_style":"amp","file":playList[i]})
            namp += 1
        elif i % 2 == 0:
            minPairVibMap.append({"vib_style":"lowfi","file":playList[i]})
            nlowfi += 1
        else:
            minPairVibMap.append({"vib_style":"ctrl","file":playList[i]})
            nctrl += 1

    assert namp == nlowfi == nctrl == styleSegmentation

    return minPairVibMap


def getFilePaths(mapping):
    paths = []
    for e in mapping:
        paths.append(e["file"])
    return paths

def constructPath(path,filename):
	filepath = join(path, filename)
	return filepath

def get_token(filename):
    first = filename.index('_')
    second = filename.index('_', first + 1)
    return filename[first+1:second]