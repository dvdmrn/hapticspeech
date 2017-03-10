import scipy.io.wavfile
import sounddevice as sd 

filename = "PHRASE_dramatist_female_edited.wav"
thing = scipy.io.wavfile.read(filename)

for x in thing[1]:
	sd.play(x, 44100)
# data, sample_frequency,encoding = wavread(filename)