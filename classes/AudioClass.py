#class for audiotrack file (stores tags externally)
class AudioTrack:
    def __init__(self, audio):
        interestParameters = ['artist', 'title', 'date', 'BPM', 'initialkey', 'genre', 'replaygain_track_gain']
        self.artist = audio["artist"][0]
        self.title = audio["title"][0]
        self.year = ''
        self.BPM = ''
        self.key = ''
        self.genre = ''
        self.replaygain_track_gain = ''