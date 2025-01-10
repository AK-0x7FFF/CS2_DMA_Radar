from abc import ABC, abstractmethod
from struct import unpack
from typing import Self

from memprocfs import FLAG_NOCACHE, FLAG_NOCACHEPUT
from memprocfs.vmmpyc import VmmProcess, VmmScatterMemory

from libs.pyMeow import MeowProcess
from libs.pyMeow.pyMeow import r_bytes
from libs.pyMeow.structure import StructMeowProcess
from utils.memory_monitor import MemoryMonitor


class MemoryReadAbstract(ABC):
    @staticmethod
    def unpack_byte(byte: bytes, format_str: str) -> bool | int | float | bytes | str | None:
        if byte is None or not len(byte): return None

        try: return unpack("<" + format_str, byte)[0]
        except Exception: return None

    @abstractmethod
    def read_memory(self, address: int, byte_size: int) -> bytes | None:
        ...

    # @MemoryMonitor.read_decorator(lambda _, __: 1)
    def read_bool(self, address: int) -> bool | None:
        return self.unpack_byte(self.read_memory(address, 1), "?")

    # @MemoryMonitor.read_decorator(lambda _, __: 1)
    def read_i8(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 1), "b")

    # @MemoryMonitor.read_decorator(lambda _, __: 1)
    def read_u8(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 1), "B")

    # @MemoryMonitor.read_decorator(lambda _, __: 2)
    def read_i16(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 2), "h")

    # @MemoryMonitor.read_decorator(lambda _, __: 2)
    def read_u16(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 2), "H")

    # @MemoryMonitor.read_decorator(lambda _, __: 4)
    def read_i32(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 4), "i")

    @MemoryMonitor.read_decorator(lambda _, __: 4)
    def read_u32(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 4), "I")

    # @MemoryMonitor.read_decorator(lambda _, __: 8)
    def read_i64(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 8), "q")

    # @MemoryMonitor.read_decorator(lambda _, __: 8)
    def read_u64(self, address: int) -> int | None:
        return self.unpack_byte(self.read_memory(address, 8), "Q")

    # @MemoryMonitor.read_decorator(lambda _, __: 4)
    def read_f32(self, address: int) -> float | None:
        return self.unpack_byte(self.read_memory(address, 4), "f")

    def read_vec(self, address: int, size: int) -> list[float] | None:
        byte = self.read_memory(address, 4 * size)
        if byte is None or not len(byte): return None

        try: return list(unpack("<%if" % size, byte))
        except Exception: return None

    # @MemoryMonitor.read_decorator(lambda _, kwargs: kwargs.get("byte_size", 50))
    def read_str(self, address: int, byte_size: int = 50) -> str | None:
        byte = self.read_memory(address, byte_size)
        if byte is None or not len(byte): return None

        try: return byte.split(b"\x00")[0].decode("utf-8")
        except Exception: return None



class MeowMemoryReadStruct(MemoryReadAbstract):
    def __init__(self, process: MeowProcess) -> None:
        self.process = process.process

    @MemoryMonitor.read_decorator(lambda args, __: args[2])
    def read_memory(self, address: int, byte_size: int) -> bytes | None:
        return r_bytes(self.process, address, byte_size)


class VmmMemoryReadStruct(MemoryReadAbstract):
    def __init__(self, process: VmmProcess) -> None:
        self.process = process

    @MemoryMonitor.read_decorator(lambda args, __: args[2])
    def read_memory(self, address: int, byte_size: int) -> bytes | None:
        return self.process.memory.read(address, byte_size, FLAG_NOCACHE | FLAG_NOCACHEPUT)


class VmmScatterMemoryRead(MemoryReadAbstract):
    def __init__(self, scatter: VmmScatterMemory) -> None:
        self.scatter = scatter

    @MemoryMonitor.read_decorator(lambda args, __: args[2])
    def read_memory(self, address: int, byte_size: int) -> bytes | None:
        return self.scatter.read(address, byte_size)

