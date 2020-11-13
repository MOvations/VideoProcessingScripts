from subprocess import call
import ast, copy, os, pickle, pprint, time
from datetime import datetime as dt
from shlex import quote
import re
import subprocess


##### Description ##############################################################
# This program looks for files in my Dropbox folders and moves them to my local
# Plex Server, which in **ATX** is my RaspberryPi with large external USB drives
# Cron job moves any changes ever two hours (setup externally from this script)
#
##### Structure #####
#
# -key, global variables
# -File Location Definitions
# -LOGGING - open pickle (tracks which remote servers have been updated)
# -Functions
# -MAIN ==> loops through any new files found and transfers them
# -LOGGING - update and save pickle file
#
# NOTE: unsure what happens when multiple remotes attempt to modify the pickle
# at the same time. Schedule timing accordingly. No ssues to date.
################################################################################


##### Key Global Variables #####

log_location = "/home/mo/Dropbox/FileShares/Scripts/Log"

# commands for check if file exists on server
opener_ssh = "ssh "
opener_scp = "scp "
server_hostname_ip = "pi@192.168.86.100"  # no space at end of string
identity_key_loc = "-i ~/.ssh/id_RasPi4 "


##### File Location Definitions #####

dropbox_folders = {
    "MoviesBulk": "/home/mo/Dropbox/FileShares/Statics/MoviesBulk/",
    "MoviesSS": "/home/mo/Dropbox/FileShares/Statics/MoviesSS/",
    "ShowsTV": "/home/mo/Dropbox/FileShares/Statics/ShowsTV/",
    "FamAnimated": "/home/mo/Dropbox/FileShares/Statics/FamAnimated/",
    "DocuSeries": "/home/mo/Dropbox/FileShares/Statics/DocuSeries/",
    "WebShows": "/home/mo/Dropbox/FileShares/Statics/WebShows/",
    "ExerciseWorkout": "/home/mo/Dropbox/FileShares/Statics/ExerciseWorkout/",
    "StandUp": "/home/mo/Dropbox/FileShares/Statics/StandUp/",
}

plex_folders = {
    "MoviesBulk": "/media/Plex/Entertainment/MoviesBulk/",
    "MoviesSS": "/media/Plex/Entertainment/MoviesSS/",
    "ShowsTV": "/media/Plex/Entertainment/ShowsTV/",
    "FamAnimated": "/media/Plex/Entertainment/FamAnimated/",
    "DocuSeries": "/media/Plex/Entertainment/Documentaries/",
    "WebShows": "/media/Plex/Entertainment/WebShows/",
    "ExerciseWorkout": "/media/Plex/Entertainment/ExerciseWorkout/",
    "StandUp": "/media/Plex/Entertainment/StandupComedy/",
}

### LOGGING ###

track = {}
if os.path.exists(str(log_location + "/pick")):
    with open(str(log_location + "/pick"), "rb") as p:
        track = pickle.load(p)
print("\n\n##################### PICKLE FILE ##################################")
pprint.pprint(track)
print("####################################################################")


##### Functions #####


##### MAIN #####

for fold in dropbox_folders:
    # print(fold)  # DEBUG
    # print(dropbox_folders[fold])  # DEBUG

    # Associate each file in 'fold' with it's directory path via dict comprehension
    # In general: dict_variable = {key:value for (key,value) in dictonary.items()}
    files = {k: dropbox_folders[fold] for k in os.listdir(dropbox_folders[fold])}
    # print(files)  # DEBUG

    for file in files:
        # print(f"{file[0]} \n\n")  # DEBUG first letter
        original_filename = copy.deepcopy(
            file
        )  # TODO need to replace these in the tracker
        file = file.replace("&", "\\&")  # why do I even allow this in my naming?
        file = file.replace("'", "\\'")
        file = file.replace('"', "\\'")  # swapping sing and double quotes
        file = file.replace(" ", "\\ ")
        file = file.replace(":", "\\:")  # why do I even allow this in my naming?
        file = file.replace(")", "\\)")
        file = file.replace("(", "\\(")
        file = file.replace("+", "\\+")  # why do I even allow this in my naming?
        file = file.replace("*", "\\*")  # why do I even allow this in my naming?
        file = file.replace("?", "\\?")  # why do I even allow this in my naming?
        file = file.replace("!", "\\!")  # why do I even allow this in my naming?
        # print(file) #DEBUG

        # First, check to see if file exists on the server
        # NOTES:
        # ssh -q $HOST [[ -f $FILE_PATH ]] && echo "File exists" || echo "File does not exist";
        # ssh -i $IDENTY_LOC $HOST [[ -f $FILE_PATH ]] && echo "File exists" || echo "File does not exist";
        # Note if you echo the pipe the response will always be zero

        cmd_file_exists = (
            f"{opener_ssh}{identity_key_loc}"
            f' {server_hostname_ip} [[ -f "'
            f'{plex_folders[fold]}{file}" ]]'
        )

        resp = os.system(cmd_file_exists)

        print(f"\nFor ' {file} ' the response was: {resp}")  # DEBUG
        # Tested with:
        # "test 'file'.txt"  'test "file".txt'  'test file!.txt'  'test? file.txt'   testfile.txt
        # and found no errors

        if resp == 0:
            print("Video Found, no need to move!")
            # add to log file
            try:
                if not str("repoATX") in track[str(original_filename)]:
                    track[str(original_filename)].append(str("repoATX"))
                    print("Filename exists in tracker... check naming")
                else:
                    pass
            except:
                pass

        else:
            #     # # cmd = opener + "scp " + OUT[fold] + "*.* " + device + ":" + IN[fold]
            #     # And now for some GD reason the source filename takes the native filename, but the output needs. the nuance
            cmd_copy_file = (
                f"{opener_scp}{identity_key_loc}"
                f"{dropbox_folders[fold]}{file}"
                f" {server_hostname_ip}:"
                f"{plex_folders[fold]}"
            )
            # print(f"Found {file} in {dropbox_folders[fold]} Which is new")
            print("\n" + cmd_copy_file)
            os.system(cmd_copy_file)

        if not str(original_filename) in track.keys():
            now = dt.now().strftime("%d/%m/%y %H:%M")
            track.setdefault(str(original_filename), [str(now)])
            track[str(original_filename)].append(str("repoATX"))
            print("Filename added to tracker")
        elif str(original_filename) in track.keys():
            if str("repoATX") in track[str(original_filename)]:
                print("Filename already in tracker")
                pass
            else:
                track[str(original_filename)].append(str("repoATX"))
                print("Filename added to tracker")
        else:
            track[str(original_filename)].append(str("repoATX"))
            print("Filename added to tracker")

# print the tracking file
print("##################### PICKLE FILE ##################################")
pprint.pprint(track)
print("####################################################################\n\n")

# Need to account for changes made to track since files have been transfered here....
# But How?
with open(str(log_location + "/pick"), "wb") as p:
    pickle.dump(track, p)
