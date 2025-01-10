from typing import Self, Type

import game
from game.player.player_controller import PlayerController
from game.player.player_pawn import PlayerPawn
from memory.address import Address
from memory.memory import VmmScatterMemoryRead
from memory.process import CS2



class PlayerEntity(PlayerController, PlayerPawn):
    def __init__(self, player_controller_address: Address, player_pawn_address: Address) -> None:
        if not all((player_controller_address, player_pawn_address)): raise ValueError()

        PlayerController.__init__(self, player_controller_address)
        PlayerPawn.__init__(self, player_pawn_address)


    def __repr__(self) -> str:
        return "PlayerEntity(%s, %s)" % (self.controller_address, self.pawn_address)

    def __bool__(self) -> bool:
        return all((self.controller_address, self.pawn_address))

    def __eq__(self, other) -> bool:
        return self.controller_address == other.controller_address and self.pawn_address == other.pawn_address

    def __hash__(self) -> int:
        return hash((self.controller_address.address, self.pawn_address.address, ))


    @classmethod
    def from_entity_index(cls, entity_list: Type["game.entity_list.EntityList"], entity_index: int) -> Self | None:
        player_controller_address = entity_list.get_entity_from_list_entry(entity_index)
        if not player_controller_address: return None

        pawn_offset = (
            player_controller_address.copy()
            .offset(CS2.schemas.client_dll.CCSPlayerController.m_hPlayerPawn)
            .u32()
        )
        player_pawn_address = entity_list.get_entity_from_list_entry(pawn_offset)
        if not player_pawn_address: return None

        return cls(player_controller_address, player_pawn_address)

    def get_scatter_mode(self, scatter_memory_read: VmmScatterMemoryRead) -> "PlayerEntity":
        return PlayerEntity(
            self.controller_address.copy().set_scatter(scatter_memory_read),
            self.pawn_address.copy().set_scatter(scatter_memory_read)
        )


    @property
    def is_on_ground(self) -> bool | None:
        if self.flags is None: return None

        return bool(self.flags & 1 << 0)


    @property
    def is_ducking(self) -> bool | None:
        if self.flags is None: return None

        return bool(self.flags & 1 << 1)


    @property
    def is_noclip_mode(self) -> bool | None:
        if self.flags is None: return None

        return bool(self.flags & 1 << 3)
