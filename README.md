# stablediffusion-script
Use Stable Diffusion AI to create an image from a textual description.

## Disclaimers

This script is without bells and whistles and has been used:
- on a Linux operation system 
- with Python 3.9.7 
- and Nvidia GPU RTX 3060 (12 GB GPU RAM).

## Prerequisites

1. Register at https://huggingface.co/ and confirm your registration with the link sent by email.
2. Log-in to huggingface.co and head over to following AI model: https://huggingface.co/CompVis/stable-diffusion-v1-4
3. Confirm the license of this model. The license ensures that output of the AI model is not used in an irresponsible way.  
4. Got to the user settings on huggingface.co and generate a user token. Secure this token locally. For example, you can use a password manager. 
5. Optional: Before leaving the huggingface.co web page, you may join an user group (organization) to share resources.

Now you are ready for your workstation. This script expects that your workstation has a GPU with Cuda abilities.

## Install

Download this repository from Github:
```
git clone https://github.com/nullpointer-io/tryout-stablediffusion.git
``` 

Change into the directory: 
```
cd ./tryout-stablediffusion
```

Install Python libraries.
```
pip install requirements.txt
```

**Recommendation**
To avoid clutter of Python libraries on your workstation you should use tools like pyenv and/or pipenv.  

## Execute

Log-in to huggingface.co by the using the huggingface command line program. 
```
huggingface-cli login
```
When prompted paste your user token created before. Don't be irritated when the pasted token is not visible on the command line. 

**Be warned for the initial run** of the script. Gigabytes of data will be downloaded at first.  

Based on your amount of GPU RAM there are to options to execute the script. 

a. Create image from text with GPU over 10 GB RAM.
```
./stablediffusion.py "What happened to Il signor Rossi cerca la felicità"
```
b. Create image from text with GPU less than 10 GB RAM. 
```
./stablediffusion.py "What happened to Il signor Rossi cerca la felicità"` --less10gb=True
```

## References

- https://huggingface.co/CompVis/stable-diffusion-v1-4
- https://huggingface.co/blog/stable_diffusion
- https://www.heise.de/news/Text-zu-Bild-Revolution-Stable-Diffusion-ermoeglicht-KI-Bildgenerieren-fuer-alle-7244307.html
