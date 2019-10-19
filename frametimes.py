def convertToTimestamp(fps, imgnum):
    frameNum = (imgnum-1)*100
    secondNum = frameNum // fps
    mins = secondNum // 60
    seconds = secondNum % 60
    return str(int(mins))+":"+str(int(seconds))
