from stable_baselines3.common.env_checker import check_env
from PokemonCrystalEnv import PokemonCrystalEnv
import gymnasium as gym

gym.register(
    id='PokemonCrystalEnv-v0',
    entry_point='PokemonCrystalEnv:PokemonCrystalEnv',
)

env = gym.make('PokemonCrystalEnv-v0')

check_env(env, warn=True)