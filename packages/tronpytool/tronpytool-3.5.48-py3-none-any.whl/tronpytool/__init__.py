#!/usr/bin/env python
# --------------------------------------------------------------------
# Copyright (c) iEXBase. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------

import pkg_resources
import sys
from eth_account import Account  # noqa: E402

# from tronpytool.compile.solwrap import SolcWrap
from .main import Tron  # noqa: E402
from .providers.simulateplayer import CoreSimulatePlayers
from .providers.http import HttpProvider  # noqa: E402

if sys.version_info < (3, 5):
    raise EnvironmentError("Python 3.5 or above is required")

__version__ = pkg_resources.get_distribution("tronpytool").version

__all__ = [
    '__version__',
    'HttpProvider',
    'Account',
    'CoreSimulatePlayers',
    'Tron'
    #  'SolcWrap'
]
