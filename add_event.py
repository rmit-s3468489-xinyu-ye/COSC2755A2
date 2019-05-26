#start import
from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
#end import

class addEvent:
    """ 
    This class is used for adding the event to the authorized Google calendar 
    by using Google canlender API.

    """
    def __init__(self):
        """
        init the scopes, creds and service. 
        Before modifying these scopes, delete the file token.json

        """
        SCOPES = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("token.json")
        creds = store.get()
        if(not creds or creds.invalid):
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build("calendar", "v3", http=creds.authorize(Http()))

    def insert(self):
        """
        Insert the borrow event following the date time format
        into Google calender.

        """
        date = datetime.now()
        date_start = date.strftime("%Y-%m-%d")
        time_start = date.strftime("%H:%M:%S")
        time_start = "{}T{}+10:00".format(date_start,time_start)
        return_day = (date + timedelta(days = 7)).strftime("%Y-%m-%d")
        return_time = (date + timedelta(days = 7)).strftime("%H:%M:%S")
        time_end = "{}T{}+10:00".format(return_day,return_time)
        event = {
            "summary": "Return the book",
            "location": "RMIT Swanston Library",
            "description": "Adding new IoT event",
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    { "method": "email", "minutes": 5 },
                    { "method": "popup", "minutes": 10 },
                ],
            }
        }

        event = self.service.events().insert(calendarId = "primary", body = event).execute()
        print("Event created: {}".format(event.get("htmlLink")))

if __name__ == "__main__":
    addEvent().insert()
