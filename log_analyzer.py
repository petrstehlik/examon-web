import json
import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

res = {}

with open('output_160.log') as f:
    content = f.readlines()
    for line in content:
        cols = line.split(':')

        if cols[0] == 'INFO' and cols[1] == 'network':
            metric = cols[2]

            if metric not in res:
                res[metric] = {
                    'x': [],
                    'y': [],
                }
            eperr = cols[3].split(',')

            epoch = int(eperr[0].split('=')[1].strip())
            error = float(eperr[1].split('=')[1].strip())

            res[metric]['x'].append(epoch)
            res[metric]['y'].append(error)

f, axarr = plt.subplots(7,2)

for i, metric in enumerate(res):
    axarr[i%7, (i % 2)].plot(res[metric]['x'][1:], res[metric]['y'][1:])
    axarr[i%7, (i % 2)].set_title(metric)
    axarr[i%7, (i % 2)].set_ylim(0)

plt.show()
