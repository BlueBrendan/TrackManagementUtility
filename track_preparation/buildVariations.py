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

    triggerStrings = ["é", "(", "'s", "pt.", ".", ",", "&", "-mix", "-extended", "-remix", "-version"]
    title = title.lower()
    newTitle = title.lower()
    for string in triggerStrings:
        if string.lower() in newTitle:
            # unique character that implies the existence of )
            if string == "(":
                if ")" in title:
                    newTitle = str(newTitle[0:newTitle.index("(")]) + str(newTitle[newTitle.index("(") + len("("):])
                    newTitle = str(newTitle[0:newTitle.index(")")]) + str(newTitle[newTitle.index(")") + len(")"):])
                    titleVariations.append(newTitle.lower())
            elif string == "&":
                titleVariations.append(newTitle.replace("&", "and").lower())
                titleVariations.append(title.replace("&", "and").lower())
                newTitle = str(newTitle[0:newTitle.index(string)]) + str(newTitle[newTitle.index(string) + len(string):])
                titleVariations.append(newTitle.lower())
                titleVariations.append(str(title[0:title.index(string)]).lower() + str(title[title.index(string) + len(string):]).lower())
            elif string == "pt.":
                titleVariations.append(title.replace(string, "part").lower())
                titleVariations.append(title.replace(string, "pt").lower())
                newTitle = str(newTitle[0:newTitle.index(string)]) + str("part") + str(newTitle[newTitle.index(string) + len(string):])
            elif string == "-remix":
                titleVariations.append(newTitle.replace(string, "-mix").lower())
                titleVariations.append(title.replace(string, "-mix").lower())
                titleVariations.append(newTitle.replace(string, "-extended-remix").lower())
                titleVariations.append(title.replace(string, "-extended-remix").lower())
            elif string == "é":
                titleVariations.append(newTitle.replace(string, "e").lower())
                titleVariations.append(title.replace(string, "e").lower())
                titleVariations.append(newTitle.replace(string, "é").lower())
                titleVariations.append(title.replace(string, "é").lower())
            else:
                newTitle = str(newTitle[0:newTitle.index(string)]) + str(newTitle[newTitle.index(string) + len(string):])
                titleVariations.append(newTitle.lower())
                if string in title: titleVariations.append(str(title[0:title.index(string)]).lower() + str(title[title.index(string) + len(string):]).lower())
    return artistVariations, titleVariations