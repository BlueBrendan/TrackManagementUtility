import tkinter as tk
import getpass
import os

#import methods
from compareDrives import compareDrives
from track_preparation.scanTagsOnline import selectFileOrDirectory
from other.checkForUpdates import checkForUpdates
from other.updatePreferences import updatePreferences

root = tk.Tk()
root.title("Track Management Utility V1.0")
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (520/2)
y = (hs/2) - (275/2)
root.geometry('%dx%d+%d+%d' % (520, 250, x, y))

def createConfigFile(flag):
    CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
    if flag=="N" and not os.path.exists(CONFIG_FILE):
        # create settings folder
        if not os.path.isdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility"):
            path = r"C:/Users/" + str(getpass.getuser()) + "/Documents"
            os.mkdir(path + "/Track Management Utility")
        # create setttings file
        file = open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt", 'w')
        file.write("-GENERAL-\nSubdirectories (B):True\nClose Scraping Window (B):True\nFirst Default Directory (S):\nSecond Default Directory (S):\n\n-SCRAPING SETTINGS-\nScrape Junodownload (B):True\nScrape Beatport (B):True\nScrape Discogs (B):True\n\n-IMAGE SCRAPING-\nReverse Image Search (B):True\nDelete Stored Images (B):True\nImage Load Wait Time (I):10\n\n-TAGGING-\nCheck Artist for Typos (B):True\nAudio naming format (S):Artist - Title\n")
        file.close()
    #force create
    if flag=="F":
        if not os.path.isdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility"):
            path = r"C:/Users/" + str(getpass.getuser()) + "/Documents"
            os.mkdir(path + "/Track Management Utility")
        # create setttings file
        file = open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt", 'w')
        file.write("-GENERAL-\nSubdirectories (B):True\nClose Scraping Window (B):True\nFirst Default Directory (S):\nSecond Default Directory (S):\n\n-SCRAPING SETTINGS-\nScrape Junodownload (B):True\nScrape Beatport (B):True\nScrape Discogs (B):True\n\n-IMAGE SCRAPING-\nReverse Image Search (B):True\nDelete Stored Images (B):True\nImage Load Wait Time (I):10\n\n-TAGGING-\nCheck Artist for Typos (B):True\nAudio naming format (S):Artist - Title\n")
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
    terms = ['Subdirectories (B)', 'Close Scraping Window (B)', 'First Default Directory (S)', 'Second Default Directory (S)', 'Scrape Junodownload (B)', 'Scrape Beatport (B)', 'Scrape Discogs (B)', "Reverse Image Search (B)", "Delete Stored Images (B)", "Image Load Wait Time (I)", "Check Artist for Typos (B)", "Audio naming format (S)"]
    options = {}
    for term in terms:
        if (term[len(term) - 2:len(term) - 1]) == 'B':
            try: options[term] = tk.BooleanVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.find('\n', config_file.index(term) + len(term))])
            except ValueError:
                os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                createConfigFile("F")
                readValuesFromConfig(CONFIG_FILE)
        elif (term[len(term) - 2:len(term) - 1]) == 'S':
            try: options[term] = tk.StringVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
            except ValueError:
                os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                createConfigFile("F")
                readValuesFromConfig(CONFIG_FILE)
        elif (term[len(term) - 2:len(term) - 1]) == 'I':
            try:
                options[term] = tk.IntVar(value=config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))])
            except ValueError:
                os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt")
                createConfigFile("F")
                readValuesFromConfig(CONFIG_FILE)
    return options

def openPreferences(CONFIG_FILE, root):
    options = readValuesFromConfig(CONFIG_FILE)
    updatePreferences(options, CONFIG_FILE, root)

def selectSearchTags(CONFIG_FILE):
    options = readValuesFromConfig(CONFIG_FILE)
    selectFileOrDirectory(options, CONFIG_FILE)

def selectCompare(CONFIG_FILE):
    options = readValuesFromConfig(CONFIG_FILE)
    compareDirectories(CONFIG_FILE)

# set preferences
CONFIG_FILE = createConfigFile("N")
options = readValuesFromConfig(CONFIG_FILE)

#file topmenu button
menufile = tk.Menubutton(root, text="File")
menufile.menu = tk.Menu(menufile, tearoff=0)
menufile["menu"] = menufile.menu
updates = tk.IntVar()
exit = tk.IntVar()
menufile.menu.add_command(label="Check for Updates", command=checkForUpdates)
menufile.menu.add_command(label="Exit", command=root.destroy)

#option topmenu button
menuoption = tk.Menubutton(root, text="Option")
menuoption.menu = tk.Menu(menuoption, tearoff=0)
menuoption['menu'] = menuoption.menu
menuoption.menu.add_command(label="Preferences", command=lambda: openPreferences(CONFIG_FILE, root))
menufile.grid(row=0, column=0, columnspan=1, sticky='w')
menuoption.grid(row=0, column=0, columnspan=1, sticky='w', padx=(30,0))

titleLabel = tk.Label(root, text="Track Management Utility").grid(row=1, column=1, pady=(5,13))
# Scans for files in a directory and find their tags online
tk.Button(root, text="Search Web for Tags", command=lambda: selectSearchTags(CONFIG_FILE)).grid(row=2, column=1, pady=(5,3))
tk.Label(root, text="Scan for files in a directory and find their tags online").grid(row=3, column=1, pady=(3,15))
# Scans for differences in files between two separate directories
tk.Button(root, text="Compare Directories", command=lambda: selectCompare(CONFIG_FILE)).grid(row=4, column=1, pady=(5,3))
tk.Label(root, text="Scan for differences in files and folders between two separate directories").grid(row=5, column=1, pady=(3, 20))
tk.Checkbutton(root, text="Include Subdirectories: ", var=options['Subdirectories (B)']).grid(row=6, column=0, columnspan=2, padx=(10,0), pady=(0, 0), sticky='w')
root.mainloop()











