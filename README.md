# tryout-stablediffusion
Simple script to explore the Stable Diffusion AI to create an image from a textual description.

## Disclaimers

This script is without bells and whistles and has been used:
- on a Linux operating system 
- with Python 3.9.7 
- together with Nvidia GPU RTX 3060 (12 GB GPU RAM)
- and 15 GB RAM.

**Note**: If the process of generating the image dies then it was running out of memory. Maybe closing some other programs can free enough memory to avoid it. Observe your memory with **htop** or **top** when necessary.

## Prerequisites

1. Register at https://huggingface.co/ and confirm your registration with the link sent by email.
2. Log-in to huggingface.co and access following AI model: https://huggingface.co/CompVis/stable-diffusion-v1-4
3. Confirm the license of this model. The license ensures that output of the AI model is not used in an irresponsible way.  
4. Go to your profile settings on huggingface.co and generate a user token. Secure this token locally. For example, use a password manager. 
5. Optional: Before leaving huggingface.co, you may join a user group (organization) to share resources.

Now you are ready for your the command line. This script expects that your computer has a GPU with CUDA abilities.

## Install

Download this repository from Github:
```
git clone https://github.com/nullpointer-io/tryout-stablediffusion.git
``` 

Change into the directory: 
```
cd ./tryout-stablediffusion
```

Install the necessary Python libraries. They include the torch library which must be matched with the CUDA version of your GPU. The size for the CUDA 11.x specific torch version is around 2 GB. In case of the proprietary Nvidia drivers on Linux the CUDA version can be evaluated with `nvidia-smi`.
```
pip install -r requirements.cuda116.txt	  # CUDA 11.6 
pip install -r requirements.cuda113.txt   # CUDA 11.3
pip install -r requirements.cuda102.txt   # CUDA 10.2
```

**Recommendation:** To avoid clutter of Python libraries on your workstation you should use tools like pyenv and/or pipenv.  

## Execute

Log-in to huggingface.co by the using the huggingface command line program. 
```
huggingface-cli login
```
When prompted paste your user token created before. Don't be irritated when the pasted token is not visible on the command line. 

**Be warned:** For the initial run of the script gigabytes of data will be downloaded at first. Take the opportunity and drink some coffee in the meantime. 

### Mind the GPU RAM

Based on your amount of GPU RAM there are to options to execute the script. 

a. Create image from text with GPU over 10 GB RAM.
```
./stablediffusion.py "a photograph of an astronaut riding a horse"
```
b. Create image from text with GPU less than 10 GB RAM. 
```
./stablediffusion.py "a photograph of an astronaut riding a horse" --over10gb=False
```

### Furhter Parameters

The image quality and output can be controlled by parameters:
```
--steps=STEPS	(Default: 15) 	-> Number of Inference Steps  
--seed=SEED 	(Default: 1024) -> Manual Generator Seed
--manualseed=MANUALSEED (Default: True) -> Enable or Disable the Manual Generator Seed
--scale=SCALE 	(Default: 7.5) 	-> Guidance Scale
```

Example:
```
./stablediffusion.py "a photograph of an astronaut riding a horse" --steps=50 --manualseed=False
```

In reference [^2] the parameters are described in detail. 

[^1]: https://huggingface.co/CompVis/stable-diffusion-v1-4
[^2]: https://huggingface.co/blog/stable_diffusion
[^3]: https://www.heise.de/news/Text-zu-Bild-Revolution-Stable-Diffusion-ermoeglicht-KI-Bildgenerieren-fuer-alle-7244307.html
