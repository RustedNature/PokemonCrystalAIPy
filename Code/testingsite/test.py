

from pyboy import PyBoy
from MemoryAddresses import MemoryAddresses

from MemoryValue import MemoryValue
from TestRewardManager import RewardManager

memory_value_list = [MemoryValue(MemoryAddresses.MapBank),
                        MemoryValue(MemoryAddresses.MapNumber),
                        MemoryValue(MemoryAddresses.LevelOfPokemon1),
                        MemoryValue(MemoryAddresses.HpOfPokemon1Byte1),
                        MemoryValue(MemoryAddresses.HpOfPokemon1Byte2),
                        MemoryValue(MemoryAddresses.LevelOfPokemon2),
                        MemoryValue(MemoryAddresses.HpOfPokemon2Byte1),
                        MemoryValue(MemoryAddresses.HpOfPokemon2Byte2),
                        MemoryValue(MemoryAddresses.LevelOfPokemon3),
                        MemoryValue(MemoryAddresses.HpOfPokemon3Byte1),
                        MemoryValue(MemoryAddresses.HpOfPokemon3Byte2),
                        MemoryValue(MemoryAddresses.LevelOfPokemon4),
                        MemoryValue(MemoryAddresses.HpOfPokemon4Byte1),
                        MemoryValue(MemoryAddresses.HpOfPokemon4Byte2),
                        MemoryValue(MemoryAddresses.LevelOfPokemon5),
                        MemoryValue(MemoryAddresses.HpOfPokemon5Byte1),
                        MemoryValue(MemoryAddresses.HpOfPokemon5Byte2),
                        MemoryValue(MemoryAddresses.LevelOfPokemon6),
                        MemoryValue(MemoryAddresses.HpOfPokemon6Byte1),
                        MemoryValue(MemoryAddresses.HpOfPokemon6Byte2),
                        MemoryValue(MemoryAddresses.NumberOfPokemonInTeam),
                        MemoryValue(MemoryAddresses.BattleType),
                        MemoryValue(MemoryAddresses.MinutesPlayTimeInGame),
                        MemoryValue(MemoryAddresses.HoursPlayTimeInGameByte1),
                        MemoryValue(MemoryAddresses.HoursPlayTimeInGameByte2),
                        MemoryValue(MemoryAddresses.WorldX),
                        MemoryValue(MemoryAddresses.WorldY)]

pyboy = PyBoy(r".\ROM\Pokemon - Kristall-Edition (Germany).gbc")
with open(r".\ROM\Pokemon - Kristall-Edition (Germany).gbc.state", "rb") as state_file:
            pyboy.load_state(state_file)
reward_manager = RewardManager()

while True:
    for memval in memory_value_list:
            memval.set_mem_value(pyboy.get_memory_value(memval.memAddress.value))
    reward_manager.update_values(memory_value_list)
    print(pyboy.botsupport_manager().tilemap_background()[:, :])
    print(pyboy.botsupport_manager().tilemap_window()[:, :])
    # print("MapBank: ", memory_value_list[0].memValue)
    # print("MapNumber: ", memory_value_list[1].memValue)
    # print("X: ", memory_value_list[25].memValue)
    # print("Y: ", memory_value_list[26].memValue)
    reward_manager.get_reward_test()
    pyboy.tick()
    