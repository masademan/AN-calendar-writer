import os
import sys
import constants
import subprocess
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


def clear_console():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)


def convert_to_24h(time_str):
    time_obj = datetime.strptime(time_str, "%I:%M %p")
    return time_obj.strftime("%H:%M")


def split_hrs_mins(time: str):
    hrs, mins = time.split(":")
    return int(hrs), int(mins)


def convert_time(time, days, is_24_hr=False, IANA_timezone=None):
    now = datetime.now()
    if not IANA_timezone:
        local_tz = now.astimezone().tzinfo
    else:
        local_tz = ZoneInfo(IANA_timezone)

    sorted_days = sorted(days, key=lambda day: constants.SCHOOL_DAYS.index(day))
    days_from_now = (constants.ALL_DAYS.index(sorted_days[0]) - int(now.strftime("%w"))) % 7

    if not is_24_hr:
        time = convert_to_24h(time)
    hrs, mins = split_hrs_mins(time)
    time_to_convert = datetime(now.year, now.month, now.day, hrs, mins) + timedelta(days=days_from_now)
    time_to_convert = time_to_convert.replace(tzinfo=local_tz)

    target_tz = ZoneInfo(constants.IANA_KEY_SCHOOL_TIMEZONE)
    target_datetime = time_to_convert.astimezone(target_tz)

    return target_datetime.strftime("%H:%M")


def get_class_data_file_name(school_year=None):
    term_name = input("School term (Fall, Winter, Spring): ").lower().lstrip().rstrip()
    if school_year == None:
        school_year_str = input("School starting year: ").lstrip().rstrip()
    else:
        school_year_str = str(school_year)

    errors = []
    # Checking term name
    if term_name not in constants.TERM_NAMES:
        errors.append(f"School term '{term_name}' is not valid")

    # Checking school year
    if not school_year_str.isnumeric():
        errors.append(f"School year '{school_year_str}' is invalid. Must be made up of only numbers")

    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"-- {error}", file=sys.stderr)

    return f"class jsons/{term_name}_{school_year_str}_{int(school_year_str) + 1}.json"


def make_choice(choices: list[str], question: str, use_quotes: bool = True) -> str:
    while True:
        clear_console()
        for i, choice in enumerate(choices):
            if use_quotes:
                print(f"{i + 1}: '{choice}'")
            else:
                print(f"{i + 1}: {choice}")
        print()
        answer = input(question)
        if answer in choices:
            return answer
        if not answer.isnumeric():
            print("Invalid answer, must be a number or must match one of the given options")
            input("Press enter to try again")
            continue
        answer = int(answer)
        if answer > len(choices):
            print("That number was too big")
            input("Press enter to try again")
            continue
        if answer < 1:
            print("That number was too small")
            input("Press enter to try again")
            continue
        break
    return choices[answer - 1]
