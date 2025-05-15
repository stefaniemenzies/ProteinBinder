# ProteinBinder

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