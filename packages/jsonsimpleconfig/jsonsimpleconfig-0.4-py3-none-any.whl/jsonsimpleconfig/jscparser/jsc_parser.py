# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import logging

from jsonsimpleconfig import JscComments, JscData, JscSection


###############################################################################
# Class                                                                       #
###############################################################################

class JscParser:
    """
    JscParser
    """

    def __init__(self):
        self.__jsc_data = None
        self.__current_section = None
        self.__current_section_data = None

    def __new_section(self, section_name):
        if section_name[0] == '[':
            section_name = section_name.lstrip('[')
        if section_name[-1] == ']':
            section_name = section_name.rstrip(']')
        if section_name != JscSection.GLOBAL_SECTION_NAME:
            section_name = section_name.strip()
            if section_name[0] != '"':
                section_name = '"' + section_name
            if section_name[-1] != '"':
                section_name = section_name + '"'

        self.__current_section = section_name
        self.__current_section_data = '{'

    def __end_section(self):
        self.__current_section_data += '}'
        if self.__jsc_data is None:
            self.__jsc_data = JscData()

        section_name = self.__current_section
        json_string = self.__current_section_data
        self.__current_section_data = self.__current_section = None
        self.__jsc_data.add_section_json_string(section_name, json_string)

    def __parse_line(self, line):
        line = JscComments.strip_comments(line)
        line = line.strip()
        if line:
            if line[0] == '[' and line[-1] == ']':
                if self.__current_section is not None and \
                        self.__current_section_data is not None:
                    self.__end_section()
                self.__new_section(line)

            else:
                if self.__current_section is None and \
                        self.__current_section_data is None:
                    self.__new_section(JscSection.GLOBAL_SECTION_NAME)
                if self.__current_section_data != '{':
                    self.__current_section_data += ','
                self.__current_section_data += line

    def parse_file(self, jsc_file_path, parse_line_by_line=False) -> JscData:
        """
        parse_file
        :param jsc_file_path:
        :param parse_line_by_line:
        :return:
        """
        self.__jsc_data = None
        try:
            with open(jsc_file_path) as jsc_file:

                if jsc_file.readable():
                    if parse_line_by_line:
                        for line in jsc_file:
                            self.__parse_line(line)
                    else:
                        jsc_text = JscComments.strip_comments(jsc_file.read())
                        lines = jsc_text.splitlines()
                        for line in lines:
                            self.__parse_line(line)
            self.__end_section()
            jsc_file.close()

        except Exception as exception:
            self.__jsc_data = None
            logging.debug(exception)

        return self.__jsc_data

    def parse_string(self, jsc_string) -> JscData:
        """
        parse_string
        :param jsc_string:
        :return:
        """
        self.__jsc_data = None
        try:
            jsc_text = JscComments.strip_comments(jsc_string)
            lines = jsc_text.splitlines()
            for line in lines:
                self.__parse_line(line)
            self.__end_section()

        except Exception as exception:
            self.__jsc_data = None
            logging.debug(exception)

        return self.__jsc_data

###############################################################################
#                                End of file                                  #
###############################################################################
