import eel
import speech_recognition as sr
import moviepy.editor as mp
import base64
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import os
import sqlite3 as sl
import dboperations as db

eel.init('web')

apikey = 'K_d21K8lTISFuDw8yr3r-kW2Bp842hdq8aKtH71Z9fP0'
url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/682e072a-737a-4529-a421-700e0063c77c'

auth = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=auth)
stt.set_service_url(url)

HOME = os.getenv('HOME')
LOCAL_APP_DIR = os.path.join(HOME, 'ScriptIt')
DB_NAME = db.create_db_dir(LOCAL_APP_DIR)
con = db.init_db(DB_NAME)



@eel.expose
def addToLocal(video_obj, video_name, uid):
    ## TODO implement video name converter to proper casing
    # Currently made to work with video_name_example-uid.mp4 type
    video_name = video_name[:-4]+'-'+str(uid)+video_name[-4:]

    video_folder_path = os.path.join(LOCAL_APP_DIR, 'Videos')
    audio_folder_path = os.path.join(LOCAL_APP_DIR, 'Audios')
    transcript_folder_path = os.path.join(LOCAL_APP_DIR, 'Transcripts')

    video_file_path = os.path.join(video_folder_path, video_name)
    audio_file_path = os.path.join(audio_folder_path, video_name[:-3]+'wav')
    transcript_file_path = os.path.join(transcript_folder_path, video_name[:-3]+'json')

    if not os.path.exists(video_folder_path):
        os.makedirs(video_folder_path)
    if not os.path.exists(audio_folder_path):
        os.makedirs(audio_folder_path)
    if not os.path.exists(transcript_folder_path):
        os.makedirs(transcript_folder_path)

    decoded_video_obj = base64.b64decode(video_obj[22:])
    with open(video_file_path, 'wb') as wfile:
        wfile.write(decoded_video_obj)

    vid = mp.VideoFileClip(video_file_path)
    vid.audio.write_audiofile(audio_file_path)

    # Create database entry
    db_info_added = db.add_info_to_db(
        con, uid, video_file_path, audio_file_path, transcript_file_path
    )
    return uid


@eel.expose
def transcribe(uid, file_name):
    print('Transcribing...')

    audio_file_path = db.get_path(con, uid, 'wav')
    transcript_file_path = db.get_path(con, uid, 'json')

    print(audio_file_path)

    results = []
    text = []

    with open(audio_file_path, 'rb') as source:
        result = stt.recognize(
            audio=source, model='en-US_BroadbandModel', timestamps=True
        ).get_result()
        
        results.append(result)

    for file in results:
        for result in file['results']:
            text.append(result['alternatives'][0]['transcript'].rstrip() + '. ')    

    with open(transcript_file_path, 'w', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=4)

    print('Transcription - Done.')
    return(''.join(text))


# @eel.expose
# def extractText(pdfObj):
#     with pb.open(pdfObj) as pdf:
#         pages = []
#         word = 'Assesment:'
#         for i in range(len(pdf.pages)):
#             page_string = pdf.pages[i].extract_text(x_tolerance=3, y_tolerance=3)
#
#             if page_string.find(word):
#                 pages.append(page_string)
#
#     with open('sched.txt', 'w') as f:
#         for page in pages:
#             f.write("%s\n" % page)
#     return('Generation success!')



eel.start('index.html')
