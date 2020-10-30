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
# mapping phrases to widgets
optionsDict = {}


def webScrapingTab(tab_parent, options, CONFIG_FILE):
    # web Scraping Tab
    tab1 = tk.Frame(tab_parent, bg=bg)
    tab_parent.pack(expand=1, fill='both')
    tab_parent.add(tab1, text="Scraping")
    # website settings
    tk.Label(tab1, text="Web Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(20, 0), pady=(20, 5), anchor="w")
    topComponentFrame = tk.Frame(tab1, bg=bg)
    topComponentFrame.pack(fill=X)
    leftComponentFrame = tk.Frame(topComponentFrame, bg=bg)
    leftComponentFrame.pack(side="left", anchor="nw")
    rightComponentFrame = tk.Frame(topComponentFrame, bg=bg)
    rightComponentFrame.pack(side="left", anchor="nw")

    # website options
    junodownloadFrame = tk.Frame(leftComponentFrame, bg=bg)
    junodownloadFrame.pack(anchor="w")
    tk.Checkbutton(junodownloadFrame, variable=options['Scrape Junodownload (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)', optionsDict, options), bg=bg).pack(padx=(30, 0), side="left")
    tk.Label(junodownloadFrame, text="Junodownload", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    beatportFrame = tk.Frame(leftComponentFrame, bg=bg)
    beatportFrame.pack(anchor="w")
    tk.Checkbutton(beatportFrame, variable=options['Scrape Beatport (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)', optionsDict, options), bg=bg).pack(padx=(30, 0), side="left")
    tk.Label(beatportFrame, text="Beatport", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    discogsFrame = tk.Frame(leftComponentFrame, bg=bg)
    discogsFrame.pack(anchor="w")
    tk.Checkbutton(discogsFrame, variable=options['Scrape Discogs (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)', optionsDict, options), bg=bg).pack(padx=(30, 0), side="left")
    tk.Label(discogsFrame, text="Discogs", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")



    # image scraping settings
    tk.Label(tab1, text="Image Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(20, 0), pady=(20, 5), anchor="w")
    # left image options
    imageOptionsContainer = tk.Frame(tab1, bg=bg)
    imageOptionsContainer.pack(fill=X)


    leftImageFrame = tk.Frame(imageOptionsContainer, bg=bg)
    leftImageFrame.pack(side="left", anchor="w")
    # web image option
    imageCheckFrame = tk.Frame(leftImageFrame, bg=bg)
    imageCheckFrame.pack(anchor="w")
    extractCheckbox = tk.Checkbutton(imageCheckFrame, variable=options['Extract Image from Website (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Extract Image from Website (B)', optionsDict, options), bg=bg)
    extractCheckbox.pack(padx=(30, 0), side="left")
    tk.Label(imageCheckFrame, text="Extract Image from Website", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # reverse image search options
    reverseImageFrame = tk.Frame(leftImageFrame, bg=bg)
    reverseImageFrame.pack(anchor="w")
    seleniumCheckbox = tk.Checkbutton(reverseImageFrame, variable=options['Reverse Image Search (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Reverse Image Search (B)', optionsDict, options), bg=bg)
    seleniumCheckbox.pack(padx=(30, 0), side="left")
    optionsDict['Reverse Image Search (B)'] = seleniumCheckbox
    tk.Label(reverseImageFrame, text="Reverse Image Search with Selenium", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    if options["Extract Image from Website (B)"].get() == False: seleniumCheckbox.config(state=DISABLED)

    # delete images
    deleteImagesFrame = tk.Frame(leftImageFrame, bg=bg)
    deleteImagesFrame.pack(anchor="w")
    deleteImages = tk.Checkbutton(deleteImagesFrame, variable=options['Delete Stored Images (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Delete Stored Images (B)', optionsDict, options), bg=bg)
    deleteImages.pack(padx=(30, 0), side="left")
    optionsDict['Delete Stored Images (B)'] = deleteImages
    tk.Label(deleteImagesFrame, text="Delete Stored Images after Completion", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    if options["Extract Image from Website (B)"].get()==False or options["Reverse Image Search (B)"].get() == False: deleteImages.config(state=DISABLED)

    # wait time
    waitTimeForm = tk.Frame(leftImageFrame, bg=bg)
    waitTimeForm.pack(anchor="w")
    waitTimeText = tk.Label(waitTimeForm, text="Image Load Wait Time (I)", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    time = StringVar(value=options["Image Load Wait Time (I)"].get())
    time.trace("w", lambda name, index, mode, time=time: timeEntrybox(CONFIG_FILE, "Image Load Wait Time (I)", time))
    waitTime = tk.Entry(waitTimeForm, width=3, textvariable=time, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    optionsDict['Image Load Wait Time (I)'] = waitTime
    validate = (waitTime.register(checkTimeValue))
    waitTime.configure(validatecommand=(validate, '%S'))
    if options["Extract Image from Website (B)"].get()==False or options["Reverse Image Search (B)"].get() == False: waitTime.config(state=DISABLED)
    waitTime.pack(padx=(35, 0), pady=(5, 0), side="left")
    waitTimeText.pack(padx=(10, 0), pady=(5, 0), side="left")
    # image display count
    imageDisplayCountForm = tk.Frame(leftImageFrame, bg=bg)
    imageDisplayCountForm.pack(anchor="w")
    imageDisplayText = tk.Label(imageDisplayCountForm, text="Number of Images Per Page (1-5)", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    imageCount = StringVar(value=options["Number of Images Per Page (I)"].get())
    imageCount.trace("w", lambda name, index, mode, imageCount=imageCount: imageEntrybox(CONFIG_FILE, "Number of Images Per Page (I)", imageCount))

    imageCountForm = tk.Entry(imageDisplayCountForm, width=3, textvariable=imageCount, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    if options["Extract Image from Website (B)"].get() == False or options["Reverse Image Search (B)"].get() == False: imageCountForm.config(state=DISABLED)
    optionsDict['Number of Images Per Page (I)'] = imageCountForm
    validate = (imageCountForm.register(checkImageValue))
    imageCountForm.configure(validatecommand=(validate, "%S", "%P"))
    imageCountForm.pack(padx=(35, 0), pady=(5, 0), side="left")
    imageDisplayText.pack(padx=(10, 0), pady=(5, 0), side="left")

    # right image options
    rightImageFrame = tk.Frame(imageOptionsContainer, bg=bg)
    rightImageFrame.pack(side="left", anchor="nw")

    # hide selenium window frame
    hideSeleniumFrame = tk.Frame(rightImageFrame, bg=bg)
    hideSeleniumFrame.pack(padx=(40, 0), anchor="w")
    # disable search checkbox
    hideSeleniumCheckbox = tk.Checkbutton(hideSeleniumFrame, variable=options['Hide Selenium Browser (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Hide Selenium Browser (B)', optionsDict, options), bg=bg)
    hideSeleniumCheckbox.pack(side="left")
    optionsDict['Hide Selenium Browser (B)'] = hideSeleniumCheckbox
    if options["Extract Image from Website (B)"].get() == False or options["Reverse Image Search (B)"].get() == False: hideSeleniumCheckbox.config(state=DISABLED)
    # disable resolution frame
    tk.Label(hideSeleniumFrame, text="Hide Selenium Browser", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # disable search frame
    disableSearchFrame = tk.Frame(rightImageFrame, bg=bg)
    disableSearchFrame.pack(padx=(40, 0), anchor="w")
    # disable search checkbox
    disableImageSearchCheckbox = tk.Checkbutton(disableSearchFrame, variable=options['Stop Search After Conditions (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Stop Search After Conditions (B)', optionsDict, options), bg=bg)
    disableImageSearchCheckbox.pack(side="left")
    if options["Extract Image from Website (B)"].get() == False or options["Reverse Image Search (B)"].get() == False: disableImageSearchCheckbox.config(state=DISABLED)
    optionsDict['Stop Search After Conditions (B)'] = disableImageSearchCheckbox
    # disable resolution frame
    tk.Label(disableSearchFrame, text="Stop Search After Conditions", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    disableResolutionFrame = tk.Frame(rightImageFrame, bg=bg)
    disableResolutionFrame.pack(anchor="w")
    width = StringVar(value=options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[0])
    width.trace("w", lambda name, index, mode, width=width: resolutionEntrybox(CONFIG_FILE, "Stop Search After Finding Image of Resolution (S)", width, "width"))
    height = StringVar(value=options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[1])
    height.trace("w", lambda name, index, mode, height=height: resolutionEntrybox(CONFIG_FILE, "Stop Search After Finding Image of Resolution (S)", height, "height"))

    widthEntrybox = tk.Entry(disableResolutionFrame, width=4, text='Threshold to Stop Search (px)', textvariable=width, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    if options["Extract Image from Website (B)"].get() == False or options["Reverse Image Search (B)"].get() == False or options['Stop Search After Conditions (B)'].get() == False: widthEntrybox.config(state=DISABLED)
    widthEntrybox.pack(padx=(45, 0), pady=(5, 0), side="left")
    tk.Label(disableResolutionFrame, text="  x  ", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(pady=(5, 0), side="left")
    heightEntrybox = tk.Entry(disableResolutionFrame, width=4, text='Threshold to Stop Search (px)', textvariable=height, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    if options["Extract Image from Website (B)"].get() == False or options["Reverse Image Search (B)"].get() == False or options['Stop Search After Conditions (B)'].get() == False: heightEntrybox.config(state=DISABLED)
    heightEntrybox.pack(pady=(5, 0), side="left")
    tk.Label(disableResolutionFrame, text=" Threshold to Stop Search (px)", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(5, 0), pady=(5, 0), side="left")
    optionsDict['Threshold to Stop Search (px)'] = [widthEntrybox, heightEntrybox]


def resolutionEntrybox(CONFIG_FILE, term, value, dimension):
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    if value.get() == '':
        if dimension == "width":
            with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('x', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + str(0)))
        elif dimension == "height":
            with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index('x', config_file.index(term)) + 1])) + str(0)))
    else:
        if dimension == "width":
            with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('x', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + str(value.get())))
        elif dimension == "height":
            with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index('x', config_file.index(term)) + 1])) + str(value.get())))
    file.close()

def timeEntrybox(CONFIG_FILE, term, value):
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    if value.get() == '':
        with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + str(0)))
    else:
        with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + str(value.get())))
    file.close()

def imageEntrybox(CONFIG_FILE, term, value):
    config_file = open(CONFIG_FILE, 'r').read()
    # convert to term
    if value.get() == '':
        with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + str(1)))
    else:
        with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index('\n', config_file.index(term) + len(term))]), str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + str(value.get())))
    file.close()

#check if input is an integer, reject if not
def checkTimeValue(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

#check if input is an integer equal to or below 5, reject if not
def checkImageValue(value, imageCount):
    if imageCount == '': return True
    try:
        int(value)
        if int(imageCount) <= 5: return True
        return False
    except ValueError:
        return False