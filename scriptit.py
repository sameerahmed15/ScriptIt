import eel
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
    transcript_path = db.get_path(con, uid, 'json')

    return tops.transcript_parser(transcript_path)


@eel.expose
def edit_transcript(uid):
    transcript_path = db.get_path(con, uid, 'json')

    return tops.transcript_edit(transcript_path)


@eel.expose
def change_transcript(uid, timestamp, new_word):
    transcript_path = db.get_path(con, uid, 'json')
    is_modified = tops.transcript_modify(transcript_path, float(timestamp), new_word)

    return is_modified


@eel.expose
def load_videos_dir():
    videos_dir_path = os.path.join(LOCAL_APP_DIR, 'Videos')
    videos_list = os.listdir(videos_dir_path)
    dom_elements = ''

    for video in videos_list:
        uid = video[-17:-4]
        dom_elements += f'<button id="{uid}" class="button1" onclick="showVideo({uid})">{video}</button>\n'

    return dom_elements


@eel.expose
def show_video(uid, time=-10):
    uid = int(uid)
    video_path = db.get_path(con, uid, 'mp4')
    video_dir = os.path.join(LOCAL_APP_DIR, 'Videos')

    transcript_path = db.get_path(con, uid, 'json')
    is_transcript_exists = False
    name = video_path.replace(video_dir, '')[1:]

    with open(video_path, 'rb') as video:
        video_b64 = base64.b64encode(video.read())
    video_b64 = 'data:video/mp4;base64,' + video_b64.decode('utf-8')

    video_dom = f'<video name="{name}" src="{video_b64}" id="uploadVideo" width="320" height="240" controls></video>\n'
    
    if os.path.exists(transcript_path):
        is_transcript_exists = True
        transcript_dom = generate_interactive_transcript(uid)
    else:
        transcript_dom = '<button id="transcribe-btn" class="button1" onclick="transcribeVideo()" disabled=false>Transcribe</button>'
    
    dom_elements = [video_dom, is_transcript_exists, transcript_dom, uid]
    
    return dom_elements


@eel.expose
def search_word(word):
    transcripts_dir_path = os.path.join(LOCAL_APP_DIR, 'Transcripts')
    transcripts_list = os.listdir(transcripts_dir_path)
    search_results = []
    dom_elements = ''

    for transcript in transcripts_list:
        uid = int(transcript[-18:-5])
        transcript_path = os.path.join(transcripts_dir_path, transcript)
        tops.transcript_search(word, transcript_path, uid, search_results)

    for i in range(len(transcripts_list)):
        occurrence = search_results[i]
        time = occurrence[1]
        uid = occurrence[2]
        video_name = f'{transcripts_list[i][:-4]}mp4'

        dom_elements += (f'<p id="{uid}" class="search-results">'
                         f'Found "{word}" in "{video_name}" '
                         f'at <button id="{time}" '
                         f'onclick="showVideo({uid},{time})">'
                         f'{time}s</button></p>\n')

    return dom_elements



eel.start('index.html')
