import numpy
import json
import sys
import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

with open(sys.argv[1]) as f:
    data = json.load(f)

    res = []
    cnt = 0

    for item in data:
        dur = (item['end'] - item['start']) // 1000

        if dur > 60:
            res.append(dur)

        else:
            cnt += 1

    plt.hist(res, bins=250, range=(0, 86400))
    plt.show()

    print(cnt)
