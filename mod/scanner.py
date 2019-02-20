"""
To define regex and other search patterns

^(?P<infperiod>\d\d)-(?P<infnumber>\d{4})(?P<inftype>\w\w)?( +(exp|expte|of) +(?P<expnumber>\d*)-(?P<expperiod>\d*)(-(?P<circunscription>\d*))?)? *(?P<comments>.*)$
'
gmi
^ asserts position at start of a line

Named Capture Group infperiod (?P<infperiod>\d\d)
\d matches a digit (equal to [0-9])
\d matches a digit (equal to [0-9])
- matches the character - literally (case insensitive)

Named Capture Group infnumber (?P<infnumber>\d{4})

\d{4} matches a digit (equal to [0-9])
{4} Quantifier — Matches exactly 4 times

Named Capture Group inftype (?P<inftype>\w\w)?
? Quantifier — Matches between zero and one times, as many times as possible, giving back as needed (greedy)
\w matches any word character (equal to [a-zA-Z0-9_])
\w matches any word character (equal to [a-zA-Z0-9_])

4th Capturing Group ( +(exp|expte|of) +(?P<expnumber>\d*)-(?P<expperiod>\d*)(-(?P<circunscription>\d*))?)?
? Quantifier — Matches between zero and one times, as many times as possible, giving back as needed (greedy)

 + matches the character   literally (case insensitive)
+ Quantifier — Matches between one and unlimited times, as many times as possible, giving back as needed (greedy)

5th Capturing Group (exp|expte|of)

 + matches the character   literally (case insensitive)

Named Capture Group expnumber (?P<expnumber>\d*)
- matches the character - literally (case insensitive)

Named Capture Group expperiod (?P<expperiod>\d*)

8th Capturing Group (-(?P<circunscription>\d*))?

 * matches the character   literally (case insensitive)
* Quantifier — Matches between zero and unlimited times, as many times as possible, giving back as needed (greedy)

Named Capture Group comments (?P<comments>.*)

.* matches any character (except for line terminators)
$ asserts position at the end of a line

Global pattern flags
g modifier: global. All matches (don't return after first match)
m modifier: multi line. Causes ^ and $ to match the begin/end of each line (not only begin/end of string)
i modifier: insensitive. Case insensitive match (ignores case of [a-zA-Z])
"""

__author__ = " María Andrea Vignau"

import re
import hashlib
from datetime import datetime
from . import config_patterns
from .stats import Stats
from . import savescan

storage_types = config_patterns["Storages"].keys()


class Storage(object):
    def __init__(self, storage_type):
        self.type = config_patterns["Storages"][storage_type]

    def scan(self, path, storageobj):
        self.rootfolder = FolderType(self.type["root"])
        self.rootfolder.scan(path, storageobj)


class FolderType(object):
    def __init__(self, folder_type):
        self.type = config_patterns["FolderTypes"][folder_type]
        self._regex = re.compile(self.type.get("regex", "").strip(), re.IGNORECASE | re.MULTILINE)
        self.parsed = False
        self.report = None

    def check(self, path):
        if path.is_file():
            return False
        if not self._regex:
            return True
        else:
            self.parsed = self._regex.match(path.name)
            if self.parsed:
                return True
        return False

    def scan(self, path, storage):
        self.path = path
        self.storage = storage
        if self.type.get("on_check", None):
            fn = getattr(savescan, self.type["on_check"])
            fn(self)
        self.scanned = datetime.now()
        self.finished = False
        self.stats = Stats()
        self.stats.update(self.path)
        try:
            for file in self.path.iterdir():
                processed = False
                for subfolderclass in self.type["subfolders"]:
                    obj = FolderType(subfolderclass)
                    if obj.check(file):
                        obj.scan(file, self.storage)
                        if obj.finished:
                            processed = True
                            self.stats.append(obj.stats)
                            break
                if not processed:
                    self.stats.update(file)
        except PermissionError:
            pass
        self.scanned = datetime.now()
        self.finished = True
        if self.type.get("on_finish", None):
            fn = getattr(savescan, self.type["on_finish"])
            fn(self)
