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
from . import default_owner
from .utils import bytes2human

@orm.db_session
def storageadd(name, drivename, parentdir, purpose, description):

    try:
        owner = Owner[default_owner]
    except orm.ObjectNotFound:
        owner = Owner(login=default_owner)

    Storage(
        name=name,
        owner=owner,
        description=description,
        drivename=drivename,
        parentdir=parentdir,
        purpose=purpose
    )


@orm.db_session
def storagedel(name):
    storage = Storage[name]
    if storage.owner.login != default_owner:
        raise PermissionError
    else:
        storage.delete()


@orm.db_session
def storagelist():
    for storage in Storage.select(lambda s: s.owner.login == default_owner):
        yield storage

@orm.db_session
def reportlist():
    for report in Report.select(lambda s: s.owner.login == default_owner):
        yield report


@orm.db_session
def storagescan(name):
    storage = Storage[name]
    if storage.owner.login != default_owner:
        raise PermissionError

    path = Drives.find_path(storage.drivename, storage.parentdir)
    if pathlib.Path(path).exists():
        storageobj = scanner.Storage(storage.purpose)
        storageobj.scan(pathlib.Path(path), storage)
        return storageobj
    else:
        raise FileNotFoundError


@orm.db_session
def reportinfo(reportname):
    try:
        rpt = Report[reportname]
        total_size = 0
        for folder in rpt.reportdirs:
            cad = "{1.storage.name:5s} {1.purpose:20s} {0:10s} {1.subpath}\\{1.name}"
            size = bytes2human(folder.byte_size)
            total_size += folder.byte_size
            yield(cad.format(size, folder))
        yield "Total size: " + bytes2human(total_size)

    except orm.ObjectNotFound:
        yield "Not founded."


@orm.db_session
def wipescannedinfo():
    orm.delete(r for r in Folder)
    orm.delete(r for r in Report)
