#!/usr/bin/env python

import sys
import subprocess
import os
import tempfile

import ocr
import frametimes

def v2text(video):
    pwd = os.getcwd()+'/'
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        if video.startswith('http'):
            ytdl = subprocess.run(["youtube-dl", "-ovideo", sys.argv[1]], check=True)
        else:
            ext = os.path.splitext(video)[1]
            os.replace(pwd+video, "video"+ext)
        videofile = [fn for fn in os.listdir(td) if fn.startswith("video")][0]
        fps = subprocess.run([pwd+"getimages.sh", videofile], check=True).stdout
        print(fps)
        return ocr.img2text(td)

def search(video, string):
    text = v2text(video)
    print(text)

if __name__ == '__main__':
    search(sys.argv[1],'')
