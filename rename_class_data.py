from read_class_data import read_json
from write_class_data import write_data
from utils import get_class_data_file_name, make_choice, clear_console

def main():
    clear_console()

    term_data_file_path = get_class_data_file_name()

    current_term_data = read_json(term_data_file_path)
    ANSWER_TO_STOP = "Quit"

    while True:
        current_class_names = list(current_term_data["classes"].keys())

        class_to_rename = make_choice(current_class_names + [ANSWER_TO_STOP], "Which class do you want to rename, or do you want to quit? ", use_quotes=False)

        if class_to_rename == ANSWER_TO_STOP:
            break

        new_class_name = input(f"What do you want to rename '{class_to_rename}' to?\n")

        current_term_data["classes"][new_class_name] = current_term_data["classes"].pop(class_to_rename)

    write_data(current_term_data, term_data_file_path, readable=True)

if __name__ == "__main__":
    main()
