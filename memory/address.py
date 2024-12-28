from functools import wraps
from logging import warning
from typing import Self, Optional, Dict, Any, Callable, Iterable

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

    @AddressCacheSystem.address_caching_decorator
    def bool(self) -> Optional[bool]: return CS2.memory_read.read_bool(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i8(self) -> Optional[int]: return CS2.memory_read.read_i8(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u8(self) -> Optional[int]: return CS2.memory_read.read_i8(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i16(self) -> Optional[int]: return CS2.memory_read.read_i16(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u16(self) -> Optional[int]: return CS2.memory_read.read_u16(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i32(self) -> Optional[int]: return CS2.memory_read.read_i32(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u32(self) -> Optional[int]: return CS2.memory_read.read_u32(self.address)

    @AddressCacheSystem.address_caching_decorator
    def i64(self) -> Optional[int]: return CS2.memory_read.read_i64(self.address)

    @AddressCacheSystem.address_caching_decorator
    def u64(self) -> Optional[int]: return CS2.memory_read.read_u64(self.address)

    @AddressCacheSystem.address_caching_decorator
    def float(self) -> Optional[float]: return CS2.memory_read.read_f32(self.address)

    @AddressCacheSystem.address_caching_decorator
    def vec(self, size: int) -> Optional[Iterable[float]]: return CS2.memory_read.read_vec(self.address, size)

    @AddressCacheSystem.address_caching_decorator
    def vec2(self) -> Optional[Vec2]: return Vec2(*CS2.memory_read.read_vec(self.address, 2))

    @AddressCacheSystem.address_caching_decorator
    def vec3(self) -> Optional[Vec3]: return Vec3(*CS2.memory_read.read_vec(self.address, 3))

    def str(self, size: int) -> Optional[str]: return CS2.memory_read.read_str(self.address, size)


class Address(AddressMemoryRead):
    def __init__(self, address: int) -> None:
        super().__init__(address)

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

    def copy(self) -> "Address":
        return Address(self.address)



