import eel
import speech_recognition as sr
import moviepy.editor as mp
import base64
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

eel.init('web')

apikey = 'K_d21K8lTISFuDw8yr3r-kW2Bp842hdq8aKtH71Z9fP0'
url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/682e072a-737a-4529-a421-700e0063c77c'

auth = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=auth)
stt.set_service_url(url)

@eel.expose
def transcribe(fileObj):
    decoded_fileObj = base64.b64decode(fileObj[22:])
    with open('pyvideo.mp4', 'wb') as wfile:
        wfile.write(decoded_fileObj)

    vid = mp.VideoFileClip('pyvideo.mp4')
    vid.audio.write_audiofile('result.wav')

    print('Transcribing...')

    results = []
    text = []
    with open('result.wav', 'rb') as source:
        result = stt.recognize(audio=source, model='en-US_BroadbandModel', timestamps=True).get_result()
        results.append(result)

    for file in results:
        for result in file['results']:
            text.append(result['alternatives'][0]['transcript'].rstrip() + '. ')    

    with open('transcript.json', 'w', encoding='utf-8') as out:
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
