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

export WANDB_PROJECT=your_project_name
export WANDB_ENTITY=your_username
export WANDB_API_KEY=your_api_key
# Activate the environment
source activate bindcraft_env

python launch.py --chains A --lengths 50,120 --number_of_final_designs 10 