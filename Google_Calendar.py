from pprint import pprint
from Google import Create_Service
import datetime
import datefinder

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
scopes = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, scopes)


def create_event(start_time_str, summary, duration=1, description='D2L', location='Online'):
    matches = list(datefinder.find_dates(start_time_str))
    now = datetime.datetime.now()
    thisYear = now.year
    if len(matches):
        start_time = matches[0]
        end_time = datetime.datetime(
            thisYear, start_time.month, start_time.day, 23, 59, 59)

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Canada/Newfoundland',
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Canada/Newfoundland',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        return service.events().insert(calendarId='primary', body=event).execute()


create_event('april 9 11 pm', 'assessment_name')
