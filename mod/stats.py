"""
Manage statistics from files and directory.

"""

from datetime import datetime

from mod.utils import bytes2human


class Stats(object):
    """Manage statistics from files and directories."""

    def __init__(self):
        self.count = 0
        self.byte_size = 0
        self.created = TimePeriod()
        self.modified = TimePeriod()
        self.accessed = TimePeriod()

    def update(self, file):
        """Update statistics with data taken from file."""
        try:
            stats = file.stat()
            self.created.update(stats.st_ctime)
            self.modified.update(stats.st_mtime)
            self.accessed.update(stats.st_atime)
            self.byte_size += stats.st_size
        except PermissionError:
            pass
        except FileNotFoundError:
            pass
        self.count += 1

    def append(self, stats):
        """Add byte size, file count and extend time periods."""
        self.created.append(stats.created)
        self.modified.append(stats.modified)
        self.accessed.append(stats.accessed)
        self.byte_size += stats.byte_size
        self.count += stats.count

    def persist(self, object):
        """To persist in an object database."""
        object.created_older, object.created_newer = self.created.todatetime()
        object.modified_older, object.modified_newer = self.modified.todatetime()
        object.accessed_older, object.accessed_newer = self.accessed.todatetime()
        object.byte_size = self.byte_size
        object.count = self.count

    def __str__(self):
        out = ["Created: %s" % self.created,
               "Modified: %s" % self.modified,
               "Accessed: %s" % self.accessed,
               "Size: " + bytes2human(self.byte_size),
               "Count: %d" % self.count
               ]
        return "\n".join(out)


class TimePeriod(object):
    def __init__(self, stat=None):
        self._older = self._newer = None
        if stat:
            self.update(stat)

    def update(self, stat):
        s = stat
        if isinstance(stat, datetime):
            s = stat.timestamp()
        if self._older is None:
            self._older = self._newer = s
        else:
            self._older = min(self._older, s)
            self._newer = max(self._newer, s)

    def append(self, timeperiod):
        if not timeperiod._older is None:
            if self._older is None:
                self._older = timeperiod._older
                self._newer = timeperiod._newer
            else:
                self._older = min(self._older, timeperiod._older)
                self._newer = max(self._newer, timeperiod._newer)

    def todatetime(self):
        """Convert to datetime to save to database."""
        fn = lambda time: datetime.fromtimestamp(time)
        if self._older is None:
            return None, None
        else:
            try:
                return fn(self._older), fn(self._newer)
            except Exception as e:
                print(e)
                return None, None

    def __str__(self):
        if self._older is None:
            return "N/A"
        tuple = self.todatetime()
        fn = lambda time: time.strftime("%Y-%m-%d %H:%M:%S")
        return "from {} to {}".format(fn(tuple[0]), fn(tuple[1]))
