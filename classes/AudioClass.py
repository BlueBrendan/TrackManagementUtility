#class for audiotrack file (stores tags externally)
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
            'Release Date': 'date',
            'Title': 'title',
            'ReplayGain': 'replaygain_track_gain',
        }
        for tag in options["Selected Tags (L)"]: setattr(self, tag.lower(), str(audio[informalTagDict[tag]][0]))

class AIFF_Track:
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
            'Release Date': 'TDRC',
            'Title': 'TIT2',
            'ReplayGain': 'TXXX:replaygain_track_gain',  # desc="replay_track_gain"
        }
        for tag in options["Selected Tags (L)"]: setattr(self, tag.lower(), str(audio[informalTagDict[tag]]))