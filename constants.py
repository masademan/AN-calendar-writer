# School datetime
ALL_DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
TIME_FORMAT = ["XX:XX", "XX:XX am", "XX:XX pm"]
IANA_KEY_SCHOOL_TIMEZONE = "America/Los_Angeles"
DATE_FORMAT = "%b %d, %Y"
FULL_NAME_TO_3_LONG = {
    "Sunday": "sun",
    "Monday": "mon",
    "Tuesday": "tue",
    "Wednesday": "wed",
    "Thursday": "thu",
    "Friday": "fri",
    "Saturday": "sat",
}

# School terms
TERM_NAMES = ["fall", "winter", "spring"]

# Empty class data
EMPTY_CLASS_DATA = ("", {"days": [], "start_time": "-00:00", "end_time": "-00:00"})

# Google calendar data
CREDENTIALS_JSON_FILE = "credentials/service_credentials.json"
CLASS_CALENDAR_ID = "71b457dede6c928cd9a1cafb0c114e792ab61054a478654fdb292f88965b839e@group.calendar.google.com"     # Default: "[CLASS CALENDAR ID]@group.calendar.google.com"
VACATION_CALENDAR_ID = "6526fe7ab5a529cf00c62da1a6b7b68ccb1eeac0bd878dcfdc92659b8c12f580@group.calendar.google.com"  # Default: "[VACATION CALENDAR ID]@group.calendar.google.com"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SCHOOL_TO_CALENDAR_FORMAT = {
    "mon": "MO",
    "tue": "TU",
    "wed": "WE",
    "thu": "TH",
    "fri": "FR",
}
