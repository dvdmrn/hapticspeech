import json


with open('stimuli.json') as f:
    data = json.load(f)

print data['assess']["female"]
