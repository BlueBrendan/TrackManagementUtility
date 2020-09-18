from pydub import AudioSegment
import tkinter as tk

#global variables
overwrite = False

def handleReplayGain(directory, var, audio, webScrapingWindow):
    global overwrite
    file = AudioSegment.from_file(directory + '/' + var, "flac")
    rgvalue = -18 - float(file.dBFS)
    if audio["replaygain_track_gain"][0] != '' and audio["replaygain_track_gain"][0] != str(round(rgvalue,2)) + " dB":
        window = tk.Toplevel()
        window.title("ReplayGain Conflict")
        ws = window.winfo_screenwidth()  # width of the screen
        hs = window.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (400 / 2)
        y = (hs / 2) - (132 / 2)
        window.geometry('%dx%d+%d+%d' % (400, 120, x, y))
        tk.Label(window, text="Existing ReplayGain value detected. Replace " + str(audio["replaygain_track_gain"][0]) + " with " + str(round(rgvalue, 2)) + " dB?", wraplength=370).pack(side="top", pady=(20,15))
        buttons = tk.Frame(window)
        buttons.pack(side="top")
        tk.Button(buttons, text="Yes", command=lambda: setTrue(window, webScrapingWindow)).pack(side="left", padx=(15, 20), pady=(10, 0))
        tk.Button(buttons, text="No", command=closePopup(window, webScrapingWindow)).pack(side="left", padx=(20, 15), pady=(10, 0))
        window.wait_window()
        if overwrite:
            audio["replaygain_track_gain"] = str(round(rgvalue,2)) + ' dB'
            audio.save()
    else:
        audio["replaygain_track_gain"] = str(round(rgvalue, 2)) + ' dB'
        audio.save()
    return audio

def setTrue(window, webScrapingWindow):
    global overwrite
    overwrite = True
    window.destroy()
    webScrapingWindow.lift()

def closePopup(popup, webScrapingWindow):
    popup.destroy()
    webScrapingWindow.lift()