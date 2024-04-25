#
#
#
#
import os


#
#
#
#
mlx_deploy_path             = "/mlx-deploy/"
mlx_deploy_path_llama       = f"{mlx_deploy_path}llama.cpp/"
mlx_deploy_path_base_model  = f"{mlx_deploy_path}base-repo/"
mlx_deploy_path_lora         = f"{mlx_deploy_path}lora-repo/"


#
#
#
#
def build_llama_repo():
  if not os.path.exists(mlx_deploy_path_llama):
    print("Repo path does not exist")
    return

  if os.path.exists(f"{mlx_deploy_path_llama}/main"):
    print("Repo is already built")
    return

  # Check if make, g++ and gcc are installed
  if os.system("make --version") != 0:
    print("Make is not installed")
    os.system("sudo apt-get install make -y")

  if os.system("g++ --version") != 0:
    print("g++ is not installed")
    os.system("sudo apt-get install g++ -y")

  if os.system("gcc --version") != 0:
    print("gcc is not installed")
    os.system("sudo apt-get install gcc -y")

  os.system(f"cd {mlx_deploy_path_llama} && make -j")


#
#
#
#
def download_llama_repo():
  if not os.path.exists(mlx_deploy_path_llama):
    os.system(f"git clone https://github.com/ggerganov/llama.cpp.git {mlx_deploy_path_llama}")
  else:
    print("Llama.cpp already exists")
  build_llama_repo()


#
#
#
#
def download_lora(repo, token):
  os.system(f"rm -rf {mlx_deploy_path_lora}")
  os.system(f"huggingface-cli download {repo} --local-dir {mlx_deploy_path_lora} --local-dir-use-symlinks False --token {token}")
  # creating ggml-adapter-model.bin
  if not os.path.exists(f"{mlx_deploy_path_llama}convert-lora-to-ggml.py"):
    print("Llama.cpp is not built")
    return

  os.system(f"pip3 install -r {mlx_deploy_path_llama}requirements.txt")
  os.system(f"{mlx_deploy_path_llama}convert-lora-to-ggml.py {mlx_deploy_path_lora}")


#
#
#
#
def download_base_model(token):
  if os.path.exists(mlx_deploy_path_base_model):
    print("Base model is already downloaded")
    return
  else:
    print("Downloading base model...")

  ##### Only Download these files #####
  repo_files = [
  "README.md",
  "config.json",
  "generation_config.json",
  "ggml-model-f16.gguf",
  "model-00001-of-00002.safetensors",
  "model-00002-of-00002.safetensors",
  "model.safetensors.index.json",
  "special_tokens_map.json",
  "tokenizer.json",
  "tokenizer.model",
  "tokenizer_config.json",
  ]

  os.system(f"huggingface-cli download google/gemma-2b {' '.join(repo_files)} --local-dir {mlx_deploy_path_base_model} --local-dir-use-symlinks False --token {token}")

  if os.path.exists(f"{mlx_deploy_path_base_model}model.gguf"):
    print("Model is already converted")
    return
  else:
    print("Converting model to gguf...")

  os.system(f"pip3 install -r {mlx_deploy_path_llama}requirements.txt")
  os.system(f"{mlx_deploy_path_llama}convert-hf-to-gguf.py {mlx_deploy_path_base_model} --outfile {mlx_deploy_path_base_model}model.gguf --outtype f16")


#
#
#
#
def merge_gguf():
  if not os.path.exists(f"{mlx_deploy_path_base_model}model.gguf"):
    print("Base model is not downloaded")
    return
  if not os.path.exists(f"{mlx_deploy_path_lora}ggml-adapter-model.bin"):
    print("Lora model is not downloaded")
    return
  if not os.path.exists(f"{mlx_deploy_path_llama}export-lora"):
    print("Llama.cpp is not built")
    return
  if os.path.exists(f"{mlx_deploy_path}model.gguf"):
    print("Merged model is already created")
    return
  os.system(f"{mlx_deploy_path_llama}export-lora -m {mlx_deploy_path_base_model}model.gguf -l {mlx_deploy_path_lora}ggml-adapter-model.bin -o {mlx_deploy_path}model.gguf")


#
#
#
#
def main():

  #
  #
  #
  #
  token     = os.getenv("HF_TOKEN")
  lora_repo = os.getenv("LORA_REPO")

  #
  #
  #
  #
  ##### Token #####
  if token is None:
    print("HF_TOKEN is not set")
    return

  ##### LoRa #####
  if lora_repo is None:
    print("LORA_REPO is not set")
    return

  #
  #
  #
  #
  print("STEP 1: Downloading Llama.cpp")
  download_llama_repo()

  print("STEP 2: Downloading Base Model")
  download_base_model(token)

  print("STEP 3: Downloading LoRa Adapter")
  download_lora(lora_repo, token)

  print("STEP 4: Merge them into a GGUF")
  merge_gguf()


if __name__ == "__main__":
  main()