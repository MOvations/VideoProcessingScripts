from subprocess import call
import os, time

################################################################################
# Uses MetaX (windows software) to add metadata to files
# Utilizes MetaX's built-in file moving operations
# Thus, input location and output location are specified explicitly
################################################################################

delay = time.sleep(1)
# MetaX location
MetaX = "C:\\Program Files (x86)\\MetaX\\MetaX.exe"

# where the files are sent after adding metadata
destination_folder = {
    "MoviesBulk": "D:\\Dropbox\\FileShares\\Statics\\MoviesBulk",
    "MoviesSS": "D:\\Dropbox\\FileShares\\Statics\\MoviesSS",
    "ShowsTV": "D:\\Dropbox\\FileShares\\Statics\\ShowsTV",
    "FamAnimated": "D:\\Dropbox\\FileShares\\Statics\\FamAnimated",
    "DocuSeries": "D:\\Dropbox\\FileShares\\Statics\\DocuSeries",
    "StandUp": "D:\\Dropbox\\FileShares\\Statics\\StandUp",
}

# source file locations
source_folder = {
    "MoviesBulk": "D:\\Finished\\MoviesBulk",
    "MoviesSS": "D:\\Finished\\MoviesSS",
    "ShowsTV": "D:\\Finished\\ShowsTV",
    "FamAnimated": "D:\\Finished\\FamAnimated",
    "DocuSeries": "D:\\Finished\\DocuSeries",
    "StandUp": "D:\\Finished\\StandUp",
}

for fold in destination_folder:
    print(fold)
    print(destination_folder[fold])

    # print the folder information that's currently being worked on
    print(MetaX, "/A", source_folder[fold], "/AT", destination_folder[fold], "/C")

    if not os.listdir(source_folder[fold]) == []:
        call([MetaX, "/A", source_folder[fold], "/AT", destination_folder[fold], "/C"])
        # print(MetaX, "/A", source_folder[fold], "/AT", destination_folder[fold], "/C") #DEBUG
    else:
        print("MoviesBulk directory is empty")
