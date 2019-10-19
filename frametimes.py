def convertToTimestamp(fps, imgnum):
    framenum = (imgnum-1)*100
    secondNum = frameNum // fps
    mins = secondNum // 60
    seconds = secondNum % 60
    return mins+":"+seconds
