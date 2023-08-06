# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Apple(KaitaiStruct):

    class BleProtocol(Enum):
        handoff = 12
        nearby_info = 16

    class HandoffClipboardStatus(Enum):
        clipboard_empty = 0
        clipboard_full = 8
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.appledata = []
        i = 0
        while not self._io.is_eof():
            self.appledata.append(self._root.Continuity(self._io, self, self._root))
            i += 1


    class Continuity(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cont_type = self._root.BleProtocol(self._io.read_u1())
            self.cont_size = self._io.read_u1()
            _on = self.cont_type
            if _on == self._root.BleProtocol.handoff:
                self._raw_body = self._io.read_bytes(self.cont_size)
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.Handoff(io, self, self._root)
            elif _on == self._root.BleProtocol.nearby_info:
                self._raw_body = self._io.read_bytes(self.cont_size)
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.NearbyInfo(io, self, self._root)
            else:
                self._raw_body = self._io.read_bytes(self.cont_size)
                io = KaitaiStream(BytesIO(self._raw_body))
                self.body = self._root.NotImplemented(io, self, self._root)


    class Handoff(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.clipboard_status = self._root.HandoffClipboardStatus(self._io.read_u1())
            self.aes_iv = self._io.read_bytes(2)
            self.authenticated_data = self._io.read_bytes(1)
            self.encrypted_data = self._io.read_bytes((self._parent.cont_size - 4))


    class NearbyInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.status_flag = self._io.read_bits_int(4)
            self.action_code = self._io.read_bits_int(4)
            self._io.align_to_byte()
            self.wifi_state_flag = self._io.read_u1()
            self.auth_tag = self._io.read_bytes(3)
            self.unkown_data = self._io.read_bytes((self._parent.cont_size - 5))


    class NotImplemented(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            i = 0
            while not self._io.is_eof():
                self.data.append(self._io.read_bytes(1))
                i += 1




