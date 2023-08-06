# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."


###############################################################################
# Class                                                                       #
###############################################################################


class JscSection:
    """
    The JSC section data container.
    """
    SECTION_GLUE = "."
    GLOBAL_SECTION_NAME = "__GLOBAL__"

    def __init__(self, name=GLOBAL_SECTION_NAME):
        self.__section = list()
        self.__section.append(name)

    def __append(self, name):
        self.__section.append('"' + name + '"')

    def go_up(self, name):
        """
        Move level up for current section

        Parameters
        ----------
        name : string
            Section name
        """
        if len(self.__section) == 1 and JscSection.GLOBAL_SECTION_NAME in self.__section:
            self.__section = list()
        self.__append(name)

    def go_down(self):
        """
        Move level down for current section
        """
        if len(self.__section) == 1:
            self.__section = list()
            self.__section.append(JscSection.GLOBAL_SECTION_NAME)
        else:
            del self.__section[-1]

    def str(self):
        """
        Get JSC data section as string

        Returns
        -------
        string
            JSC data section as string.
        """
        if len(self.__section) == 1 and JscSection.GLOBAL_SECTION_NAME in self.__section:
            section_name = None
        else:
            section_name = JscSection.SECTION_GLUE.join(self.__section)
        return section_name

###############################################################################
#                                End of file                                  #
###############################################################################
