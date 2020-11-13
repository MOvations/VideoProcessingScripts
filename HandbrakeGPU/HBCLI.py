import os
import datetime as dt
import time
import numpy as np

################################################################################
# This code walks through a series of preset files and compresses the same input
# file using different settings (stored in *.json files)
# (subjectively) optimizing video quality vs file size.
# For the given "MO" presets, quality (subjective) is typically best around or
# one setting lower than the fastest encode time...
# Thus for, similar shows/movies a smaller or singular preset range can be given
# to shorten processing time.
################################################################################


d = []
tbd = [22, 23, 24, 25, 26]
print(tbd[0])

for i in tbd:
    print("The run is {}".format(i))
    start = dt.datetime.now()

    # General form of command to run Handbrake on GPU
    # HandBrakeCLI --preset-import-file saved_preset_filename.json -Z "Name_You_Gave_The_Preset" -i input_filename.mp4 -o output_filename.mp4
    cmd = f'HandBrakeCLI --preset-import-file MO{i}.json -Z "MO{i}" -i INPUT_FILE.mp4 -o OUTPUT_FILE_SETTING{i}.mp4'
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
