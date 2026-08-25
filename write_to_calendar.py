import constants
from tqdm import tqdm
from utils import split_hrs_mins
from datetime import datetime, timedelta
from google.oauth2 import service_account
from read_class_data import read_term_data
from googleapiclient.discovery import build
from delete_from_calendar import clear_all_term_holidays

def create_calendar_event(event_name, start_datetime, end_datetime, day_of_week_repeat, repeat_until_datetime, verbosity=2):
    # 1. Authenticate using the service account
    creds = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_JSON_FILE, scopes=constants.SCOPES)
    
    # 2. Build the service
    service = build('calendar', 'v3', credentials=creds)

    # 3. Construct the event body
    event_body = {
        'summary': event_name,
        'start': {
            'dateTime': start_datetime,
            'timeZone': constants.IANA_KEY_SCHOOL_TIMEZONE,
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': constants.IANA_KEY_SCHOOL_TIMEZONE,
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;BYDAY={day_of_week_repeat};UNTIL={repeat_until_datetime}'
        ],
        'reminders': {
            'useDefault': True,
        },
    }

    # 4. Push the event to the calendar
    try:
        if verbosity == 2: print("Creating event...")
        created_event = service.events().insert(
            calendarId=constants.CALENDAR_ID, 
            body=event_body
        ).execute()

        if verbosity == 2: print(f"Success! Event '{event_name}' created")
        # if verbosity == 2: print(f"Success! Event '{event_name}' was created: {created_event.get('htmlLink')}")
        
    except Exception as e:
        if verbosity >= 1: print(f"An error occurred: {e}")

def add_one_class(term_data, class_name, verbosity=2):
    term_begin_datetime = datetime.strptime(term_data["start_date"], constants.DATE_FORMAT)

    class_data = term_data["classes"][class_name]
    class_days = class_data["days"]
    sorted_days = sorted(class_days, key=lambda day: constants.SCHOOL_DAYS.index(day))
    days_from_now = min((constants.ALL_DAYS.index(day) - int(term_begin_datetime.strftime("%w")))%7 for day in sorted_days)

    # start_datetime
    start_hrs, start_mins = split_hrs_mins(class_data["start_time"])
    start_datetime = term_begin_datetime + timedelta(days=days_from_now, hours=start_hrs, minutes=start_mins)
    
    # end_datetime
    end_hrs, end_mins = split_hrs_mins(class_data["end_time"])
    end_datetime = term_begin_datetime + timedelta(days=days_from_now, hours=end_hrs, minutes=end_mins)

    # day_of_week_repeat
    day_of_week_repeat = ",".join(map(lambda day: constants.SCHOOL_TO_CALENDAR_FORMAT[day], class_days))

    # repeat_until_datetime
    repeat_until_datetime = datetime.strptime(term_data["end_date"], constants.DATE_FORMAT) + timedelta(hours=23, minutes=59, seconds=59)

    create_calendar_event(
        class_name,
        start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        day_of_week_repeat,
        repeat_until_datetime.strftime("%Y%m%dT%H%M%SZ"),
        verbosity
    )

def add_all_classes(term_data, verbosity=2):
    for class_name in tqdm(term_data["classes"], disable=verbosity != 0):
        add_one_class(term_data, class_name, verbosity)

if __name__ == '__main__':
    term_data = read_term_data()
    print("Adding all the classes")
    add_all_classes(term_data, verbosity=0)

    print("\nRemoving events on holidays")
    clear_all_term_holidays(term_data, verbosity=0)
    
    print()