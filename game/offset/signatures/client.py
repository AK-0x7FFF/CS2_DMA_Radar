from game.offset.signatures.struct import Signatures
from game.offset.signatures.type_hint import SignaturesClientTypeHint
from memory.pattern import Pattern
from memory.process import CS2


def dump_client_signatures() -> Signatures:
    module_buffer = CS2.memory_read.read_memory(CS2.client.base, CS2.client.size)
    return (
        Signatures()
        .add(
            "dwEntityList",
            Pattern("48 89 35 ?? ?? ?? ?? 48 85 F6", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
        )
        .add(
            "dwGameEntitySystem_getHighestEntityIndex",
            Pattern("8B 81 ?? ?? ?? ?? 89 02 48 8B C2 C3 CC CC CC CC 48 89 5C 24 ?? 48 89 6C 24", CS2.client.base, module_buffer)
            .aob_scan()
            .slice(2, 4)
        )
        .add(
            "dwGameRules",
            Pattern("48 89 1D ?? ?? ?? ?? FF 15 ?? ?? ?? ?? 84 C0", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
        )
        .add(
            "dwGlobalVars",
            Pattern("48 89 15 ?? ?? ?? ?? 48 89 42", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
        )
        .add(
            "dwLocalPlayerController",
            Pattern("48 89 05 ?? ?? ?? ?? 8B 9E", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
        )
        .add(
            "dwLocalPlayerPawn",
            Pattern("48 8D 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 48 83 EC ?? 8B 0D", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
            .add(0x168)
        )
        .add(
            "dwPlantedC4",
            Pattern("48 8B 15 ?? ?? ?? ?? 41 FF C0", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
        )
        .add(
            "dwViewAngles",
            Pattern(
                "48 89 05 ?? ?? ?? ?? 0F 57 C0 0F 11 05", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
            .add((
                Pattern(
                    "F2 41 0F 10 84 30 ?? ?? ?? ??", CS2.client.base, module_buffer)
                .aob_scan()
                .slice(6, 10)
                .offset
            ))
        )
        .add(
            "dwViewMatrix",
            Pattern("48 8D 0D ?? ?? ?? ?? 48 C1 E0 06", CS2.client.base, module_buffer)
            .aob_scan()
            .rip()
        )
    )


# def dwCSGOInput(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 48 8D 05 ?? ?? ?? ?? 48 C7 05 ?? ?? ?? ?? ?? ?? ?? ?? 48 89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? 48 8D 05", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwEntityList(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 35 ?? ?? ?? ?? 48 85 F6", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwGameEntitySystem(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8B 1D ?? ?? ?? ?? 48 89 1D", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwGameEntitySystem_getHighestEntityIndex(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("8B 81 ?? ?? ?? ?? 89 02 48 8B C2 C3 CC CC CC CC 48 89 5C 24 ?? 48 89 6C 24", CS2.client.base, module_buffer)
#         .aob_scan()
#         .slice(2, 4)
#     )
#
# def dwGameRules(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 1D ?? ?? ?? ?? FF 15 ?? ?? ?? ?? 84 C0", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwGlobalVars(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 15 ?? ?? ?? ?? 48 89 42", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwGlowManager(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8B 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 8B 41", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwLocalPlayerController(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 05 ?? ?? ?? ?? 8B 9E", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwLocalPlayerPawn(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8D 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 48 83 EC ?? 8B 0D", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#         .add(328)
#     )
#
# def dwPlantedC4(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8B 15 ?? ?? ?? ?? 41 FF C0", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwPrediction(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8D 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 48 83 EC ?? 8B 0D", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# # def dwSensitivity(module_buffer: bytes = None) -> Pattern:
# #     return (
# #         Pattern("48 8B 05 ?? ?? ?? ?? 48 8B 40 ?? F3 41 0F 59 F4", CS2.client.base, module_buffer)
# #         .search(
# #         .rip()
# #     )
#
# # def dwSensitivity_sensitivity(module_buffer: bytes = None) -> Pattern:
# #     return (
# #         Pattern("FF 50 ?? 4C 8B C6 48 8D 55 ?? 48 8B CF E8 ?? ?? ?? ?? 84 C0 0F 85 ?? ?? ?? ?? 4C 8D 45 ?? 8B D3 48 8B CF E8 ?? ?? ?? ?? E9 ?? ?? ?? ?? F3 0F 10 06", CS2.client.base, module_buffer)
# #         .search(
# #         .slice(2, 3)
# #     )
#
# def dwViewAngles(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 48 8D 05 ?? ?? ?? ?? 48 C7 05 ?? ?? ?? ?? ?? ?? ?? ?? 48 89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? 48 8D 05", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#         .add(21528)
#     )
#
# def dwViewMatrix(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8D 0D ?? ?? ?? ?? 48 C1 E0 06", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwViewRender(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 89 05 ?? ?? ?? ?? 48 8B C8 48 85 C0", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )
#
# def dwWeaponC4(module_buffer: bytes = None) -> Pattern:
#     return (
#         Pattern("48 8B 15 ?? ?? ?? ?? 48 8B 5C 24 ?? FF C0 89 05 ?? ?? ?? ?? 48 8B C6 48 89 34 EA 48 8B 6C 24 ?? C6 86 ?? ?? ?? ?? ?? 80 BE", CS2.client.base, module_buffer)
#         .aob_scan()
#         .rip()
#     )