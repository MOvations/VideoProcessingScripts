from datetime import datetime as dt
import logging, os, time, shutil, pickle, pprint

log_location = "D:\\Dropbox\\FileShares\\Scripts\\Log"

now = dt.now().strftime("%d/%m/%y %H:%M")
print(now)

track = {}
if os.path.exists(str(log_location + "\\pick")):
    with open(str(log_location + "\\pick"), "rb") as p:
        track = pickle.load(p)

pprint.pprint(track)

# No need to re-write the file, 'with' statement closes the file on completeion of load
# with open(str(log_location + "\\pick"), "wb") as p:
#     pickle.dump(track, p)
