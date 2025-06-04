#!/bin/bash
#SBATCH --job-name=setup_env
#SBATCH --output=setup_env.log
#SBATCH --error=setup_env.err
#SBATCH --time=01:00:00
#SBATCH --partition=parallel
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

# Load necessary modules (if required)
module load miniconda

# Create a new conda environment if not already created
if ! conda env list | grep -q bindcraft_env; then
    conda create -y -n bindcraft_env python=3.11 
fi

# Activate the environment
source activate bindcraft_env

# Install pip requirements
python -m pip install -r requirements.txt

# Run setup.py
python setup.py