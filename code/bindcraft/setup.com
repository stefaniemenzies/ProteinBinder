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
module load opence

cd $global_storage/ProteinBinder/code/bindcraft
# Create a new conda environment if not already created in global_Storage path
conda create -y --prefix $global_storage/bindcraft_env python=3.13

ENV TMPDIR=$global_storage/bindcraft_env/tmp #needed for pyrosetta! 
# Activate the environment
conda activate $global_storage/bindcraft_env

# Install pip requirements
python -m pip install -r requirements.txt --no-cache-dir

# Run setup.py
python setup.py

##should take about 10 minutes to run