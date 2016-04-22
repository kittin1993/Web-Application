from __future__ import print_function
import httplib2
import os

from apiclient import discovery

import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

# from webapps.settings import BASE_DIR

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    print("123")
    print(parser)
    parser.add_argument("process")
    #parser.add_argument("port")
    flags = parser.parse_args()
    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    # flags = None
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart. son
# this json file is in directory /.credentials in the base directory
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # home_dir = os.path.expanduser('~')
    json_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # json_dir = BASE_DIR
    credential_dir = os.path.join(json_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def add_google_calendar(place, address, time, content):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # 'Z' indicates UTC time
    # now = datetime.datetime.utcnow().isoformat() + 'Z'
    event = {
        'summary': 'Travel Go: ' + place,
        'location': address,
        'description': content,
        'start': {
            'date': time,
            # 'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'date': time,
            # 'dateTime': '2016-04-22T17:00:00-07:00',
            # 'timeZone': 'America/Los_Angeles',
        },
        # 'recurrence': [
        #     'RRULE:FREQ=DAILY;COUNT=2'
        # ],
        # 'attendees': [
        #     {'email': 'jerrytaotz@gmail.com'},
        # ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    calendar = service.calendars().get(calendarId='primary').execute()
    print(calendar['summary'])
