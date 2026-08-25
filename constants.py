# School datetime
SCHOOL_DAYS = ["mon", "tue", "wed", "thu", "fri"]
ALL_DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
TIME_FORMAT = ["XX:XX", "XX:XX am", "XX:XX pm"]
IANA_KEY_SCHOOL_TIMEZONE = "America/Los_Angeles"
DATE_FORMAT = "%b %d, %Y"

# School terms
TERM_NAMES = ["fall", "winter", "spring"]

# Empty class data
EMPTY_CLASS_DATA = ("", {"days": [], "start_time": "-00:00", "end_time": "-00:00"})

# Google calendar data
CREDENTIALS_JSON_FILE = 'credentials/service_credentials.json'
CALENDAR_ID = '[YOUR GOOGLE CALENDAR ID]@group.calendar.google.com'
SCOPES = ['https://www.googleapis.com/auth/calendar']
SCHOOL_TO_CALENDAR_FORMAT = {
    "mon": "MO",
    "tue": "TU",
    "wed": "WE",
    "thu": "TH",
    "fri": "FR",
}
