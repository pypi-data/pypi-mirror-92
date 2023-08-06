# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

###############################################################################
# Import(s)                                                                   #
###############################################################################

import datetime


###############################################################################
# Class                                                                       #
###############################################################################

class JscCommon:
    """
    The class for all misc tools.
    """

    @staticmethod
    def get_timestamp(time=True, seconds=False, microseconds=False, utc=False):
        """
        Get timestamp with predefined format.

        Parameters
        ----------
        time : bool
            Show time with date
        seconds : bool
            Show seconds
        microseconds : bool
            Show microseconds
        utc : bool
            Use UTC format

        Returns
        -------
        string
            Timestamp with required format.

        """

        if utc:
            today_date = datetime.datetime.utcnow()
        else:
            today_date = datetime.datetime.now()
        timestamp = (
            str("%04d" % today_date.year) + "-"
            "" + str("%02d" % today_date.month) + "-"
            "" + str("%02d" % today_date.day))
        if time:
            timestamp += (
                " " + str("%02d" % today_date.hour) + ":" + str("%02d" % today_date.minute))
            if seconds:
                timestamp += ("." + str("%02d" % today_date.second))
                if microseconds:
                    timestamp += ("." + str("%06d" % today_date.microsecond))
        return timestamp

###############################################################################
#                                End of file                                  #
###############################################################################
