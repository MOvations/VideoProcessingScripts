import os
import datetime as dt
import time
import numpy as np

d = []
tbd = [22, 23, 24, 25, 26]
print(tbd[0])

for i in tbd:
    print("The run is {}".format(i))
    start = dt.datetime.now()

    cmd = 'HandBrakeCLI --preset-import-file MO{0}.json -Z "MO{1}" -i Stuber.mp4 -o Stuber{2}.mp4'.format(
        i, i, i
    )
    print(cmd)

    os.system(cmd)

    # cmd = "ls -la -{}".format(i)                         # Debugging
    time.sleep(1.5 + np.random.rand())  # for debugging
    end = dt.datetime.now()
    print("Process started at {} and ended at {}".format(start, end))
    delta = end - start
    d.append(delta.seconds)
    print(d)


for j in range(len(d)):
    # Range(len(  fixed some unknown error with for j in d....
    print("Run: {0}  MO{1} Time: {2} sec".format(j, tbd[j], d[j]))
