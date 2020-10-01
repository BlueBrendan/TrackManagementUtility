from bs4 import BeautifulSoup
import requests
import tkinter as tk
import time
import random

def sendRequest(url, headers, webScrapingWindow, leftComponentFrame):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return soup
    except requests.exceptions.ConnectionError:
        tk.Label(leftComponentFrame, text="Connection refused", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), anchor='w')
        refresh(webScrapingWindow)
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return False

def refresh(webScrapingWindow):
    webScrapingWindow.update()