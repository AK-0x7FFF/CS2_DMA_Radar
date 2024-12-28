import memory


_address_type_hint = "memory.address.Address"

class SignaturesClientTypeHint:
    dwEntityList:                             _address_type_hint
    dwGameEntitySystem:                       _address_type_hint
    dwGameEntitySystem_getHighestEntityIndex: _address_type_hint
    dwGameRules:                              _address_type_hint
    dwGlobalVars:                             _address_type_hint
    dwLocalPlayerController:                  _address_type_hint
    dwLocalPlayerPawn:                        _address_type_hint
    dwPlantedC4:                              _address_type_hint
    dwViewAngles:                             _address_type_hint
    dwViewMatrix:                             _address_type_hint

class SignaturesEngine2TypeHint:
    dwBuildNumber:                   _address_type_hint
    dwNetworkGameClient:             _address_type_hint
    dwNetworkGameClient_signOnState: _address_type_hint

class SignaturesTypeHint:
    client: SignaturesClientTypeHint
    engine2: SignaturesEngine2TypeHint


