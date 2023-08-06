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

from jsonsimpleconfig import JscParser, JscData, JsonExtractor


###############################################################################
# Class                                                                       #
###############################################################################

class Jsc2JsonHelper:

    @staticmethod
    def convert(jsc_file, json_file):

        jsc_parser = JscParser()
        jsc_data = jsc_parser.parse_file(jsc_file)

        if jsc_data is not None and isinstance(jsc_data, JscData):
            logging.info('JSC file is correct. Generating JSON ...')
            logging.info('JSON location: %s', json_file)
            json_extractor = JsonExtractor(jsc_data)
            json_extractor.extract_to_file(json_file)

        else:
            logging.error('Incorrect JSC or file is empty.')

###############################################################################
#                                End of file                                  #
###############################################################################
