#! /bin/sh
# -*- coding: utf-8 -*-
""":"
exec python3 $0 ${1+"$@"}
"""
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__doc__ = "Return JSON Simple Config print config file"
__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import argparse
import json
import logging
import signal
import sys

from jsonsimpleconfig import Jsc, JsonExtractor

###############################################################################
# Module Variable(s)                                                          #
###############################################################################

VERSION_STRING = "0.0.1"
APPLICATION_NAME_STRING = "JSC print"


###############################################################################
# Module                                                                      #
###############################################################################

def parameters():
    """
    parameters
    :return:
    """
    parser = argparse.ArgumentParser(description=APPLICATION_NAME_STRING)
    parser.add_argument('-v', '--version', action='version', version=APPLICATION_NAME_STRING + " - " + VERSION_STRING)
    parser.add_argument('-i', '--in', type=argparse.FileType('r'), help='Input file path (JSC file)', required=True)
    parser.add_argument('-f', '--format', choices={'TEXT', 'HTML', 'JSON'}, help='The output format', required=False)
    logging_level_choices = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }
    parser.add_argument('-ll', '--logging_level', dest="loggingLevel", choices=logging_level_choices.keys(),
                        help='Output log level', required=False)
    args, _ = parser.parse_known_args()

    if vars(args)['loggingLevel'] is None:
        level = logging.CRITICAL
    else:
        level = logging_level_choices.get(vars(args)['loggingLevel'], logging.CRITICAL)
    logging.basicConfig(format='[%(asctime)s][%(levelname)-8s] [%(module)-20s] - %(message)s',
                        datefmt='%Y.%m.%d %H:%M.%S', level=level)

    return {'jsc_file': (vars(args)['in']).name, 'format': (vars(args)['format'])}


def main(argv=sys.argv):
    """
    main
    :param argv:
    """
    signal.signal(signal.SIGINT, handler)
    args = parameters()
    jsc_data = Jsc.get(args['jsc_file'])
    if jsc_data is not None:
        if args['format'] is not None and "HTML".lower() == args['format'].lower():
            jsc_data.print_html()
        elif args['format'] is not None and "JSON".lower() == args['format'].lower():
            json_extractor = JsonExtractor(jsc_data)
            if json_extractor is not None:
                json_extractor.extract_data_to_json()
                try:
                    json_string = json.dumps(json_extractor.get_json(), ensure_ascii=False)
                except json.JSONDecodeError as error:
                    json_string = None
                    logging.debug(error)
                if json_string is not None:
                    print(json_string)
        else:
            jsc_data.print()


def handler(signum, frame):
    """
    handler
    :param signum:
    :param frame:
    """
    sys.exit()


# Execute main function
if __name__ == '__main__':
    main()
    sys.exit()

###############################################################################
#                                End of file                                  #
###############################################################################
