# class for the FLAC format
class FLAC_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
        self.imageSelection = "THUMB"
        if browser != '': self.browser = browser
        else: self.browser = ''
        self.stop = False

# class for all file formats that use Vorbis tags (OGG)
class Vorbis_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
        self.imageSelection = "THUMB"
        if browser != '': self.browser = browser
        else: self.browser = ''
        self.stop = False

# class for all file formats that use ID3 tags (MP3, AIFF)
class ID3_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]]))
        self.imageSelection = "THUMB"
        if browser != '': self.browser = browser
        else: self.browser = ''
        self.stop = False

# class for ALAC file format (MP4)
class M4A_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict and tag != "Image" and tag != "Compilation":
                #key value contained in bytes form
                if tag.lower() == 'key':
                    if len(audio[informalTagDict[tag]]) > 0: setattr(self, tag.lower(), audio[informalTagDict[tag]][0].decode('utf-8'))
                    else: setattr(self, tag.lower(), "")
                elif len(audio[informalTagDict[tag]]) > 0: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
                else: setattr(self, tag.lower(), "")
        self.imageSelection = "THUMB"
        if browser != '': self.browser = browser
        else: self.browser = ''
        self.stop = False