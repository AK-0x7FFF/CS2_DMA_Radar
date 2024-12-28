from memory.address import Address
from memory.process import CS2


class PlayerController:
    def __init__(self, player_controller_address: Address) -> None:
        self.controller_address = player_controller_address


    @property
    def name(self) -> str | None:
        return (
            self.controller_address.copy()
            .offset(CS2.schemas.client_dll.CCSPlayerController.m_sSanitizedPlayerName)
            .pointer()
            .str(64)
        )


    @property
    def money(self) -> int | None:
        return (
            self.controller_address.copy()
            .offset(CS2.schemas.client_dll.CCSPlayerController.m_pInGameMoneyServices)
            .pointer()
            .offset(CS2.schemas.client_dll.CCSPlayerController_InGameMoneyServices.m_iAccount)
            .i32()
        )


    @property
    def steam_id(self) -> int | None:
        return (
            self.controller_address.copy()
            .offset(CS2.schemas.client_dll.CBasePlayerController.m_steamID)
            .u64()
        )