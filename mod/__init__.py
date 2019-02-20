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

import pprint
# pprint.pprint(config_patterns)
