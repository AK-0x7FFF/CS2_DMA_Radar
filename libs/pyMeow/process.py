from logging import error
from struct import unpack

from error import ProcessNotFoundError
from utils.memory_monitor import MemoryMonitor
from utils.vec import Vec2, Vec3
from .pyMeow import process_running, enum_modules, open_process, process_exists, pid_exists

from typing import Union, Generator, Any, Optional, Sequence

from .module import MeowModule
from .pyMeow import r_int8, r_int16, r_int, r_int64, r_uint16, r_uint, r_uint64, r_float, r_bool, r_bytes, r_string, r_floats
from .structure import StructMeowProcess








class MeowProcessMemoryRead:
    def __init__(self, process: StructMeowProcess):
        self._process = process

    # @staticmethod
    # def unpack_byte(byte: bytes, format_str: str) -> Optional[Any]:
    #     try:
    #         return unpack("<" + format_str, byte)[0]
    #     except Exception as error_reason:
    #         error("UnpackByteError: (byte: %s, format_str: %s, error: %s)" % (byte, "<" + format_str, error_reason))


    @MemoryMonitor.read_decorator(lambda _, __: 1)
    def i8(self, address: int) -> Optional[int]:
        return r_int8(self._process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 2)
    def i16(self, address: int) -> Optional[int]:
        return r_int16(self._process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 4)
    def i32(self, address: int) -> Optional[int]:
        return r_int(self._process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 8)
    def i64(self, address: int) -> Optional[int]:
        return r_int64(self._process, address)

    # def u8(self, address: int) -> Optional[int]:
    #     return r_uint8(self.process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 2)
    def u16(self, address: int) -> Optional[int]:
        return r_uint16(self._process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 4)
    def u32(self, address: int) -> Optional[int]:
        return r_uint(self._process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 8)
    def u64(self, address: int) -> Optional[int]:
        return r_uint64(self._process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 4)
    def f32(self, address: int) -> Optional[float]:
        return r_float(self._process, address)

    @MemoryMonitor.read_decorator(lambda _, __: 1)
    def bool(self, address: int) -> Optional[bool]:
        return r_bool(self._process, address)

    @MemoryMonitor.read_decorator(lambda args, kwargs: kwargs.get("size", 50))
    def bytes(self, address: int, size: int = 50) -> Optional[Any]:
        return r_bytes(self._process, address, size)

    @MemoryMonitor.read_decorator(lambda args, kwargs: kwargs.get("size", 50))
    def str(self, address: int, size: int = 50) -> Optional[str]:
        try: string = r_string(self._process, address, size)
        except Exception: return None
        if not isinstance(string, str): return None

        return string

    @MemoryMonitor.read_decorator(lambda args, kwargs: args[2] * 4)
    def vec(self, address: int, size: int) -> Optional[Sequence[float]]:
        return r_floats(self._process, address, size)

    def vec2(self, address: int) -> Optional[Vec2]:
        return Vec2(*self.vec(address, 2))

    def vec3(self, address: int) -> Optional[Vec3]:
        return Vec3(*self.vec(address, 3))



class MeowProcess:
    def __init__(self, process: Union[str, int, StructMeowProcess]) -> None:
        if isinstance(process, str):
            if not process_exists(process): raise ProcessNotFoundError()
            self.process = open_process(process)
        elif isinstance(process, int):
            if not pid_exists(process): raise ProcessNotFoundError()
            self.process = open_process(process)
        elif isinstance(process, StructMeowProcess):
            self.process = process
        else:
            raise ValueError()
        self.memory_read = MeowProcessMemoryRead(self.process)


    def __getitem__(self, item: str) -> Any:
        return self.process.get(item, None)

    def __repr__(self) -> str:
        return str(self.process)

    @property
    def name(self) -> str:
        return self.process.get("name")

    @property
    def pid(self) -> int:
        return self.process.get("pid")

    @property
    def handle(self) -> int:
        return self.process.get("handle")

    @property
    def running(self) -> bool:
        return process_running(self.process)

    def modules(self) -> Generator[MeowModule, None, None]:
        modules = enum_modules(self.process)
        for module_struct in modules:
            yield MeowModule(self.process, module_struct)

    # def get_memory_read_counter(self) -> int:
    #     count = self.read_counter
    #     self.read_counter = 0
    #
    #     return count