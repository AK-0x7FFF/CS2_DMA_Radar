from typing import Self

from error import ProcessDoesNotSetupError
# from game.planted_c4_entity import PlantedC4
from game.player.player_entity import PlayerEntity
from memory.address import Address
from memory.process import CS2


class EntityList:
    MAX_PLAYER_INDEX = 1 << 6

    _entity_list_address: Address | None = None
    class _player_cache:
        index_2_controller: dict[int, Address] = dict()
        controller_2_pawn : dict[Address, Address] = dict()

    player_entities: list[PlayerEntity] = list()
    # planted_c4_entities: list[PlantedC4] = list()
    world_entities: list = list()


    @classmethod
    def clear_cache(cls) -> None:
        cls._player_cache.index_2_controller.clear()
        cls._player_cache.controller_2_pawn.clear()


    @classmethod
    def get_local_player(cls) -> PlayerEntity | None:
        controller_address = CS2.signatures.client.dwLocalPlayerController.pointer()
        pawn_address = CS2.signatures.client.dwLocalPlayerPawn.pointer()
        if not all((controller_address, pawn_address)): return None

        return PlayerEntity(
            player_controller_address=controller_address,
            player_pawn_address=pawn_address
        )


    @classmethod
    def get_entity_from_list_entry(cls, offset: int, auto_next_entry: bool = True) -> Address | None:
        return cls._entity_list_address.pointer_chain(
            0x10 + ((0x08 * ((offset & 0x7FFF) >> 0x9)) if auto_next_entry else 0x0),
            0x78 * (offset & 0x1FF)
        )


    @classmethod
    def update_entity_list_address(cls) -> Self:
        if not CS2.is_setup(): raise ProcessDoesNotSetupError()

        cls._entity_list_address = CS2.signatures.client.dwEntityList.pointer()
        return cls


    @classmethod
    def get_player_entity_in_cache(cls, entity_index: int) -> PlayerEntity | None:
        player_controller_address = cls._player_cache.index_2_controller.get(entity_index, None)
        if player_controller_address is None: return None

        player_pawn_address = cls._player_cache.controller_2_pawn.get(player_controller_address, None)
        if player_pawn_address is None: return None

        return PlayerEntity(player_controller_address, player_pawn_address)


    @classmethod
    def update_player_entities(cls, is_read_cache: bool = True, is_write_cache: bool = True) -> Self:
        player_entities = list()
        for entity_index in range(cls.MAX_PLAYER_INDEX):
            if is_read_cache and (player_entity := cls.get_player_entity_in_cache(entity_index)) is not None:
                player_entities.append(player_entity)
                continue

            player_entity = PlayerEntity.from_entity_index(cls, entity_index)
            if player_entity is None: continue

            if not player_entity.controller_address or not player_entity.pawn_address:
                continue

            if is_write_cache:
                cls._player_cache.index_2_controller.update({entity_index: player_entity.controller_address})
                cls._player_cache.controller_2_pawn.update({player_entity.controller_address: player_entity.pawn_address})

            player_entities.append(player_entity)

        cls.player_entities = player_entities
        return cls


    # @classmethod
    # def update_planted_c4_entities(cls) -> Self:
    #     is_c4_planted = CS2.signatures.client.dwGameRules.pointer().offset(CS2.schemas.client_dll.C_CSGameRules.m_bBombPlanted).bool()
    #     if not is_c4_planted:
    #         cls.planted_c4_entities = list()
    #         return cls
    #
    #     planted_c4_list_address = CS2.signatures.client.dwPlantedC4.pointer()
    #     list_max_size = CS2.signatures.client.dwPlantedC4.copy().offset(0x8).u32()
    #
    #     planted_c4_list = list()
    #     for index in range(list_max_size):
    #         planted_c4_address = planted_c4_list_address.copy().offset(index * 0x8).pointer()
    #         if not planted_c4_address: continue
    #
    #         planted_c4 = PlantedC4(planted_c4_address)
    #         if planted_c4.a is None: continue
    #
    #         planted_c4_list.append(planted_c4)
    #         print(index, planted_c4)
    #
    #     cls.planted_c4_entities = planted_c4_list
    #     return cls
