#############################################################
#  I used this on movie frles is ATX, noticed it overwrites files and will take some
# time when doing so. Should fix that, also need to find a way to handly TV shows
# Will simply move files into folders,
# next step will be to examine metadata, rename, then organize into season folders
# ############################################################
import os, re, sys, shutil

# dr = sys.argv[1]  # If sending as a cmd argument
dr = "D:\\MoveTEST"  # Define directory in code
# dr = "N:\\Entertainment\\ShowsTV"

corrected = {
    "SHAMELESS": "SHAMELESS (US)",
    "THE MORNING SHOW": "THE MORNING SHOW (2019)",
    "ITS ALWAYS SUNNY IN PHILADELPHIA": "IT'S ALWAYS SUNNY IN PHILADELPHIA",
    "COMEDIANS IN CARS GETTING COFFEE": "CICGC",
}


def path(dr, f):
    """ Creates the path to the target file based on directory 'dr' and filename 'f' """
    return os.path.join(dr, f)


def notSpace(n, f):
    """ Finds the next character after a space """
    s = f[n]
    while s.isspace() == True:
        # print("In loop") #DEBUG
        n += 1
        s = f[n]
    return s


def cleanChar(s):
    """ Cleans the characters in a string to be used to create a filename or Folder """
    for c in "~`!@#$%$^&*_=-/?":
        s = s.replace(c, "")

    # everything I could think of to deal with whitespace nonsense
    s = s.replace("    ", " ")
    s = s.replace("   ", " ")
    s = s.replace("  ", " ")
    s = s.strip()

    s = s.upper()
    s = cleanMeta_Filename(s)
    return s.upper()


def cleanMeta_Filename(s):
    """ Defines a dictionary of filenames to correct video file imports for other services to correctly get metadata (PLEX, MetaX) """

    for c in corrected.keys():
        if s == c:
            s = corrected[c]
            print(f"Correcting {c} to {s}")
    return s


for f in os.listdir(dr):
    fsrc = path(dr, f)
    if os.path.isfile(fsrc):
        regex = re.compile("[sS]\d{1,2}")
        m = re.search(regex, f)
        if m != None:
            s = f[: m.start()]
            print(f"{f} will be moved to {s} unless it is a number")
            target = path(dr, cleanChar(s))
            print(target)

            #  Does the file already exist?
            if not os.path.exists(target):
                os.mkdir(target)

            if not os.path.exists(path(target, f)):
                shutil.move(fsrc, path(target, f))  # comment out for testing purposes
                pass
            else:
                dupes = path(dr, "Dupes")
                if not os.path.exists(dupes):
                    os.mkdir(dupes)
                # Probably add ability to compare meta/file info here (FUTURE)
                shutil.move(fsrc, path(dupes, f))

        else:
            pass
