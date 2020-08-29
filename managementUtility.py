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

# set preferences
CONFIG_FILE = r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt"
if not os.path.exists(CONFIG_FILE):
    print("DOES NOT EXIST")
    #create settings folder
    if not os.path.isdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility"):
        print("DIRECTORY NOT FOUND")
        path = r"C:/Users/" + str(getpass.getuser()) + "/Documents"
        os.mkdir(path + "/Track Management Utility")
    #create setttings file
    file = open(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Settings.txt", 'w')
    file.write("Subdirectories:True\n")
    file.write("Close scraping window:True\n")
    file.write("First Default Directory:\n")
    file.write("Second Default Directory:\n")
    file.close()

config_file=open(CONFIG_FILE, 'r').read()
menufile = Menubutton(root, text="File")
menuoption = Menubutton(root, text="Option")
term = "Subdirectories:"
subdirectories = BooleanVar(value=config_file[config_file.index(term)+len(term):config_file.find('\n', config_file.index(term)+len(term))])
term = "Close scraping window:"
closeScrapingWindow = BooleanVar(value=config_file[config_file.index(term)+len(term):config_file.index('\n', config_file.index(term)+len(term))])
term = "First Default Directory:"
firstDefaultDirectory = config_file[config_file.index(term)+len(term):config_file.index('\n', config_file.index(term) + len(term))]
term = "Second Default Directory:"
secondDefaultDirectory = config_file[config_file.index(term)+len(term):config_file.index('\n', config_file.index(term) + len(term))]

#file topmenu button
menufile.menu = Menu(menufile, tearoff=0)
menufile["menu"] = menufile.menu
updates = IntVar()
exit = IntVar()
menufile.menu.add_command(label="Check for Updates", command=checkForUpdates)
menufile.menu.add_command(label="Exit", command=root.destroy)

#option topmenu button
menuoption.menu = Menu(menuoption, tearoff=0)
menuoption['menu'] = menuoption.menu
menuoption.menu.add_command(label="Preferences", command=updatePreferences)
menufile.grid(row=0, column=0, columnspan=1, sticky=W)
menuoption.grid(row=0, column=0, columnspan=1, sticky=W, padx=(30,0))

    # threading.Thread(target=test, args=('Z',)).start()

#handle subdirectory selection
def subdirectorySelection(CONFIG_FILE, config_file):
    #if true, turn option to false
    term = "Subdirectories:"
    if config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]=="True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term))+1]) + "True", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term))+1])) + "False"))
        file.close()
    #if false, turn option to true
    elif config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]=="False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1]) + "False", str(str(config_file[config_file.index(term):config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()

def compareDirectories(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    term = "First Default Directory:"
    firstDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    term = "Second Default Directory:"
    secondDefaultDirectory = config_file[config_file.index(term) + len(term):config_file.index('\n', config_file.index(term) + len(term))]
    compareDrives(CONFIG_FILE, firstDefaultDirectory, secondDefaultDirectory)

titleLabel = Label(root, text="Track Management Utility").grid(row=1, column=1, pady=(5,13))
# Scans for files in a directory and find their tags online
Button(root, text="Search Web for Tags", command=lambda: selectFileOrDirectory(CONFIG_FILE, subdirectories, closeScrapingWindow)).grid(row=2, column=1, pady=(5,3))
Label(root, text="Scan for files in a directory and find their tags online").grid(row=3, column=1, pady=(3,15))
# Scans for differences in files between two separate directories
Button(root, text="Compare Directories", command=lambda: compareDirectories(CONFIG_FILE)).grid(row=4, column=1, pady=(5,3))
Label(root, text="Scan for differences in files and folders between two separate directories").grid(row=5, column=1, pady=(3, 20))
Checkbutton(root, text="Include Subdirectories: ", var=subdirectories, command=lambda: subdirectorySelection(CONFIG_FILE, config_file)).grid(row=6, column=0, columnspan=2, padx=(10,0), pady=(0, 0), sticky=W)
root.mainloop()











