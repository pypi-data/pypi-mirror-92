"""
Pythonic Interface to EBUS Daemon (ebusd).

:class:`Ebus` represents one connection to a EBUSD instance.
"""
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

from . import types
from .circuitmap import CircuitMap  # noqa
from .connection import CommandError  # noqa
from .connection import Connection  # noqa
from .connection import EbusdShutdown  # noqa
from .const import AUTO  # noqa
from .const import NA  # noqa
from .const import OK  # noqa
from .ebus import Ebus  # noqa
from .icon import get_icon  # noqa
from .msg import BrokenMsg  # noqa
from .msg import Error  # noqa
from .msg import Field  # noqa
from .msg import Msg  # noqa
from .msgdecoder import MsgDecoder  # noqa
from .msgdecoder import UnknownMsgError  # noqa
from .msgdef import FieldDef  # noqa
from .msgdef import MsgDef  # noqa
from .msgdef import VirtFieldDef  # noqa
from .msgdef import resolve_prio  # noqa
from .msgdefdecoder import decode_msgdef  # noqa
from .msgdefs import MsgDefs  # noqa
