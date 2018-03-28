# testIndexes = range(0,180)

# def testIndexStyle(indexes):
#     style1 = 0
#     style2 = 0
#     style3 = 0
#     for e in indexes:
#         if e % 3 == 0:
#             style1 += 1
#         elif e % 2 == 0:
#             style2 += 1
#         else:
#             style3 += 1
#     print("styles:","\n1:",style1,"\n2:",style2,"\n3:",style3)
#     try:
#         assert style1 == style2 == style3
#     except:
#         print("didn't work")

# testIndexStyle(testIndexes)

a = 1
i = "global"
def add1(a):
 return a+1

def testMemory(i):
    print "param location: "+hex(id(i))
    i = add1(a)
    print "new location:   "+hex(id(i))

testMemory(a)
print "global:         "+hex(id(i))