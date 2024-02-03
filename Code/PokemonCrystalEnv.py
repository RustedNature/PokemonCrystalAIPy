from uuid import uuid4
import gymnasium as gym
from gymnasium import  spaces
import numpy as np
from Code.MemoryAddresses import MemoryAddresses
from Code.MemoryValue import MemoryValue
from Code.MoveManager import MoveManager
from Code.RewardManager import RewardManager

from scipy.ndimage import zoom


import numpy as np
import matplotlib.pyplot as plt


from gymnasium import spaces
from pyboy import PyBoy
from pyboy.utils import WindowEvent



class PokemonCrystalEnv(gym.Env):
    metadata = {'render_modes': ['none']}
    def __init__(self, max_steps=2000, uuid=None):
        super(PokemonCrystalEnv, self).__init__()
        self.render_mode = 'train'
        self.reward_manager = RewardManager()
        self.pyboy = PyBoy("Files./ROM/Pokemon - Kristall-Edition (Germany).gbc", window_type="headless")
        self.pyboy.set_emulation_speed(0)
        self.load_initial_state()
        self.is_episode_done = False
        self.step_count = 0
        self.move_manager = MoveManager()
        self.max_steps = max_steps
        self.observation = np.zeros((1,58,64))
        self.reward = 0
        self.done = False
        self.env_id = uuid4()       
        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Discrete(8)
        self.observation_space = spaces.Box(low=0, high=255, shape=(1,58,64), dtype=np.uint8)
        self.memory_value_list = [MemoryValue(MemoryAddresses.MapBank),
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
       
        self.reset()

    def step(self, action):
        # Execute one time step within the environment
        self.make_action(action)
       
        
        return self.observation, self.reward, self.done, False, {}


    

    def make_action(self, action):

        for i in range(24):
            self.pyboy.tick()
            if i == 8:
                self.release_buttons()     
        if self.step_count >= self.max_steps:
            self.is_episode_done = True
       
       
        screen_memory = self.get_screen_memory()

        self.read_memory()
        self.reward_manager.update_values(self.memory_value_list)
        self.press_button(action)
        self.observation = self.get_pyboy_image_as_numpy_array()
        #image.imsave(f"tus/Run{self.step}.png", self.observation.reshape(144,160,3), format="png")
        self.reward = self.reward_manager.get_reward(action, self.observation,screen_memory)
        



        self.done = self.is_episode_done
        self.step_count += 1
    

    def get_screen_memory(self):
        screen_memory = []
        for i in range(0xC4A0, 0xC607+1):
            screen_memory.append(self.pyboy.get_memory_value(i))
        return screen_memory
    

    def release_buttons(self):
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        self.pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_SELECT)


    def press_button(self, movement):
        if movement == 0:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
        elif movement == 1:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
        elif movement == 2:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
        elif movement == 3:
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        elif movement == 4:
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
        elif movement == 5:
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
        elif movement == 6:
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
        elif movement == 7:
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_SELECT)

    def reset(self, seed=None, options=None):
        super().reset( seed=seed, options=options)
        self.reward_manager.reset()
        self.load_initial_state()
        self.observation = self.get_pyboy_image_as_numpy_array()
        self.is_episode_done = False
        self.step_count = 0
        self.release_buttons()
        print("----------------------reset----------------------")
        return self.observation, {}
    
    def render(self):
        image = self.pyboy.botsupport_manager().screen().screen_ndarray().astype(np.uint8)

        # Switch the red and blue channels
        image = image[:, :, ::-1]

        plt.imsave(f"Files/temp_screenshots/{self.env_id}eval{self.step_count}.png", image, format="png")
        
    
    def get_uuid(self):
        return self.env_id



    def load_initial_state(self):
        with open("Files/ROM/save.state", "rb") as state_file:
            self.pyboy.load_state(state_file)


    def get_pyboy_image_as_numpy_array(self):
        image = self.pyboy.botsupport_manager().screen().screen_ndarray()
        grayscale_image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        resized_image = zoom(grayscale_image, (0.4, 0.4))
        return resized_image.reshape((1,58,64)).astype(np.uint8)
          
    def read_memory(self):
        for memval in self.memory_value_list:
            memval.set_mem_value(self.pyboy.get_memory_value(memval.memAddress.value))

  