from typing import Iterable, Self, Generic

from game.offset.signatures.type_hint import SignaturesClientTypeHint, SignaturesEngine2TypeHint
from memory.pattern import Pattern


# class Signatures:
#     def __init__(self) -> None:
#         self._signatures = dict()
#
#     def __len__(self) -> int:
#         return len(self._signatures)
#
#     def __getitem__(self, item: str) -> Pattern | None:
#         if isinstance(item, str): return None
#         return self._signatures.get(item, None)
#
#     def add(self, signature_name: str, pattern: Pattern) -> Self:
#         self._signatures.update({
#             signature_name: pattern.to_address()
#         })
#         return self
#
#     def build(self) -> SignaturesClientTypeHint | SignaturesEngine2TypeHint:
#         signatures = type("signatures", (), self._signatures)()
#         return signatures


class Signatures(dict):
    def __init__(self):
        super().__init__()

    def add(self, signature_name: str, pattern: Pattern) -> Self:
        super().update({signature_name: pattern})
        return self

    def update_module_base(self, module_base: int) -> Self:
        self.update({
            signature_name: pattern.update_module_base(module_base)
            for signature_name, pattern in self.items()
        })

        return self

    def build(self) -> SignaturesClientTypeHint | SignaturesEngine2TypeHint:
        signatures = type("Signatures", (), {
            signature_name: pattern.to_address()
            for signature_name, pattern in self.items()
        })()
        return signatures


# if __name__ == '__main__':
    # Signatures_().update()