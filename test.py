# from datetime import datetime

# local_tz = datetime.now().astimezone().tzinfo
# print("Timezone Name:", local_tz.tzname(None))
# print("UTC Offset:", local_tz.utcoffset(None))


# from datetime import datetime

# def convert_to_24h(time_str):
#     # Parse the 12-hour string into a datetime object
#     # %I = 12-hour format, %M = minutes, %p = AM/PM indicator
#     time_obj = datetime.strptime(time_str, "%I:%M %p")
    
#     # Format the datetime object into a 24-hour string (%H = 24-hour format)
#     return time_obj.strftime("%H:%M")

# # Examples
# print(convert_to_24h("01:35 PM"))  # Output: 13:35
# print(convert_to_24h("12:15 AM"))  # Output: 00:15
# print(convert_to_24h("12:00 PM"))  # Output: 12:00


# import constants
# a = ("", {"days": [], "start_time": "00:00", "end_time": "00:00"})
# b = ("", {"days": [], "start_time": "-00:00", "end_time": "-00:00"})
# print(a==constants.EMPTY_CLASS_DATA)
# print(b==constants.EMPTY_CLASS_DATA)


# from constants import IANA_KEY_SCHOOL_TIMEZONE
# from utils import get_datetime_in_tz
# print(get_datetime_in_tz(IANA_KEY_SCHOOL_TIMEZONE))