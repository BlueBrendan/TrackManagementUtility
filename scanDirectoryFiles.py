import os
from tkinter import filedialog
from functools import partial
from mutagen.flac import FLAC

def scanDirectoryFiles(subdirectories):
    directory = filedialog.askdirectory()
    if directory!='':
        if (subdirectories.get()==True):
            directorySearch(directory, True)
        else:
            directorySearch(directory, False)
    # DIRECTORIES.append(r"G:\\Music\\FLAC Collection\\")
    # response = input("Check subdirectories? (y/n): ")
    # while response.lower()!='y' and response.lower()!='n':
    #     response = input("Invalid input, try again (y/n): ")
    # if response=='y':
    #     subdirectories = True
    # else:
    #     subdirectories = False
    # for directory in directories:
    #     directorySearch(directory, subdirectories)

def directorySearch(directory, subdirectories):
    files = os.listdir(directory)
    print("\nScanning for files in " + directory)
    interestParameters = ['artist', 'title', 'date', 'bpm', 'initialkey', 'genre', 'replaygain_track_gain']
    if subdirectories == True:
        for i in files:
                if os.path.isdir(str(directory + "\\" + str(i))):
                    directorySearch(directory + "\\" + str(i), subdirectories)
                else:
                    if i.endswith(".flac"):
                        print(i)
                        audio = FLAC(directory + "\\" + str(i))
                        fileParameters = []
                        for x in audio:
                            fileParameters.append(x)
                        for x in fileParameters:
                            # delete extraneous tags
                            if x not in interestParameters:
                                print("Deleting " + str(x))
                                audio[x] = ""
                                audio.pop(x)
                                audio.save()
                        for x in interestParameters:
                            # add tags of interest if missing
                            if x not in fileParameters:
                                audio[x] = ""
                                audio.save()
    else:
        #single directory search
        for i in files:
            if i.endswith(".flac"):
                print(i)
                audio = FLAC(directory + "\\" + str(i))
                fileParameters = []
                for x in audio:
                    fileParameters.append(x)
                for x in fileParameters:
                    # delete extraneous tags
                    if x not in interestParameters:
                        print("Deleting " + str(x))
                        audio[x] = ""
                        audio.pop(x)
                        audio.save()
                for x in interestParameters:
                    # add tags of interest if missing
                    if x not in fileParameters:
                        audio[x] = ""
                        audio.save()
