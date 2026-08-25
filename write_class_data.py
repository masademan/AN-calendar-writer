import os
import sys
import json
import constants
from datetime import datetime
from read_class_data import read_json
from utils import (
    convert_time,
    clear_console,
    get_class_data_file_name,
)

def get_one_class_data():
    print("Enter '\\q' at any time to quit")
    class_name = input("Class name: ").lstrip().rstrip()
    if "\\q" in class_name:
        print("Found quit command in 'class name'")
        return "\\q", constants.EMPTY_CLASS_DATA[1], True
    
    start_time = input("Start time (local time): ").lower().lstrip().rstrip()
    if "\\q" in start_time:
        print("Found quit command in 'start time'")
        return "\\q", constants.EMPTY_CLASS_DATA[1], True
    
    end_time = input("End time (local time): ").lower().lstrip().rstrip()
    if "\\q" in end_time:
        print("Found quit command in 'end time'")
        return "\\q", constants.EMPTY_CLASS_DATA[1], True
    
    days = input("Days (3 letter form, separated by ','): ").lower()
    if "\\q" in days:
        print("Found quit command in 'days'")
        return "\\q", constants.EMPTY_CLASS_DATA[1], True
    days = days.split(",")

    for i in range(len(days)):
        days[i] = days[i].lstrip().rstrip()

    # Checking days
    day_errors = []
    for day in days:
        if day not in constants.SCHOOL_DAYS:
            day_errors.append(f"Day '{day}' is not valid")

    # Checking times
    time_errors = []
    is_24_hr = {
        "start_time": False,
        "end_time": False
    }
    for time_type, time in zip(["start_time", "end_time"], [start_time, end_time]):
        split_time = time.split(" ")
        hrs = split_time[0].split(":")[0]
        mins = split_time[0].split(":")[1]
        if len(split_time) == 1:
            # 24 hr clock
            if not (hrs.isnumeric() and 0 <= int(hrs) < 24):
                time_errors.append(f"{time_type} hour '{hrs}' is invalid")

            is_24_hr[time_type] = True
        else:
            # 12 hr clock
            if not (hrs.isnumeric() and 0 < int(hrs) <= 12):
                time_errors.append(f"{time_type} hour '{hrs}' is invalid")
            if split_time[1] not in {"am", "pm"}:
                time_errors.append(f"{time_type} '{split_time[1]}' is not valid (am / pm)")

        if not (mins.isnumeric() and 0 <= int(mins) < 60):
            time_errors.append(f"{time_type} minute '{mins}' is invalid")

    # Print errors
    stop_program = False
    if day_errors:
        print()
        print(f"Days must be in {constants.SCHOOL_DAYS}", file=sys.stderr)
        for error in day_errors:
            print(f"-- {error}", file=sys.stderr)
        stop_program = True
    if time_errors:
        if not stop_program: print()
        print("Time formatting errors:", file=sys.stderr)
        for error in time_errors:
            print(f"-- {error}", file=sys.stderr)
        stop_program = True

    if stop_program:
        return *constants.EMPTY_CLASS_DATA, True

    data_dict = {
        "days": days,
        "start_time": convert_time(start_time, days, is_24_hr["start_time"]),
        "end_time": convert_time(end_time, days, is_24_hr["end_time"]),
    }

    return class_name, data_dict, day_errors != [] or time_errors != []

def get_all_class_data():
    data = {}

    while True:
        clear_console()
        class_name, class_data, had_error = get_one_class_data()

        if "\\q" in class_name:
            print("The quit command has been found")
            input("Press enter to continue and exit")
            break

        if had_error:
            print("There were errors in your class data so it won't be added")
            input("Press continue to add another class or try adding this class again")
            continue

        continue_answer = ""
        if class_name in data:
            continue_answer = input(f"WARNING! Class name '{class_name}' already was inputted, override? (y/n): ").lower().lstrip().rstrip()

        if (class_name, class_data) != constants.EMPTY_CLASS_DATA and continue_answer != "n":
            data[class_name] = class_data

    clear_console()
    return data

def get_start_end_dates():
    start_date_str = input("When does the term start? (example 'Aug 26, 2026'): ")
    end_date_str = input("When does the term end? (example 'Dec 11, 2026'): ")

    start_date = datetime(2026, 8, 26)
    end_date = datetime(2026, 12, 11)

    errors = []
    # Check start date
    try:
        start_date = datetime.strptime(start_date_str, constants.DATE_FORMAT)
    except ValueError:
        errors.append(f"Start date '{start_date_str}' was not formatted correctly")
    except:
        errors.append(f"Another error occurred when trying to process start date '{start_date_str}'")
        
    # Check end date
    try:
        end_date = datetime.strptime(end_date_str, constants.DATE_FORMAT)
    except ValueError:
        errors.append(f"End date '{end_date_str}' was not formatted correctly")
    except:
        errors.append(f"Another error occurred when trying to process end date '{end_date_str}'")

    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"-- {error}", file=sys.stderr)
        sys.exit(-1)

    return start_date.strftime(constants.DATE_FORMAT), end_date.strftime(constants.DATE_FORMAT)

def get_one_holiday():
    holiday_date_str = input("When is one of the holidays? (example 'Dec 25, 2026'): ")

    if "\\q" in holiday_date_str:
        print("Found quit command")
        return "\\q", True

    holiday_date = datetime(2026, 12, 25)

    errors = []
    # Check start date
    try:
        holiday_date = datetime.strptime(holiday_date_str, constants.DATE_FORMAT)
    except ValueError:
        errors.append(f"Holiday date '{holiday_date_str}' was not formatted correctly")
    except:
        errors.append(f"Another error occurred when trying to process start date '{holiday_date_str}'")

    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"-- {error}", file=sys.stderr)

    return holiday_date.strftime(constants.DATE_FORMAT), errors != []

def get_holidays():
    data = set()

    clear_console()
    print("Enter '\\q' at any time to quit")
    while True:
        holiday_date, had_error = get_one_holiday()

        if "\\q" in holiday_date:
            print("The quit command has been found")
            input("Press enter to continue and exit")
            break

        if had_error:
            print("There were errors in your class data so it won't be added")
            input("Press continue to add another class or try adding this class again")
            continue

        data.add(holiday_date)
        print()

    clear_console()
    return sorted(list(data), key=lambda date: datetime.strptime(date, constants.DATE_FORMAT))

def get_term_data():
    all_data = {}
    class_data = get_all_class_data()
    start_date, end_date = get_start_end_dates()
    holidays = get_holidays()

    all_data["classes"] = class_data
    all_data["holidays"] = holidays
    all_data["start_date"] = start_date
    all_data["end_date"] = end_date

    return all_data

def write_data(data, file_name: str, readable=False):
    if not file_name.endswith(".json"): file_name += ".json"

    with open(file_name, "w") as f:
        if readable:
            json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            json.dump(data, f)

def write_term_data(readable=False):
    term_data = get_term_data()
    file_path = get_class_data_file_name(term_data["start_date"].split(", ")[-1])

    if os.path.exists(file_path):
        old_term_data = read_json(file_path)
        for key in term_data:
            if not term_data[key] and old_term_data[key]:
                term_data[key] = old_term_data[key]

    write_data(term_data, file_path, readable=readable)

if __name__ == "__main__":
    write_term_data(readable=True)