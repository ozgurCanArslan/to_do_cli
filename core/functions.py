import json
import typer


CATEGORIES_FILE = "categories.json"
CATEGORY_COLORS = [
    "blue",
    "cyan",
    "green",
    "magenta",
    "red",
    "white",
    "yellow",
    "purple",
    "violet",
]


def load_json(json_file=CATEGORIES_FILE):
    """load json file from json_file"""
    try:
        with open(json_file, encoding="utf-8") as file:
            parsed_json = json.load(file)
    except Exception as err:
        typer.echo(err)
        parsed_json = []
    return parsed_json


def write_json(json_file=CATEGORIES_FILE, content=None):
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)


def update_categories(method: str, field: str, new_field="", color=None):
    categories = load_json()
    error_message = None
    if method == "add":
        categories[field] = color
    elif method == "del":
        try:
            del categories[field]
        except Exception as err:
            typer.echo(err)
            error_message = "{}NotFound".format(field)
    elif method == "update":
        try:
            del categories[field]
            categories[new_field] = color
        except Exception as err:
            typer.echo(err)
            error_message = "{}NotFound".format(field)
    else:
        raise ValueError("{}NotSupported".format(method))
    if error_message is not None:
        raise ValueError(error_message)
    write_json(content=categories)


def check_colors():
    "check colors in categories_file remove wrong colored fields"
    categories = load_json()
    checked_dict = categories
    for category in categories:
        if categories[category] not in CATEGORY_COLORS:
            checked_dict[category] = "gray"

    write_json(content=checked_dict)
