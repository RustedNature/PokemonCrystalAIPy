# Pokemon Crystal AI in Py

## Now in Python with Baselines3

What a journey it has been for me, now coding in Python :D

## What is it?

This is my second attempt to train an AI that plays Pokemon Crystal, now entirely in Python using Baselines3.  
[PyBoy](https://github.com/Baekalfen/PyBoy) remains my favorite emulator, as it is a convenient and accessible emulator directly integrated into Python.  
[Baselines 3](https://stable-baselines3.readthedocs.io/en/master/) is my new choice for the AI framework; I'm currently too lazy to implement PPO on my own.

## What is implemented?

- Pokemon Crystal Environment
- Training cycle
- Creation of Deterministic and Non-Deterministic videos after each training cycle
- Reward based on exploration (Tilemap) - Tilemap is faster, but I haven't tested its viability yet
- Reward based on exploration (Images)
- Reward for important events such as reaching the professor's lab, getting the first Pokemon, Pokemon leveling up, speaking with mom, etc.

## How far has the AI progressed?

As of now, not very far. But I am confident it can reach Rosalia City.

### Checklist

- Speaking with mom ✅
- Going outside ❎
- Reaching Prof ❎
- Taking the first Pokemon ❎
- Heading up to Route 29 ❎
- Reaching Rosalia City ❎
- Going all the way up to the other Prof ❎
- Going back to the first Prof ❎

For now, this is my goal. I will determine when the AI is fit enough to accomplish this.
