import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from mutagen.flac import FLAC
from mutagen.flac import Picture
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
from io import BytesIO
import base64

# import methods
from commonOperations import resource_path

# global variables
bg = "#282f3b" # main bg color
secondary_bg = "#364153" # secondary color

complete = False
def compareDrives(CONFIG_FILE, firstDefaultDirectory, secondDefaultDirectory, options, root):
    global complete
    if firstDefaultDirectory == '': first_directory = filedialog.askdirectory(master=root, title="Select First Directory")
    else: first_directory = filedialog.askdirectory(initialdir=firstDefaultDirectory, title="Select First Directory")
    if first_directory!='':
        # write value to firstDefaultDirectory
        if firstDefaultDirectory == '' or first_directory != firstDefaultDirectory: writeFirstDefaultDirectory(CONFIG_FILE, first_directory)
        if secondDefaultDirectory == '': second_directory = filedialog.askdirectory(title="Select Second Directory")
        else: second_directory = filedialog.askdirectory(initialdir=secondDefaultDirectory, title="Select Second Directory")
        if first_directory!='' and second_directory!='':
            # write value to secondDefaultDirectory
            if secondDefaultDirectory == '' or second_directory != secondDefaultDirectory: writeSecondDefaultDirectory(CONFIG_FILE, second_directory)
            if first_directory != second_directory:
                firstDirectoryFileCount=0
                secondDirectoryFileCount=0
                differenceCount=0
                directoryCount=0
                firstDirectoryFileCount, differenceCount, directoryCount = directorySearch(first_directory, second_directory, firstDirectoryFileCount, differenceCount, directoryCount, options)
                secondDirectoryFileCount, differenceCount, directoryCount = directorySearch(second_directory, first_directory, secondDirectoryFileCount, differenceCount, directoryCount, options)
                messagebox.showinfo(title="Search Complete", message="Files in First Directory: " + str(firstDirectoryFileCount) + "\nFiles in Second Directory: " + str(secondDirectoryFileCount) + "\nTotal File Difference: " + str(differenceCount) + "\nTotal Directory Difference: " + str(directoryCount) + '\n')
            else: messagebox.showinfo(title="Identical Directories", message="You selected the same directory twice, genius")

