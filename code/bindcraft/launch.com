#!/bin/bash
#SBATCH --job-name=launch_bindcraft
#SBATCH --output=launch_bindcraft.log
#SBATCH --error=launch_bindcraft.err
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
conda activate $global_storage/bindcraft_env

python launch.py