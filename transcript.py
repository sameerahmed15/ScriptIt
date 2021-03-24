import speech_recognition as sr
import moviepy.editor as mp
"""
clip = mp.VideoFileClip(r"video.mp4") 
clip.audio.write_audiofile(r"converted.wav") """

import speech_recognition as sr

def main():
    sound = "converted.wav"

    r = sr.Recognizer()
    file = sr.AudioFile(sound)

    with file as source:
        audio = r.listen(source)

        print("Converting Audio To Text ..... ")


    try:
        print("Converted Audio Is : \n" + r.recognize_google(audio))


    except Exception as e:
        print("Error {} : ".format(e) )



if __name__ == "__main__":
    main()

 
""" with open('recognized.txt',mode ='w') as file: 
   file.write("Recognized Speech:") 
   file.write("\n") 
   file.write(result) 
   print("ready!") """