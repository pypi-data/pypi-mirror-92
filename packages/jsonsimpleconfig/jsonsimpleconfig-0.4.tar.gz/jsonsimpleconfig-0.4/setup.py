# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2020 by xmz                                           *
# * ********************************************************************* *
"""
JSON Simple Config Setup
"""
__author__ = "Marcin Zelek"
__email__ = "marcin.zelek@gmail.com"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."
__license__ = "MIT"
__version__ = "0.4"

###############################################################################
# Import(s)                                                                   #
###############################################################################

import os

from setuptools import setup

###############################################################################
# Module                                                                      #
###############################################################################

DESCRIPTION = 'The simple idea to prepare configuration for your application.'


def read(fname):
    """test"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


try:
    LONG_DESCRIPTION = read('README.rst')
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name='jsonsimpleconfig',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords="json configuration jsc simple config",
    author=__author__,
    author_email=__email__,
    license=__license__,
    url='https://github.com/xmzxmz/jsonsimpleconfig',
    package_data={'': ['jscresources/*.template']},
    include_package_data=True,
    packages=['jsonsimpleconfig',
              'jsonsimpleconfig.jsccommon',
              'jsonsimpleconfig.jscdata',
              'jsonsimpleconfig.jscextractor',
              'jsonsimpleconfig.jschelper',
              'jsonsimpleconfig.jscparser'],
    entry_points={
        'console_scripts':
            [
                'json2jsc = jsonsimpleconfig.json2jsc:main',
                'jsc2json = jsonsimpleconfig.jsc2json:main',
                'jsc_value = jsonsimpleconfig.jsc_value:main',
                'jsc_print = jsonsimpleconfig.jsc_print:main',
                'jscValue = jsonsimpleconfig.jsc_value:main',
                'jscPrint = jsonsimpleconfig.jsc_print:main',
            ],
    },
    zip_safe=False
)

###############################################################################
#                                End of file                                  #
###############################################################################
