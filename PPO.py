
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


max_steps = 8192
n_steps = 2048
batch_size = 1536
n_epochs = 1
gamma = 0.998
ent_coef = 0.75
learning_rate = 0.002
eval_steps = 5000
model_path_name = "Files/models/ppo_pokemon_tiles.zip"
envs_num = 16

def make_env():
    def _init():
        env = PokemonCrystalEnv(max_steps=max_steps)
        env = Monitor(env)
        return env
    return _init

def eval_model(deterministic=True):
    files = glob.glob('Files/tus/*')
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
    create_grid_video(suffix)



def create_grid_video(suffix = ""):
    files = glob.glob('Files/temp_screenshots/*')
    files.sort()
    uuids_list = []
    for f in range(0,len(files),eval_steps):
        filename = os.path.basename(files[f])
        filename = filename.split("eval")
        uuid = filename[0] 
        if uuid not in uuids_list:
            uuids_list.append(uuid)


    runs_grid = [[None]*4 for _ in range(envs_num//4)]
    for i in range(0,len(uuids_list)):
        run_images = []
        for j in range(eval_steps):
            img = imageio.v3.imread(f"Files/temp_screenshots/{uuids_list[i]}eval{j+1}.png")
            run_images.append(img)
        # Add the run to the grid
        runs_grid[i//4][i%4] = run_images

    # Concatenate the images into a grid for each frame
    grid_images = []
    for frame in range(eval_steps):
        grid_frame = np.concatenate([np.concatenate([runs_grid[i][j][frame] for j in range(envs_num//4)], axis=1) for i in range(4)], axis=0)
        grid_images.append(grid_frame)

    # Save the grid images as a video
    imageio.mimsave(f'Files/videos/{suffix}.mp4', grid_images, fps=60)

if __name__ == "__main__":

    
    envs_init_list = [make_env() for _ in range(envs_num)]  

    envs = SubprocVecEnv(envs_init_list)  # Pass the list of functions to DummyVecEnv

    checkpoint_callback = CheckpointCallback(save_freq=5_000, save_path='Files/modelsCheckpoint/',
                                            name_prefix=f"PokeAI_Steps{max_steps}_Batch{batch_size}_Epochs{n_epochs}_Gamma{gamma}_learning_rate{learning_rate}_ent_coef{ent_coef}")
    try:
        model = PPO.load(model_path_name, envs, verbose=2, tensorboard_log="Files/tensorboard_log")
        model.ent_coef = ent_coef
        model.learning_rate = learning_rate
        print("Model loaded")
    except:
        model = PPO('CnnPolicy', envs, n_steps= n_steps , batch_size=batch_size, n_epochs= n_epochs, gamma=gamma, ent_coef=ent_coef, learning_rate=learning_rate , verbose=2, tensorboard_log="Files/tensorboard_log/")
   
        print("No model found")
 
    # Train the agent
    model.learn(total_timesteps= max_steps * envs_num * 100, progress_bar=True, callback=checkpoint_callback)

    # Save the trained model
    model.save(model_path_name)
    print("Model saved")
    
    videos = glob.glob('Files/Videos/*')
    for v in videos:
        os.remove(v)

    eval_model(deterministic=True)
    eval_model(deterministic=False)

    mean_reward, _ = evaluate_policy(model, envs, n_eval_episodes=1,return_episode_rewards=True)
    print(mean_reward, "+/-", _)
        