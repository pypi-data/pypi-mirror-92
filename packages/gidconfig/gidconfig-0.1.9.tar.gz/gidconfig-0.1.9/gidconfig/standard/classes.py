
# region [Imports]

# * Standard Library Imports -->
import os
import configparser
from typing import Union
from datetime import datetime, timedelta
from pprint import pprint
# * Third Party Imports -->
from fuzzywuzzy import fuzz

# * Gid Imports -->
import gidlogger as glog

# * Local Imports -->
from gidconfig.data.enums import Get
from gidconfig.utility.functions import readit
# endregion [Imports]


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


class ConfigHandler(configparser.ConfigParser):
    def __init__(self, config_file=None, auto_read=True, auto_save=True, allow_no_value=True, **kwargs):
        super().__init__(**kwargs, allow_no_value=allow_no_value)
        self.config_file = '' if config_file is None else config_file
        self.auto_read = auto_read
        self.auto_save = auto_save
        self._method_select = {Get.basic: self.get, Get.boolean: self.getboolean, Get.int: self.getint, Get.list: self.getlist, Get.path: self.get_path, Get.datetime: self.get_datetime}
        self.annotation_replacements = {'[DEFAULT]': 'Options in this section are used if those options are not set in a Section'}
        if self.auto_read is True:
            self.read(self.config_file)

        self.saved_comments = {}

    def _store_comments(self, config_file):
        self.stored_comments = {}
        _section = ''
        with open(config_file, 'r') as conf_f:
            content_lines = conf_f.read().splitlines()
        for index, line in enumerate(content_lines):
            if line.startswith('['):
                _section = line.replace('[', '').replace(']', '').strip()
            if line.startswith(';'):
                if _section not in self.stored_comments:
                    self.stored_comments[_section] = []
                self.stored_comments[_section].append((content_lines[index + 1].split('=')[0].strip(), line.replace(';', '')))

    def _clean_comments(self):
        with open(self.config_file, 'r') as in_conf:
            content = in_conf.read()
        with open(self.config_file, 'w') as out_conf:
            for line in content.splitlines():
                if line.startswith(';'):
                    line = line.lstrip('=').strip()
                out_conf.write(line + '\n')

    def getlist(self, section, option, delimiter=',', as_set=False, casefold_items=False):
        _raw = self.get(section, option).strip()
        if _raw.endswith(delimiter):
            _raw = _raw.rstrip(delimiter)
        if _raw.startswith(delimiter):
            _raw = _raw.lstrip(delimiter).strip()
        _out = _raw.replace(delimiter + ' ', delimiter).split(delimiter)
        _out = list(map(lambda x: x.strip(), _out))
        if casefold_items is True:
            _out = list(map(lambda x: x.casefold(), _out))
        if as_set is True:
            _out = set(_out)
        return _out

    def list_from_keys_only(self, section, as_set=True):
        _result = self.options(section)
        _out = []
        for line in _result:
            if line != '':
                _out.append(line)
        if as_set is True:
            _out = set(_out)
        return _out

    def get_path(self, section, option, cwd_symbol='+cwd+'):
        _raw_path = self.get(section, option)
        if cwd_symbol in _raw_path:
            _out = _raw_path.replace(cwd_symbol, os.getcwd()).replace('\\', '/')
        elif '+userdata+' in _raw_path:
            _out = _raw_path.replace('+userdata+', os.getenv('APPDATA')).replace('\\', '/')
        elif _raw_path == 'notset':
            _out = None
        else:
            _out = os.path.join(_raw_path).replace('\\', '/')
        return _out

    def _best_fuzzymatch(self, in_term, in_targets: Union[list, set, frozenset, tuple, dict]):
        # Todo: replace with process.extractOne() from fuzzywuzzy!
        _rating_list = []
        for _target in in_targets:
            _rating_list.append((_target, fuzz.ratio(in_term, _target)))
        _rating_list.sort(key=lambda x: x[1], reverse=True)
        log.debug("with a fuzzymatch, the term '%s' was best matched to '%s' with and Levenstein-distance of %s", in_term, _rating_list[0][0], _rating_list[0][1])
        return _rating_list[0][0]

    def get_timedelta(self, section, option, amount_seperator=' ', delta_seperator=','):
        _raw_timedelta = self.get(section, option)
        if _raw_timedelta != 'notset':
            _raw_timedelta_list = _raw_timedelta.split(delta_seperator)
            _arg_dict = {'days': 0,
                         'seconds': 0,
                         'microseconds': 0,
                         'milliseconds': 0,
                         'minutes': 0,
                         'hours': 0,
                         'weeks': 0}
            for raw_delta_data in _raw_timedelta_list:
                _amount, _typus = raw_delta_data.strip().split(amount_seperator)
                _key = self._best_fuzzymatch(_typus, _arg_dict)
                _arg_dict[_key] = float(_amount) if '.' in _amount else int(_amount)
            return timedelta(**_arg_dict)

    def get_datetime(self, section, option, dtformat=None):
        _date_time_string = self.get(section, option)
        if _date_time_string == "notset":
            return None
        _dtformat = '%Y-%m-%d %H:%M:%S' if dtformat is None else dtformat
        return datetime.strptime(_date_time_string, _dtformat).astimezone()

    def set_datetime(self, section, option, datetime_object, dtformat=None):
        _dtformat = '%Y-%m-%d %H:%M:%S' if dtformat is None else format
        self.set(section, option, datetime_object.strftime(_dtformat))
        if self.auto_save is True:
            self.save()

    def set(self, section, option, value):
        if isinstance(value, list):
            value = ', '.join(list(map(str, value)))
        if not isinstance(value, str):
            value = str(value)
        super().set(section, option, value)
        if self.auto_save is True:
            self.save()

    def add_comment(self, section, option, comment):
        orig_value = self.get(section, option)
        self.remove_option(section, option)
        self.set(section, ';' + comment, '')
        self.set(section, option, orig_value)

    def enum_get(self, section: str, option: str, typus: Get = Get.basic):
        return self._method_select.get(typus, self.get)(section, option)

    def save(self):
        for section, value in self.saved_comments.items():
            for option, comment in value:
                self.add_comment(section, option, value)
        with open(self.config_file, 'w') as confile:
            self.write(confile)
        self._clean_comments()
        self.read()

    def read(self, filenames=None):

        _configfile = self.config_file if filenames is None else filenames
        self._store_comments(_configfile)
        super().read(self.config_file)

    def set_annotation_replacement(self, replacements: dict):
        for key, value in replacements.items():
            self.annotation_replacements[key] = value

    def get_annotated_config(self):
        content = readit(self.config_file)
        for target, annotation in self.annotation_replacements.items():
            replacement = f";; {annotation}\n{target}"
            content = content.replace(target, replacement)
        return content

    def __contains__(self, item: object) -> bool:
        return item in self.sections()


if __name__ == '__main__':
    pass
