import os
import sys
import json
import constants
from datetime import datetime
from read_class_data import read_json
from read_from_calendar import find_holiday_dates
from utils import (
    make_choice,
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
    is_24_hr = {"start_time": False, "end_time": False}
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
        if not stop_program:
            print()
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


def get_official_json_file_path():
    files = [f for f in os.listdir("./official class jsons/")]
    return make_choice(files, "Which file do you want? ")


def convert_one_class_data(official_class_data, time_zone):
    # Class name
    class_name = official_class_data["title"]

    # Start time
    start_time = official_class_data["startTime"]

    # End time
    end_time = official_class_data["endTime"]

    # Days
    days = list(map(lambda day: constants.FULL_NAME_TO_3_LONG[day], official_class_data["days"]))

    data_dict = {
        "days": days,
        "start_time": convert_time(start_time, days, True, time_zone),
        "end_time": convert_time(end_time, days, True, time_zone),
    }

    return class_name, data_dict


def get_beginning_school_year(start_date):
    start_date_obj = datetime.strptime(start_date, constants.DATE_FORMAT)
    july_of_the_year = datetime(year=start_date_obj.year, month=7, day=15)

    if start_date_obj > july_of_the_year:
        return start_date_obj.year
    return start_date_obj.year - 1


def convert_term_data(include_optional_classes=True, include_official_json: bool = False):
    offical_term_data_path = "official class jsons/" + get_official_json_file_path()
    offical_term_data = read_json(offical_term_data_path)

    # Get start date
    start_date = datetime.strptime(offical_term_data["term"]["startDate"], "%Y-%m-%d").strftime(constants.DATE_FORMAT)

    # Get end date
    end_date = datetime.strptime(offical_term_data["term"]["endDate"], "%Y-%m-%d").strftime(constants.DATE_FORMAT)

    # Get class data
    class_data = {}
    time_zone = offical_term_data["timeZone"]

    for single_class in offical_term_data["classes"]:
        if single_class["optional"] and not include_optional_classes:
            continue

        class_name, official_class_data = convert_one_class_data(single_class, time_zone)
        class_data[class_name] = official_class_data

    # Get file path
    beginning_school_year = get_beginning_school_year(start_date)
    file_path = f"class jsons/{offical_term_data["term"]["name"].split(" ")[0].lower()}_{beginning_school_year}_{beginning_school_year + 1}.json"

    if include_official_json:
        return class_data, start_date, end_date, file_path, offical_term_data_path
    return class_data, start_date, end_date, file_path


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


def has_holidays_calendar_id():
    return hasattr(constants, "VACATION_CALENDAR_ID") and constants.VACATION_CALENDAR_ID != "[VACATION CALENDAR ID]@group.calendar.google.com"


def get_holidays_and_format(start_date: datetime, end_date: datetime):
    holiday_data = find_holiday_dates(start_date, end_date)

    holiday_dates: list[datetime] = []
    for item in holiday_data:
        holiday_dates.append(datetime.strptime(item["date"], "%Y-%m-%d"))

    holiday_dates.sort()

    holiday_dates_str = []
    for holiday_date in holiday_dates:
        holiday_dates_str.append(holiday_date.strftime(constants.DATE_FORMAT))

    return holiday_dates_str


def get_term_data(
    has_file=False, classes_to_ignore=[], include_optional_classes=True, separated_data: tuple[dict[str, dict | str], str, str, str] | None = None
):
    all_data = {}

    if not separated_data:
        file_path = ""
        if not has_file:
            class_data = get_all_class_data()
            start_date, end_date = get_start_end_dates()
        else:
            class_data, start_date, end_date, file_path = convert_term_data(include_optional_classes)
    else:
        class_data, start_date, end_date, file_path = separated_data

    if has_holidays_calendar_id():
        holidays = get_holidays_and_format(start_date, end_date)
    else:
        holidays = get_holidays()

    for class_name in classes_to_ignore:
        class_data.pop(class_name, None)

    all_data["classes"] = class_data
    all_data["holidays"] = holidays
    all_data["start_date"] = start_date
    all_data["end_date"] = end_date

    return all_data, file_path


def write_data(data, file_name: str, readable=False):
    if not file_name.endswith(".json"):
        file_name += ".json"

    with open(file_name, "w") as f:
        if readable:
            json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            json.dump(data, f)


def choose_classes_to_ignore(json_file_path: str, include_optional_classes: bool) -> list[str]:
    class_data = read_json(json_file_path)

    all_classes = []
    for single_class in class_data["classes"]:
        if single_class["optional"] and not include_optional_classes:
            continue

        class_name, _ = convert_one_class_data(single_class, class_data["timeZone"])
        all_classes.append(class_name)

    classes_to_ignore = []

    STOPPING_KEY_WORD = "No more events to ignore"

    while True:
        class_choice = make_choice(all_classes + [STOPPING_KEY_WORD], "Which event do you want to not include in the calendar? ", use_quotes=False)

        if class_choice == STOPPING_KEY_WORD:
            break

        classes_to_ignore.append(class_choice)
        all_classes.pop(all_classes.index(class_choice))

    return classes_to_ignore


def write_term_data(
    has_file=False,
    readable=False,
    classes_to_ignore=[],
    include_optional_classes=True,
    separated_data: tuple[dict[str, dict | str], str, str, str] | None = None,
):
    term_data, file_path = get_term_data(has_file, classes_to_ignore, include_optional_classes, separated_data)
    if not file_path:
        file_path = get_class_data_file_name(term_data["start_date"].split(", ")[-1])

    if os.path.exists(file_path):
        old_term_data = read_json(file_path)
        for key in term_data:
            if not term_data[key] and old_term_data[key]:
                term_data[key] = old_term_data[key]

    write_data(term_data, file_path, readable=readable)

    print(f"Data file saved at '{file_path}'")


def get_yn_answer_to_question(question: str) -> bool:
    while True:
        clear_console()
        answer = input(question)
        if answer not in "yn":
            print(f"Your answer '{answer}' is invalid, try again")
            input("Press continue to try again")
            continue
        break

    return answer == "y"


def main():
    json_answer = get_yn_answer_to_question("Do you have a .json from the AN schedule? (y/n) ")

    separated_data = None
    classes_to_ignore = []
    include_optional_classes = True
    if json_answer:
        separated_data = convert_term_data(include_official_json=True)

        include_optional_classes = get_yn_answer_to_question("Do you want to have the optional events in your calendar? (y/n) ")

        if include_optional_classes:
            ignore_answer = get_yn_answer_to_question("Are there specific events you don't want to include in your calendar? (y/n) ")
        else:
            ignore_answer = get_yn_answer_to_question("Are there other events you don't want to include in your calendar? (y/n) ")
        if ignore_answer:
            classes_to_ignore = choose_classes_to_ignore(json_file_path=separated_data[4], include_optional_classes=include_optional_classes)

    # write_term_data(
    #     has_file=json_answer,
    #     readable=True,
    #     classes_to_ignore=classes_to_ignore,
    #     include_optional_classes=include_optional_classes,
    #     separated_data=separated_data[:4],
    # )

    # write_term_data(has_file=answer=="y", readable=True, classes_to_ignore=["Astra Nova Book Club"])


if __name__ == "__main__":
    main()

    # write_term_data(has_file=answer=="y", readable=True, include_optional_classes=False)
    # write_term_data(has_file=answer=="y", readable=True, classes_to_ignore=["Astra Nova Book Club"])
    # write_term_data(has_file=answer=="y", readable=True)
