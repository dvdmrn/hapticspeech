from os import listdir
from os.path import isfile, join
import random

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

def constructPath(path,filename):
	filepath = join(path, filename)
	return filepath

def get_token(filename):
    first = filename.index('_')
    second = filename.index('_', first + 1)
    return filename[first+1:second]