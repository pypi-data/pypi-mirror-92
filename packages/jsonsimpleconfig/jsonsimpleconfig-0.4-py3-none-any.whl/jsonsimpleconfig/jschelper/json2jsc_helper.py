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

from jsonsimpleconfig import Json, JscData, JscExtractor


###############################################################################
# Class                                                                       #
###############################################################################

class Json2JscHelper:

    @staticmethod
    def convert(json_file, jsc_file):

        json_parser = Json(json_file)
        json_data = json_parser.parse()

        if json_data['data'] is not None:
            if isinstance(json_data['data'], dict):
                logging.info('JSON file is correct. Generating JSC ...')
                logging.info('JSC location: %s', jsc_file)
                jsc_data = JscData.from_json(json_data['data'])
                jsc_extractor = JscExtractor(jsc_data)
                jsc_extractor.extract_to_file(jsc_file)
            else:
                logging.error('JSON data without root name cannot be converted into JSC.')

        else:
            logging.error('Incorrect JSON or file is empty.')
            if json_data['status'] is not None:
                logging.debug(json_data['status'])

###############################################################################
#                                End of file                                  #
###############################################################################
