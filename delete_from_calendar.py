import constants
from tqdm import tqdm
from datetime import datetime
from zoneinfo import ZoneInfo
from google.oauth2 import service_account
from read_class_data import read_term_data
from googleapiclient.discovery import build

def delete_calendar_event(event_name_to_delete, verbosity=2):
    # 1. Authenticate using the service account
    creds = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_JSON_FILE, scopes=constants.SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    try:
        if verbosity == 2: print(f"Searching for events matching: '{event_name_to_delete}'...")
        
        # 2. Search the calendar
        # The 'q' parameter searches titles, descriptions, and attendees
        events_result = service.events().list(
            calendarId=constants.CALENDAR_ID,
            q=event_name_to_delete,
        ).execute()
        
        events = events_result.get('items', [])

        if not events:
            if verbosity == 2: print("No matching events found.")
            return

        # 3. Loop through the search results to find an exact match
        for event in events:
            # 'q' does a broad keyword search, so we verify the exact title here
            if event.get('summary') == event_name_to_delete:
                event_id = event['id']
                if verbosity == 2: print(f"Found exact match: {event.get('summary')} (ID: {event_id})")
                
                # 4. Delete the event using its ID
                service.events().delete(
                    calendarId=constants.CALENDAR_ID, 
                    eventId=event_id
                ).execute()
                
                if verbosity == 2: print("Success! Event and all its repeating instances have been deleted.")
                
                # Stop after deleting the first exact match to avoid deleting duplicates
                return 
                
        if verbosity == 2: print("Found some search results, but none matched that exact title.")

    except Exception as e:
        if verbosity >= 1: print(f"An error occurred: {e}")

def delete_all_term_classes(term_data, verbosity=2):
    for class_name in tqdm(term_data["classes"], disable=verbosity != 0):
        delete_calendar_event(class_name, verbosity)

def clear_day_of_events(target_date, verbosity=2):
    creds = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_JSON_FILE, scopes=constants.SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    # 1. Define the exact start and end of the target day (RFC 3339 format)
    # E.g., 2026-12-25T00:00:00-08:00

    dt = datetime.strptime(target_date, constants.DATE_FORMAT)
    local_tz = ZoneInfo(constants.IANA_KEY_SCHOOL_TIMEZONE)

    time_min = dt.replace(hour=0, minute=0, second=0, tzinfo=local_tz).isoformat()
    time_max = dt.replace(hour=23, minute=59, second=59, tzinfo=local_tz).isoformat()

    try:
        if verbosity == 2: print(f"Searching for all events on {target_date}...")
        
        # 2. Get all events on that specific day
        events_result = service.events().list(
            calendarId=constants.CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,      # MAGIC TRICK: Breaks recurring events into individual instances
            orderBy='startTime'     # Required when using singleEvents=True
        ).execute()
        
        events = events_result.get('items', [])

        if not events:
            if verbosity == 2: print("No events found on this day.")
            return

        if verbosity == 2: print(f"Found {len(events)} event(s). Deleting them...")

        # 3. Loop through and delete each specific instance
        for event in events:
            event_name = event.get('summary', 'Unnamed Event')
            event_id = event['id']  # This is now an Instance ID, not the Master ID
            
            if verbosity == 2: print(f" - Deleting: {event_name}")
            
            # Deleting an Instance ID only removes that one specific day
            service.events().delete(
                calendarId=constants.CALENDAR_ID, 
                eventId=event_id
            ).execute()
            
        if verbosity == 2: print("Success! All events on this day have been removed.")

    except Exception as e:
        if verbosity >= 1: print(f"An error occurred: {e}")

def clear_all_term_holidays(term_data, verbosity=2):
    for holiday_date in tqdm(term_data["holidays"], disable=verbosity != 0):
        clear_day_of_events(holiday_date, verbosity)

if __name__ == '__main__':
    term_data = read_term_data()
    delete_all_term_classes(term_data, verbosity=0)