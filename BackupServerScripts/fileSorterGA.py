### This program checks folders for additions, and moves them upon arrival ###

from datetime import datetime as dt
import logging, os, time, shutil, pickle, pprint

### Funcations ###
def move(src, dest):
    """Simply Moves a file given Source and Destination and Try/Except"""
    if not os.path.exists(dest):
        # Try/Except loop in case file is being transfered
        try:
            # move(this_file, to_that_file)
            shutil.move(src, dest)
            # logging.info("Added to {}: \t".format(d)  + to_that_file)
        except Exception:
            print("Whoops, file in use")  # Debug to capture
            pass
    else:
        print("File already exists: {}".format(dest))


def copy(src, dest):
    """Simply COPIES a file given Source and Destination, preserves meta data"""
    if not os.path.exists(dest):
        # Try/Except loop in case file is being transfered
        try:
            shutil.copy2(src, dest)
            # logging.info("Added to {}: \t".format(d)  + to_that_file)
        except Exception:
            print("Whoops, file in use")  # Debug to capture
            pass
    else:
        print("File already exists: {}".format(dest))


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


### Filel locations ###
# Note, there may be times to use  "."
staticsBaseDir = "D:\\Dropbox\\FileShares\\Statics"
sources = {
    "mow": "D:\\Dropbox\\FileShares\\Mowery\\toMO",
    "coy": "D:\\Dropbox\\FileShares\\Coy\\toMark",
}
destinations = {
    "repoGA": "N:\\Entertainment",
    "coy": "D:\\Dropbox\\FileShares\\Coy\\toCoy",
    "mow": "D:\\Dropbox\\FileShares\\Mowery\\toMOW",
}

### LOGGING ###
log_location = "D:\\Dropbox\\FileShares\\Scripts\\Log"
# logging.basicConfig(
#     filename=str(log_location + "\\" + "Sorter.log"),
#     level=logging.INFO,
#     format="%(asctime)s:%(levelname)s:%(message)s",
# )
# Here I pickle a tacking file so that I can delete the files once they've hit all destinations
track = {}
if os.path.exists(str(log_location + "\\pick")):
    with open(str(log_location + "\\pick"), "rb") as p:
        track = pickle.load(p)

# Some other variables
delay = time.sleep(1)  # how often to check folders, 60 sec
sep = "\n\t"
before = []


### Move Content from Mowery and Coy to Statics Dir ###
for source, location in sources.items():
    os.chdir(location)
    all_subdirs = [d for d in os.listdir(".") if os.path.isdir(d)]
    print("Folders: {}: {}".format(source, all_subdirs))

    # Loop over folders here
    for d in all_subdirs:
        # Clever way to track subfolder changes (For RealTime tracking, i.e., future work)
        # to ONLY drop in statics
        after = newFiles(location + "\\" + str(d))
        # Only use "added" for now
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        before = after

        # make sure target folder exists in STATICS
        folder_sub = str(staticsBaseDir) + "\\" + str(d)
        if not os.path.exists(folder_sub):
            os.makedirs(folder_sub)

        # Loop over files in subfolders and MOVE files to STATICS
        for file, target in after.items():
            this_file = str(target) + "\\" + str(file)
            to_that_file = str(folder_sub) + "\\" + str(file)
            if not str(file) in track.keys():
                track.setdefault(str(file), [])
                track[str(file)].append(str(source))
            elif str(file) in track.keys():
                pass
            else:
                track[str(file)].append(str(source))

            print("TO: " + to_that_file)
            move(this_file, to_that_file)


### Move Content from STATICS to repoGA, Mowery, and Coy ###
os.chdir(staticsBaseDir)
all_subdirs = [d for d in os.listdir(".") if os.path.isdir(d)]
print("Folders: {}".format(all_subdirs))

# Loop over folders here
for d in all_subdirs:
    # What's new
    after = newFiles(staticsBaseDir + "\\" + str(d))
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    before = after
    # if added:
    #     logging.info("\n    Added to {}: \n\t".format(d) + sep.join(added))
    # print("REMOVED: " + sep.join(removed))

    ### LOOP OVER DESTINATIONS HERE ###
    for destination, target in destinations.items():
        # Mowery gets a dump, everthing else in folders
        if destination == "mow":
            folder_sub = str(target)
        else:
            folder_sub = str(target) + "\\" + str(d)
            # make sure target folder exists
            if not os.path.exists(folder_sub):
                os.makedirs(folder_sub)

        # Mowery won't need the webshows
        if destination == 'mow' and d == 'WebShows':
            continue        

        # Loop over files in subfolder here
        for file, location in after.items():
            this_file = str(location) + "\\" + str(file)
            to_that_file = str(folder_sub) + "\\" + str(file)

            ### MEAT AND POTATIOES of the copying and tracking ###
            # this bit of nonsense tracks & copies what files go where
            # files will not be returned to Mowery/Coy if they orginated there
            if not str(file) in track.keys():
                track.setdefault(str(file), [])
                track[str(file)].append(str(destination))
                print("TO: " + to_that_file)
                copy(this_file, to_that_file)
            elif str(file) in track.keys():
                if str(destination) in track[str(file)]:
                    pass
                else:
                    track[str(file)].append(str(destination))
                    print("TO: " + to_that_file)
                    copy(this_file, to_that_file)
            else:
                track[str(file)].append(str(destination))
                print("TO: " + to_that_file)
                copy(this_file, to_that_file)

pprint.pprint(track)
with open(str(log_location + "\\pick"), "wb") as p:
    pickle.dump(track, p)


### Reference - Logging Statements ###

# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
