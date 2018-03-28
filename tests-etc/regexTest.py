import re

token = "121_asdf_vf"
m = re.findall(r'\d+', token)
formattedToken = m


print "1" in m[0]
print "121" == m[0]
print m[0]
