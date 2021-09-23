with open("OutFinal_Copy2", "r") as f:
    l = f.readlines()


with open("diff", "r") as f:
    l2 = f.readlines()

for i in range(len(l2)):
    l2[i] = l2[i].rstrip()
    

hashes = []
for i in l:
    h = i.split(",")[0]
    hashes.append(h)
    if h not in l2:
        print(i, end='')


