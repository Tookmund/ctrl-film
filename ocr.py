#!/usr/bin/env python
import os
import sys
import pytesseract
from collections import OrderedDict
from frametimes import convertToTimestamp

def img2text(folder, fps):
    d = OrderedDict()
    for pic in sorted(os.listdir(folder)):
        if pic.endswith('.png'):
            t = pic[4:-4]
            ts = convertToTimestamp(float(fps), int(t))
            d[ts] = pytesseract.image_to_string(folder+'/'+pic)
    return d

if __name__ == '__main__':
    img2text(sys.argv[1])
