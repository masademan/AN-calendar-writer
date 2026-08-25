import os
import sys
import json
from utils import get_class_data_file_name

def read_json(file_path: str):
    if not file_path.endswith(".json"): file_path += ".json"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: The specified file was not found", file=sys.stderr)
        sys.exit(-1)
    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON formatting", file=sys.stderr)
        sys.exit(-1)

    return data

def read_term_data():
    file_path = get_class_data_file_name()
    if os.path.exists(file_path):
        return read_json(file_path)
    return None

if __name__ == "__main__":
    data = read_term_data()
    print(json.dumps(data, indent=4, ensure_ascii=False))