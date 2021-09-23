import os
import numpy
with open('final', 'r') as f:
    ll = f.readlines()

Matrix = numpy.zeros((8,8), dtype=int)

for l in ll:
    d = l.lstrip().rstrip().split(" ")
    x, y = d[1].split("->")
    if int(x)<=7 and int(y)<=7:
        Matrix[int(x)][int(y)] = int(d[0])

idx = ["EMERG", "ALERT", "CRIT", "ERROR", "WARNING", "NOTICE", "INFO", "DEBUG"]
print("{} & {EMERG} & {ALERT} & {CRIT} & {ERR} & {WARNING} & {NOTICE} & {INFO} & {DEBUG}\\\ ")
print("\midrule")
for i in range(8):
    out = '{0} & {1} & {2} & {3} & {4} & {5} & {6} & {7} & {8} \\\\'.format(idx[i], Matrix[i][0], Matrix[i][1], Matrix[i][2], Matrix[i][3],Matrix[i][4], Matrix[i][5], Matrix[i][6], Matrix[i][7])
    print(out)
   
sum = 0
for i in range(8):
    for j in range(8):
        if i != j:
            sum += Matrix[i][j]
            
print("Total changes: " + str(sum))

sum = 0
for i in range(8):
    for j in range(8):
        if i == 3 or i == 4 or i == 6 or i == 7:
            if j == 3 or j == 4 or j == 6 or j == 7:
                if i != j:
                    sum += Matrix[i][j]
            
print("changes between ERR, WARNING, INFO, and DEBUG levels: " + str(sum))
