# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *

"""
JSC Config class - JSC Config singleton to keep current configuration data
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

class JscConfig:
    """JSC Config class."""
    _jsc_configs = ['/etc/jsc/main.jsc']
    __instance = None
    __jsc_data = None

    def init(self):
        """
        Initial load config from _jsc_configs files.
        """
        for jsc_file in self._jsc_configs:
            self.merge_jsc_file(jsc_file)

    def __new__(cls):
        if JscConfig.__instance is None:
            JscConfig.__instance = object.__new__(cls)
            JscConfig.__instance.init()
        return JscConfig.__instance

    @staticmethod
    def get():
        """
        Get the current configuration instance.
        """
        return JscConfig()

    @staticmethod
    def delete():
        """
        Clean current instance and allow to create new initialization for configuration.
        """
        if JscConfig.__instance is not None:
            JscConfig.__instance = None

    def get_data(self):
        """
        Returns JSC data stored for current configuration.

        Returns
        -------
        dict
            The JSC data stored at the current config
        """
        return self.__jsc_data

    def merge_jsc_file(self, jsc_file):
        """
        Merge your JSC file to current configuration.

        Parameters
        ----------
        jsc_file : string
            JSC file path
        """
        jsc_parser = JscParser()
        self.merge_jsc(jsc_parser.parse_file(jsc_file))

    def merge_jsc(self, jsc_data):
        """
        Merge your JSC data to current configuration.

        Parameters
        ----------
        jsc_data : JscData
            JSC data to merge to current configuration
        """
        if jsc_data is not None and isinstance(jsc_data, JscData):
            if self.__jsc_data is not None and isinstance(self.__jsc_data, JscData):
                self.__jsc_data.merge(jsc_data)
            else:
                self.__jsc_data = jsc_data

    def get_value(self, section_name, key, default=None):
        """
        Get value for provided section and key.
        For 'Global' variable section name should be None.

        Parameters
        ----------
        section_name : string
            Section name
        key : string
            Key name
        default : dict
            Default value if key does not exist

        Returns
        -------
        dict
            The value of the section key.
        """
        if self.__jsc_data is not None and isinstance(self.__jsc_data, JscData):
            return self.__jsc_data.get_value(section_name, key, default)

        return None

    def get_section(self, section_name, default=None):
        """
        Get full section branches.

        Parameters
        ----------
        section_name : string
            Section name
        default : dict
            Default value if section does not exist

        Returns
        -------
        dict
            The section branch structure.
        """
        if self.__jsc_data is not None and isinstance(self.__jsc_data, JscData):
            data = self.__jsc_data.get_section(section_name)
            if data is None:
                data = default
            return data
        return None

###############################################################################
#                                End of file                                  #
###############################################################################
