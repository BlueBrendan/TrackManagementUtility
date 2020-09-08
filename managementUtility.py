from tkinter import *
from compareDrives import compareDrives
from scanTagsOnline import selectFileOrDirectory
from checkForUpdates import checkForUpdates
from updatePreferences import updatePreferences
import getpass
import os

root = Tk()
root.title("Track Management Utility V1.0")
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (520/2)
y = (hs/2) - (330/2)
root.geometry('%dx%d+%d+%d' % (520, 250, x, y))


def createConfigFile():
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    if not os.path.exists(CONFIG_FILE):
        # create settings folder
        if not os.path.isdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility"):
            print("DIRECTORY NOT FOUND")
            path = r"C:/Users/" + str(getpass.getuser()) + "/Documents"
            os.mkdir(path + "/Track Management Utility")
        # create setttings file
        file = open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt", 'w')
        file.write("Subdirectories (B):True\n")
        file.write("Close Scraping Window (B):True\n")
        file.write("First Default Directory (S):\n")
        file.write("Second Default Directory (S):\n")
        file.write("Scrape Junodownload (B):True\n")
        file.write("Scrape Beatport (B):True\n")
        file.write("Scrape Discogs (B):True\n")
        file.write("Reverse Image Search (B):True\n")
        file.write("Delete Stored Images (B):True\n")
        file.close()
    return CONFIG_FILE

#handle subdirectory selection
def subdirectorySelection(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    #if true, turn option to false
    term = "Subdirectories (B)"
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]=="True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term))+1]) + "True", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term))+1])) + "False"))
        file.close()
    #if false, turn option to true
    elif config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]=="False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "False", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()

def compareDirectories(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    term = "First Default Directory (S):"
    firstDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    term = "Second Default Directory (S):"
    secondDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    compareDrives(CONFIG_FILE, firstDefaultDirectory, secondDefaultDirectory)

def readValuesFromConfig(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    terms = ['Subdirectories (B)', 'Close Scraping Window (B)', 'First Default Directory (S)', 'Second Default Directory (S)', 'Scrape Junodownload (B)', 'Scrape Beatport (B)', 'Scrape Discogs (B)', "Reverse Image Search (B)", "Delete Stored Images (B)"]
    options = {}
    for term in terms:
        if (term[len(term) - 2:len(term) - 1]) == 'B':
            try: options[term] = BooleanVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.find('\n', config_file.index(term) + len(term))])
            except ValueError:
                os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                createConfigFile()
                readValuesFromConfig(CONFIG_FILE)
        elif (term[len(term) - 2:len(term) - 1]) == 'S':
            try: options[term] = config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]
            except ValueError:
                os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                createConfigFile()
                readValuesFromConfig(CONFIG_FILE)
    return options

def openPreferences(CONFIG_FILE):
    options = readValuesFromConfig(CONFIG_FILE)
    updatePreferences(options, CONFIG_FILE)

def selectSearchTags(CONFIG_FILE):
    options = readValuesFromConfig(CONFIG_FILE)
    selectFileOrDirectory(CONFIG_FILE, options)

def selectCompare(CONFIG_FILE):
    options = readValuesFromConfig(CONFIG_FILE)
    compareDirectories(CONFIG_FILE)

# set preferences
CONFIG_FILE = createConfigFile()
options = readValuesFromConfig(CONFIG_FILE)

#file topmenu button
menufile = Menubutton(root, text="File")
menufile.menu = Menu(menufile, tearoff=0)
menufile["menu"] = menufile.menu
updates = IntVar()
exit = IntVar()
menufile.menu.add_command(label="Check for Updates", command=checkForUpdates)
menufile.menu.add_command(label="Exit", command=root.destroy)

#option topmenu button
menuoption = Menubutton(root, text="Option")
menuoption.menu = Menu(menuoption, tearoff=0)
menuoption['menu'] = menuoption.menu
menuoption.menu.add_command(label="Preferences", command=lambda: openPreferences(CONFIG_FILE))
menufile.grid(row=0, column=0, columnspan=1, sticky=W)
menuoption.grid(row=0, column=0, columnspan=1, sticky=W, padx=(30,0))

titleLabel = Label(root, text="Track Management Utility").grid(row=1, column=1, pady=(5,13))
# Scans for files in a directory and find their tags online
Button(root, text="Search Web for Tags", command=lambda: selectSearchTags(CONFIG_FILE)).grid(row=2, column=1, pady=(5,3))
Label(root, text="Scan for files in a directory and find their tags online").grid(row=3, column=1, pady=(3,15))
# Scans for differences in files between two separate directories
Button(root, text="Compare Directories", command=lambda: selectCompare(CONFIG_FILE)).grid(row=4, column=1, pady=(5,3))
Label(root, text="Scan for differences in files and folders between two separate directories").grid(row=5, column=1, pady=(3, 20))
Checkbutton(root, text="Include Subdirectories: ", var=options['Subdirectories (B)'], command=lambda: subdirectorySelection(CONFIG_FILE)).grid(row=6, column=0, columnspan=2, padx=(10,0), pady=(0, 0), sticky=W)
root.mainloop()