def directorySearch(first_directory, second_directory, directoryFileCount, differenceCount, directoryCount, options):
    if complete == True:
        return differenceCount, directoryCount
    first_directory_files = os.listdir(first_directory)
    second_directory_files = os.listdir(second_directory)
    for var in first_directory_files:
        # check if file var is a directory
        if os.path.isdir(str(first_directory) + '/' + str(var)) and complete==False:
            # check if second_directory has the same directory
            if var not in second_directory_files:
                directoryCount+=1
                popup = tk.Toplevel()
                popup.title("Directory Conflict Detected")
                ws = popup.winfo_screenwidth()  # width of the screen
                hs = popup.winfo_screenheight()  # height of the screen
                x = (ws / 2) - (550 / 2)
                y = (hs / 2) - (260 / 2)
                popup.geometry('%dx%d+%d+%d' % (550, 180, x, y))
                popup.config(bg=bg)
                tk.Label(popup, text=var + " (" + str(len([name for name in os.listdir(first_directory + '/' + var)])) + " file(s) inside)", wraplength=500, font=('Proxima Nova Rg', 13), fg="white", bg=bg).pack(pady=(15, 5))
                tk.Label(popup, text="Found in " + first_directory, wraplength=500, font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(pady=(5, 5))
                tk.Label(popup, text="Not found in " + second_directory, wraplength=500, font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(pady=(5, 20))
                buttonFrame = tk.Frame(popup, bg=bg)
                buttonFrame.pack()
                tk.Button(buttonFrame, text='Copy', command=lambda: copyDirectory(first_directory, second_directory, var, options, popup), font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(side="left", padx=(20, 20))
                tk.Button(buttonFrame, text='Delete', command=lambda: deleteDirectory(first_directory, var, popup), font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(side="left", padx=(20, 20))
                tk.Button(buttonFrame, text='Ignore', command=popup.destroy, font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(side="left", padx=(20, 20))
                popup.protocol("WM_DELETE_WINDOW", lambda arg=popup: on_exit(arg))
                popup.iconbitmap(resource_path('favicon.ico'))
                popup.wait_window()
            # check files within that directory with those in the directory of second_directory
            else: directoryFileCount, differenceCount, directoryCount = directorySearch(first_directory + '/' + var, second_directory + '/' + var, directoryFileCount, differenceCount, directoryCount, options)
        elif complete==False:
            directoryFileCount+=1
            # check if second_directory has the same file
            if var not in second_directory_files:
                differenceCount+=1
                popup = tk.Toplevel()
                popup.title("File Conflict Detected")
                ws = popup.winfo_screenwidth()  # width of the screen
                hs = popup.winfo_screenheight()  # height of the screen
                x = (ws / 2) - (550 / 2)
                y = (hs / 2) - (275 / 2)
                popup.geometry('%dx%d+%d+%d' % (550, 250, x, y))
                if len(var) > 65:
                    x = (ws / 2) - ((550 + ((len(var) - 65) * 9)) / 2)
                    popup.geometry('%dx%d+%d+%d' % ((550 + ((len(var) - 65) * 9)), 270, x, y))
                popup.config(bg=bg)
                tk.Label(popup, text=var, font=('Proxima Nova Rg', 13), fg="white", bg=bg).pack(pady=(25,26))
                tk.Label(popup, text="Present in " + first_directory, wraplength=500, font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(pady=(0,30))
                tk.Label(popup, text="Missing in " + second_directory, wraplength=500, font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(pady=(0,30))
                # artwork from FLAC
                if var.endswith(".flac"):
                    audio = FLAC(first_directory + '/' + var)
                    picture = audio.pictures
                    if len(picture) > 0:
                        y = (hs / 2) - (550 / 2)
                        popup.update_idletasks()
                        popup.geometry('%dx%d+%d+%d' % (popup.winfo_width(), 500, x, y))
                        stream = BytesIO(picture[0].data)
                        image = Image.open(stream).convert("RGBA")
                        stream.close()
                        directoryImageImport = image.resize((200, 200), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(directoryImageImport)
                        directoryImage = tk.Label(popup, image=photo, bg=bg)
                        directoryImage.image = photo
                        directoryImage.pack(side="top", pady=(0,30))
                # artwork from MP3, AIFF, or WAV
                elif var.endswith(".mp3") or var.endswith(".aiff") or var.endswith(".wav"):
                    audio = MP3(first_directory + '/' + var)
                    if 'APIC:' in audio:
                        image = audio["APIC:"]
                        if image != b'':
                            y = (hs / 2) - (550 / 2)
                            popup.geometry('%dx%d+%d+%d' % (550, 500, x, y))
                            stream = BytesIO(image.data)
                            image = Image.open(stream).convert("RGBA")
                            stream.close()
                            directoryImageImport = image.resize((200, 200), Image.ANTIALIAS)
                            photo = ImageTk.PhotoImage(directoryImageImport)
                            directoryImage = tk.Label(popup, image=photo, bg=bg)
                            directoryImage.image = photo
                            directoryImage.pack(side="top", pady=(0, 30))
                # artwork from OGG
                elif var.endswith(".ogg"):
                    audio = OggVorbis(first_directory + '/' + var)
                    if "metadata_block_picture" in audio:
                        imageFrame = audio["metadata_block_picture"]
                        if imageFrame[0] != '':
                            y = (hs / 2) - (550 / 2)
                            popup.geometry('%dx%d+%d+%d' % (550, 500, x, y))
                            data = base64.b64decode(imageFrame[0])
                            image = Picture(data)
                            stream = BytesIO(image.data)
                            image = Image.open(stream).convert("RGBA")
                            stream.close()
                            directoryImageImport = image.resize((200, 200), Image.ANTIALIAS)
                            photo = ImageTk.PhotoImage(directoryImageImport)
                            directoryImage = tk.Label(popup, image=photo, bg=bg)
                            directoryImage.image = photo
                            directoryImage.pack(side="top", pady=(0, 30))
                # artwork from M4A
                elif var.endswith(".m4a"):
                    audio = MP4(first_directory + '/' + var)
                    if "covr" in audio:
                        image = audio["covr"]
                        if len(image) != 0:
                            y = (hs / 2) - (550 / 2)
                            popup.geometry('%dx%d+%d+%d' % (550, 500, x, y))
                            stream = BytesIO(image[0])
                            image = Image.open(stream).convert("RGBA")
                            stream.close()
                            directoryImageImport = image.resize((200, 200), Image.ANTIALIAS)
                            photo = ImageTk.PhotoImage(directoryImageImport)
                            directoryImage = tk.Label(popup, image=photo, bg=bg)
                            directoryImage.image = photo
                            directoryImage.pack(side="top", pady=(0, 30))
                buttonFrame = tk.Frame(popup, bg=bg)
                buttonFrame.pack(pady=(10, 10))
                tk.Button(buttonFrame, text='Copy', command=lambda: copyFile(first_directory, second_directory, var, popup), font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(side="left", padx=(20, 20))
                tk.Button(buttonFrame, text='Delete', command=lambda: deleteFile(first_directory, var, popup), font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(side="left", padx=(20, 20))
                tk.Button(buttonFrame, text='Ignore', command=popup.destroy, font=('Proxima Nova Rg', 11), fg="white", bg=bg).pack(side="left", padx=(20, 20))
                popup.protocol("WM_DELETE_WINDOW", lambda arg=popup: on_exit(arg))
                popup.iconbitmap(resource_path('favicon.ico'))
                popup.wait_window()
    return directoryFileCount, differenceCount, directoryCount

def copyFile(first_directory, second_directory, var, popup):
    # copy file var from first_directory to second_directory
    shutil.copy(str(first_directory) + '/' + str(var), str(second_directory) + '/' + str(var))
    popup.destroy()

def deleteFile(first_directory, var, popup):
    # delete file var from first_directory
    os.remove(str(first_directory) + '/' + str(var))
    popup.destroy()

def copyDirectory(first_directory, second_directory, var, options, popup):
    # check if directory contents should be copied as well
    if options['Copy Directory Contents (B)'].get():
        # recursively copy directory var from first_directory to second_directory
        shutil.copytree(str(first_directory) + '/' + str(var), str(second_directory) + '/' + str(var))
        popup.destroy()
    else:
        # copy the directory but not its contents
        os.mkdir(str(second_directory) + '/' + str(var))
        popup.destroy()

def deleteDirectory(first_directory, var, popup):
    # recursively delete directory var from first_directory
    shutil.rmtree(str(first_directory) + '/' + str(var))
    popup.destroy()

def on_exit(popup):
    popup.destroy()
    global complete
    complete = True

def writeFirstDefaultDirectory(CONFIG_FILE, first_directory):
    config_file=open(CONFIG_FILE, 'r').read()
    term = "First Default Directory (S):"
    with open(CONFIG_FILE, 'wt', encoding='utf-8') as file: file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index('\n', config_file.index(term))]), term + first_directory))
    file.close()

def writeSecondDefaultDirectory(CONFIG_FILE, second_directory):
    config_file=open(CONFIG_FILE, 'r').read()
    term = "Second Default Directory (S):"
    with open(CONFIG_FILE, 'wt', encoding='utf-8') as file: file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index('\n', config_file.index(term))]), term + second_directory))
    file.close()