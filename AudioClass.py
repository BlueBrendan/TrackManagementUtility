from PIL import Image
from mutagen.flac import Picture
from io import BytesIO
import base64

# class for the FLAC format
class FLAC_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
        self.imageSelection = "THUMB"
        if browser != '':  self.browser = browser
        else: self.browser = 'NA'
        self.stop = False
        picture = audio.pictures
        if len(picture) > 0 and options['Stop Search After Conditions (B)'].get():
            stream = BytesIO(picture[0].data)
            image = Image.open(stream).convert("RGBA")
            width, height = image.size
            if width >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[0]) and height >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[1]): self.stop = True
            stream.close()

# class for all file formats that use Vorbis tags (OGG)
class Vorbis_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
        self.imageSelection = "THUMB"
        if browser != '': self.browser = browser
        else: self.browser = 'NA'
        self.stop = False
        if "metadata_block_picture" in audio and options['Stop Search After Conditions (B)'].get():
            imageFrame = audio["metadata_block_picture"]
            if imageFrame[0] != '':
                data = base64.b64decode(imageFrame[0])
                image = Picture(data)
                stream = BytesIO(image.data)
                image = Image.open(stream).convert("RGBA")
                width, height = image.size
                if width >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[0]) and height >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[1]): self.stop = True
                stream.close()

# class for all file formats that use ID3 tags (MP3, AIFF)
class ID3_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]]))
        self.imageSelection = "THUMB"
        if browser != '': self.browser = browser
        else: self.browser = 'NA'
        self.stop = False
        if 'APIC:' in audio and options['Stop Search After Conditions (B)'].get():
            image = audio["APIC:"]
            if image != b'':
                stream = BytesIO(image.data)
                image = Image.open(stream).convert("RGBA")
                width, height = image.size
                if width >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[0]) and height >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[1]): self.stop = True
                stream.close()

# class for ALAC file format (MP4)
class M4A_Track:
    def __init__(self, audio, options, informalTagDict, browser):
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict and tag != "Image" and tag != "Compilation":
                # key value contained in bytes form
                if tag.lower() == 'key':
                    if len(audio[informalTagDict[tag]]) > 0: setattr(self, tag.lower(), audio[informalTagDict[tag]][0].decode('utf-8'))
                    else: setattr(self, tag.lower(), "")
                elif len(audio[informalTagDict[tag]]) > 0: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
                else: setattr(self, tag.lower(), "")
        self.imageSelection = "THUMB"
        if browser != '': self.browser = browser
        else: self.browser = 'NA'
        self.stop = False
        if "covr" in audio and options['Stop Search After Conditions (B)'].get():
            image = audio["covr"]
            if len(image) != 0:
                stream = BytesIO(image[0])
                image = Image.open(stream).convert("RGBA")
                width, height = image.size
                if width >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[0]) and height >= int(options["Stop Search After Finding Image of Resolution (S)"].get().split('x')[1]): self.stop = True
                stream.close()