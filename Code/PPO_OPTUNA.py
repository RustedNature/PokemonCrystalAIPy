from time import sleep
import cv2
import optuna
from matplotlib import image, pyplot as plt
import matplotlib
import numpy as np
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import DummyVecEnv , SubprocVecEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
from PokemonCrystalEnv import PokemonCrystalEnv
import gymnasium as gym
from stable_baselines3.common.env_util import make_vec_env

def make_env():
    def _init():
        env = PokemonCrystalEnv()
        env = Monitor(env)
        return env
    return _init

if __name__ == "__main__":

    envs_num = 16
    # Register the environment

    envs_init_list = [make_env() for _ in range(envs_num)]  

    envs = SubprocVecEnv(envs_init_list)  # Pass the list of functions to DummyVecEnv

   


    def objective(trial):
        # Suggest values for the hyperparameters
        n_steps = trial.suggest_int('n_steps', 64, 2048)
        batch_size = trial.suggest_int('batch_size', 1, 2048)
        n_epochs = trial.suggest_int('n_epochs', 1, 128)
        ent_coef = trial.suggest_float('ent_coef', 0.0, 1.0)
        learning_rate = trial.suggest_float('lr', 1e-5, 1)
        gamma = trial.suggest_float('gamma', 0.9, 1.0)
        gae_lambda = trial.suggest_float('gae_lambda', 0.9, 1.0)

        # Create the PPO model with the suggested hyperparameters
        model = PPO("CnnPolicy", envs, n_steps=n_steps, verbose=1, batch_size=batch_size, n_epochs=n_epochs, ent_coef=ent_coef, learning_rate=learning_rate , gamma=gamma, gae_lambda=gae_lambda)

        # Train the model for a fixed number of timesteps
        model.learn(total_timesteps=8000 * envs_num * 4)

        # Evaluate the model on the environment and return the mean reward
        print("Evaluating")
        mean_reward, _ = evaluate_policy(model, envs, n_eval_episodes=10)
        print("Evaluation done")
        print("Mean reward:", mean_reward)
        return mean_reward

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20, show_progress_bar=True, n_jobs=1)

    print("Best trial:")
    trial = study.best_trial

    print(" Value: ", trial.value)

    print(" Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")