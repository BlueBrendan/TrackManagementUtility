import tkinter as tk
from tkinter.tix import *

# import methods
from options.checkboxHandling import checkbox

# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"
# invalid selection color
invalid_bg = "#801212"

def webScrapingTab(tab_parent, options, CONFIG_FILE):
    # web Scraping Tab
    tab1 = tk.Frame(tab_parent, bg=bg)
    tab_parent.pack(expand=1, fill='both')
    tab_parent.add(tab1, text="Scraping")
    # website settings
    tk.Label(tab1, text="Web Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    topComponentFrame = tk.Frame(tab1, bg=bg)
    topComponentFrame.pack(fill=X)
    leftComponentFrame = tk.Frame(topComponentFrame, bg=bg)
    leftComponentFrame.pack(side="left", anchor="nw")
    rightComponentFrame = tk.Frame(topComponentFrame, bg=bg)
    rightComponentFrame.pack(side="left", anchor="nw")

    # website options
    junodownloadFrame = tk.Frame(leftComponentFrame, bg=bg)
    junodownloadFrame.pack(anchor="w")
    tk.Checkbutton(junodownloadFrame, variable=options['Scrape Junodownload (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Junodownload (B)', [], True, 0), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(junodownloadFrame, text="Junodownload", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    beatportFrame = tk.Frame(leftComponentFrame, bg=bg)
    beatportFrame.pack(anchor="w")
    tk.Checkbutton(beatportFrame, variable=options['Scrape Beatport (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Beatport (B)', [], True, 0), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(beatportFrame, text="Beatport", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    discogsFrame = tk.Frame(leftComponentFrame, bg=bg)
    discogsFrame.pack(anchor="w")
    tk.Checkbutton(discogsFrame, variable=options['Scrape Discogs (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Scrape Discogs (B)', [], True, 0), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(discogsFrame, text="Discogs", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # web image option
    imageOptions = []
    imageCheckFrame = tk.Frame(rightComponentFrame, bg=bg)
    imageCheckFrame.pack(anchor="w")
    tk.Checkbutton(imageCheckFrame, variable=options["Extract Image from Website (B)"], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, "Extract Image from Website (B)", imageOptions, options['Reverse Image Search (B)'].get(), 1), bg=bg).pack(padx=(20, 0), side="left")
    tk.Label(imageCheckFrame, text="Extract Image from Website", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")

    # image scraping settings
    tk.Label(tab1, text="Image Scraping", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(padx=(10, 0), pady=(20, 5), anchor="w")
    imageScrapingSuboptions = []

    # left image options
    imageOptionsContainer = tk.Frame(tab1, bg=bg)
    imageOptionsContainer.pack(fill=X)
    leftImageFrame = tk.Frame(imageOptionsContainer, bg=bg)
    leftImageFrame.pack(side="left", anchor="w")
    # reverse image search options
    reverseImageFrame = tk.Frame(leftImageFrame, bg=bg)
    reverseImageFrame.pack(anchor="w")
    seleniumCheckbox = tk.Checkbutton(reverseImageFrame, variable=options['Reverse Image Search (B)'], onvalue=True, offvalue=False,  activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Reverse Image Search (B)', imageScrapingSuboptions, True, 0), bg=bg)
    seleniumCheckbox.pack(padx=(20, 0), side="left")
    tk.Label(reverseImageFrame, text="Reverse Image Search with Selenium", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    if options["Extract Image from Website (B)"].get() == False: seleniumCheckbox.config(state=DISABLED)
    imageOptions.append(seleniumCheckbox)

    # delete images
    deleteImagesFrame = tk.Frame(leftImageFrame, bg=bg)
    deleteImagesFrame.pack(anchor="w")
    deleteImages = tk.Checkbutton(deleteImagesFrame, variable=options['Delete Stored Images (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Delete Stored Images (B)', [], True, 0), bg=bg)
    deleteImages.pack(padx=(20, 0), side="left")
    tk.Label(deleteImagesFrame, text="Delete Stored Images after Completion", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    if options["Extract Image from Website (B)"].get()==False or options["Reverse Image Search (B)"].get() == False: deleteImages.config(state=DISABLED)
    imageScrapingSuboptions.append(deleteImages)
    imageOptions.append(deleteImages)

    # wait time
    waitTimeForm = tk.Frame(leftImageFrame, bg=bg)
    waitTimeForm.pack(anchor="w")
    waitTimeText = tk.Label(waitTimeForm, text="Image Load Wait Time (s)", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    time = StringVar(value=options["Image Load Wait Time (I)"].get())
    time.trace("w", lambda name, index, mode, time=time: timeEntrybox(CONFIG_FILE, "Image Load Wait Time (I)", time))

    waitTime = tk.Entry(waitTimeForm, width=3, textvariable=time, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    validate = (waitTime.register(checkTimeValue))
    waitTime.configure(validatecommand=(validate, '%S'))
    imageScrapingSuboptions.append(waitTime)
    imageOptions.append(waitTime)

    if options["Extract Image from Website (B)"].get()==False or options["Reverse Image Search (B)"].get() == False: waitTime.config(state=DISABLED)
    waitTime.pack(padx=(25, 0), side="left")
    waitTimeText.pack(padx=(10, 0), pady=(5, 0), side="left")

    # image display count
    imageDisplayCountForm = tk.Frame(leftImageFrame, bg=bg)
    imageDisplayCountForm.pack(anchor="w")
    imageDisplayText = tk.Label(imageDisplayCountForm, text="Number of Images Per Page (1-5)", font=("Proxima Nova Rg", 11), fg="white", bg=bg)
    imageCount = StringVar(value=options["Number of Images Per Page (I)"].get())
    imageCount.trace("w", lambda name, index, mode, imageCount=imageCount: imageEntrybox(CONFIG_FILE, "Number of Images Per Page (I)", imageCount))

    imageCountForm = tk.Entry(imageDisplayCountForm, width=3, textvariable=imageCount, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    validate = (imageCountForm.register(checkImageValue))
    imageCountForm.configure(validatecommand=(validate, "%S", "%P"))
    imageCountForm.pack(padx=(25, 0), side="left")
    imageDisplayText.pack(padx=(10, 0), pady=(5, 0), side="left")
    imageScrapingSuboptions.append(imageCountForm)
    imageOptions.append(imageCountForm)

    # right image options
    rightImageFrame = tk.Frame(imageOptionsContainer, bg=bg)
    rightImageFrame.pack(side="left", anchor="nw")
    # disable search frame
    disableSearchFrame = tk.Frame(rightImageFrame, bg=bg)
    disableSearchFrame.pack(padx=(40, 0), anchor="w")
    # disable search checkbox
    stopSearchSuboptions = []
    disableImageSearchCheckbox = tk.Checkbutton(disableSearchFrame, variable=options['Stop Search After Conditions (B)'], onvalue=True, offvalue=False, activebackground=bg, command=lambda: checkbox(CONFIG_FILE, 'Stop Search After Conditions (B)', stopSearchSuboptions, True, 0), bg=bg)
    disableImageSearchCheckbox.pack(side="left")
    imageOptions.append(disableImageSearchCheckbox)
    imageScrapingSuboptions.append(disableImageSearchCheckbox)

    # disable resolution frame
    tk.Label(disableSearchFrame, text="Stop Search After Conditions", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    disableResolutionFrame = tk.Frame(rightImageFrame, bg=bg)
    disableResolutionFrame.pack(anchor="w")
    width = StringVar(value=options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[0])
    width.trace("w", lambda name, index, mode, width=width: resolutionEntrybox(CONFIG_FILE, "Stop Search After Finding Image of Resolution (S)", width, "width"))
    height = StringVar(value=options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[1])
    height.trace("w", lambda name, index, mode, height=height: resolutionEntrybox(CONFIG_FILE, "Stop Search After Finding Image of Resolution (S)", height, "height"))

    widthEntrybox = tk.Entry(disableResolutionFrame, width=4, textvariable=width, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    widthEntrybox.pack(padx=(40, 0), side="left")
    tk.Label(disableResolutionFrame, text="  x  ", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    heightEntrybox = tk.Entry(disableResolutionFrame, width=4, textvariable=height, validate="key", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg)
    heightEntrybox.pack(side="left")
    tk.Label(disableResolutionFrame, text=" Threshold to Stop Search (px)", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left")
    imageOptions.append(widthEntrybox)
    imageOptions.append(heightEntrybox)
    imageScrapingSuboptions.append(widthEntrybox)
    imageScrapingSuboptions.append(heightEntrybox)
    stopSearchSuboptions.append(widthEntrybox)
    stopSearchSuboptions.append(heightEntrybox)



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