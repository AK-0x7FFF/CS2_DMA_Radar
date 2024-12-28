from typing import Optional

from memory.address import Address
from memory.process import CS2
from utils.vec import Vec3


class PlantedC4:
    def __init__(self, address: Address):
        self.address = address

    def __repr__(self) -> str:
        return "PlantedC4(%s)" % self.address


    @staticmethod
    def _get_game_time() -> Optional[float]:
        return CS2.signatures.client.dwGlobalVars.pointer().offset(0x34).float()

    @property
    def is_ticking(self) -> Optional[bool]:
        return self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_bBombTicking).bool()

    @property
    def site(self) -> Optional[str]:
        return ("A", "B", "C")[self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_nBombSite).i8()]

    @property
    def explode_game_time(self) -> Optional[float]:
        return self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_flC4Blow).float()

    @property
    def explode_time_left(self) -> Optional[float]:
        return self.explode_game_time - self._get_game_time()

    @property
    def is_defusing(self) -> Optional[bool]:
        return self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_bBeingDefused).bool()

    @property
    def defuse_game_time(self) -> Optional[float]:
        return self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_flDefuseCountDown).float()

    @property
    def defuse_time_length(self) -> Optional[float]:
        return self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_flDefuseLength).float()

    @property
    def defuse_time_left(self) -> Optional[float]:
        return self.defuse_game_time - self._get_game_time()

    @property
    def can_defused(self) -> Optional[bool]:
        return self.defuse_game_time < self.explode_game_time

    @property
    def pos(self) -> Optional[Vec3]:
        return self.address.copy().offset(CS2.schemas.client_dll.CBaseAnimGraph.m_vLastSlopeCheckPos).vec3()

    @property
    def next_beep_game_time(self) -> Optional[float]:
        return self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_flNextBeep).float()

    @property
    def next_beep_time(self) -> Optional[float]:
        return self.next_beep_game_time - self._get_game_time()

    # @property
    # def a(self):
    #     return self.address.copy().offset(CS2.schemas.client_dll.C_PlantedC4.m_bC4Activated).bool()
