import os
from mutagen.flac import FLAC
import PIL.Image
import PIL.ImageTk
from io import BytesIO
import shutil
from tkinter import *
from functools import partial
from tkinter import messagebox
from tkinter import filedialog

complete = False
def compareDrives(CONFIG_FILE, firstDefaultDirectory, secondDefaultDirectory):
    global complete
    if firstDefaultDirectory == '':
        first_directory = filedialog.askdirectory(title="Select First Directory")
    else:
        first_directory = filedialog.askdirectory(initialdir=firstDefaultDirectory, title="Select First Directory")
    if first_directory!='':
        #check directory and default values for a match
        if firstDefaultDirectory == '' or first_directory != firstDefaultDirectory:
            # write value to firstDefaultDirectory
            writeFirstDefaultDirectory(CONFIG_FILE, first_directory)
        if secondDefaultDirectory == '':
            second_directory = filedialog.askdirectory(title="Select Second Directory")
        else:
            second_directory = filedialog.askdirectory(initialdir=secondDefaultDirectory, title="Select Second Directory")
        if first_directory!='' and second_directory!='':
            if secondDefaultDirectory == '' or second_directory != secondDefaultDirectory:
                # write value to secondDefaultDirectory
                writeSecondDefaultDirectory(CONFIG_FILE, second_directory)
            if first_directory != second_directory:
                fileCount=0
                directoryCount=0
                fileCount, directoryCount = directorySearch(first_directory, second_directory, fileCount, directoryCount)
                fileCount, directoryCount = directorySearch(second_directory, first_directory, fileCount, directoryCount)
                messagebox.showinfo(title="Search Complete", message="Total File Difference: " + str(fileCount) + "\nTotal Directory Difference: " + str(directoryCount) + '\n')
            else:
                messagebox.showinfo(title="Identical Directories", message="You selected the same directory twice, genius")

def directorySearch(first_directory, second_directory, fileCount, directoryCount):
    if complete == True:
        return fileCount, directoryCount
    first_directory_files = os.listdir(first_directory)
    second_directory_files = os.listdir(second_directory)
    for var in first_directory_files:
        #check if file var is a directory
        if os.path.isdir(str(first_directory) + '/' + str(var)) and complete==False:
            #check if second_directory has the same directory
            if var not in second_directory_files:
                directoryCount+=1
                popup = Toplevel()
                popup.title("Directory Conflict Detected")
                ws = popup.winfo_screenwidth()  # width of the screen
                hs = popup.winfo_screenheight()  # height of the screen
                x = (ws / 2) - (450 / 2)
                y = (hs / 2) - (260 / 2)
                popup.geometry('%dx%d+%d+%d' % (450, 180, x, y))
                popup.columnconfigure(0, weight=1)
                popup.columnconfigure(1, weight=1)
                popup.columnconfigure(2, weight=1)
                Label(popup, text=var + " (" + str(len([name for name in os.listdir(first_directory + '/' + var)])) + " file(s) inside)", wraplength=420, font=("TkDefaultFont", 9, 'bold')).grid(row=0, column=0, columnspan=3, pady=(15, 5))
                Label(popup, text="Found in " + first_directory, wraplength=420).grid(row=2, column=0, columnspan=3, pady=(5, 5))
                Label(popup, text="Not found in " + second_directory, wraplength=420).grid(row=3, column=0, columnspan=3, pady=(5, 20))
                Button(popup, text='Copy', command=partial(copyDirectory, first_directory, second_directory, var, popup)).grid(row=4, column=0)
                Button(popup, text='Delete', command=partial(deleteDirectory, first_directory, var, popup)).grid(row=4, column=1)
                Button(popup, text='Ignore', command=popup.destroy).grid(row=4, column=2)
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
                ws = popup.winfo_screenwidth()  # width of the screen
                hs = popup.winfo_screenheight()  # height of the screen
                x = (ws / 2) - (500 / 2)
                y = (hs / 2) - (506 / 2)
                popup.geometry('%dx%d+%d+%d' % (500, 460, x, y))
                popup.columnconfigure(0, weight=1)
                popup.columnconfigure(1, weight=1)
                popup.columnconfigure(2, weight=1)
                Label(popup, text=var, wraplength=420, font=("TkDefaultFont", 9, 'bold')).pack(side=TOP, pady=(20,5))
                Label(popup, text="Found in " + first_directory, wraplength=420).pack(side=TOP, pady=(15,5))
                Label(popup, text="Not found in " + second_directory, wraplength=420).pack(side=TOP, pady=(15,30))
                #artwork from FLAC
                audio = FLAC(first_directory + '/' + var)
                picture = audio.pictures
                if len(picture) > 0:
                    stream = BytesIO(picture[0].data)
                    image = PIL.Image.open(stream).convert("RGBA")
                    stream.close()
                    directoryImageImport = image.resize((200, 200), PIL.Image.ANTIALIAS)
                    photo = PIL.ImageTk.PhotoImage(directoryImageImport)
                    directoryImage = Label(popup, image=photo)
                    directoryImage.image = photo
                    directoryImage.pack(side=TOP, pady=(0,30))
                buttons = Frame(popup)
                buttons.pack(side=TOP)
                Button(buttons, text='Copy',command=partial(copyFile, first_directory, second_directory, var, popup)).pack(side="left", padx=(45,45))
                Button(buttons, text='Delete', command=partial(deleteFile, first_directory, var, popup)).pack(side="left", padx=(45,45))
                Button(buttons, text='Ignore', command=popup.destroy).pack(side="left", padx=(45,45))
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

def writeFirstDefaultDirectory(CONFIG_FILE, first_directory):
    config_file=open(CONFIG_FILE, 'r').read()
    term = "First Default Directory (S):"
    with open(CONFIG_FILE, 'wt', encoding='utf-8') as file:
        file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index('\n', config_file.index(term))]), term + first_directory))
    file.close()

def writeSecondDefaultDirectory(CONFIG_FILE, second_directory):
    config_file=open(CONFIG_FILE, 'r').read()
    term = "Second Default Directory (S):"
    with open(CONFIG_FILE, 'wt', encoding='utf-8') as file:
        file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index('\n', config_file.index(term))]), term + second_directory))
    file.close()