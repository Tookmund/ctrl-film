#!/usr/bin/env python
import os
import sys
import pytesseract

def img2text(folder):
    s = ''
    for pic in os.listdir(folder):
        if pic.endswith('.png'):
           s += pytesseract.image_to_string(folder+'/'+pic)
    return s

if __name__ == '__main__':
    img2text(sys.argv[1])
