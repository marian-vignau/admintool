"""
Many utilities classes or functions

"""
import yaml  # fades pyyaml
import logging

logger = logging.getLogger('tools')
hdlr = logging.FileHandler('tools.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)



def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


class Tables(object):
    def __init__(self, string_format):
        """

        :param string_format:
        sample:
            - header: purpose
              format: 1.purpose
              length: 10

        """
        self.string_format = yaml.load(string_format)
        self.line_format = ""
        for item in self.string_format:
            length = item.get("length", 15)
            item_format = item.get("format", "{}")
            item_format = item_format.replace("}", ":%ds}|" % length)
            self.line_format += item_format

        print(self.string_format)
        print(self.line_format)
        print(self.show_header())


    def show_header(self):
        sal = ""
        for x in self.string_format:
            length = x.get("length", 15)
            item = "_" * length + x.get("header", "")
            sal += item[:-length] + ":"
        return sal

    def show_item(self, values):
        return self.line_format.format(values)
