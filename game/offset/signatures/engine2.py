from game.offset.signatures.struct import Signatures
from game.offset.signatures.type_hint import SignaturesEngine2TypeHint
from memory.pattern import Pattern
from memory.process import CS2


def dump_engine2_signatures() -> Signatures:
    module_buffer = CS2.memory_read.read_memory(CS2.engine2.base, CS2.engine2.size)
    return (
        Signatures()
        .add(
            "dwBuildNumber",
            Pattern("89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? FF 15 ?? ?? ?? ??", CS2.engine2.base, module_buffer)
            .aob_scan()
            .rip(2, 6)
        )
        .add(
            "dwNetworkGameClient",
            Pattern("48 89 3D ?? ?? ?? ?? 48 8D 15", CS2.engine2.base, module_buffer)
            .aob_scan()
            .rip()
        )
        .add(
            "dwNetworkGameClient_signOnState",
            Pattern("44 8B 81 ?? ?? ?? ?? 48 8D 0D", CS2.engine2.base, module_buffer)
            .aob_scan()
            .slice(3, 5)
        )
    )


# def dwBuildNumber(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? FF 15 ?? ?? ?? ??", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .rip(2, 6)
#     )
#
# def dwNetworkGameClient(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 3D ?? ?? ?? ?? 48 8D 15", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwNetworkGameClient_clientTickCount(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 83 B9", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .slice(2, 4)
#     )
#
# def dwNetworkGameClient_deltaTick(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("89 83 ?? ?? ?? ?? 8B 41", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .slice(2, 4)
#     )
#
# def dwNetworkGameClient_isBackgroundMap(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("0F B6 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 0F B6 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 48 89 5C 24", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .slice(3, 6)
#     )
#
# def dwNetworkGameClient_localPlayer(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 83 C0 ?? 48 8D 04 40 8B 0C C1", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .slice(3, 4)
#         .add(230)
#     )
#
# def dwNetworkGameClient_maxClients(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 8B 81 ?? ?? ?? ?? FF C0", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .slice(2, 4)
#     )
#
# def dwNetworkGameClient_serverTickCount(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 83 B9", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .slice(2, 4)
#     )
#
# def dwNetworkGameClient_signOnState(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("44 8B 81 ?? ?? ?? ?? 48 8D 0D", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .slice(3, 5)
#     )
#
# def dwWindowHeight(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("8B 05 ?? ?? ?? ?? 89 03", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .rip(2, 6)
#     )
#
# def dwWindowWidth(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("8B 05 ?? ?? ?? ?? 89 07", CS2.engine2.base, module_buffer)
#         .aob_scan()
#         .rip(2, 6)
#     )

# def dwSoundService(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 05 ?? ?? ?? ?? 4C 8D 44 24 ?? 48 8D 05", CS2.engine2.base, module_buffer)
#         .search()
#         .rip()
#     )
#
# def dwEngineViewData(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 05 ?? ?? ?? ?? 4C 8D 44 24 ?? 48 8D 05", CS2.engine2.base, module_buffer)
#         .search()
#         .rip()
#         .add(156)
#     )