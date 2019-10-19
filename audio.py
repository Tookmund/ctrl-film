import time
import requests
from collections import OrderedDict
import boto3

import s3

def aud2text(filename, h):
    transcribe = boto3.client('transcribe')
    s3.uploadfile(filename, f"pending-{h}.wav")
    job_name = h
    job_uri = f"https://s3.us-east-1.amazonaws.com/search-in-video/pending-{h}.wav"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)
    r = requests.get(status.Transcript.TranscriptFileUri)
    return r.text()
