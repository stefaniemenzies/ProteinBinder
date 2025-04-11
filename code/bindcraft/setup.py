#@title Installation
import os, time, gc, io
import contextlib
import json
from datetime import datetime
from ipywidgets import HTML, VBox
from IPython.display import display
import subprocess
import tarfile
def install_bindcraft_components():
    """
    Install BindCraft components and download AlphaFold parameters if not already installed.
    """
    # Check if BindCraft components are already installed
    if not os.path.isfile("bindcraft/params/done.txt"):
        print("Installing required BindCraft components")
        print("Pulling BindCraft code from Github")
        os.makedirs('bindcraft/', exist_ok=True)
        if not os.path.isdir("bindcraft/.git"):
            os.system("git submodule add https://github.com/martinpacesa/BindCraft bindcraft/")
        os.system("git submodule update --init --recursive")
        os.system("chmod +x bindcraft/functions/dssp")
        os.system("chmod +x bindcraft/functions/DAlphaBall.gcc")

        print("Installing ColabDesign")
        import urllib.request
        # Ensure AlphaFold params are downloaded
        if not os.path.isfile("bindcraft/params/done.txt"):
            print("Downloading AlphaFold params")
                
            os.makedirs("bindcraft/params", exist_ok=True)
            # Download AlphaFold params using urllib
            url = "https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar"
            tar_path = "alphafold_params_2022-12-06.tar"
            print("Downloading AlphaFold params...")
            urllib.request.urlretrieve(url, tar_path)

            # Extract the tar file
            print("Extracting AlphaFold params...")
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(path="bindcraft/params")

            # Create the done.txt file
            with open("bindcraft/params/done.txt", "w") as f:
                f.write("")

            # Clean up the tar file
            os.remove(tar_path)
      
        print("BindCraft installation is finished, ready to run!")
    else:
        print("BindCraft components already installed, ready to run!")

if __name__ == "__main__":
    install_bindcraft_components()