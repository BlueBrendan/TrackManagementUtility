import tkinter as tk
from tkinter.tix import *

# import methods
from options.checkboxHandling import checkbox

# global variables
# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"
# invalid selection color
invalid_bg = "#801212"
optionsDict = {}

def comparisonTab(tab_parent, options, CONFIG_FILE):
    # Drive Comparison Settings Tab
    tab4 = tk.Frame(tab_parent, bg=bg)
    tab_parent.add(tab4, text="Drive Comparison")
    topComponentFrame = tk.Frame(tab4, bg=bg)
    topComponentFrame.pack(fill=X)
    tk.Label(topComponentFrame, text="Drive Comparison", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    leftComponentFrame = tk.Frame(topComponentFrame, bg=bg)
    leftComponentFrame.pack(side="left", anchor="nw")

    # subdirectory checkbox
    subdirectoriesFrame = tk.Frame(leftComponentFrame, bg=bg)
    subdirectoriesFrame.pack(anchor="w")
    subdirectories = tk.Checkbutton(subdirectoriesFrame, variable=options['Subdirectories (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Subdirectories (B)', optionsDict, options), bg=bg)
    subdirectories.pack(padx=(20, 0), side="left")
    tk.Label(subdirectoriesFrame, text="Include Subdirectories", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    optionsDict['Subdirectories (B)'] = subdirectories

    # directory copy checkbox
    directoryCopyFrame = tk.Frame(leftComponentFrame, bg=bg)
    directoryCopyFrame.pack(anchor="w")
    directoryContentCopy = tk.Checkbutton(directoryCopyFrame, variable=options['Copy Directory Contents (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Copy Directory Contents (B)', optionsDict, options), bg=bg)
    directoryContentCopy.pack(padx=(20, 0), side="left")
    tk.Label(directoryCopyFrame, text="Include Directory Contents When Copying Directories", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    optionsDict['Copy Directory Contents (B)'] = directoryContentCopy