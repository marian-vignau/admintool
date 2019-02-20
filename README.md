

Utility to scan, control, manage and optimize use of storage on forensic work

## Concepts:

Storage: A storage space, can be a drive or a folder.

Folder: A scanned folder in the filesystem, can be mounted or not.

Storage type: Purpose of storage, can be finished reports, deliverables, work in progress, data, backup

Use type: What is the use of this particular sub folder.
        It depends on the storage's type, plus a criteria based on subfolder name

Report: Number of report. At least, has a year, number and type

First/Last Created: First/last created folder in the type

First/Last Modified: First/last modified folder in the type

First/Last Seen: First/last seen folder in the type



## Modules:

data\<user>.yml: all config stuff, it is separated from user to user

database: Manage the database

drive: scans all drives and search about connected ones, UNC names, etc. Necessary to name storages

scan: scans a directory

main: CLI front-end

## Using it:

Activate virtualenv, 
````
> virtualenv venv
> venv/Script/activate.bat
> pip install --editable .
````

Install actual module in develop mode
````
> python setup.py develop --no-deps
````

Use on console
````
> tools.exe
````
