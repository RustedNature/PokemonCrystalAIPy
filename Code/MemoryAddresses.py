import enum


class MemoryAddresses(enum.Enum):
    LevelOfPokemon1 = 0xDCFE
    HpOfPokemon1Byte1 = 0xDD01
    HpOfPokemon1Byte2 = 0xDD02

    LevelOfPokemon2 = 0xDD2E
    HpOfPokemon2Byte1 = 0xDD31
    HpOfPokemon2Byte2 = 0xDD32

    LevelOfPokemon3 = 0xDD5E
    HpOfPokemon3Byte1 = 0xDD61
    HpOfPokemon3Byte2 = 0xDD62

    LevelOfPokemon4 = 0xDD8E
    HpOfPokemon4Byte1 = 0xDD91
    HpOfPokemon4Byte2 = 0xDD92

    LevelOfPokemon5 = 0xDDBE
    HpOfPokemon5Byte1 = 0xDDB1
    HpOfPokemon5Byte2 = 0xDDB2

    LevelOfPokemon6 = 0xDDEE
    HpOfPokemon6Byte1 = 0xDDE1
    HpOfPokemon6Byte2 = 0xDDE2

    NumberOfPokemonInTeam = 0xDCD7

    MapBank = 0xDCB5
    MapNumber = 0xDCB6
    
    WorldY = 0xDCB7
    WorldX = 0xDCB8

    BattleType = 0xD22D

    MinutesPlayTimeInGame = 0xD4C6
    HoursPlayTimeInGameByte1 = 0xD4C4
    HoursPlayTimeInGameByte2 = 0xD4C5
