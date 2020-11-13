from datetime import datetime as dt
import logging, os, time, shutil, pickle, pprint, copy
from pathlib import Path
import subprocess
from subprocess import call
import send2trash

### HandBrake File Settings ###
hb_CLI = "D:\\Staging\\HandBrakeCLI.exe"
configLoc = "D:\\Staging\\SHQRF232.json"
HBDir = "D:\\Staging\\toHB\\"
FinDir = "D:\\Finished\\"
PODir = "D:\\Staging\\fromPlayOn\\"

# the command that replicates the batch script:
# copies all mp4 files from playon folder to their staging location
cmd = 'for /r "D:\\Playon\\" %x in (*.mp4) do move "%x" "D:\\Staging\\fromPlayOn\\"'
print(cmd)
os.system(cmd)

delay = time.sleep(3)
delay

files = os.listdir(PODir)
print(files)

for file in files:
    # copy the filename for comparison later
    orginal = copy.deepcopy(file)

    # crap to filter out:
    file = file.replace("&", "")
    file = file.replace(":", "")
    file = file.replace("+", "")
    file = file.replace("*", "")
    file = file.replace("?", "")
    file = file.replace("!", "")
    file = file.replace("^", "")
    file = file.replace("%", "")
    file = file.replace("$", "")
    file = file.replace("#", "")
    file = file.replace("~", "")
    file = file.replace("@", "")

    if orginal != file:
        src = PODir + orginal
        dst = PODir + file
        print("{}\n{}".format(src, dst))
        os.rename(str(src), str(dst))
    else:
        pass

delay

before = os.listdir(HBDir)
##### DO THE AVIDEMUX THING ######

command = "D:\\Dropbox\\FileShares\\Scripts\\The Actual Scripts that do the things\\Avidemux\\TrimPlayOnSplashScreenSL_Rev2C.exe"
# command = command.replace(" ", "\\ ")
print(command)
subprocess.call([command])

files = os.listdir(PODir)
print("Removing the following files from 'fromPlayOn': ")
print(files)
for file in files:
    # os.remove(PODir + file)                             # Perma delete
    send2trash.send2trash((PODir + file))           # Sends to recycle

##### DO THE HANDBRAKE THING ######


def cli(src, dst):
    call(
        [
            hb_CLI,
            "--preset-import-file",
            configLoc,
            "-e",
            "qsv_h265",
            "-i",
            src,
            "-o",
            dst,
        ]
    )
    print("Copying: {}\n To: {}".format(src, dst))


def newFiles(folder_to_track):
    # vidDict = dict([(f, folder_to_track) for f in os.listdir(folder_to_track)])
    fileDict = {}
    for f in os.listdir(folder_to_track):
        path = os.path.join(folder_to_track, f)
        if os.path.isdir(path):
            # skip directories
            continue
        else:
            fileDict[f] = folder_to_track
    return fileDict


after = os.listdir(HBDir)
added = [f for f in after if not f in before]
removed = [f for f in before if not f in after]
print("New: {}".format(added))
print("Existing: {}".format(before))
time.sleep(10)

for file in added:
    print("working on: {}".format(file))
    src = HBDir + str(file)
    dst = FinDir + str(file)
    cli(src, dst)


print("Removing the following files from 'ftoHB': ")
print(files)
for file in files:
    # os.remove(PODir + file)                             # Perma delete
    send2trash.send2trash((HBDir + file))           # Sends to recycle
