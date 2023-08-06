"""
taeg Python API
"""

import platform

from .check import logs
from .check.notebook import Notebook
from .version import __version__

# whether Taeg is running on Window
_WINDOWS = platform.system() == "Windows"
