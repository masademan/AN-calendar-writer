from utils import make_choice, clear_console
from write_class_data import main as writing_json_data
from write_to_calendar import main as writing_to_calendar
from delete_from_calendar import main as delete_from_calendar

def main():
    actions = ["Write to json", "Write to calendar", "Delete from calendar", "Quit"]
    while True:
        clear_console()

        action = make_choice(actions, "What action to do? ", use_quotes=False)

        if action == actions[0]:
            writing_json_data()
        elif action == actions[1]:
            writing_to_calendar()
        elif action == actions[2]:
            delete_from_calendar()
        elif action == actions[3]:
            return

        input("Press enter to continue")

if __name__ == "__main__":
    main()