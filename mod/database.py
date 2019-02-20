"""
Define database persistent storage using PonyORM
"""
__author__ = " María Andrea Vignau"


from datetime import datetime
from decimal import Decimal
from . import database_filename

from pony import orm  # fades pony

db = orm.Database()


class Owner(db.Entity):
    login = orm.PrimaryKey(str)  # owner name. Defaults to user name
    storages = orm.Set("Storage")  # storages drives or directory
    reports = orm.Set("Report")  # conjunto de reportes relevados


class Storage(db.Entity):
    name = orm.PrimaryKey(str)  # storage short unique name
    owner = orm.Required(Owner)
    description = orm.Required(str)  # description
    drivename = orm.Required(str)  # unique name of drive where storage reside
    parentdir = orm.Required(str)  # root path. It can be empty
    purpose = orm.Required(str)  # purpose of storage. Can be finished reports, wip reports, backup, data, etc
    folders = orm.Set("Folder")


class Report(db.Entity):
    reportname = orm.PrimaryKey(str)
    owner = orm.Required(Owner)
    data = orm.Optional(str)  # aditional info, yaml format
    reportdirs = orm.Set("Folder")


class Folder(db.Entity):
    folderid = orm.PrimaryKey(str)  # sha1 hash of complete path plus storage name
    storage = orm.Required(Storage)
    report = orm.Optional(Report)
    name = orm.Required(str)  # directory name
    rootdir = orm.Required(str)  # first level dir
    subpath = orm.Optional(str)  # other levels paths. Complete path is rootdir + subpath + name
    purpose = orm.Required(str)  # identified purpose of the folder
    byte_size = orm.Optional(Decimal, 20, 2)  # size in bytes
    scanned = orm.Optional(datetime)  # when this folder was last scanned
    created_older = orm.Optional(datetime)  # older created file scanned
    created_newer = orm.Optional(datetime)  # newer created file scanned
    modified_older = orm.Optional(datetime)  # older modified file scanned
    modified_newer = orm.Optional(datetime)  # newer modified file scanned
    accessed_older = orm.Optional(datetime)  # older accessed file scanned
    accessed_newer = orm.Optional(datetime)  # newer accessed file scanned
    count = orm.Optional(int)  # count of


db.bind(provider='sqlite', filename=database_filename, create_db=True)

db.generate_mapping(create_tables=True)

