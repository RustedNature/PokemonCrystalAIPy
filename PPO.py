import math
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
from Code.PokemonCrystalEnv import PokemonCrystalEnv
from stable_baselines3.common.env_util import make_vec_env
import numpy as np
import imageio
import glob
import os
from Code.Logger import Logger

logger = Logger().get_logger()

envs_num = 8
temp_screenshots_path = "Files/temp_screenshots"
videos_path = "Files/videos"
max_steps = 4096
n_steps = 2048
batch_size = 512
n_epochs = 3
gamma = 0.998
ent_coef = 0.75
learning_rate = 0.002
eval_steps = 2000
model_path = "Files/models"
model_name = "ppo_pokemon_tiles"
model_path_name = model_path + "/" + model_name

def make_env():
    def _init():
        env = PokemonCrystalEnv(max_steps=max_steps)
        env = Monitor(env)
        return env
    return _init

def eval_model(deterministic=True):
    files = glob.glob(temp_screenshots_path + "/*")
    for f in files:
        os.remove(f)
    obs = envs.reset()
    for i in range(eval_steps):
        action, _states = model.predict(obs, deterministic=deterministic)
        obs, reward, done, info = envs.step(action)
        envs.render()

            
        if done.all():
            obs = envs.reset()
    suffix = "Deterministic" if deterministic else "NonDeterministic"
    create_grid_video(suffix= suffix)





def create_grid_video(suffix="", temp_screenshots_path="Files/temp_screenshots/", eval_steps=eval_steps, envs_num=envs_num, videos_path="Files/videos/"):
    logger.info(f"Creating grid video with suffix {suffix}")

    try:
        # Get list of files in the directory
        files = glob.glob(os.path.join(temp_screenshots_path, '*'))
        files.sort()

        # Extract unique UUIDs from the filenames
        uuids_list = []
        for f in range(0, len(files), eval_steps):
            filename = os.path.basename(files[f])
            uuid = filename.split("eval")[0]
            if uuid not in uuids_list:
                uuids_list.append(uuid)


        # Calculate the size of the largest possible square that fits within envs_num
        grid_size = int(math.ceil(math.sqrt(envs_num)))

        # Initialize the grid with None
        runs_grid = [[None]*grid_size for _ in range(grid_size)]

        # Load images for each UUID and add to the grid
        for i, uuid in enumerate(uuids_list):
            try:
                run_images = [imageio.v3.imread(os.path.join(temp_screenshots_path, f"{uuid}eval{j+1}.png")) for j in range(eval_steps)]
                runs_grid[i // grid_size][i % grid_size] = run_images
            except Exception as e:
                logger.error(f"Failed to load images for UUID {uuid}: {e}")

        blank_image = np.zeros_like(run_images[0])
        for i in range(grid_size):
            for j in range(grid_size):
                if runs_grid[i][j] is None:
                    runs_grid[i][j] = [blank_image]*eval_steps

        # Concatenate the images into a grid for each frame
        grid_images = []
        for frame in range(eval_steps):
            grid_frame = np.concatenate([np.concatenate([runs_grid[i][j][frame] for j in range(grid_size)], axis=1) for i in range(grid_size)], axis=0)
            grid_images.append(grid_frame)

        # Save the grid images as a video
        try:
            imageio.mimsave(os.path.join(videos_path, f'{suffix}.mp4'), grid_images, fps=60)
            logger.info(f"Grid video saved successfully with suffix {suffix}")
        except Exception as e:
            logger.error(f"Failed to save grid video: {e}")

    except Exception as e:
        logger.error(f"An unexpected error occurred while creating grid video: {e}")

if __name__ == "__main__":

    
    envs_init_list = [make_env() for _ in range(envs_num)]  

    envs = SubprocVecEnv(envs_init_list)  # Pass the list of functions to DummyVecEnv

    checkpoint_callback = CheckpointCallback(save_freq=5_000, save_path='Files/modelsCheckpoint/',
                                            name_prefix=f"PokeAI"+ model_name)
    try:
        model = PPO.load(model_path_name, envs, verbose=2, tensorboard_log="Files/tensorboard_log")
        model.ent_coef = ent_coef
        model.learning_rate = learning_rate
        model.n_epochs = n_epochs
        
        logger.info("Model loaded")
    except:
        model = PPO('CnnPolicy', envs, n_steps= n_steps , batch_size=batch_size, n_epochs= n_epochs, gamma=gamma, ent_coef=ent_coef, learning_rate=learning_rate , verbose=2, tensorboard_log="Files/tensorboard_log/")
   
        logger.info("No model found")
 
    # Train the agent
    # model.learn(total_timesteps= max_steps * envs_num * 50, progress_bar=True, callback=checkpoint_callback)

    # Save the trained model
    model.save(model_path_name)
    logger.info("Model saved")
    
    videos = glob.glob(videos_path + "/*")
    for v in videos:
        os.remove(v)

    eval_model(deterministic=True)
    eval_model(deterministic=False)

    mean_reward, _ = evaluate_policy(model, envs, n_eval_episodes=1,return_episode_rewards=True)
    logger.info(mean_reward)
        