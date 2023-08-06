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

from jsonsimpleconfig import JscParser


###############################################################################
# Class                                                                       #
###############################################################################

class Jsc:
    class JsonSimpleConfig:
        def __init__(self, jsc_file):
            self.__jsc_file = jsc_file
            logging.debug('Parsing JSC file: %s', jsc_file)
            jsc_parser = JscParser()
            self.__jsc_data = jsc_parser.parse_file(jsc_file)

        __jsc_data = None

        def get(self):
            return self.__jsc_data

        def get_file(self):
            return self.__jsc_file

    __instance = None

    @staticmethod
    def set_logging_level(level):
        logging.basicConfig(format='[%(asctime)s][%(levelname)-8s] [%(module)-20s] - %(message)s',
                            datefmt='%Y.%m.%d %H:%M.%S', level=level)

    @staticmethod
    def set_debug_logging_level():
        Jsc.set_logging_level(logging.DEBUG)

    @staticmethod
    def get(jsc_file, refresh=False):
        if refresh or \
                not Jsc.__instance or \
                Jsc.__instance.get_file() != jsc_file:
            Jsc.__instance = Jsc.JsonSimpleConfig(jsc_file)

        return Jsc.__instance.get()

    @staticmethod
    def gets(jsc_data):
        jsc_parser = JscParser()
        return jsc_parser.parse_string(jsc_data)

    @staticmethod
    def get_value(jsc_file, section, key):
        jsc_data = Jsc.get(jsc_file, True)
        if jsc_data is not None:
            return jsc_data.get_value(section, key)
        return None

###############################################################################
#                                End of file                                  #
###############################################################################
