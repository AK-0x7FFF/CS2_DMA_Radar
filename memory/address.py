from copy import copy
from functools import wraps
from logging import warning
from typing import Self, Optional, Dict, Any, Callable, Iterable

from memory.memory import VmmScatterMemoryRead
from memory.process import CS2
from utils.vec import Vec2, Vec3



class AddressCacheSystem:
    cache_system_enable: bool = True
    _cache: Dict[int, Dict[str, Any]] = dict()

    @staticmethod
    def address_caching_decorator(func: Callable) -> Callable[[Any], Any]:
        @wraps(func)
        def wrapper(address_object: "AddressMemoryRead", *args, **kwargs) -> Any:
            if not AddressCacheSystem.cache_system_enable:
                return func(address_object, *args, **kwargs)

            try:
                memory_type = func.__name__

                value: Optional[Any] = None
                if AddressCacheSystem._cache.get(address_object.address, None) is not None:
                    value = AddressCacheSystem._cache.get(address_object.address).get(memory_type, None)
                    # print("read cache: %s, %s" % (memory_type, address_object.address))

                if value is None:
                    value = func(address_object, *args, **kwargs)
                    AddressCacheSystem._cache.update({address_object.address: {memory_type: value}})
                    # print("wrote cache: %s, %s" % (memory_type, address_object.address))
            except Exception:
                value = func(address_object, *args, **kwargs)
                warning("Can't Cache Address: %s" % address_object.address)
            return value
        return wrapper

    @classmethod
    def clear_cache(cls, target_address: Optional[int] = None) -> None:
        if target_address is None: cls._cache.clear()
        else: cls._cache.pop(target_address)



class AddressMemoryRead(AddressCacheSystem):
    def __init__(self, address: int) -> None:
        self.address = address
        self._memory_reader = CS2.memory_read

    @AddressCacheSystem.address_caching_decorator
    def bool(self) -> Optional[bool]: return self._memory_reader.read_bool(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i8(self) -> Optional[int]: return self._memory_reader.read_i8(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u8(self) -> Optional[int]: return self._memory_reader.read_i8(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i16(self) -> Optional[int]: return self._memory_reader.read_i16(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u16(self) -> Optional[int]: return self._memory_reader.read_u16(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i32(self) -> Optional[int]: return self._memory_reader.read_i32(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u32(self) -> Optional[int]: return self._memory_reader.read_u32(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i64(self) -> Optional[int]: return self._memory_reader.read_i64(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u64(self) -> Optional[int]: return self._memory_reader.read_u64(self.address)

    @AddressCacheSystem.address_caching_decorator
    def float(self) -> Optional[float]: return self._memory_reader.read_f32(self.address)

    @AddressCacheSystem.address_caching_decorator
    def vec(self, size: int) -> Optional[Iterable[float]]: return self._memory_reader.read_vec(self.address, size)

    @AddressCacheSystem.address_caching_decorator
    def vec2(self) -> Optional[Vec2]: return Vec2(*self._memory_reader.read_vec(self.address, 2))

    @AddressCacheSystem.address_caching_decorator
    def vec3(self) -> Optional[Vec3]: return Vec3(*self._memory_reader.read_vec(self.address, 3))

    @AddressCacheSystem.address_caching_decorator
    def str(self, size: int) -> Optional[str]: return self._memory_reader.read_str(self.address, size)


class Address(AddressMemoryRead):
    def __init__(self, address: int, scatter_memory_read: VmmScatterMemoryRead | None = None) -> None:
        super().__init__(address)
        if scatter_memory_read is not None: self.set_scatter(scatter_memory_read)

    def __repr__(self) -> str:
        return "Address(%s / %s)" % (self.address, hex(self.address))

    def __eq__(self, other: int | Self) -> bool:
        if isinstance(other, int): return self.address == other
        if isinstance(other, Address): return self.address == other.address
        return False

    def __hash__(self) -> int:
        return hash((self.address, ))

    def __bool__(self) -> bool:
        return self.address != 0

    def offset(self, value: int) -> Self:
        self.address += value
        return self

    def pointer(self) -> Self:
        return Address(self.u64())

    def pointer_chain(self, *args: int) -> Self | None:
        address = self.copy()

        for offset_value in args:
            if not isinstance(offset_value, int):
                raise ValueError()

            address = address.offset(offset_value).pointer()
            if address.address is None: return Address(0)

        return address

    def set_scatter(self, scatter_memory_read: VmmScatterMemoryRead) -> Self:
        self._memory_reader = scatter_memory_read
        return self

    def copy(self) -> "Address":
        address = Address(self.address, self._memory_reader)
        return address
        # return Address(self.address)
        # return copy(self)



