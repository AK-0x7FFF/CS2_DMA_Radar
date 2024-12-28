from re import search
from typing import Self

from error import PatternConvertError
from memory.address import Address
from memory.process import CS2


# class Pattern:
#     def __init__(self, pattern: str, module: Union[str, Module]):
#         self.pattern = pattern
#
#         self.module: Module
#         if isinstance(module, str): self.module = {module.name: module for module in CS2.modules()}.get(module)
#         else: self.module = module
#
#         self._address = None
#
#     @property
#     def address(self) -> int:
#         return self._address
#
#     @property
#     def offset(self) -> int:
#         offset = self._address - self.module.base * (self._address // self.module.base)
#
#         return offset
#
#     def toAddress(self) -> Address:
#         return Address(self._address)
#
#     def search_meow(self, *args, **kwargs) -> Self:
#         self._address = aob_scan_module(CS2.process, self.module.name, self.pattern)[0]
#         return self
#
#     def search_py(self, *args, module_buffer: bytes = None, **kwargs) -> Self:
#         if module_buffer is None:
#             module_buffer = self.module.buffer
#
#         pattern_buffer = rb"".join([
#             rb"." if "?" in hex_byte else rb"\x%s" % hex_byte.encode("utf-8")
#             for hex_byte in self.pattern.split(" ")
#         ])
#
#         match_offset = search(pattern_buffer, module_buffer).start()
#         address = self.module.base + match_offset
#
#         self._address = address
#         return self
#
#     def search(self, *args, **kwargs) -> Self:
#         try: return self.search_py(*args, **kwargs)
#         except Exception:
#             print("meow mode:", self.pattern)
#             print(self.search_meow(*args, **kwargs).address)
#             return self.search_meow(*args, **kwargs)
#
#
#     def add(self, value: int) -> Self:
#         self._address += value
#         return self
#
#     def rip(self, offset: int = 3, length: int = 7) -> Self:
#         self._address = self._address + CS2.i32(self._address + offset) + length
#         return self
#
#     def slice(self, start: int, end: int) -> Self:
#         address = CS2.bytes(self._address + start, end - start)
#         self._address = int.from_bytes(address, byteorder="little")
#         return self


class Pattern:
    def __init__(self, pattern: str, module_base: int, module_buffer: bytes):
        self.pattern = pattern

        self._module_base = module_base
        self._module_buffer = module_buffer

        self._pattern_offset: int | None = None

    def __repr__(self) -> str:
        return "Pattern(\"%s\", %s)" % (self.pattern, hex(self.address))

    @property
    def address(self) -> int:
        return self._module_base + self._pattern_offset

    def to_address(self) -> Address:
        return Address(self._module_base + self._pattern_offset)

    @property
    def offset(self) -> int:
        return self._pattern_offset

    @staticmethod
    def pattern_str_to_regex_bytes(pattern: str) -> bytes:
        return rb"".join([
            rb"[\s\S]{1}" if "?" in hex_byte else rb"\x" + hex_byte.encode("utf-8")
            for hex_byte in pattern.split(" ")
        ])

    def aob_scan(self, auto_trans_2_regex: bool = True) -> Self:
        try:
            if auto_trans_2_regex: pattern_match_bytes = self.pattern_str_to_regex_bytes(self.pattern)
            else: pattern_match_bytes = self.pattern
            match_offset = search(pattern_match_bytes, self._module_buffer)

            if match_offset is None: raise PatternConvertError(self.pattern, pattern_match_bytes)
            self._pattern_offset = match_offset.start()
            return self

        except PatternConvertError as error: raise error
        except Exception as error_reason: raise PatternConvertError(self.pattern, error_reason)


    def pattern_bytes(self, offset: int, size: int) -> bytes:
        return self._module_buffer[self._pattern_offset + offset:self._pattern_offset + offset + size]


    def add(self, value: int) -> Self:
        self._pattern_offset += value
        return self

    def rip(self, offset: int = 3, length: int = 7) -> Self:
        self._pattern_offset = self._pattern_offset + CS2.memory_read.unpack_byte(self.pattern_bytes(offset, 4), "I") + length
        return self

    def slice(self, start: int, end: int) -> Self:
        byte = self.pattern_bytes(start, end - start)
        self._pattern_offset = int.from_bytes(byte, "little")

        return self

    def update_module_base(self, module_base: int) -> Self:
        self._module_base = module_base
        return self