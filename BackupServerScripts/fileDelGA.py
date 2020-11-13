### This program checks folders for additions, and moves them upon arrival ###

from datetime import datetime as dt
import logging, os, time, shutil, pickle, pprint, copy

### Functions ###
def removeFile(ky, loctn):

    # Probably a good idea to change cwd
    os.chdir(loctn)
    # find all the folders, because I didn't pass them
    # a bit of a waste, but may be more universal
    for f in os.listdir(loctn):
        path = os.path.join(loctn, f)
        if os.path.isdir(path):
            # print(path + "\\" + str(key))
            if os.path.exists(path + "\\" + str(key)):
                os.remove(path + "\\" + str(key))
            else:
                # print("File Does Not Exist Here")
                continue
        else:
            continue


### Filel locations ###
# Note, there may be times to use  "."
staticsBaseDir = "D:\\Dropbox\\FileShares\\Statics"
### LOGGING ###
log_location = "D:\\Dropbox\\FileShares\\Scripts\\Log"

track = {}
if os.path.exists(str(log_location + "\\pick")):
    with open(str(log_location + "\\pick"), "rb") as f:
        track = pickle.load(f)
pprint.pprint(track)

for key in list(track):
    if "coy" and "mow" and "repoGA" and "repoSL" and "repoATX" in track[key]:
        print("File {} exits in all locations, Deleting".format(key))
        removeFile(key, staticsBaseDir)
        track.pop(key)
    elif "coy" and "repoGA" and "repoSL" and "repoATX" in track[key]:
        # IF this is a webshow
        webShows = staticsBaseDir + "\\WebShows\\" + key
        print(webShows)
pprint.pprint(track)

with open(str(log_location + "\\pick"), "wb") as f:
    pickle.dump(track, f)

