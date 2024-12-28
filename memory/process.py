from logging import info
from operator import itemgetter
from pickle import load, dump, HIGHEST_PROTOCOL
from time import time
from typing import Self, Generator

from memprocfs import Vmm
from memprocfs.vmmpyc import VmmProcess, VmmModule

from game.offset.schemas.type_hint import SchemasTypeHint
from game.offset.signatures.type_hint import SignaturesTypeHint
from error import ProcessModuleNotFoundError, ProcessNotFoundError, ProcessDoesNotSetupError, DeviceNotFoundError
from libs.pyMeow import MeowModule, MeowProcess
from libs.pyMeow.pyMeow import open_process, process_exists, module_exists
from memory.memory import MemoryReadAbstract, MeowMemoryReadStruct, VmmMemoryReadStruct
from memory.module import ModuleAbstract, MeowModuleStruct, VmmModuleStruct


class CS2MeowMode:
    PROCESS_NAME: str

    process:     MeowProcess | None
    memory_read: MeowMemoryReadStruct | None

    client:       MeowModuleStruct | None
    engine2:      MeowModuleStruct | None
    schemasystem: MeowModuleStruct | None
    tier0:        MeowModuleStruct | None

    @classmethod
    def is_process_exist(cls) -> bool:
        return process_exists(cls.PROCESS_NAME)

    @classmethod
    def is_process_ready(cls) -> bool:
        cs2_process = open_process(cls.PROCESS_NAME)
        return all(
            module_exists(cs2_process, module_name)
            for module_name in (
                "client.dll",
                "engine2.dll",
                "inputsystem.dll",
                "matchmaking.dll",
                "schemasystem.dll",
                "tier0.dll"
            )
        )


    @classmethod
    def setup(cls):
        if not cls.is_process_exist():
            raise ProcessNotFoundError()

        try:
            cls.process: MeowProcess = MeowProcess(cls.PROCESS_NAME)
        except Exception:
            raise ProcessNotFoundError()
        else:
            info("Success Found %s Process: pid->%s" % (cls.PROCESS_NAME, cls.process.pid))

        # get modules
        try:
            modules: Generator[MeowModule, None, None] = cls.process.modules()
            CS2.client, CS2.engine2, CS2.schemasystem, CS2.tier0 = itemgetter(
                "client.dll",
                "engine2.dll",
                "schemasystem.dll",
                "tier0.dll",
            )({
                module.name: MeowModuleStruct(module)
                for module in modules
            })
        except Exception: raise ProcessModuleNotFoundError()
        else: info("Success Found Modules: " + ", ".join([
            "%s->%s" % (module.name, module.base)
            for module in (
                cls.client,
                cls.engine2,
                cls.schemasystem,
                cls.tier0,
            )]))

        cls.memory_read = MeowMemoryReadStruct.set_process(cls.process)
        return cls



class CS2VmmMode:
    PROCESS_NAME: str

    vmm_device:  Vmm                 | None
    process:     VmmProcess          | None
    memory_read: VmmMemoryReadStruct | None

    client:       VmmModuleStruct | None
    engine2:      VmmModuleStruct | None
    schemasystem: VmmModuleStruct | None
    tier0:        VmmModuleStruct | None

    @classmethod
    def is_process_exist(cls) -> bool:
        return any(process.name == cls.PROCESS_NAME for process in cls.vmm_device.process_list())

    @classmethod
    def is_process_ready(cls) -> bool:
        cs2_process: VmmProcess = cls.vmm_device.process(cls.PROCESS_NAME)
        modules: list[VmmModule] = [module.name for module in cs2_process.module_list()]

        return all(
            module_name in modules
            for module_name in (
                "client.dll",
                "engine2.dll",
                "inputsystem.dll",
                "matchmaking.dll",
                "schemasystem.dll",
                "tier0.dll"
            )
        )

    @classmethod
    def setup(cls):
        if not cls.is_process_exist():
            raise ProcessNotFoundError()

        try: cls.process: VmmProcess = cls.vmm_device.process(cls.PROCESS_NAME)
        except Exception: raise ProcessNotFoundError()
        else: info("Success Found %s Process: pid->%s" % (cls.PROCESS_NAME, cls.process.pid))

        # get modules
        try:
            modules: Generator[VmmModule, None, None] = cls.process.module_list()
            cls.client, cls.engine2, cls.schemasystem, cls.tier0 = itemgetter(
                "client.dll",
                "engine2.dll",
                "schemasystem.dll",
                "tier0.dll",
            )({
                module.name: VmmModuleStruct(module)
                for module in modules
            })
        except Exception:
            raise ProcessModuleNotFoundError()
        else:
            info("Success Found Modules: " + ", ".join([
                "%s->%s" % (module.name, module.base)
                for module in (
                    cls.client,
                    cls.engine2,
                    cls.schemasystem,
                    cls.tier0,
                )]))

        cls.memory_read = VmmMemoryReadStruct.set_process(cls.process)
        info("Found %s🎉" % (cls.PROCESS_NAME, ))
        return cls




