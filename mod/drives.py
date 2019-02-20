"""
Para obtener en Windows toda la información sobre los dispositivos montados en drive letters
Para instalar win32api:
) Bajar de https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32
) Abrir windows/system32/cmd.exe con privilegios de administrador
) Ir al directorio del proyecto cd path_proyecto
) activar el venv: venv/Scripts/activate.bat
) instalar el wheel elegido según la version de python
pip install pywin32-221-cp34-cp34m-win_amd64.whl
) activar con python.exe venv\Scripts\pywin32_postinstall.py -install
para activar se requieren privilegios de administrador
"""

__author__ = "María Andrea Vignau"

import string
import os
import ctypes
import subprocess
import platform
import win32api  # fades pywin32

kernel32 = ctypes.windll.kernel32


class symbolic_drives(object):
    """Use operating system api to list current drives and find a description"""

    def __init__(self):
        self._drives = []
        self._mapped = {}
        self._get_drives()
        self._net_mapped_drives()
        self._scan_drives_names()

    def _get_drives(self):
        """Get a list of all used drive letters"""
        bitmask = kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                self._drives.append(letter)
            bitmask >>= 1

    def _net_mapped_drives(self):
        """Get de UNC of every mapped drive letter to a net resource"""
        y = subprocess.check_output(["net", "use"], encoding="utf8", errors="ignore")
        for line in y.split("\n"):
            for drive_letter in self._drives:
                if drive_letter.upper() + ":" in line.split("  "):
                    info = [phrase.strip() for phrase in line.split("  ") if phrase > ""]
                    self._mapped[info[2].split("\\")[-1]] = drive_letter

    def _scan_drives_names(self):
        """Get the names of all local drives"""
        for drive_letter in self._drives:
            if not drive_letter in self._mapped.values():
                try:
                    data = win32api.GetVolumeInformation(drive_letter + ":\\")
                    self._mapped[data[0]] = drive_letter
                except Exception as e:
                    pass

    def find_path(self, drivename, *subdirs):
        """return a path using drive name instead of drive letter"""
        if drivename in self._mapped:
            joint = [self._mapped[drivename] + ":"]
            joint.extend(subdirs)
            return os.sep.join(joint)
        return None

    def find_drivename(self, driveletter):
        """Return the scanned drive name from drive letter"""
        for k in self._mapped.values():
            if k == driveletter:
                return self._mapped[k]
        return None

    def current_names(self):
        return ["%s:" % k for k in self._mapped.values()] + list(self._mapped.keys())

    def volumen_information(self):
        out = []
        for drive_letter in self._drives:
            try:
                out += ["%s: %s" % (drive_letter, win32api.GetVolumeInformation(drive_letter + ":\\"))]
            except Exception as e:
                print(e)
        out += [subprocess.check_output(["net", "use"], encoding="utf8", errors="ignore")]
        out += [platform.uname().node]
        return out

    def __str__(self):
        return '\n'.join(["%2s: %s" % (v, k) for (k, v) in self._mapped.items()])


Drives = symbolic_drives()
