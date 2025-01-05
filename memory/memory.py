from abc import ABC, abstractmethod
from struct import unpack
from typing import Self

from memprocfs import FLAG_NOCACHE
from memprocfs.vmmpyc import VmmProcess

from libs.pyMeow import MeowProcess
from libs.pyMeow.pyMeow import r_bytes
from libs.pyMeow.structure import StructMeowProcess
from utils.memory_monitor import MemoryMonitor


class MemoryReadAbstract(ABC):
    _process: MeowProcess | VmmProcess


    @staticmethod
    def unpack_byte(byte: bytes, format_str: str) -> bool | int | float | bytes | str | None:
        if byte is None or not len(byte): return None

        try: return unpack("<" + format_str, byte)[0]
        except Exception: return None

    @classmethod
    @abstractmethod
    def set_process(cls, process: MeowProcess | VmmProcess) -> Self:
        ...

    @classmethod
    @abstractmethod
    def read_memory(cls, address: int, byte_size: int) -> bytes | None:
        ...

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 1)
    def read_bool(cls, address: int) -> bool | None:
        return cls.unpack_byte(cls.read_memory(address, 1), "?")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 1)
    def read_i8(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 1), "b")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 1)
    def read_u8(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 1), "B")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 2)
    def read_i16(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 2), "h")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 2)
    def read_u16(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 2), "H")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 4)
    def read_i32(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 4), "i")

    @classmethod
    @MemoryMonitor.read_decorator(lambda _, __: 4)
    def read_u32(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 4), "I")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 8)
    def read_i64(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 8), "q")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 8)
    def read_u64(cls, address: int) -> int | None:
        return cls.unpack_byte(cls.read_memory(address, 8), "Q")

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, __: 4)
    def read_f32(cls, address: int) -> float | None:
        return cls.unpack_byte(cls.read_memory(address, 4), "f")

    @classmethod
    def read_vec(cls, address: int, size: int) -> list[float] | None:
        byte = cls.read_memory(address, 4 * size)
        if byte is None or not len(byte): return None

        try: return list(unpack("<%if" % size, byte))
        except Exception: return None

    @classmethod
    # @MemoryMonitor.read_decorator(lambda _, kwargs: kwargs.get("byte_size", 50))
    def read_str(cls, address: int, byte_size: int = 50) -> str | None:
        byte = cls.read_memory(address, byte_size)
        if byte is None or not len(byte): return None

        try: return byte.split(b"\x00")[0].decode("utf-8")
        except Exception: return None



class MeowMemoryReadStruct(MemoryReadAbstract):
    _process: StructMeowProcess

    @classmethod
    def set_process(cls, process: MeowProcess) -> Self:
        cls._process = process.process
        return cls

    @classmethod
    @MemoryMonitor.read_decorator(lambda args, __: args[2])
    def read_memory(cls, address: int, byte_size: int) -> bytes | None:
        return r_bytes(cls._process, address, byte_size)


class VmmMemoryReadStruct(MemoryReadAbstract):
    _process: VmmProcess

    @classmethod
    def set_process(cls, process: VmmProcess) -> Self:
        cls._process = process
        return cls

    @classmethod
    @MemoryMonitor.read_decorator(lambda args, __: args[2])
    def read_memory(cls, address: int, byte_size: int) -> bytes | None:
        return cls._process.memory.read(address, byte_size, FLAG_NOCACHE)

