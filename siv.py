#!/usr/bin/env python

import sys
import subprocess
import os
import tempfile
import json
import io

import s3
import ocr
import frametimes

def v2json(video):
    pwd = os.getcwd()+'/'
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        if video.startswith('http'):
            filename = subprocess.run(['youtube-dl', '--get-filename', video], text=True, capture_output=True).stdout[:-1]
        else:
            filename = video
        screen = filename+".screen"
        fobj = s3.download(screen)
        if not fobj:
            if video.startswith('http'):
                ytdl = subprocess.run(["youtube-dl", video], check=True)
            else:
                ext = os.path.splitext(video)[1]
                os.replace(pwd+video, video)
        else:
            return fobj.read()
        videofile = [fn for fn in os.listdir(td)][0]
        fps = subprocess.run([pwd+"getimages.sh", videofile], check=True, capture_output=True, text=True).stdout.split('\n')[0]
        d = ocr.img2text(td, fps)
        j = json.dumps(d)
        s = io.BytesIO(j.encode())
        s3.upload(s, screen)
        return j

if __name__ == '__main__':
    print(v2json(sys.argv[1]))
