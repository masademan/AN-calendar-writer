import re
import constants
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

def find_holiday_dates(search_start, search_end, verbosity=1):
    creds = service_account.Credentials.from_service_account_file(
        constants.CREDENTIALS_JSON_FILE, scopes=constants.SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    local_tz = ZoneInfo(constants.IANA_KEY_SCHOOL_TIMEZONE)
    
    # 1. Format the start and end dates for the API
    start_dt = datetime.strptime(search_start, constants.DATE_FORMAT).replace(tzinfo=local_tz)
    end_dt = datetime.strptime(search_end, constants.DATE_FORMAT).replace(
        hour=23, minute=59, second=59, tzinfo=local_tz)

    try:
        if verbosity == 2: print(f"Fetching events between {search_start} and {search_end}...")
        
        # 2. Grab ALL events in that timeframe
        events_result = service.events().list(
            calendarId=constants.VACATION_CALENDAR_ID,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True, 
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            if verbosity == 2: print("No events found in this date range.")
            return []

        # List to store our extracted dates
        holiday_dates = []

        # 3. Define our Regular Expression (Regex) patterns
        # Pattern 1: Starts with "No School", optionally followed by a space and parentheses
        pattern_no_school = re.compile(r"^No School(?:\s+\(.*?\))?$")
        
        # Pattern 2: Exactly "Thanksgiving Break", "Winter Break", or "Spring Break"
        # pattern_break = re.compile(r"^(Thanksgiving|Winter|Spring) Break$")
        pattern_break = re.compile(r"\w+ Break$")

        # 4. Filter the events and extract the dates
        for event in events:
            title = event.get('summary', '')
            
            # Check if the title matches either of our patterns
            if pattern_no_school.match(title) or pattern_break.match(title):
                
                # Google formats all-day events differently than timed events. 
                # This grabs the date regardless of the format.
                start_info = event['start'].get('date') or event['start'].get('dateTime')
                end_info = event['end'].get('date') or event['end'].get('dateTime')
                
                # Slice the string to keep only the 'YYYY-MM-DD' portion
                start_str = start_info[:10]
                end_str = end_info[:10]

                start_dt = datetime.strptime(start_str, "%Y-%m-%d")
                end_dt = datetime.strptime(end_str, "%Y-%m-%d")

                if start_dt == end_dt:
                    holiday_dates.append({
                        "title": title,
                        "date": start_str
                    })
                else:
                    current_dt = start_dt
                    while current_dt < end_dt:
                        holiday_dates.append({
                            "title": title,
                            "date": current_dt.strftime("%Y-%m-%d")
                        })
                        current_dt += timedelta(days=1)

        # 5. Print the results
        if verbosity == 2:
            print(f"\nFound {len(holiday_dates)} matching holidays:")
            for holiday in holiday_dates:
                print(f"- {holiday['date']}: {holiday['title']}")

        # Now you can use the `holiday_dates` list elsewhere in your code!
        return holiday_dates
            
    except Exception as e:
        if verbosity > 0: print(f"An error occurred: {e}")

if __name__ == '__main__':
    import json
    print(json.dumps(find_holiday_dates("Aug 26, 2026", "Dec 11, 2026"), indent=4))
