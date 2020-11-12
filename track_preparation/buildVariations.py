from tkinter.tix import *

def buildVariations(artist, title):
    # strip title of common prefixes like "Original Mix" or "Extended Mix"
    artistVariations = []
    titleVariations = []
    if " (Original Mix)" in title:
        titleVariations.append(title[0:title.index(" (Original Mix)")].lower())
    # strip title of spaces, paranthesis, ampersands, and other symbols that might botch the search
    spaces = re.finditer(" ", title)
    spacePositions = [match.start() for match in spaces]
    for var in spacePositions:
         title = title[0:var] + "-" + title[var + 1:]
    titleVariations.append(title.lower())
    spaces = re.finditer(" ", artist)
    spacePositions = [match.start() for match in spaces]
    for var in spacePositions:
        artist = artist[0:var] + "-" + artist[var + 1:]
    artistVariations.append(artist.lower())

    triggerStrings = ["feat.", "é", '(', "'s", "pt.", ".", ",", "&", "-mix", '-extended', '-original', '-instrumental', "-remix", "-version"]
    for string in triggerStrings:
        # feat.
        if string == 'feat.':
            for title in titleVariations:
                if ' feat.' in title: titleVariations.append(title.replace(' feat.', '').lower())
                elif 'feat. ' in title: titleVariations.append(title.replace('feat. ', '').lower())
        # é
        if string == 'é':
            titleVariations = stringReplace(string, titleVariations, "é", 'e')
            titleVariations = stringReplace(string, titleVariations, "é", 'é')
        # parenthesis
        elif string == '(':
            for title in titleVariations:
                if '(' in title and ')' in title: titleVariations.append(title.replace('(', '').replace(')', '').lower())
        # apostrophe
        elif string == "'s": titleVariations = stringReplace(string, titleVariations, "'s", 's')
        # pt.
        elif string == 'pt.': titleVariations = stringReplace(string, titleVariations, 'pt.', 'part')
        # part
        elif string == 'part': titleVariations = stringReplace(string, titleVariations, 'part', 'pt.')
        # dot
        elif string == '.': titleVariations = stringReplace(string, titleVariations, '.', '')
        # comma
        elif string == ',': titleVariations = stringReplace(string, titleVariations, ',', '')
        # ampersand
        elif string == '&':
            for title in titleVariations:
                if '-&' in title:
                    titleVariations.append(title.replace('&', 'and').lower())
                    titleVariations.append(title.replace('-&', '').lower())
                elif '&-' in title:
                    titleVariations.append(title.replace('&', 'and').lower())
                    titleVariations.append(title.replace('&-', '').lower())
        # -mix
        elif string == '-mix':
            titleVariations = stringReplace(string, titleVariations, '-mix', '')
            titleVariations = stringReplace(string, titleVariations, 'mix', 'remix')
        # -remix
        elif string == '-remix':
            titleVariations = stringReplace(string, titleVariations, '-remix', '')
            titleVariations = stringReplace(string, titleVariations, 'remix', 'mix')
        # -extended
        elif string == '-extended':
            titleVariations = stringReplace(string, titleVariations, '-extended', '')
            titleVariations = stringCutoff('-extended', titleVariations)
        # -original
        elif string == '-original':
            titleVariations = stringReplace(string, titleVariations, '-original', '')
            titleVariations = stringCutoff('-original', titleVariations)
        # instrumental
        elif string == '-instrumental':
            titleVariations = stringReplace(string, titleVariations, '-instrumental', '')
            titleVariations = stringCutoff('-instrumental', titleVariations)
        # version
        elif string == '-version':
            titleVariations = stringReplace(string, titleVariations, 'version', 'mix')
            titleVariations = stringReplace(string, titleVariations, 'version', 'remix')
            titleVariations = stringCutoff('-version', titleVariations)
    return artistVariations, titleVariations

def stringReplace(string, titleVariations, before, after):
    for title in titleVariations:
        if string in title: titleVariations.append(title.replace(before, after))
    return titleVariations

def stringCutoff(string, titleVariations):
    for title in titleVariations:
        if string in title: titleVariations.append(str(title[0:title.index(string)]).lower())
    return titleVariations