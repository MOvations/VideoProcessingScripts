#############################################################
#  I used this on movie frles is ATX, noticed it overwrites files and will take some
# time when doing so. Should fix that, also need to find a way to handly TV shows
# ############################################################
import os, sys, shutil

# dr = sys.argv[1]  # If sending as a cmd argument
dr = "N:\\Entertainment\\TestFILES\\"  # Define directory in code


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


for f in os.listdir(dr):
    fsrc = path(dr, f)
    if os.path.isfile(fsrc):
        s = f[0]

        # Ignore articles as first letter
        if f[:4].lower() == "the ":
            s = notSpace(4, f)
        elif f[:3].lower() == "an ":
            s = notSpace(3, f)
        elif f[:2].lower() == "a ":
            s = notSpace(2, f)

        print(f"{f} will be moved to {s} unless it is a number")

        target = path(dr, s.upper()) if s.isalpha() else path(dr, "#")

        #  Does the file already exist?
        if not os.path.exists(target):
            os.mkdir(target)
        shutil.move(fsrc, path(target, f))  # comment out for testing purposes
