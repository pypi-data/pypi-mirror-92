"""Pythonic EBUS Representation."""
import asyncio
import collections
import logging

from .connection import CommandError, Connection
from .const import OK
from .msg import BrokenMsg, filter_msg
from .msgdecoder import MsgDecoder, UnknownMsgError
from .msgdef import resolve_prio
from .msgdefdecoder import decode_msgdef
from .msgdefs import MsgDefs
from .util import repr_

_LOGGER = logging.getLogger(__name__)
_CMD_FINDMSGDEFS = "find -a -F type,circuit,name,fields"


class Ebus:

    """
    Pythonic EBUS Representation.

    This instance connects to an EBUSD instance and allows to read, write or monitor.
    """

    def __init__(self, host, port, timeout=10, scaninterval=10, scans=3, msgdefs=None):
        self.connection = Connection(host=host, port=port, autoconnect=True, timeout=timeout)
        self.scaninterval = scaninterval
        self.scans = scans
        self.msgdefcodes = []
        self.msgdecoder = MsgDecoder(msgdefs or MsgDefs())
        _LOGGER.info(f"{self}")

    def __repr__(self):
        return repr_(
            self,
            args=(self.connection.host, self.connection.port),
            kwargs=(
                ("timeout", self.timeout, 10),
                ("scaninterval", self.scaninterval, 10),
                ("scans", self.scans, 3),
            ),
        )

    @property
    def ident(self):
        """Ident."""
        return f"{self.host}:{self.port}"

    @property
    def host(self):
        """Host Name or IP."""
        return self.connection.host

    @property
    def port(self):
        """Port."""
        return self.connection.port

    @property
    def timeout(self):
        """Timeout."""
        return self.connection.timeout

    @property
    def msgdefs(self):
        """Message Defintions."""
        return self.msgdecoder.msgdefs

    @msgdefs.setter
    def msgdefs(self, msgdefs):
        self.msgdecoder.msgdefs = msgdefs

    def __copy__(self):
        return Ebus(
            self.host,
            self.port,
            timeout=self.timeout,
            scaninterval=self.scaninterval,
            scans=self.scans,
            msgdefs=self.msgdefs,
        )

    async def async_wait_scancompleted(self):
        """Wait until scan is completed."""
        cnts = []
        while True:
            await self.connection.async_request(_CMD_FINDMSGDEFS)
            cnt = sum([1 async for line in self.connection.async_read()])
            cnts.append(cnt)
            if len(cnts) < self.scans or not all(cnt == cnts[-1] for cnt in cnts[-self.scans : -1]):
                await asyncio.sleep(self.scaninterval)
            else:
                break

    async def async_load_msgdefs(self):
        """
        Load Message Definitions from EBUSD.

        Alias for `load_msgdefcodes` and `decode_msgdefcodes`.
        """
        await self.async_load_msgdefcodes()
        self.decode_msgdefcodes()

    async def async_load_msgdefcodes(self):
        """Load EBUS Message Definition Codes."""
        _LOGGER.info("load_msgdefcodes()")
        self.msgdefcodes = msgdefcodes = []
        await self.connection.async_request(_CMD_FINDMSGDEFS)
        async for line in self.connection.async_read():
            line = line.strip()
            if line:
                try:
                    msgdef = decode_msgdef(line)
                except ValueError as exc:
                    _LOGGER.warning(f"Cannot decode message definition '{line}' ({exc})")
                if not msgdef.circuit.startswith("scan"):
                    msgdefcodes.append(line)

    def decode_msgdefcodes(self):
        """Decode `msgdefcodes` and use as `msgdefs`."""
        _LOGGER.info("decode_msgdefcodes()")
        # Decode
        msgdefs = []
        for msgdefcode in self.msgdefcodes:
            try:
                msgdefs.append(decode_msgdef(msgdefcode))
            except ValueError as exc:
                _LOGGER.warning(f"Cannot decode message definition '{msgdefcode}' ({exc})")
        # Sort
        self.msgdefs.clear()
        for msgdef in sorted(msgdefs, key=lambda msgdef: (msgdef.circuit, msgdef.name)):
            self.msgdefs.add(msgdef)

    async def async_read(self, msgdef, ttl=None):
        """
        Read Message.

        Raises:
            ValueError: on decoder error
        """
        _LOGGER.info(f"read({msgdef!r}, ttl={ttl!r})")
        return await self._async_read(msgdef, ttl)

    async def async_write(self, msgdef, value, ttl=0):
        """Write Message."""
        _LOGGER.info(f"write({msgdef!r}, value={value!r}, ttl={ttl!r})")
        if not msgdef.write:
            raise ValueError(f"Message is not writeable '{msgdef}'")
        fullmsgdef = self.msgdefs.get(msgdef.circuit, msgdef.name)
        if fullmsgdef != msgdef:
            # Read
            if not msgdef.read:
                raise ValueError(f"Message is not read-modify-writable '{msgdef}'")
            await self.connection.async_request("read", msgdef.name, c=msgdef.circuit, m=ttl)
            line = await self.connection.async_readresp(check=False)
            values = line.split(";")
            # Modify
            for fielddef in msgdef.fields:
                encvalue = fielddef.type_.encode(value)
                values[fielddef.idx] = str(encvalue)
        else:
            values = [str(fielddef.type_.encode(value)) for fielddef in msgdef.fields]
        # Write
        await self.connection.async_request("write", msgdef.name, ";".join(values), c=msgdef.circuit)
        resp = await self.connection.async_readresp()
        if resp != "done":
            raise CommandError(resp)

    async def async_listen(self, msgdefs=None):
        """Listen to EBUSD, decode and yield."""
        _LOGGER.info(f"listen(msgdefs={msgdefs!r})")
        async for msg in self._async_listen(msgdefs):
            yield msg

    async def async_setprio(self, msgdef, setprio=None):
        """
        Read Message.

        Raises:
            ValueError: on decoder error
        """
        _LOGGER.info(f"async_setprio({msgdef!r}, setprio={setprio!r})")
        msgdef = msgdef.replace(setprio=resolve_prio(msgdef, setprio or msgdef.setprio))
        await self._async_read(msgdef)

    async def async_observe(self, msgdefs=None, ttl=None):
        """
        Observe.

        Observe `msgdefs` messages.
        """
        _LOGGER.info(f"observe(msgdefs={msgdefs!r}, ttl={ttl!r})")
        msgdefs = msgdefs or self.msgdefs
        data = collections.defaultdict(lambda: None)

        # read all
        for msgdef in msgdefs:
            if msgdef.read:
                msg = await self._async_read(msgdef, ttl=ttl)
                _LOGGER.debug("observe-read: {msg}")
                msg = filter_msg(msg, msgdefs)
                if msg:
                    if msg.valid:
                        data[msgdef.ident] = msg
                    yield msg
            elif msgdef.update:
                data[msgdef.ident] = None

        # find new values (which got updated while we where reading)
        await self.connection.async_request("find -d")
        async for line in self.connection.async_read(check=False):
            msg = self._decode_msg(line)
            _LOGGER.debug("observe-find: {msg}")
            msg = filter_msg(msg, msgdefs)
            if msg and msg != data[msg.msgdef.ident]:
                yield msg
                data[msg.msgdef.ident] = msg

        # listen
        async for msg in self._async_listen(msgdefs):
            _LOGGER.debug("observe-listen: {msg}")
            yield msg

    async def async_get_state(self):
        """Return state string."""
        _LOGGER.info("get_state()")
        return await self._async_get_state()

    async def _async_get_state(self):
        try:
            await self.connection.async_request("state")
            state = await self.connection.async_readresp()
            if state.startswith("signal acquired"):
                return OK
            else:
                return state
        except (ConnectionError, CommandError):
            return "no ebusd connection"

    async def async_is_online(self):
        """Return if we are online."""
        _LOGGER.info("is_online()")
        state = await self._async_get_state()
        return state == OK

    async def async_get_info(self):
        """Return info dict."""
        _LOGGER.info("get_info()")
        info = {}
        await self.connection.async_request("info")
        async for line in self.connection.async_read():
            name, value = line.split(":", 1)
            info[name.strip()] = value.strip()
        return info

    async def async_cmd(self, cmd, infinite=False, check=False):
        """Send `cmd` to EBUSD and Receive Response."""
        _LOGGER.info(f"cmd({cmd!r}, infinite={infinite!r}, check={check!r})")
        await self.connection.async_write(cmd)
        async for line in self.connection.async_read(infinite=infinite, check=check):
            yield line

    async def _async_read(self, msgdef, ttl=None):
        try:
            await self.connection.async_request("read", msgdef.name, c=msgdef.circuit, p=msgdef.setprio, m=ttl)
            line = await self.connection.async_readresp(check=False)
        except CommandError as exc:
            return BrokenMsg(msgdef, str(exc))
        else:
            return self.msgdecoder.decode_value(msgdef, line)

    async def _async_listen(self, msgdefs):
        await self.connection.async_request("listen")
        resp = await self.connection.async_readresp()
        if resp != "listen started":
            raise CommandError(f"Listen could not be started: {resp}")
        async for line in self.connection.async_read(check=False):
            msg = self._decode_msg(line)
            msg = filter_msg(msg, msgdefs)
            if msg:
                yield msg

    def _decode_msg(self, line):
        if line:
            try:
                return self.msgdecoder.decode_line(line)
            except UnknownMsgError:
                pass
            except ValueError as exc:
                _LOGGER.warning(f"Cannot decode message in {line!r}: {exc}")
        return None
