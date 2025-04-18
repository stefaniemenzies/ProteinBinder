#@title setup **RFdiffusion** (~3min)
import os, time, signal
import sys, random, string, re
from PysmartDL import *
from PysmartDL import SmartDL
import tarfile
import zipfile

if not os.path.isdir("RFdiffusion"):
  print("installing RFdiffusion...")
  
  url = "https://files.ipd.uw.edu/krypton/ananas"
  dest = os.path.join(os.getcwd(), "ananas")
  downloader = SmartDL(url, dest)
  downloader.start()
  os.system("chmod +x ananas")

os.makedirs("params", exist_ok=True)

# send param download into background
urls = [
  "https://files.ipd.uw.edu/krypton/schedules.zip",
  "http://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt",
  "http://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt",
  "http://files.ipd.uw.edu/pub/RFdiffusion/f572d396fae9206628714fb2ce00f72e/Complex_beta_ckpt.pt",
  "https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar"
]
os.makedirs("RFdiffusion/models", exist_ok=True)
for url in urls:
  dest_dir = os.getcwd()

  if url.endswith(".pt"):
    dest_dir = os.path.join(dest_dir, "RFdiffusion", "models")
  downloader = SmartDL(url, dest_dir)
  downloader.start()

# Extract the alphafold parameters tar file
tar_path = os.path.join(dest_dir, "alphafold_params_2022-12-06.tar")
with tarfile.open(tar_path, "r") as tar:
  tar.extractall(path="params")

# Create a done.txt file to indicate completion
with open("params/done.txt", "w") as f:
  f.write("Download and extraction complete.")

# Extract the schedules.zip file
with zipfile.ZipFile("schedules.zip", 'r') as zip_ref:
  zip_ref.extractall()
os.remove("schedules.zip")



if 'RFdiffusion' not in sys.path:
  os.environ["DGLBACKEND"] = "pytorch"
  sys.path.append('RFdiffusion')