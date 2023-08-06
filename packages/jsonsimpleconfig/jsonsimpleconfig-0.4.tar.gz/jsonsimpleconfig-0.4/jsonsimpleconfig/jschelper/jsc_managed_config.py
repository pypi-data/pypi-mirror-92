# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

"""
JSC Config Managed class - JSC Config Managed
"""

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

from jsonsimpleconfig import JscParser, JscData


###############################################################################
# Class                                                                       #
###############################################################################

class JscConfigManaged:
    """JSC Config Managed class."""
    _jsc_config_file = None
    __jsc_data = None

    def __init__(self,
                 jsc_config_file,
                 base_jsc_data=None):
        self._jsc_config_file = jsc_config_file
        if base_jsc_data:
            self.__jsc_data = base_jsc_data

    def __enter__(self):
        jsc_parser = JscParser()
        self.__merge_jsc(jsc_parser.parse_file(self._jsc_config_file))
        return self.__jsc_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._jsc_config_file = None
        self.__jsc_data = None

    def __merge_jsc(self, jsc_data):
        if jsc_data is not None and isinstance(jsc_data, JscData):
            if self.__jsc_data is not None and isinstance(self.__jsc_data, JscData):
                self.__jsc_data.merge(jsc_data)
            else:
                self.__jsc_data = jsc_data

###############################################################################
#                                End of file                                  #
###############################################################################
