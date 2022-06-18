from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ms_graph import generate_access_token, GRAPH_API_ENDPOINT

import requests
import json
import os

class Google: # Κλάση Google
    def __init__(self, event_details): # Αρχικοποίηση
        self.scope = ['https://www.googleapis.com/auth/calendar'] # Ορίζουμε το scope με δυνατότητα Ανάγνωσης και Γραφής στο ημερολόγιο
        self.creds = None
        self.event_details = event_details
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.scope)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request)
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', self.scope)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        page_token = None
        
        self.service = build('calendar', 'v3', credentials=self.creds)
        self.calId = ''
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if(calendar_list_entry['summary'] == 'Αγώνες Ιστιοπλοΐας - SailCAL'):
                    self.calId = calendar_list_entry['id']
                    break
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        if self.calId == '':
            calendar = {
                'summary': 'Αγώνες Ιστιοπλοΐας - SailCAL',
                'timeZone': 'Europe/Athens'
            }
            created_calendar = self.service.calendars().insert(body=calendar).execute()
            for calendar_list_entry in calendar_list['items']:
                if(calendar_list_entry['summary'] == 'Αγώνες Ιστιοπλοΐας - SailCAL'):
                    self.calId = calendar_list_entry['id']    

    def event(self):
        event = {
            'summary': self.event_details['summary'],
            'location': self.event_details['location'],
            'description': self.event_details['description'],
            'start': {
                'dateTime': self.event_details['dtstart'],
                'timeZone': 'Europe/Athens',
            },
            'end': {
                'dateTime': self.event_details['dtend'],
                'timeZone': 'Europe/Athens',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        service = build('calendar', 'v3', credentials=self.creds)
        event = service.events().insert(calendarId=self.calId, body=event).execute()#Εκτύπωση του ημερολογίου στο webmail 

class Microsoft: # Κλάση Microsoft
    def __init__(self, event_details):
        self.event_details = event_details # Η μεταβλητή με τα στοιχεία του ημερολογίου
        self.scope = ['Calendars.ReadWrite'] # Ορίζουμε το scope με δυνατότητα Ανάγνωσης και Γραφής στο ημερολόγιο
        self.app_id = '6212604b-52a3-40a7-a3dc-b9bc919b0424'
        self.access_token = generate_access_token(self.app_id, self.scope)
        self.headers = {'Authorization':    'Bearer ' + self.access_token['access_token']}
    
    def event(self):
        self.event_body = {
            "subject": self.event_details['summary'],
            "body": {
                "contentType": "HTML",
                "content": self.event_details['description']
            },
            "start": {
                "dateTime": self.event_details['dtstart'],
                "timeZone": "Europe/Istanbul"
            },
            "end": {
                "dateTime": self.event_details['dtend'],
                "timeZone": "Europe/Istanbul"
            },
            "location":{
                "displayName": self.event_details['location']
            },
        }
        requests.post(GRAPH_API_ENDPOINT + f'/me/events', headers=self.headers, json = self.event_body) #Εκτύπωση του ημερολογίου στο webmail 
