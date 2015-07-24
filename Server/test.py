r=open("Errored Data (processing).txt", "r")


print 1
from functions import processdata
print 1
xs="9.81"
ys="9.81"
zs="9.81"
#print str(processdata("^^^^^^^^^^ |-0.47405192| ********** |-0.23523031| ********** |9.60015| ##########\n"))
dt = processdata("^^^^^^^^^^ |-0.1388637| ********** |-0.17776948| ********** |9.528324| ##########\n\n\n\n\n\n\n\n")
accdatasx=[]
accdatasy=[]
accdatasz=[]
for i in range(len(dt[0])):
    accdatasx.append(str(float(dt[0][i])))
    accdatasy.append(str(float(dt[1][i])))
    accdatasz.append(str(float(dt[2][i])))

dt = processdata("^^^^^^^^^^ |-0.47405192| ********** |-0.23523031| ********** |9.60015| ##########\n")

for i in range(len(dt[0])):
    accdatasx.append(str(float(dt[0][i])))
    accdatasy.append(str(float(dt[1][i])))
    accdatasz.append(str(float(dt[2][i])))

dt = processdata("^^^^^^^^^^ |-0.47405192| ********** |-0.23523031| ********** |9.60015| ##########\n")

for i in range(len(dt[0])):
    accdatasx.append(str(float(dt[0][i])))
    accdatasy.append(str(float(dt[1][i])))
    accdatasz.append(str(float(dt[2][i])))

print accdatasx,accdatasy,accdatasz