class CS2(CS2MeowMode, CS2VmmMode):
    PROCESS_NAME = "cs2.exe"
    WINDOW_NAME = "Counter-Strike 2"

    vmm_device:  Vmm | None = None
    process:     MeowProcess | VmmProcess | None = None
    memory_read: MemoryReadAbstract | None = None

    client:       ModuleAbstract | None = None
    engine2:      ModuleAbstract | None = None
    schemasystem: ModuleAbstract | None = None
    tier0:        ModuleAbstract | None = None

    signatures: SignaturesTypeHint | None = None
    schemas:    SchemasTypeHint    | None = None


    @classmethod
    def meow_mode(cls) -> Self:
        if cls.vmm_device is not None:
            cls.vmm_device.close()
            cls.vmm_device = None

        for func_name in (
            "is_process_exist",
            "is_process_ready",
            "setup",
        ):
            # idea from https://blog.csdn.net/Gscsd_T/article/details/79092704
            setattr(
                cls, func_name,
                getattr(super(cls, cls), func_name)
            )

        info("toggle to 🐱[Meow Mode]!")
        return cls


    @classmethod
    def vmm_mode(cls) -> Self:
        try:
            cls.vmm_device: Vmm = Vmm([
                '-device', 'fpga',
                '-disable-python', '-disable-symbols', '-disable-symbolserver', '-disable-yara',
                '-disable-yara-builtin',
                '-debug-pte-quality-threshold', '64'
            ])
        except Exception: raise DeviceNotFoundError()

        for func_name in (
                "is_process_exist",
                "is_process_ready",
                "setup",
        ):
            # idea from https://blog.csdn.net/Gscsd_T/article/details/79092704
            # and https://csruiliu.github.io/blog/20211021-python-multi-inheritance/
            setattr(
                cls, func_name,
                getattr(super(cls.__bases__[0], cls), func_name)
            )

        info("toggle to 👾[DMA Mode]!")
        return cls


    @classmethod
    def is_process_exist(cls) -> bool:
        ...

    @classmethod
    def is_process_ready(cls) -> bool:
        ...

    @classmethod
    def setup(cls) -> Self:
        ...

    @classmethod
    def is_setup(cls) -> bool:
        return None not in (
            cls.process,
            cls.memory_read
        )

    @classmethod
    def dump_offset(cls) -> Self:
        if not cls.is_setup(): raise ProcessDoesNotSetupError()

        from game.offset.signatures.dump import dump_signatures
        cls.signatures = dump_signatures()
        info("Success Dumped Signatures! 🔥🔥🔥")

        from game.offset.schemas.dump import dump_schemas
        cls.schemas = dump_schemas()
        info("Success Dumped Schemas! 🔥🔥🔥")

        # from game.offset.convars.dump import dump_convars
        # cls.convars = dump_convars()
        # # print(cls.convars)
        # info("Success Dumped Convars")

        return cls

    @classmethod
    def dump_offset_snapshot(cls, file_name: str) -> Self:
        from game.offset.signatures.client import dump_client_signatures
        from game.offset.signatures.engine2 import dump_engine2_signatures
        from game.offset.schemas.dump import dump_schemas

        signatures = dict(
            client_dll=dump_client_signatures(),
            engine2_dll=dump_engine2_signatures()
        )
        schemas = dump_schemas(False)

        pkl_data = dict(
            t=time(),
            signatures=signatures,
            schemas=schemas,
        )

        dump(pkl_data, open(file_name, "wb"), protocol=HIGHEST_PROTOCOL)
        return cls

    @classmethod
    def load_offset_snapshot(cls, file_name: str) -> Self:
        data = load(open(file_name, "rb"))

        signatures = type("Signatures", (SignaturesTypeHint,), dict(
            client=data.get("signatures").get("client_dll").update_module_base(CS2.client.base).build(),
            engine2=data.get("signatures").get("engine2_dll").update_module_base(CS2.engine2.base).build()
        ))()

        def dict_2_class(arg: dict[str, int | dict]):
            return type("Schemas", (SchemasTypeHint,), {
                key: dict_2_class(value) if isinstance(value, dict) else value
                for key, value in arg.items()
            })()

        schemas = dict_2_class(data.get("schemas"))

        cls.signatures = signatures
        cls.schemas = schemas

        info("Success Load Snapshot! 🔥🔥🔥")
        return cls

    # @classmethod
    # def update_offset(cls, debug_pkl: str | None = None) -> Self:
    #     if debug_pkl is None:
    #         from game.offset.signatures.dump import dump_signatures
    #         cls.signatures = dump_signatures()
    #
    #         from game.offset.schemas.dump import dump_schemas
    #         cls.schemas = dump_schemas(("client.dll", ))
    #     else:
    #         cls.signatures, cls.schemas = load(open(debug_pkl, "rb"))
    #         debug("loaded offset from %s" % debug_pkl)
    #
    #     return cls

    # @classmethod
    # def export_offset_debug_pkl(cls) -> Self:
    #     from game.offset.signatures.dump import dump_signatures
    #     from game.offset.schemas.dump import dump_schemas
    #
    #     pkl_data = (
    #         dump_signatures(),
    #         dump_schemas(("client.dll",))
    #     )
    #
    #     dump(pkl_data, open("offset_dumps_snapshot.pkl", "wb"), protocol=HIGHEST_PROTOCOL)
    #     return cls




def main():
    print(CS2.meow_mode().is_process_ready())

if __name__ == '__main__':
    main()