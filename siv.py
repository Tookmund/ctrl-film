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
status = manager.dict()

def v2json(video, h):
    if not h in processes and not h in results:
        results[h] = None
        status[h] = ''
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

def getstatus(h):
    return status[h]

def runv2json(video, h, results):
    pwd = os.getcwd()+'/'
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        if video.startswith('http'):
            filename = subprocess.run(['youtube-dl', '--get-filename', video], universal_newlines=True, stdout=subprocess.PIPE).stdout[:-1]
        else:
            filename=video
        status[h] = "Downloading from S3"
        jb = s3.download(h)
        if not jb:
            if video.startswith('http'):
                status[h] = "Downloading file"
                ytdl = subprocess.run(["youtube-dl", video], check=True)
            status[h] = "Getting images..."
            fps = subprocess.run([pwd+"getimages.sh", filename], check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout.split('\n')[0]
            status[h] = "OCRing images"
            sd = ocr.img2text(td, fps)
            status[h] = "Extracting audio"
            subprocess.run([pwd+"getaudio.sh", filename])
            status[h] = "Transcribing audio"
            ad = audio.aud2text(filename+".wav", h)
            status[h] = "Converting to JSON"
            d = {'screen': sd, 'audio': ad}
            jv = json.dumps(d)
            s = io.BytesIO(jv.encode())
            status[h] = "Uploading to S3"
            s3.upload(s, h)
            results[h] = jv
        else:
            results[h] = jb
        print("FINISHED "+h)

if __name__ == '__main__':
    h = hash.hash(sys.argv[1])
    v2json(sys.argv[1], h)
    result = None
    while(result is None):
        time.sleep(5)
        result = getresults(h)
    print(result)
