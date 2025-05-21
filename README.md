# ProteinBinder

## Overview

This repository contains a collection of Jupyter notebooks that demonstrate how to use the ProteinBinder library for protein-protein interaction prediction. There are also 2 folders for code to launch these on-prem using HPC. 

The 2 folders are:
- 'code' - contains the code to run the notebooks on a local machine or HPC cluster.
- 'notebooks' - contains the Jupyter notebooks that demonstrate how to use the ProteinBinder library.

## Getting Started with BindCraft

Whether running locally or on an HPC cluster, the argparser contains default values for the parameters. You can change these values to suit your needs, or enter them from the command line. The argparser also contains a help option that will print out the available options and their default values.


### Local Installation
To get started with the ProteinBinder library, you will need to install the library and its dependencies. The easiest way to do this is to use the provided `requirements.txt` file. You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```

Then you can use the 'setup.py' file to install the library, and collect necessary data files:

```bash
python setup.py
```

Finally, you can launch the runs using the 'launch.py' script. This script will launch the runs on your local machine or HPC cluster. You can specify the number of runs to launch and the number of threads to use for each run.

```bash
python launch.py 
```
This will launch on your local machine. 

### Running on HPC
if you want to run the script on an HPC cluster, running slurm, after building a python environment, you can use the following command:

```bash
sbatch setup.com
```
to download useful data files, and then run the launch script:

```bash
sbatch launch.com
```




## Running notebooks locally

The notebooks in this repository are designed to be run in Google Colab. However, if you want to run them locally, the easiest way is to use the Colab Docker image. This image is a lightweight version of the Colab runtime that can be run on your local machine. It includes all the necessary dependencies and libraries to run the notebooks.

### Connecting to Colab
Option 1. Colab Docker runtime image
Install Docker on your local machine. Note that europe-docker.pkg.dev and asia-docker.pkg.dev are alternative mirrors to us-docker.pkg.dev below. Downloads will be faster for users in those continents. The images are identical. Start a runtime:

        docker run -p 127.0.0.1:9000:8080 us-docker.pkg.dev/colab-images/public/runtime
      
For GPU support, with NVIDIA drivers and the NVIDIA container toolkit installed, use:

        docker run --gpus=all -p 127.0.0.1:9000:8080 us-docker.pkg.dev/colab-images/public/runtime
      
The image has been tested with NVIDIA T4, L4, and A100 GPUs.

Once the container has started, it will print a message with the initial backend URL used for authentication, of the form 'http://127.0.0.1:9000/?token=...'. Make a copy of this URL as you'll need to provide this for step 2 below.

Option 2. Jupyter runtime
Install Jupyter on your local machine. New notebook servers are started normally, though you will need to set a flag to explicitly trust WebSocket connections from the Colab frontend.

  jupyter notebook \
    --NotebookApp.allow_origin='https://colab.research.google.com' \
    --port=8888 \
    --NotebookApp.port_retries=0 \
    --NotebookApp.allow_credentials=True