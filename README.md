# Track Management Utility V1.0

## Preface
Track Management Utility is targeted at a narrow niche of music connoisseurs who care enough about music to store, manage, and organize their (digital) collection on a local hard disk. 
This description mostly applies to DJs, live performers, audiophiles, and serious hobbyists/enthusiasts – people who are passionate enough for their craft to care about keeping a consistent tagging paradigm across their entire collection, which may consist of several thousand tracks or more that span across dozens of genres.

Track Management Utility currently supports six audio formats: .FLAC, .WAV, .MP3, .M4A, .AIFF, and .OGG. It will not recognize files with any other extension.

## Setup
1. Download the Track Management Utility folder from https://drive.google.com/drive/folders/1JeQbg10mIm5QU4qEjOOVwoe2vtmDOfqA?usp=sharing
2. Run Track Management Utility.exe

Do not delete or tamper with any of the other files in the folder; they are required for Track Management Utility to run properly. You can create a shortcut of the .exe file on the Desktop for easier access.

## Overview
Track Management Utility scrapes tags from music stores/DJ pools Junodownload and Beatport, as well as the music database Discogs. The operation details can be found in the Track Management Utility Documentation PDF.

## Dependencies
Track Management Utility is written in Python and uses Tkinter, Python's standard out-of-the-box graphical interface. Dependencies include Mutagen for audio file handling/tag editing, Beautiful Soup for preliminary tag scraping from the web, Selenium for reverse image search, and Pillow for image handling.

## Contact
If you'd like to report an issue or make a suggestion, you can contact me at brendanchoudj@gmail.com
