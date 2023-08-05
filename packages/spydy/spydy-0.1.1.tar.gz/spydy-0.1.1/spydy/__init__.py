from .urls import *
from .request import *
from .parsers import *
from .store import *


__version__ = "0.1.0"

LOGO = '''
  ____                     _
 / ___|  _ __   _   _   __| | _   _
 \___ \ | '_ \ | | | | / _` || | | |
  ___) || |_) || |_| || (_| || |_| |
 |____/ | .__/  \__, | \__,_| \__, |
        |_|     |___/         |___/   {!r}

'''.format(__version__)

print(LOGO)