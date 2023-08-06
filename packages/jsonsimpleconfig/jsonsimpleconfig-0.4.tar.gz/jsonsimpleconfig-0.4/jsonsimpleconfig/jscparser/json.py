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
import sys

from jsonsimpleconfig import JscData


###############################################################################
# Class                                                                       #
###############################################################################

class Json:
    """
    Json
    """

    def __init__(self, file):
        self.__file = file

    def parse(self):
        """
        parse
        :return:
        """

        try:
            json_data = open(self.__file)
            data = json.load(json_data)
            status = None
            json_data.close()

        except json.JSONDecodeError as exception:
            data = None
            status = exception.msg

        except Exception as exception:
            data = None
            status = sys.exc_info()
            logging.debug(exception)

        return {'data': data, 'status': status}

    @staticmethod
    def parse_file_json(json_file_path) -> JscData:
        """
        parse_file_json
        :param json_file_path: path to the JSON file
        :return: JSC Data
        """
        try:
            with open(json_file_path) as json_file:
                json_data = json.load(json_file)
                jsc_data = JscData.from_json(json_data)
        except Exception as exception:
            jsc_data = None
            logging.debug(exception)

        return jsc_data

    @staticmethod
    def parse_string_json(json_string) -> JscData:
        """
        parse_string_json
        :param json_string: JSON string
        :return: JSC Data
        """
        try:
            json_data = json.loads(json_string)
            jsc_data = JscData.from_json(json_data)
        except Exception as exception:
            jsc_data = None
            logging.debug(exception)

        return jsc_data

###############################################################################
#                                End of file                                  #
###############################################################################
