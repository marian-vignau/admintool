"""
Functions to manage data
Database defined in database.py
Drives and StoragesTypes

"""

import os
import pathlib
from pony import orm  # fades pony
from .database import *
from .drives import Drives
from . import scanner

@orm.db_session
def storageadd(name, drivename, parentdir, purpose, description, owner=os.getlogin()):
    try:
        owner = Owner[owner]
    except orm.ObjectNotFound:
        owner = Owner(login=owner)

    Storage(
        name=name,
        owner=owner,
        description=description,
        drivename=drivename,
        parentdir=parentdir,
        purpose=purpose
    )


@orm.db_session
def storagedel(name, owner=os.getlogin()):
    storage = Storage[name]
    if storage.owner.login != owner:
        raise PermissionError
    else:
        storage.delete()


@orm.db_session
def storagelist(owner=os.getlogin()):
    for storage in Storage.select(lambda s: s.owner.login == owner):
        yield storage


@orm.db_session
def storagescan(name, owner=os.getlogin()):
    storage = Storage[name]
    if storage.owner.login != owner:
        raise PermissionError

    path = Drives.find_path(storage.drivename, storage.parentdir)
    if pathlib.Path(path).exists():
        storageobj = scanner.Storage(storage.purpose)
        storageobj.scan(pathlib.Path(path), storage)
        return storageobj
    else:
        raise FileNotFoundError
