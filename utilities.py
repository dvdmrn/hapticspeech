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

def get_wavfiles():
    path = "stimuli/"
    # put names of wavfiles in a list
    wavfiles = [f for f in listdir(path) if isfile(join(path, f))]
    if '.DS_Store' in wavfiles:
        wavfiles.remove('.DS_Store')
    random.shuffle(wavfiles)
    return wavfiles

def constructPath(path,filename):
	filepath = join(path, filename)
	return filepath
