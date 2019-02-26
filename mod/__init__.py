import pathlib
import os
import yaml

default_owner = os.getlogin()
database_path = pathlib.Path.cwd()
while not (database_path / "data").exists():
    if database_path == database_path.parent:
        raise FileNotFoundError
    database_path = database_path.parent
# orm.set_sql_debug(True)
database_filename = str(database_path / "data" / (default_owner + '002.sqlite'))
filename = str(database_path / "data" / (default_owner + '.yml'))
with open(filename, "r") as fa:
    patterns = fa.read()

config_patterns = yaml.load(patterns)

def extract_purposes(folders):
    """Extract registered purposes in foldertypes lists."""
    purposes_detected = []
    if isinstance(folders, dict):
        folders_list = folders.items()
    elif isinstance(folders, list):
        folders_list = folders

    for item in folders_list:
        if isinstance(item, tuple):
            item = item[1]
        if isinstance(item, dict):
            if item.get("purpose", False) and not item["purpose"] in purposes_detected:
                purposes_detected.append(item["purpose"])
            if item.get("subfolders", False):
                purposes_detected.extend(extract_purposes(item["subfolders"]))
    return purposes_detected


possible_purposes = extract_purposes(config_patterns["FolderTypes"])
possible_purposes.sort()
