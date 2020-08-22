import os
import shutil
from tkinter import *
from functools import partial
from tkinter import messagebox
from tkinter import filedialog

complete = False

def compareDrives(state):
    global complete
    complete = state
    first_directory = filedialog.askdirectory(title="Select First Directory")
    if first_directory!='':
        second_directory = filedialog.askdirectory(title="Select Second Directory")
        if first_directory!='' and second_directory!='':
            if first_directory != second_directory:
                fileCount=0
                directoryCount=0
                fileCount, directoryCount = directorySearch(first_directory, second_directory, fileCount, directoryCount)
                fileCount, directoryCount = directorySearch(second_directory, first_directory, fileCount, directoryCount)
                print("\nSEARCH COMPLETE\nTotal File Difference: " + str(fileCount) + "\nTotal Directory Difference: " + str(directoryCount) + '\n')
            else:
                messagebox.showinfo(title="Identical Directories", message="You selected the same directory twice, genius")

def directorySearch(first_directory, second_directory, fileCount, directoryCount):
    if complete == True:
        return fileCount, directoryCount
    first_directory_files = os.listdir(first_directory)
    second_directory_files = os.listdir(second_directory)
    for var in first_directory_files:
        print(str(first_directory) + '/' + str(var))
        #check if file var is a directory
        if os.path.isdir(str(first_directory) + '/' + str(var)) and complete==False:
            #check if second_directory has the same directory
            if var not in second_directory_files:
                directoryCount+=1
                popup = Toplevel()
                popup.title("Directory Conflict Detected")
                message = "Directory " + str(var) + " was found in " + str(first_directory) + " but not " + str(second_directory) + "\nWould you like to copy this directory over, delete it, or ignore it?"
                Label(popup, text=message).grid(row=0, column=1)
                Button(popup, text='Copy', command=partial(copyDirectory, first_directory, second_directory, var, popup)).grid(row=1, column=0)
                Button(popup, text='Delete', command=partial(deleteDirectory, first_directory, var, popup)).grid(row=1, column=1)
                Button(popup, text='Ignore', command=popup.destroy).grid(row=1, column=2)
                popup.protocol("WM_DELETE_WINDOW", lambda arg=popup: on_exit(arg))
                popup.wait_window()
            #check files within that directory with those in the directory of second_directory
            else:
                fileCount, directoryCount = directorySearch(first_directory + '/' + var, second_directory  + '/' + var, fileCount, directoryCount)
        elif complete==False:
            #check if second_directory has the same file
            if var not in second_directory_files:
                fileCount+=1
                popup = Toplevel()
                popup.title("Directory Conflict Detected")
                message = "File " + str(var) + " was found in " + str(first_directory) + " but not " + str(second_directory) + "\nWould you like to copy this directory over, delete it, or ignore it?"
                Label(popup, text=message).grid(row=0, column=1)
                Button(popup, text='Copy',command=partial(copyFile, first_directory, second_directory, var, popup)).grid(row=1, column=0)
                Button(popup, text='Delete', command=partial(deleteFile, first_directory, var, popup)).grid(row=1, column=1)
                Button(popup, text='Ignore', command=popup.destroy).grid(row=1, column=2)
                popup.protocol("WM_DELETE_WINDOW", lambda arg=popup: on_exit(arg))
                popup.wait_window()


    return fileCount, directoryCount



def copyFile(first_directory, second_directory, var, popup):
    #copy file var from first_directory to second_directory
    shutil.copy(str(first_directory) + '/' + str(var), str(second_directory) + '/' + str(var))
    popup.destroy()

def deleteFile(first_directory, var, popup):
    #delete file var from first_directory
    os.remove(str(first_directory) + '/' + str(var))
    popup.destroy()

def copyDirectory(first_directory, second_directory, var, popup):
    #recursively copy directory var from first_directory to second_directory
    shutil.copytree(str(first_directory) + '/' + str(var), str(second_directory) + '/' + str(var))
    popup.destroy()

def deleteDirectory(first_directory, var, popup):
    #recursively delete directory var from first_directory
    shutil.rmtree(str(first_directory) + '/' + str(var))
    popup.destroy()

def on_exit(popup):
    popup.destroy()
    global complete
    complete = True
