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
import transcribe
import hash

def v2json(video, h=None):
    pwd = os.getcwd()+'/'
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        if video.startswith('http'):
            filename = subprocess.run(['youtube-dl', '--get-filename', video], text=True, capture_output=True).stdout[:-1]
            if h is None:
                h = hash.hash(video)
        else:
            filename=video
            if h is None:
                h = hash.hash(open(filename))
        screen = h+".screen"
        sobj = s3.download(screen)
        #audio = filename+".audio"
        #aobj = s3.download(audio)
        if not sobj:
            if video.startswith('http'):
                ytdl = subprocess.run(["youtube-dl", video], check=True)
            fps = subprocess.run([pwd+"getimages.sh", filename], check=True, capture_output=True, text=True).stdout.split('\n')[0]
            sd = ocr.img2text(td, fps)
            jv = json.dumps(d)
            s = io.BytesIO(jv.encode())
            s3.upload(s, screen)
            sobj = sd
            #ad = transcribe(td+filename)
            #ja = json.dumps(d)
            #a = io.BytesIO(jv.encode())
            #s3.upload(a, audio)
            #aobj = a
        return sobj

if __name__ == '__main__':
    print(v2json(sys.argv[1]))
