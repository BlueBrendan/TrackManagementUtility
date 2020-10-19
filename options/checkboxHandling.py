from tkinter.tix import *

def checkbox(CONFIG_FILE, term, suboptions, condition, count):
    config_file = open(CONFIG_FILE, 'r').read()
    # if true, turn option to false
    if config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "True":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "True",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "False"))
        file.close()
        if len(suboptions) > 0:
            #disable all provided suboptions
            for suboption in suboptions:
                suboption.configure(state=DISABLED)
    # if false, turn option to true
    elif config_file[config_file.index(term) + len(term) + 1:config_file.index('\n', config_file.index(term) + len(term))] == "False":
        with open(CONFIG_FILE, 'wt') as file:
            file.write(config_file.replace(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1]) + "False",str(str(config_file[config_file.index(term) + 1:config_file.index(':', config_file.index(term)) + 1])) + "True"))
        file.close()
        if len(suboptions) > 0:
            # enable all provided suboptions
            if condition:
                for suboption in suboptions: suboption.configure(state=NORMAL)
            # only enable first suboption
            else:
                for i in range(count): suboptions[i].configure(state=NORMAL)