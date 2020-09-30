import tkinter as tk
from tkinter.tix import *
import webbrowser

#main bg color
bg = "#282f3b"
#secondary color
secondary_bg = "#364153"

#global variables
currentPage=0

def rerenderControls(pageFrame, webScrapingPage):
    # page counter and navigation buttons
    tk.Button(pageFrame, text=" > ", state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="e").pack(side="right", padx=(0, 30))
    tk.Label(pageFrame, text=str(webScrapingPage) + "/" + str(webScrapingPage), font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor='e').pack(side="right", padx=(10, 10))
    tk.Button(pageFrame, text=" < ", state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="e").pack(side="right")

def enableControls(pageFrame, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, componentFrame):
    global currentPage
    currentPage = webScrapingPage
    #clear page frame
    widgetList = allWidgets(pageFrame)
    for item in widgetList: item.pack_forget()
    rightButton = tk.Button(pageFrame, text=" > ", state=DISABLED, font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="e", command=lambda: navigateRight(leftButton, rightButton, pageIndicator, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, componentFrame))
    rightButton.pack(side="right", padx=(0, 30))
    pageIndicator = tk.Label(pageFrame, text=str(webScrapingPage) + "/" + str(webScrapingPage), font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor='e')
    pageIndicator.pack(side="right", padx=(10, 10))
    leftButton = tk.Button(pageFrame, text=" < ", font=("Proxima Nova Rg", 11), fg="white", bg=bg, anchor="e", command=lambda: navigateLeft(leftButton, rightButton, pageIndicator, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, componentFrame))
    if webScrapingPage <= 1: leftButton.config(state=DISABLED)
    leftButton.pack(side="right")

def navigateLeft(leftButton, rightButton, pageIndicator, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, componentFrame):
    global currentPage
    currentPage-=1
    if currentPage <= 1: leftButton.config(state=DISABLED)
    rightButton.config(state=NORMAL)
    #rerender page indicator
    pageIndicator.config(text=str(currentPage) + "/" + str(webScrapingPage))

    # rerender left and right components
    widgetList = allWidgets(componentFrame)
    for item in widgetList: item.pack_forget()

    leftComponentFrame = tk.Frame(componentFrame, bg=bg)
    leftComponentFrame.pack(side="left", anchor="w", fill=Y)
    rightComponentFrame = tk.Frame(componentFrame, bg=bg)
    rightComponentFrame.pack(side="right", anchor="e", fill=Y)

    # left component
    renderLeftComponent(webScrapingLeftPane, leftComponentFrame, webScrapingLinks)
    # right component
    renderRightComponent(webScrapingRightPane, rightComponentFrame)

def navigateRight(leftButton, rightButton, pageIndicator, webScrapingLeftPane, webScrapingRightPane, webScrapingLinks, webScrapingPage, componentFrame):
    global currentPage
    currentPage+=1
    if currentPage == webScrapingPage: rightButton.config(state=DISABLED)
    leftButton.config(state=NORMAL)
    # rerender page indicator
    pageIndicator.config(text=str(currentPage) + "/" + str(webScrapingPage))

    # rerender left and right components
    widgetList = allWidgets(componentFrame)
    for item in widgetList: item.pack_forget()

    leftComponentFrame = tk.Frame(componentFrame, bg=bg)
    leftComponentFrame.pack(side="left", anchor="w", fill=Y)
    rightComponentFrame = tk.Frame(componentFrame, bg=bg)
    rightComponentFrame.pack(side="right", anchor="e", fill=Y)

    #left component
    renderLeftComponent(webScrapingLeftPane, leftComponentFrame, webScrapingLinks)
    # right component
    renderRightComponent(webScrapingRightPane, rightComponentFrame)

def renderLeftComponent(webScrapingLeftPane, leftComponentFrame, webScrapingLinks):
    widget = webScrapingLeftPane[currentPage]
    children = widget.winfo_children()
    for child in range(len(children)):
        if child == 0:
            link = tk.Label(leftComponentFrame)
            for key in children[child].configure(): link.config({key: children[child].cget(key)})
            # bind website link to click
            link.bind("<Button-1>", lambda e, link=webScrapingLinks[currentPage]: webbrowser.open_new(link))
            link.pack(padx=(10, 0), pady=(0, 25), anchor="w")
        else:
            tk.Label(leftComponentFrame, text=children[child]["text"], font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), pady=(5, 0), anchor="w")

def renderRightComponent(webScrapingRightPane, rightComponentFrame):
    widget = webScrapingRightPane[currentPage]
    children = widget.winfo_children()
    for child in range(len(children)):
        image = tk.Label(rightComponentFrame)
        for key in children[child].configure():
            image.config({key: children[child].cget(key)})
        image.pack(padx=(0, 100), anchor="e")

def allWidgets(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() : _list.extend(item.winfo_children())
    return _list
