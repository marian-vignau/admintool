import hashlib
import yaml
import codecs

from pony import orm  # fades pony

from .database import *
from .utils import logger


def append_name(folderscanner):
    import codecs
    with codecs.open("subfolders", "a") as fh:
        fh.write("%s --> %s\n" % (folderscanner.path, folderscanner.stor))
    print("%s --> %s" % (folderscanner.path, folderscanner.path.parent))


@orm.db_session
def save_on_db(folderscanner):
    cad = folderscanner.storage.name + ";" + str(folderscanner.path)
    id = hashlib.sha1(cad.encode("utf8")).hexdigest()
    try:
        folder = Folder[id]
    except orm.ObjectNotFound:
        drivepath=str(folderscanner.path.drive)
        folder = Folder(
            folderid=id,
            storage=folderscanner.storage,
            report=folderscanner.report,
            name=str(folderscanner.path.name),
            rootdir=drivepath,
            subpath=str(folderscanner.path.parent)[len(drivepath)+1:],
            purpose=folderscanner.type["purpose"]

        )
    else:
        print("existe", cad)
    folderscanner.stats.topersist(folder)


@orm.db_session
def start_report(folderscanner):
    # 'infperiod': '17',
    # 'infnumber': '0045',
    # 'inftype': None,
    # 'expnumber': None,
    # 'expperiod': None,
    # 'circunscription': None,
    # 'comments': ''
    values = folderscanner.parsed.groupdict()
    values["infperiod"] = int(values["infperiod"])
    values["infnumber"] = int(values["infnumber"])
    values["inftype"] = "RE" if values["inftype"] is None else values["inftype"].upper()
    reportname = "{infperiod:02d}{inftype}{infnumber:04d}".format(**values)
    try:
        folderscanner.report = Report[reportname]
    except orm.ObjectNotFound:
        folderscanner.report = Report(
            owner=folderscanner.storage.owner,
            reportname=reportname,
            data=yaml.dump(values, default_flow_style=False)
        )


def save_report(folderscanner):
    save_on_db(folderscanner)


def log_subfolder(folderscanner):
    with codecs.open("subfolders.csv", "a", encoding="utf8") as fh:
        fh.write("{};{}\n".format(folderscanner.path.name, folderscanner.path.parent))
    save_on_db(folderscanner)
