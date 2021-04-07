import eel
import speech_recognition as sr
import moviepy.editor as mp
import base64
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import json
import sqlite3 as sl
import dboperations as db
import transcriptops as tops

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
def add_to_local(video_obj, video_name, uid):
    ## TODO implement video name converter to proper casing
    # Currently made to work with video_name_example-uid.mp4 type
    video_name = video_name[:-4]+'-'+str(uid)+video_name[-4:]

    video_folder_path = os.path.join(LOCAL_APP_DIR, 'Videos')
    audio_folder_path = os.path.join(LOCAL_APP_DIR, 'Audios')
    transcript_folder_path = os.path.join(LOCAL_APP_DIR, 'Transcripts')

    video_file_path = os.path.join(video_folder_path, video_name)
    audio_file_path = os.path.join(audio_folder_path, video_name[:-3]+'wav')
    transcript_file_path = os.path.join(transcript_folder_path, video_name[:-3]+'json')
    inttrndom_file_path = os.path.join(transcript_folder_path, 'inttrndom_'+video_name[:-3]+'txt')
    edittrndom_file_path = os.path.join(transcript_folder_path, 'edittrndom_'+video_name[:-3]+'txt')

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
        con, uid, video_file_path, audio_file_path, transcript_file_path,
        inttrndom_file_path, edittrndom_file_path
    )
    return uid


@eel.expose
def transcribe(uid, file_name):
    print('Transcribing...')

    audio_file_path = db.get_path(con, uid, 'wav')
    transcript_file_path = db.get_path(con, uid, 'json')
    dom_file_path = db.get_path(con, uid, 'inttrn')

    results = []
    text = []

    with open(audio_file_path, 'rb') as source:
        result = stt.recognize(
            audio=source, model='en-US_BroadbandModel', timestamps=True,
            word_alternatives_threshold=0.0
        ).get_result() 
        results.append(result)

    for file in results:
        for result in file['results']:
            text.append(result['alternatives'][0]['transcript'].rstrip() + '. ')    

    with open(transcript_file_path, 'w', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=4)

    transcript_dom_field = generate_interactive_transcript(uid)

    print('Transcription - Done.')
    return transcript_dom_field


@eel.expose
def generate_interactive_transcript(uid):
    transcript_file_path = db.get_path(con, uid, 'json')
    dom_file_path = db.get_path(con, uid, 'inttrn')
    return tops.transcript_parser(transcript_file_path, dom_file_path)


@eel.expose
def edit_transcript(uid):
    transcript_path = db.get_path(con, uid, 'json')
    dom_path = db.get_path(con, uid, 'edittrn')

    edit_dom_field = tops.transcript_edit(transcript_path, dom_path)
    return edit_dom_field


@eel.expose
def change_transcript(uid, timestamp, new_word):
    transcript_path = db.get_path(con, uid, 'json')
    is_modified = tops.transcript_modify(transcript_path, float(timestamp), new_word)
    
    return is_modified


eel.start('index.html')
