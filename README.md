# ScripIt

ScriptIt is a Python application for transcribing video files. It is intended to be used for transcribing video lectures of courses, but it can be used for any other video as well. The production version will have functionality to search text within videos, and to extract dates from PDF documents to generate schedules. 

![ScriptIt's dashboard interface.](img/dashboard.png)

## Build

***Ensure that python 3.x.x is set as your default python.*** 

Run the following commands in a terminal at the project directory:
1. `pip install pyinstaller`
2. `python -m eel scriptit.py web --noconsole --onefile`

The application executable will be found in the *dist* directory.


## Running the Application

In case the application is not built, enter the following command in a terminal at the project directory:

`python main.py`


## Prerequisites

1. [Python 3.x.x](https://www.python.org/downloads/)
    - Minimum version required: Python 3.0.0
2. [Eel](https://pypi.org/project/Eel/)
    - Minimum version required: 0.12.1
3. [MoviePy](https://pypi.org/project/moviepy/)
    - Minimum version required: 1.0.0
4. [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
    - Minimum version required: 3.6.0
