import tkinter as tk
from tkinter.tix import *
from PIL import Image, ImageTk
import getpass
import os

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variables
currentPage = 1

def handleFinalReport(finalTitles, finalResults, characters, imageCounter, imageSelections, webScrapingWindow, thumbnails, options, CONFIG_FILE):
        global currentPage
        currentPage = 1
        finalReportWindow = tk.Toplevel()
        finalReportWindow.title("Final Report")
        finalReportWindow.configure(bg=bg)
        ws = finalReportWindow.winfo_screenwidth()  # width of the screen
        hs = finalReportWindow.winfo_screenheight()  # height of the screen
        y = (hs / 2) - (682 / 2)
        x = (ws / 2) - (550 / 2)
        finalReportWindow.geometry('%dx%d+%d+%d' % (550, 620, x, y))
        if characters > 40:
            x = (ws / 2) - ((550 + (characters * 1.5)) / 2)
            finalReportWindow.geometry('%dx%d+%d+%d' % (550 + (characters * 1.5), 620, x, y))
        tk.Label(finalReportWindow, text="Final Report", font=("Proxima Nova Rg", 13), fg="white", bg=bg).pack(side="top", pady=(30, 15))
        # frame for title
        titleFrame = tk.Frame(finalReportWindow, bg=bg)
        titleFrame.pack(side="top", anchor="n")
        tk.Label(titleFrame, text=finalTitles[0] + "\n", font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10, anchor="w").pack(side="top", anchor="w")
        # frame for report contents
        contentFrame = tk.Frame(finalReportWindow, bg=bg)
        contentFrame.pack(side="top", anchor="center")
        # remove leading newline character
        tk.Label(contentFrame, text=finalResults[0].lstrip() + '\n', font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10, anchor="w").pack(anchor="center")
        # frame for image
        imageFrame = tk.Frame(finalReportWindow, bg=bg)
        imageFrame.pack(side="top", anchor="n")
        renderImage(imageFrame, imageSelections, imageCounter, thumbnails, 0)

        # navigation buttons
        navigationButtons = tk.Frame(finalReportWindow, bg=bg)
        navigationButtons.pack(pady=(10, 10))
        rightNavigationButton = tk.Button(navigationButtons, text=" > ", font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="e", width=2, command=lambda: navigateRight(leftNavigationButton, rightNavigationButton, titleFrame, contentFrame, imageFrame, finalTitles, finalResults, imageSelections, imageCounter, thumbnails, pageIndicator))
        rightNavigationButton.pack(side="right")
        if len(finalResults) == 1: rightNavigationButton.config(state=DISABLED)
        pageIndicator = tk.Label(navigationButtons, text=str(currentPage) + "/" + str(len(finalResults)), font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor='e')
        pageIndicator.pack(side="right", padx=(10, 10))
        leftNavigationButton = tk.Button(navigationButtons, text=" < ", state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="e", width=2, command=lambda: navigateLeft(leftNavigationButton, rightNavigationButton, titleFrame, contentFrame, imageFrame, finalTitles, finalResults, imageSelections, imageCounter, thumbnails, pageIndicator))
        leftNavigationButton.pack(side="right")

        # load button and checkbox
        tk.Button(finalReportWindow, text='OK', command=lambda: completeSearch(finalReportWindow, webScrapingWindow, options), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side=TOP, pady=(35, 15))
        closeWindowButtonFrame = tk.Frame(finalReportWindow, bg=bg)
        closeWindowButtonFrame.pack()
        tk.Checkbutton(closeWindowButtonFrame, var=options["Close Scraping Window (B)"], activebackground=bg, command=lambda: closeScrapingWindowSelection(CONFIG_FILE), bg=bg).pack(side="left", pady=(0,10))
        tk.Label(closeWindowButtonFrame, text="Close scraping window", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", pady=(0,10))
        finalReportWindow.protocol('WM_DELETE_WINDOW', lambda: completeSearch(finalReportWindow, webScrapingWindow, options))
        finalReportWindow.iconbitmap(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/favicon.ico")
        finalReportWindow.lift()

def navigateLeft(leftNavigationButton, rightNavigationButton, titleFrame, contentFrame, imageFrame, finalTitles, finalResults, imageSelections, imageCounter, thumbnails, pageIndicator):
    global currentPage
    currentPage-=1
    # handle navigation frame
    if currentPage == 1: leftNavigationButton.config(state=DISABLED)
    rightNavigationButton.config(state=NORMAL)
    pageIndicator.config(text=str(currentPage) + "/" + str(len(finalResults)))

    # rerender title, content, and image frame
    widgetList = allWidgets(titleFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(contentFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(imageFrame)
    for item in widgetList: item.pack_forget()
    tk.Label(titleFrame, text=finalTitles[(currentPage-1)] + "\n", font=("Proxima Nova Rg", 11), fg="white", bg=bg, bd=-10, anchor="w").pack(side="top", anchor="w")
    # remove leading newline character
    tk.Label(contentFrame, text=finalResults[(currentPage-1)].lstrip() + '\n', font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10, anchor="center").pack(anchor="center")
    renderImage(imageFrame, imageSelections, imageCounter, thumbnails, (currentPage-1))

def navigateRight(leftNavigationButton, rightNavigationButton, titleFrame, contentFrame, imageFrame, finalTitles, finalResults, imageSelections, imageCounter, thumbnails, pageIndicator):
    global currentPage
    currentPage+=1
    # handle navigation frame
    if currentPage == len(finalResults): rightNavigationButton.config(state=DISABLED)
    leftNavigationButton.config(state=NORMAL)
    pageIndicator.config(text=str(currentPage) + "/" + str(len(finalResults)))

    # rerender title, content, and image frame
    widgetList = allWidgets(titleFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(contentFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(imageFrame)
    for item in widgetList: item.pack_forget()
    tk.Label(titleFrame, text=finalTitles[(currentPage-1)] + "\n", font=("Proxima Nova Rg", 11), fg="white", bg=bg, bd=-10, anchor="w").pack(side="top", anchor="w")
    # remove leading newline character
    tk.Label(contentFrame, text=finalResults[(currentPage-1)].lstrip() + '\n', font=("Proxima Nova Rg", 11), fg="white", bg=bg, justify="left", bd=-10, anchor="center").pack(anchor="center")
    renderImage(imageFrame, imageSelections, imageCounter, thumbnails, (currentPage-1))

def renderImage(contentFrame, imageSelections, imageCounter, thumbnails, index):
    # load non-thumbnailimage
    if imageCounter >= 1 and imageSelections[index][0] != 'THUMB':
        fileImageImport = imageSelections[index][0]
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(contentFrame, image=photo, bg=bg)
        fileImage.image = photo
        fileImage.pack(side="top", pady=(10, 15), anchor="n")
        # resolution
        tk.Label(contentFrame, text=str(imageSelections[index][1]) + "x" + str(imageSelections[index][2]), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(0, 10), anchor="n")
    # load thumbnail image
    else:
        fileImageImport = thumbnails[index][0]
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(contentFrame, image=photo, bg=bg)
        fileImage.image = photo
        fileImage.pack(side="top", pady=(10, 15))
        # resolution
        tk.Label(contentFrame, text=str(thumbnails[index][1]) + "x" + str(thumbnails[index][2]), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="top", pady=(0, 10))

#handle subdirectory selection
def closeScrapingWindowSelection(CONFIG_FILE):
    config_file = open(CONFIG_FILE, 'r').read()
    #if true, turn option to false
    term = "Close Scraping Window (B)"
    if config_file[config_file.index(term) + len(term)+1:config_file.index('\n', config_file.index(term) + len(term))]=="True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term))+1]) + "True", str(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term))+1])) + "False"))
        file.close()
    #if false, turn option to true
    elif config_file[config_file.index(term) + len(term)+1:config_file.index('\n', config_file.index(term) + len(term))]=="False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term)) + 1]) + "False", str(str(config_file[config_file.index(term)+1:config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()

def completeSearch(finalReportWindow, webScrapingWindow, options):
    finalReportWindow.destroy()
    if options["Close Scraping Window (B)"].get() != False: webScrapingWindow.destroy()
    else: webScrapingWindow.lift()
    # delete all images in temp if both revese image search and delete stored image options are both true
    if options["Delete Stored Images (B)"].get() == True:
        images = os.listdir(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/")
        for image in images: os.remove(r"C:/Users/" + str(getpass.getuser()) + "/Documents/Track Management Utility/Temp/" + str(image))

def allWidgets(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children(): _list.extend(item.winfo_children())
    return _list