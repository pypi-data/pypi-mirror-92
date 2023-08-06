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
import os
import os.path
from string import Template

import jsonsimpleconfig


###############################################################################
# Class                                                                       #
###############################################################################

class JscHeader:

    def __init__(self, options={'defaultHeader': True,
                                'allowCustomHeader': False,
                                'customHeaderFilePath': '/etc/jsonsimpleconfig/header.template'}):
        self.__options = options

    def __header_template(self, file_path) -> Template:
        header = None
        try:
            if os.path.isfile(file_path):
                filein = open(file_path)
                if filein:
                    jsc_template_file = Template(filein.read())
                    if self.__options.get('headerTemplateData'):
                        header = jsc_template_file.substitute(self.__options.get('headerTemplateData'))
        except OSError as error:
            logging.debug(error)
        return header

    def str(self) -> str:
        header = file_path = None

        if self.__options.get('allowCustomHeader') and \
                ("customHeaderFilePath" in self.__options) and \
                os.path.isfile(self.__options.get('customHeaderFilePath')):
            file_path = self.__options.get('customHeaderFilePath')

        elif self.__options.get('defaultHeader'):
            path = os.path.abspath(jsonsimpleconfig.__file__)
            path = os.path.dirname(path)
            file_path = os.path.join(path, 'jscresources/defaultHeader.template')

        if file_path is not None:
            header = self.__header_template(file_path)

        return header

###############################################################################
#                                End of file                                  #
###############################################################################
