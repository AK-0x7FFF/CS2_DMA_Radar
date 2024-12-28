from memory.address import Address
from memory.process import CS2
from utils.vec import Vec3, Vec2


class PlayerPawn:
    def __init__(self, player_pawn_address: Address) -> None:
        self.pawn_address = player_pawn_address


    @property
    def health(self) -> int | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.C_BaseEntity.m_iHealth)
            .u16()
        )

    @property
    def team_num(self) -> int | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.C_BaseEntity.m_iTeamNum)
            .u8()
        )

    @property
    def pos(self) -> Vec3 | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.C_BasePlayerPawn.m_vOldOrigin)
            .vec3()
        )

    @property
    def angle(self) -> Vec2 | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.C_CSPlayerPawnBase.m_angEyeAngles)
            .vec2()
        )

    @property
    def flags(self) -> int | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.C_BaseEntity.m_fFlags)
            .u32()
        )

    @property
    def has_armor(self) -> bool | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.C_CSPlayerPawn.m_ArmorValue)
            .bool()
        )

    @property
    def has_helmet(self) -> bool | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.CCSPlayer_ItemServices.m_bHasHelmet)
            .bool()
        )

    @property
    def has_defuser(self) -> bool | None:
        return (
            self.pawn_address.copy()
            .offset(CS2.schemas.client_dll.CCSPlayer_ItemServices.m_bHasDefuser)
            .bool()
        )



