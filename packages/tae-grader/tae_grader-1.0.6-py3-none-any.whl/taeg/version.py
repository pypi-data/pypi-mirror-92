"""
TAE-Grader version and printable logo
"""

import sys

from textwrap import dedent

__version__ = "1.0.6"

LOGO_WITH_VERSION = fr"""
________________  ___________   ________ 
\__    ___/  _  \ \_   _____/  /  _____/ 
  |    | /  /_\  \ |    __)_  /   \  ___ 
  |    |/    |    \|        \ \    \_\  \
  |____|\____|__  /_______  /  \______  /
                \/        \/          \/ 
                                                v{__version__}
"""

def print_version_info(logo=False):
    if logo:
        print(LOGO_WITH_VERSION + "\n")
    print(dedent(f"""\
        Python version: {".".join(str(v) for v in sys.version_info[:3])}
        TAE-Grader version: {__version__}
    """))
