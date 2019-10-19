#!/usr/bin/env python

import sys
import subprocess
import os
import tempfile
import json
import io
from multiprocessing import Process

import s3
import ocr
import frametimes
import hash

processes = {}
results = {}
def v2json(video, h):
    p = Process(target=runv2json, args=(video, h, results))
    processes[h] = p
    results[h] = None
    p.start()


def getresults(h):
    if results[h] is None and !processes[h].is_alive():
        raise Exception(h)
    return results[h]

def runv2json(video, h, results):
    pwd = os.getcwd()+'/'
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        if video.startswith('http'):
            filename = subprocess.run(['youtube-dl', '--get-filename', video], text=True, capture_output=True).stdout[:-1]
        else:
            filename=video
        screen = h+".screen"
        print(screen)
        sobj = s3.download(screen)
        if not sobj:
            if video.startswith('http'):
                ytdl = subprocess.run(["youtube-dl", video], check=True)
            fps = subprocess.run([pwd+"getimages.sh", filename], check=True, capture_output=True, text=True).stdout.split('\n')[0]
            sd = ocr.img2text(td, fps)
            jv = json.dumps(sd)
            s = io.BytesIO(jv.encode())
            s3.upload(s, screen)
            results[h] = jv
        else:
            results[h] = sobj

if __name__ == '__main__':
    print(v2json(sys.argv[1], hash.hash(sys.argv[1])))
