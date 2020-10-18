#compares two runtimes. Return false if the difference between the two falls within the threshold (5s by default), return True otherwise

def compareRuntime(runtime, audio):
    if runtime == '': return False
    minutes = int(runtime.split(':')[0])
    seconds = int(runtime.split(':')[1])
    runtime = minutes * 60 + seconds
    difference = abs(runtime - audio.info.length)
    #max difference in seconds
    if difference > 5:return True
    else:return False