from datetime import datetime as dt
import logging, os, time, shutil, pickle, pprint

### This program checks folders for additions, and moves them upon arrival ###

### Funcations ###
def move(src, dest):
    """Simply Moves a file given Source and Destination
    *Future: have anyother script process the file"""
    shutil.move(src, dest)


def copy(src, dest):
    """Simply COPIES a file given Source and Destination, preserves META data"""
    shutil.copy2(src, dest)


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
baseDir = "D:\\Dropbox\\FileShares\\Statics"
folder_destination = "N:\\Entertainment"
log_location = "D:\\Dropbox\\FileShares\\Scripts\\Log"


delay = time.sleep(1)  # how often to check folders, 60 sec
sep = "\n\t"
now = dt.now().strftime("%d/%m/%y %H:%M")
before = []


### LOGGING ###
logging.basicConfig(
    filename=str(log_location + "\\" + "Sorter.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

track = {}
if os.path.exists(str(log_location + "\\pick")):
    with open(str(log_location + "\\pick"), "rb") as p:
        track = pickle.load(p)

# What folders are present?
os.chdir(baseDir)
all_subdirs = [d for d in os.listdir(".") if os.path.isdir(d)]
print("Folders: {}".format(all_subdirs))

### MAIN ### ##################################################
# Run constantly or a set number of times
i = 0
while i < 1:
    i += 1
    delay

    # Loop over folders here
    for d in all_subdirs:

        folder_drop = baseDir + "\\" + str(d)
        after = newFiles(folder_drop)

        # Cleverly way to track subfolder changes
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        before = after

        # make sure target folder exists
        folder_sub = str(folder_destination) + "\\" + str(d)
        if not os.path.exists(folder_sub):
            os.makedirs(folder_sub)

        # Loop over files in subfolder here
        for file, location in after.items():
            this_file = str(location) + "\\" + str(file)
            to_that_file = folder_sub + "\\" + str(file)
            print(this_file + "\n    TO:   " + to_that_file)

            # Does the file already exist iin the folder?
            if not os.path.exists(to_that_file):
                # Try/Except loop in case file is being transfered
                if not str(file) in track.keys():
                    now = dt.now().strftime("%d/%m/%y %H:%M")
                    track.setdefault(str(file), [str(now)])
                    track[str(file)].append(str("repoSL"))
                else:
                    track[str(file)].append(str("repoSL"))

                try:
                    copy(this_file, to_that_file)
                    logging.info("Added to {}: \t".format(d) + to_that_file)
                except Exception:
                    print("Whoops there it is")  # Debug to capture
                    pass
            else:
                print("\n File already exists: {}".format(to_that_file))

        # if added:
        #     logging.info("\n    Added to {}: \n\t".format(d) + sep.join(added))
        print("REMOVED: " + sep.join(removed))

pprint.pprint(track)
with open(str(log_location + "\\pick"), "wb") as p:
    pickle.dump(track, p)

### Reference - Logging Statements ###

# DEBUG: Detailed information, typically of interest only when diagnosing problems.
# INFO: Confirmation that things are working as expected.
# WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR: Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
