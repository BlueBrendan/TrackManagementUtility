#class for the FLAC format
class FLAC_Track:
    def __init__(self, audio, options):
        informalTagDict = {
            'Artist': 'artist',
            'Album': 'album',
            'Album Artist': 'albumartist',
            'BPM': 'bpm',
            'Comment': 'comment',
            'Compilation': 'compilation',
            'Copyright': 'copyright',
            'Discnumber': 'discnumber',
            'Genre': 'genre',
            'Key': 'initialkey',
            'Release_Date': 'date',
            'Title': 'title',
            'ReplayGain': 'replaygain_track_gain',
        }
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
        self.imageSelection = "THUMB"

#class for all file formats that use Vorbis tags (OGG)
class Vorbis_Track:
    def __init__(self, audio, options):
        informalTagDict = {
            'Artist': 'artist',
            'Album': 'album',
            'Album Artist': 'albumartist',
            'BPM': 'bpm',
            'Comment': 'comment',
            'Compilation': 'compilation',
            'Copyright': 'copyright',
            'Discnumber': 'discnumber',
            'Genre': 'genre',
            'Image': 'metadata_block_picture',
            'Key': 'initialkey',
            'Release_Date': 'date',
            'Title': 'title',
            'ReplayGain': 'replaygain_track_gain',
        }
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))
        self.imageSelection = "THUMB"

#class for all file formats that use ID3 tags (MP3, AIFF)
class ID3_Track:
    def __init__(self, audio, options):
        informalTagDict = {
            'Artist': 'TPE1',
            'Album': 'TALB',
            'Album Artist': 'TPE2',
            'BPM': 'TBPM',
            'Comment': 'COMM::eng',  # lang="eng"
            'Compilation': 'TCMP',
            'Copyright': 'TCOP',
            'Discnumber': 'TPOS',
            'Genre': 'TCON',
            'Image': 'APIC:',
            'Key': 'TKEY',
            'Release_Date': 'TDRC',
            'Title': 'TIT2',
            'ReplayGain': 'TXXX:replaygain_track_gain',  # desc="replay_track_gain"
        }
        for tag in options["Selected Tags (L)"]:
            if tag in informalTagDict: setattr(self, tag.lower(), str(audio[informalTagDict[tag]]))
        self.imageSelection = "THUMB"