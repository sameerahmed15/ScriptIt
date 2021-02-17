import eel
import speech_recognition as sr
import moviepy.editor as mp
import base64
import tempfile
import os

# temp_path = tempfile.gettempdir()

eel.init('web')

@eel.expose
def transcribe(fileObj):
    # print(temp_path)
    decoded_fileObj = base64.b64decode(fileObj[22:])
    # with open(os.path.join(temp_path, 'pyvideo.mp4'), 'wb') as wfile:
    with open('pyvideo.mp4', 'wb') as wfile:
        wfile.write(decoded_fileObj)

    vid = mp.VideoFileClip('pyvideo.mp4')
    vid.audio.write_audiofile('result.wav')

    rcgnzr = sr.Recognizer()

    with sr.AudioFile('result.wav') as source:
        source_audio = rcgnzr.record(source)
        f = open("transcript.txt", "w")
        f.write(rcgnzr.recognize_google(source_audio))
        f.close()

    return('Transcription success!')

eel.start('index.html')
