d = {0: [2, 3], 3: [1, 5], 4: [6, 2]}
a = 0
fl = 0
pos = 2
for i in d.copy():
    if a == i:
        d[i][1] += 1
        fl = 1
        break
if fl == 0:
    d.update({a: [pos, 1]})
fl = 0

print(d)
