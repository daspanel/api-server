# -*- coding: utf-8 -*-
"""
apiserver
~~~~~~~~~~~~~~~~~~~

Contains all the code you need for an DASPANEL API server.

:copyright: (c) 2016 by Abner G Jacobsen
:licence: GPL-3, see LICENCE for more details
"""
from __future__ import absolute_import, unicode_literals
import logging

# Generate your own AsciiArt at:
# patorjk.com/software/taag/#f=Calvin%20S&t=Daspanel API
__banner__ = r"""
╔╦╗┌─┐┌─┐┌─┐┌─┐┌┐┌┌─┐┬    ╔═╗╔═╗╦
 ║║├─┤└─┐├─┘├─┤│││├┤ │    ╠═╣╠═╝║
═╩╝┴ ┴└─┘┴  ┴ ┴┘└┘└─┘┴─┘  ╩ ╩╩  ╩  by Abner G Jacobsen
"""

__title__ = 'apiserver'
__summary__ = 'Contains all the code you need for an DASPANEL API server.'
__uri__ = 'https://github.com/daspanel/apiserver'

__version__ = '0.0.1'

__author__ = 'Abner G Jacobsen'
__email__ = 'abner@apoana.com.br'

__license__ = 'GPL-3.0'
__copyright__ = 'Copyright 2016 Abner G Jacobsen'

# the user should dictate what happens when a logging event occurs
logging.getLogger(__name__).addHandler(logging.NullHandler())
