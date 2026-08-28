from utils import make_choice, clear_console
from write_class_data import main as writing_json_data
from rename_class_data import main as rename_class_name
from write_to_calendar import main as writing_to_calendar
from delete_from_calendar import main as delete_from_calendar

def main():
    actions = ["Write to json", "Change class names", "Write to calendar", "Delete from calendar", "Quit"]
    while True:
        clear_console()

        action = make_choice(actions, "What action to do? ", use_quotes=False)
        result = None

        if action == actions[0]:
            result = writing_json_data()
        elif action == actions[1]:
            result = rename_class_name()
        elif action == actions[2]:
            result = writing_to_calendar()
        elif action == actions[3]:
            result = delete_from_calendar()
        elif action == actions[4]:
            result = clear_console()
            return

        if not result:
            input("Press enter to continue")

if __name__ == "__main__":
    main()