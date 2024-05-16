import re
import os


def extract_op_string(op_string):
    try:
        op_dict = eval(op_string)
    except SyntaxError:
        start_index = op_string.find("{")
        end_index = op_string.rfind("}") + 1
        dict_string = op_string[start_index:end_index]
        op_dict = eval(dict_string)
    return op_dict


def count_folders(directory):
    return len(
        [
            name
            for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))
        ]
    )


def remove_parentheses(text):
    return re.sub(r"\s*\([^)]*\)", "", text).strip()


def replace_options(tasks, food_options):
    for task_id, task_description in tasks.items():
        if "(options =" in task_description:
            start_index = task_description.find("(options = ") + len("(options = ")
            end_index = task_description.find(")")
            options = task_description[start_index:end_index].split(", ")
            for i in range(len(options)):
                option = options[i]
                if option in food_options:
                    task_description = task_description.replace(
                        option, str(food_options[option])
                    )
                    tasks[task_id] = task_description

    return tasks

def write_file(content, file_name):
    try:
        with open(file_name, "w") as f:
            f.write(content)
        return True
    except Exception:
        return False
