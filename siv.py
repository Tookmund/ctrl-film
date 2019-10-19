#!/usr/bin/env python

import sys
import subprocess
import os
import tempfile
import json
import io
import time
import multiprocessing

import s3
import ocr
import frametimes
import audio
import hash

processes = {}
manager = multiprocessing.Manager()
results = manager.dict()

def v2json(video, h):
    results[h] = None
    p = multiprocessing.Process(target=runv2json, args=(video, h, results))
    processes[h] = p
    p.start()


def getresults(h):
    if results[h] is None:
        processes[h].join(timeout=0)
        if processes[h].is_alive() is None:
            raise Exception(h)
    ret = results[h]
    del results[h]
    del processes[h]
    return ret

def runv2json(video, h, results):
    pwd = os.getcwd()+'/'
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        if video.startswith('http'):
            filename = subprocess.run(['youtube-dl', '--get-filename', video], universal_newlines=True, stdout=subprocess.PIPE).stdout[:-1]
        else:
            filename=video
        jb = s3.download(h)
        if not jb:
            if video.startswith('http'):
                ytdl = subprocess.run(["youtube-dl", video], check=True)
            fps = subprocess.run([pwd+"getimages.sh", filename], check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.split('\n')[0]
            sd = ocr.img2text(td, fps)
            subprocess.run([pwd+"getaudio.sh", filename])
            ad = audio.aud2text(filename+".mp3", h)
            d = {'screen': sd, 'audio': ad}
            jv = json.dumps(d)
            s = io.BytesIO(jv.encode())
            s3.upload(s, h)
            results[h] = jv
        else:
            results[h] = jb

if __name__ == '__main__':
    h = hash.hash(sys.argv[1])
    v2json(sys.argv[1], h)
    result = None
    while(result is None):
        time.sleep(5)
        result = getresults(h)
    print(result)
