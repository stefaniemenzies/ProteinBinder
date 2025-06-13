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
module add miniforge/20240923
source activate pyrosetta
export LANG=utf8

cd $global_storage/ProteinBinder/code/bindcraft


# Install pip requirements
python -m pip install -r requirements.txt --no-cache-dir


# Run setup.py
python setup.py

##should take about 10 minutes to run