import platform

from pylambdalib.elements import *
from pylambdalib.element_objects import *
if platform.system() == "Linux":
    from pylambdalib.utils import get_connection