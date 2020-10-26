from tkinter.tix import *

# global variables
optionsHierarchyDict = {
    'Extract Image from Website (B)': 'Reverse Image Search (B)',
    'Reverse Image Search (B)': ['Delete Stored Images (B)', 'Image Load Wait Time (I)', 'Number of Images Per Page (I)', 'Stop Search After Conditions (B)'],
    'Stop Search After Conditions (B)': 'Threshold to Stop Search (px)',
}

def checkbox(CONFIG_FILE, term, suboptions, options):
    config_file = open(CONFIG_FILE, 'r').read()
    checked = True
    # if true, turn option to false
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "True":
        with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "True",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "False"))
        file.close()
        checked = False
    elif config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "False":
        with open(CONFIG_FILE, 'wt') as file: file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "False",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()
        checked = True
    nestedOptionCheck(checked, term, suboptions, options)

# handle nested options
def nestedOptionCheck(checked, term, suboptions, options):
    if term in optionsHierarchyDict:
        if type(optionsHierarchyDict[term]) == list:
            for item in optionsHierarchyDict[term]:
                if checked: stop = optionsListSubroutine(suboptions, item, NORMAL, options)
                else: stop = optionsListSubroutine(suboptions, item, DISABLED, options)
                if not stop: nestedOptionCheck(checked, item, suboptions, options)
        else:
            if checked:
                if not optionSubroutine(suboptions, term, NORMAL, options): nestedOptionCheck(checked, optionsHierarchyDict[term], suboptions, options)
            else:
                if not optionSubroutine(suboptions, term, DISABLED, options): nestedOptionCheck(checked, optionsHierarchyDict[term], suboptions, options)

# check/uncheck all nested options, stop if option was disabled and unchecked
def optionSubroutine(suboptions, term, state, options):
    stop = False
    if type(suboptions[optionsHierarchyDict[term]]) == list:
        for item in suboptions[optionsHierarchyDict[term]]:
            if state != item.cget('state') and item.cget('state') == DISABLED: stop = True
            item.configure(state=state)
    else:
        if suboptions[optionsHierarchyDict[term]].cget('state') == DISABLED and options[optionsHierarchyDict[term]].get() == False: stop = True
        suboptions[optionsHierarchyDict[term]].configure(state=state)
    return stop

def optionsListSubroutine(suboptions, term, state, options):
    stop = False
    if type(suboptions[term]) == list:
        for item in suboptions[term]:
            if state != item.cget('state') and item.cget('state') == DISABLED: stop = True
            item.configure(state=state)
    else:
        if suboptions[term].cget('state') == DISABLED and options[term].get() == False: stop = True
        suboptions[term].configure(state=state)
    return stop