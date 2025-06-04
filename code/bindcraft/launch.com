#!/bin/bash
#SBATCH --job-name=setup_env
#SBATCH --output=setup_env.log
#SBATCH --error=setup_env.err
#SBATCH --time=12:00:00
#SBATCH --partition=gpu-medium
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G

# Load necessary modules (if required)
module load miniconda

export WANDB_PROJECT=BindCraft
export WANDB_ENTITY=stefmenzies-lancaster-university
export WANDB_API_KEY=20c7dbd2196d09dfa1144bf9389190ff9cb2b8ce
# Activate the environment
source activate bindcraft_env

python launch.py
