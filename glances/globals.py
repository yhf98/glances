# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# SPDX-FileCopyrightText: 2023 Nicolas Hennion <nicolas@nicolargo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only
#

"""Common objects shared by all Glances modules."""

################
# GLOBAL IMPORTS
################

import errno
import os
import sys
import platform
import ujson
from operator import itemgetter, methodcaller
import unicodedata
import types
import subprocess
from datetime import datetime
import re
import base64

import queue
from configparser import ConfigParser, NoOptionError, NoSectionError
from statistics import mean
from xmlrpc.client import Fault, ProtocolError, ServerProxy, Transport, Server
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

# Correct issue #1025 by monkey path the xmlrpc lib
from defusedxml.xmlrpc import monkey_patch

monkey_patch()

##############
# GLOBALS VARS
##############

# OS constants (some libraries/features are OS-dependent)
BSD = sys.platform.find('bsd') != -1
LINUX = sys.platform.startswith('linux')
MACOS = sys.platform.startswith('darwin')
SUNOS = sys.platform.startswith('sunos')
WINDOWS = sys.platform.startswith('win')
WSL = "linux" in platform.system().lower() and "microsoft" in platform.uname()[3].lower()

# Set the AMPs, plugins and export modules path
work_path = os.path.realpath(os.path.dirname(__file__))
amps_path = os.path.realpath(os.path.join(work_path, 'amps'))
plugins_path = os.path.realpath(os.path.join(work_path, 'plugins'))
exports_path = os.path.realpath(os.path.join(work_path, 'exports'))
sys_path = sys.path[:]
sys.path.insert(1, exports_path)
sys.path.insert(1, plugins_path)
sys.path.insert(1, amps_path)

# Types
text_type = str
binary_type = bytes
bool_type = bool
long = int

# Alias errors
PermissionError = OSError

# Alias methods
viewkeys = methodcaller('keys')
viewvalues = methodcaller('values')
viewitems = methodcaller('items')


###################
# GLOBALS FUNCTIONS
###################


def printandflush(string):
    """Print and flush (used by stdout* outputs modules)"""
    print(string, flush=True)


def to_ascii(s):
    """Convert the bytes string to a ASCII string
    Usefull to remove accent (diacritics)"""
    if isinstance(s, binary_type):
        return s.decode()
    return s.encode('ascii', 'ignore').decode()


def listitems(d):
    return list(d.items())


def listkeys(d):
    return list(d.keys())


def listvalues(d):
    return list(d.values())


def iteritems(d):
    return iter(d.items())


def iterkeys(d):
    return iter(d.keys())


def itervalues(d):
    return iter(d.values())


def u(s, errors='replace'):
    if isinstance(s, text_type):
        return s
    return s.decode('utf-8', errors=errors)


def b(s, errors='replace'):
    if isinstance(s, binary_type):
        return s
    return s.encode('utf-8', errors=errors)


def nativestr(s, errors='replace'):
    if isinstance(s, text_type):
        return s
    elif isinstance(s, (int, float)):
        return s.__str__()
    else:
        return s.decode('utf-8', errors=errors)


def system_exec(command):
    """Execute a system command and return the result as a str"""
    try:
        res = subprocess.run(command.split(' '), stdout=subprocess.PIPE).stdout.decode('utf-8')
    except Exception as e:
        res = 'ERROR: {}'.format(e)
    return res.rstrip()


def subsample(data, sampling):
    """Compute a simple mean subsampling.

    Data should be a list of numerical itervalues

    Return a subsampled list of sampling lenght
    """
    if len(data) <= sampling:
        return data
    sampling_length = int(round(len(data) / float(sampling)))
    return [mean(data[s * sampling_length : (s + 1) * sampling_length]) for s in range(0, sampling)]


def time_serie_subsample(data, sampling):
    """Compute a simple mean subsampling.

    Data should be a list of set (time, value)

    Return a subsampled list of sampling length
    """
    if len(data) <= sampling:
        return data
    t = [t[0] for t in data]
    v = [t[1] for t in data]
    sampling_length = int(round(len(data) / float(sampling)))
    t_subsampled = [t[s * sampling_length : (s + 1) * sampling_length][0] for s in range(0, sampling)]
    v_subsampled = [mean(v[s * sampling_length : (s + 1) * sampling_length]) for s in range(0, sampling)]
    return list(zip(t_subsampled, v_subsampled))


