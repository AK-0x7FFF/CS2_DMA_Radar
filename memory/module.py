from abc import ABC, abstractmethod

from memprocfs.vmmpyc import VmmModule

from libs.pyMeow import MeowModule



class ModuleAbstract(ABC):
    _module = MeowModule | VmmModule

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def base(self) -> int: ...

    @property
    @abstractmethod
    def size(self) -> int: ...


class MeowModuleStruct(ModuleAbstract):
    def __init__(self, module: MeowModule):
        self._module: MeowModule = module

    @property
    def name(self) -> str:
        return self._module.name

    @property
    def base(self) -> int:
        return self._module.base

    @property
    def size(self) -> int:
        return self._module.size


class VmmModuleStruct(ModuleAbstract):
    def __init__(self, module: VmmModule):
        self._module: VmmModule = module

    @property
    def name(self) -> str:
        return self._module.name

    @property
    def base(self) -> int:
        return self._module.base

    @property
    def size(self) -> int:
        return self._module.image_size


