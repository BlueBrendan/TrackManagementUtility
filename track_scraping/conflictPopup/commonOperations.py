import tkinter as tk
from tkinter.tix import *
from PIL import Image, ImageTk
import getpass
import math

# import methods
from track_preparation.initiateTrack.commonOperations import resource_path

# main bg color
bg = "#282f3b"
# secondary color
secondary_bg = "#364153"

def reloadThumbnail(thumbnail, track, buttons, conflictFrame, thumbnailFrame):
    if type(thumbnail) != str:
        photo = ImageTk.PhotoImage(thumbnail[0])
        thumbnailImage = tk.Label(conflictFrame, image=photo)
        thumbnailImage.image = photo
        thumbnailButton = tk.Button(thumbnailFrame, image=photo, bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictFrame))
        thumbnailButton.pack(side="top")
        buttons.append(thumbnailButton)
    else:
        fileImageImport = Image.open(resource_path('Thumbnail.png'))
        fileImageImport = fileImageImport.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(thumbnailFrame, image=photo, bg=bg)
        fileImage.image = photo
        thumbnailButton = tk.Button(thumbnailFrame, image=photo, font=("Proxima Nova Rg", 11), bg="yellow", highlightcolor='yellow', highlightthickness=3, command=lambda: selectImage("THUMB", track, thumbnailButton, buttons, conflictFrame))
        thumbnailButton.pack(side="top", pady=(5, 10))
        buttons.append(thumbnailButton)
    return buttons

#needs to be updated
def loadImageButtons(start, end, imageFrame, images, resolutionsFrame, conflictFrame, track, buttons, page, options):
    imageButtons = []
    imageResolutions = []

    for i in range((start + (page * options["Number of Images Per Page (I)"].get())), min((start + (page * options["Number of Images Per Page (I)"].get()) + options["Number of Images Per Page (I)"].get()), end)):
        fileImageImport = images[i][0]
        photo = ImageTk.PhotoImage(fileImageImport)
        fileImage = tk.Label(imageFrame, image=photo)
        fileImage.image = photo
        imageButtons.append(tk.Button(imageFrame, image=photo, highlightthickness=3, command=lambda i=i: selectImage(i, track, imageButtons[i - (start + (page * options["Number of Images Per Page (I)"].get()))], buttons, conflictFrame)))
        imageButtons[len(imageButtons) - 1].pack(side="left", padx=(20, 20))
        buttons.append(imageButtons[len(imageButtons) - 1])
        imageResolutions.append(str(images[i][1]) + "x" + str(images[i][2]))
    # print resolutions underneath respective images
    for i in imageResolutions: tk.Label(resolutionsFrame, text=i, font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", padx=(90, 90), pady=(5, 5))

def loadNavigation(start, end, pageFrame, imageFrame, images, resolutionsFrame, conflictFrame, thumbnailFrame, track, thumbnail, page, direction, options):
    leftButton = tk.Button(pageFrame, text=" < ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="w", state=NORMAL, command=lambda: navigateLeft(start, end, imageFrame, images, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail, page, options))
    leftButton.pack(side="left", padx=(0, 15), pady=(15, 10))
    tk.Label(pageFrame, text=str(page + 1) + "/" + str(math.ceil(float(end - start) / float(options["Number of Images Per Page (I)"].get()))), font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(side="left", pady=(15, 10))
    # right button
    rightButton = tk.Button(pageFrame, text=" > ", font=("Proxima Nova Rg", 11), fg="white", bg=secondary_bg, anchor="e",  state=NORMAL, command=lambda: navigateRight(start, end, imageFrame, images, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail, page, options))
    rightButton.pack(side="left", padx=(15, 0), pady=(15, 10))
    if direction == "left":
        # deactivate left button if on first page
        if page == 0: leftButton.config(state=DISABLED)
    elif direction == "right":
        # deactivate right button if on last page
        if page+1 == math.ceil((end - start)/ float(options["Number of Images Per Page (I)"].get())): rightButton.config(state=DISABLED)
    elif direction == "load":
        # deactive right button if there is only one page
        leftButton.config(state=DISABLED)
        if math.ceil(float(end - start) / float(options["Number of Images Per Page (I)"].get())) == 1: rightButton.config(state=DISABLED)

#selecting image to variable
def selectImage(i, track, button, buttons, window):
    track.imageSelection = i
    #unhighlight all buttons
    for item in buttons: item.config(bg="white", highlightcolor="white")
    #highlight selected button
    button.config(bg="yellow", highlightcolor="yellow")
    window.update()

def navigateLeft(start, end, imageFrame, images, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail, page, options):
    page -= 1
    track.imageSelection = "THUMB"
    # buttons starts off as a list already containing the thumbnail button
    buttons = []
    # reload thumbnailFrame, imageFrame, resolutions Frame, and pageFrame
    reloadFrames(thumbnailFrame, imageFrame, resolutionsFrame, pageFrame)
    # reload thumbnail
    buttons = reloadThumbnail(thumbnail, track, buttons, conflictFrame, thumbnailFrame)
    # reload image buttons
    loadImageButtons(start, end, imageFrame, images, resolutionsFrame, conflictFrame, track, buttons, page, options)
    # reload navigation buttons and page indicator
    loadNavigation(start, end, pageFrame, imageFrame, images, resolutionsFrame, conflictFrame, thumbnailFrame, track, thumbnail, page, "left", options)

def navigateRight(start, end, imageFrame, images, resolutionsFrame, pageFrame, conflictFrame, thumbnailFrame, track, thumbnail, page, options):
    page += 1
    track.imageSelection = "THUMB"
    # buttons starts off as a list already containing the thumbnail button
    buttons = []
    # reload thumbnailFrame, imageFrame, resolutions Frame, and pageFrame
    reloadFrames(thumbnailFrame, imageFrame, resolutionsFrame, pageFrame)
    # reload thumbnail
    buttons = reloadThumbnail(thumbnail, track, buttons, conflictFrame, thumbnailFrame)
    # reload image buttons
    loadImageButtons(start, end, imageFrame, images, resolutionsFrame, conflictFrame, track, buttons, page, options)
    # reload navigation buttons and page indicator
    loadNavigation(start, end, pageFrame, imageFrame, images, resolutionsFrame, conflictFrame, thumbnailFrame, track, thumbnail, page, "right", options)

def reloadFrames(thumbnailFrame, imageFrame, resolutionsFrame, pageFrame):
    widgetList = allWidgets(thumbnailFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(imageFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(resolutionsFrame)
    for item in widgetList: item.pack_forget()
    widgetList = allWidgets(pageFrame)
    for item in widgetList: item.pack_forget()

def allWidgets(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() : _list.extend(item.winfo_children())
    return _list