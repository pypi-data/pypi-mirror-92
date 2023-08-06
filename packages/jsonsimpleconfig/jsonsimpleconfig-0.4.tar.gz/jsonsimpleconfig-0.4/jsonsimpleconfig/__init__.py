"""
JSON Simple Config

The simple idea to prepare and manage configuration for your application.
"""

# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

###############################################################################
# Import(s)                                                                   #
###############################################################################

from .jsccommon import JscComments, JscCommon
from .jscdata import JscData, JscSection
from .jscparser import Json, JscParser
from .jscextractor import JscExtractor, JscHeader, JsonExtractor
from .jschelper import Jsc, Json2JscHelper, Jsc2JsonHelper, JscConfig, JscConfigManaged as JscDataFromFile


###############################################################################
# Module                                                                      #
###############################################################################

def load(jsc_file, refresh=False):
    """
    load
    :param jsc_file:
    :param refresh:
    :return:
    """
    return Jsc.get(jsc_file, refresh)


def loads(jsc_string):
    """
    loads
    :param jsc_string:
    :return:
    """
    return Jsc.gets(jsc_string)


def load_json(json_file):
    """
    load_json
    :param json_file:
    :return:
    """
    return Json.parse_file_json(json_file)


def loads_json(json_string):
    """
    loads_json
    :param json_string:
    :return:
    """
    return Json.parse_string_json(json_string)


__all__ = (
    'JscCommon',
    'JscComments',
    'Json2JscHelper',
    'Jsc2JsonHelper',
    'Json',
    'JscParser',
    'JscData',
    'JscSection',
    'JscExtractor',
    'JscExtractor',
    'JscHeader',
    'JsonExtractor',
    'JscDataFromFile',
    'JscConfig',
    'Jsc',
)

###############################################################################
#                                End of file                                  #
###############################################################################
