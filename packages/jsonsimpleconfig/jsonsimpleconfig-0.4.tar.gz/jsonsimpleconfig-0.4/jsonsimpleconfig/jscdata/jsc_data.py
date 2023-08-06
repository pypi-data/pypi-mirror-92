# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import json
import logging
import os
import sys

from .jsc_section import JscSection


###############################################################################
# Class                                                                       #
###############################################################################

class JscData:
    """
    The JSC data container.
    """

    def __init__(self):
        self.__section = JscSection()
        self.__jsc = {}

    def __section_from_json(self, section_data):
        if isinstance(section_data, dict):
            keys = list(section_data.keys())
            if not keys:
                self.__section.go_down()
            else:
                for key, value in section_data.items():
                    if isinstance(value, dict):
                        self.__section.go_up(key)
                        self.__section_from_json(value)
                    else:
                        section_name = self.__section.str()
                        if section_name is None:
                            section_name = JscSection.GLOBAL_SECTION_NAME

                        if section_name not in self.__jsc:
                            self.__jsc[section_name] = {}
                        self.__jsc[section_name][key] = value

                    if key == keys[-1]:
                        self.__section.go_down()

    def add_section_data(self, section_name, section_data):
        """
        Put data for JSC tree section

        Parameters
        ----------
        section_name : string
            Section name
        section_data : dict
            Section data
        """
        if section_name[0] == '[':
            section_name = section_name.lstrip('[')
        if section_name[-1] == ']':
            section_name = section_name.rstrip(']')
        for key, value in section_data.items():
            if section_name not in self.__jsc:
                self.__jsc[section_name] = {}
            self.__jsc[section_name][key] = value

    def add_section_json_string(self, section_name, section_json_string):
        """
        Put data for JSC tree section using JSON format
        If JSON is correct will be added as JSC data branch

        Parameters
        ----------
        section_name : string
            Section name
        section_json_string : string
            Section data as JSON string
        """
        try:
            section_data = json.loads(section_json_string)
            self.add_section_data(section_name, section_data)

        except json.JSONDecodeError as exception:
            logging.error(exception.msg)
            logging.error(sys.exc_info())
            logging.error(section_json_string)
        except Exception as exception:
            logging.error(sys.exc_info())
            logging.debug(exception)

    def get_value(self, section_name, key, default=None) -> dict:
        """
        Get value for provided section and key
        For 'Global' variable section name should be None

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
        value = default
        section_data = self.get_section(section_name)
        if section_data and key in section_data:
            value = section_data.get(key)
        return value

    def get_section(self, section_name=None) -> dict:
        """
        Get full section branches

        Parameters
        ----------
        section_name : string
            Section name

        Returns
        -------
        dict
            The section branch structure.
        """
        if section_name is None or section_name == '':
            section_name = JscSection.GLOBAL_SECTION_NAME
        elif section_name != JscSection.GLOBAL_SECTION_NAME:
            section_name = section_name.strip()
            if section_name[0] != '"':
                section_name = '"' + section_name
            if section_name[-1] != '"':
                section_name = section_name + '"'
        if section_name in self.get_section_names():
            return self.__jsc[section_name]
        return None

    def get_section_names(self):
        """
        Get all sections

        Returns
        -------
        dict
            Return list of the sections names or None if JSC is not defined.
        """
        if self.__jsc is not None:
            return self.__jsc.keys()
        return None

    def merge(self, jsc_data):
        """
        Merge another JSC data into current data

        Parameters
        ----------
        jsc_data : JscData
            JSC data from another source
        """
        if jsc_data is not None and isinstance(jsc_data, JscData):
            section_names = jsc_data.get_section_names()
            if section_names is not None:
                self.__merge_section_names(jsc_data, section_names)

    def __merge_section_names(self, jsc_data, section_names):
        for section_name in section_names:
            section_data = jsc_data.get_section(section_name)
            if isinstance(section_data, dict):
                for key in section_data:
                    value = section_data.get(key)
                    if section_name not in self.__jsc:
                        self.__jsc[section_name] = {}
                    self.__jsc[section_name][key] = value

    def str(self) -> str:
        """
        Get JSC data structure as string

        Returns
        -------
        string
            JSC data as string.
        """
        jsc_data_string = os.linesep
        section_names = self.get_section_names()
        if section_names is not None:
            for section_name in section_names:
                section_print = "* Section"
                if section_name == JscSection.GLOBAL_SECTION_NAME:
                    section_print += " (Global):"
                else:
                    section_print += " - {}:".format(section_name)
                jsc_data_string += section_print + os.linesep
                section_data = self.get_section(section_name)
                if isinstance(section_data, dict):
                    for key in section_data:
                        value = section_data.get(key)
                        jsc_data_string += '*** [' + str(key) + '] : [' + str(value) + ']' + os.linesep

        return jsc_data_string

    def str_html(self) -> str:
        """
        Get JSC data structure as string with new line as <br> for HTML format

        Returns
        -------
        string
            HTML format of JSC data.
        """
        return self.str().replace(os.linesep, '<br>' + os.linesep)

    def print(self):
        """
        Prints JSC string data
        """
        print(self.str())

    def print_html(self):
        """
        Prints JSC data as HTML format
        """
        print(self.str_html())

    def convert_from_json(self, json_data):
        """
        Converts JSC data section from JSON

        Parameters
        ----------
        json_data : dict
            JSON data to convert as dict
        """
        self.__section_from_json(json_data)

    @staticmethod
    def from_json(json_data):
        """
        Get JSC data from JSON

        Parameters
        ----------
        json_data : dict
            JSON data to convert as dict

        Returns
        -------
        string
            JSC data from provided JSON.
        """
        jsc_data = JscData()
        jsc_data.convert_from_json(json_data)
        return jsc_data

###############################################################################
#                                End of file                                  #
###############################################################################
