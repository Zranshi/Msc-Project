import matplotlib.pyplot as plt
from collections import defaultdict

with open("./output.txt", "r") as f:
    lines = f.readlines()

plt.rcParams.update({"font.size": 10})

counters = defaultdict(lambda: 0)
for line in lines:
    (index, mapping, counter) = line.split("|")
    counter = int(counter)
    counters[counter] += 1

elses = []
visable = []
for k, v in counters.items():
    if v<150:
        elses.append(k)
    else:
        visable.append(k)

keys, values = [], []
for k in visable:
    keys.append(k)
    values.append(counters[k])

elses_value = 0
for k in elses:
    elses_value += counters[k]

keys.append("else")
values.append(elses_value)



fig, ax = plt.subplots()

ax.pie(values, labels=keys)

plt.show()