def to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 1.8 + 32


def is_admin():
    """
    https://stackoverflow.com/a/19719292
    @return: True if the current user is an 'Admin' whatever that
    means (root on Unix), otherwise False.
    Warning: The inner function fails unless you have Windows XP SP2 or
    higher. The failure causes a traceback to be printed and this
    function to return False.
    """

    if os.name == 'nt':
        import ctypes
        import traceback

        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print("Admin check failed with error: %s" % e)
            traceback.print_exc()
            return False
    else:
        # Check for root on Posix
        return os.getuid() == 0


def key_exist_value_not_none(k, d):
    # Return True if:
    # - key k exists
    # - d[k] is not None
    return k in d and d[k] is not None


def key_exist_value_not_none_not_v(k, d, value='', lengh=None):
    # Return True if:
    # - key k exists
    # - d[k] is not None
    # - d[k] != value
    # - if lengh is not None and len(d[k]) >= lengh
    return k in d and d[k] is not None and d[k] != value and (lengh is None or len(d[k]) >= lengh)


def disable(class_name, var):
    """Set disable_<var> to True in the class class_name."""
    setattr(class_name, 'enable_' + var, False)
    setattr(class_name, 'disable_' + var, True)


def enable(class_name, var):
    """Set disable_<var> to False in the class class_name."""
    setattr(class_name, 'enable_' + var, True)
    setattr(class_name, 'disable_' + var, False)


def safe_makedirs(path):
    """A safe function for creating a directory tree."""
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST:
            if not os.path.isdir(path):
                raise
        else:
            raise


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Source: https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " secs"
        if second_diff < 120:
            return "a min"
        if second_diff < 3600:
            return str(second_diff // 60) + " mins"
        if second_diff < 7200:
            return "an hour"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours"
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return str(day_diff) + " days"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks"
    if day_diff < 365:
        return str(day_diff // 30) + " months"
    return str(day_diff // 365) + " years"


def urlopen_auth(url, username, password):
    """Open a url with basic auth"""
    return urlopen(
        Request(
            url,
            headers={'Authorization': 'Basic ' + base64.b64encode(('%s:%s' % (username, password)).encode()).decode()},
        )
    )


def json_dumps(data):
    """Return the object data in a JSON format.

    Manage the issue #815 for Windows OS with UnicodeDecodeError catching.
    """
    try:
        return ujson.dumps(data)
    except UnicodeDecodeError:
        return ujson.dumps(data, ensure_ascii=False)


def json_dumps_dictlist(data, item):
    if isinstance(data, dict):
        try:
            return json_dumps({item: data[item]})
        except (TypeError, IndexError, KeyError):
            return None
    elif isinstance(data, list):
        try:
            # Source:
            # http://stackoverflow.com/questions/4573875/python-get-index-of-dictionary-item-in-list
            # But https://github.com/nicolargo/glances/issues/1401
            return json_dumps({item: list(map(itemgetter(item), data))})
        except (TypeError, IndexError, KeyError):
            return None
    else:
        return None


def string_value_to_float(s):
    """Convert a string with a value and an unit to a float.
    Example:
    '12.5 MB' -> 12500000.0
    '32.5 GB' -> 32500000000.0
    Args:
        s (string): Input string with value and unit
    Output:
        float: The value in float
    """
    convert_dict = {
        None: 1,
        'B': 1,
        'KB': 1000,
        'MB': 1000000,
        'GB': 1000000000,
        'TB': 1000000000000,
        'PB': 1000000000000000,
    }
    unpack_string = [
        i[0] if i[1] == '' else i[1].upper() for i in re.findall(r'([\d.]+)|([^\d.]+)', s.replace(' ', ''))
    ]
    if len(unpack_string) == 2:
        value, unit = unpack_string
    elif len(unpack_string) == 1:
        value = unpack_string[0]
        unit = None
    else:
        return None
    try:
        value = float(unpack_string[0])
    except ValueError:
        return None
    return value * convert_dict[unit]
