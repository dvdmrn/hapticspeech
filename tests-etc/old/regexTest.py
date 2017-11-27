import re

m = re.search('\_.*\_', 'asdfasdf_ooooooop_fdsav_poop.wav')
m.group(0)
print(m.group(0)[1:-1])