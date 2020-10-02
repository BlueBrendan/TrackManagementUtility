from bs4 import BeautifulSoup
import requests
import tkinter as tk
import time
import random
import queue
import threading
import time

def prepareRequest(url, headers, webScrapingWindow, leftComponentFrame):
    try:
        q = queue.Queue(5)
        s = queue.Queue(5)
        requestThread = threading.Thread(target=sendRequest, args=(url, headers, q, s))
        requestThread.start()
        webScrapingWindow.after(100, lambda: checkQueue(q, webScrapingWindow))
        soup = s.get()
        # generate random waiting time to avoid being blocked
        waitThread = threading.Thread(target=wait, args=(q, ))
        waitThread.start()
        webScrapingWindow.after(100, lambda: checkQueue(q, webScrapingWindow))
        return soup
    except requests.exceptions.ConnectionError:
        tk.Label(leftComponentFrame, text="Connection refused", font=("Proxima Nova Rg", 11), fg="white", bg=bg).pack(padx=(10, 0), anchor='w')
        refresh(webScrapingWindow)
        # generate random waiting time to avoid being blocked
        time.sleep(random.uniform(1, 3.5))
        return False

def sendRequest(url, headers, q, s):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    s.put(soup)
    q.put("Finished")

def wait(q):
    print
    time.sleep(random.uniform(1, 3.5))
    q.put("Finished")

def checkQueue(q, webScrapingWindow):
    try:
        task = q.get(False)
    except queue.Empty:
        webScrapingWindow.after(100, lambda: checkQueue(q, webScrapingWindow))

def refresh(webScrapingWindow):
    webScrapingWindow.update()