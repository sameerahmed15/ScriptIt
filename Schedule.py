import pdfplumber
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
import re


Assessments = {'Assignments': 'ASSIGNMENT',
               'Quizzes':  'QUIZ',
               'Tests': 'TEST',
               'Labs': 'LAB',
               'Exams': 'EXAM',
               'Mid-terms': 'MID-TERM',
               'Midterms': 'MIDTERM',
               'Finals': 'FINAL',
               'Projects': 'PROJECT'}
Months = {'January': 'JAN',
          'February': 'FEB',
          'March': 'MAR',
          'April': 'APR',
          'May': 'MAY',
          'June': 'JUN',
          'July': 'JUL',
          'August': 'AUG',
          'September': 'SEP',
          'October': 'OCT',
          'November': 'NOV',
          'December': 'DEC'}

with pdfplumber.open(r"C:\Users\HP\Documents\GitHub\Software_Design_Project\test files\5400.pdf") as pdf:
    for pdf_page in pdf.pages:
        data = pdf_page.extract_text()
        start = data.upper().find("ASSESSMENT")
        end = data.find(":", (start+100))
        Assessment = data[start:end]

        tokenize_text = word_tokenize(Assessment)

        stop_words = set(stopwords.words("english"))
        punctuations = ['.']
        filered_text = [w for w in tokenize_text if w not in punctuations]

        for a, t in enumerate(filered_text):
            if t.upper().startswith(tuple(Months.values())):
                for f, b in enumerate(reversed(filered_text[:a])):
                    if b.upper().startswith(tuple(Assessments.values())):
                        print(b, t, filered_text[a+1])
                        break
