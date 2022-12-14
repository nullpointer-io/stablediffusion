# stablediffusion
Scripts to use the Stable Diffusion AI to create images from a textual description.

## Disclaimers

This script is without bells and whistles. But it has some features like:
- Collecting images in a directory and store accompanying information in a CSV file.  
- A companion script for scaling the created images also with AI support.

I have used these scripts:
- On a Linux operating system 
- With Python 3.9.7 
- Together with Nvidia GPU RTX 3060 (12 GB GPU RAM)
- And 15 GB RAM.

**Note**: If the process of generating the image dies then it was running out of memory. Maybe closing some other programs can free 
enough memory to avoid it. Observe your memory with **htop** or **top** when necessary.

## Prerequisites

Before pulling files from obscure internet sources it is worthwhile to follow the instructions of the original Stable Diffuser project. There are not too many steps to accomplish and it is easily done.

1. Register at https://huggingface.co/ and confirm your registration with the link sent by email.
2. Login to huggingface.co and access the AI model: https://huggingface.co/CompVis/stable-diffusion-v1-4
3. Confirm the license of the model. The license ensures that output of the AI model is not used in an irresponsible way.
4. Go to your profile settings on huggingface.co and generate a user token. Secure this token locally. For example, use a password manager. 
5. Optional: Before leaving huggingface.co, you may join a user group (organization) to share resources.

Now you are ready for your the command line. This script expects that your computer has a GPU with CUDA abilities.

## Install

Download this repository from Github:
```
git clone https://github.com/nullpointer-io/stablediffusion.git
``` 

Change into the directory: 
```
cd ./stablediffusion
```

Install the necessary Python libraries. The incorporated torch library must be matched with the CUDA version of your GPU. Note: The 
size of the torch library for CUDA 11.6 is around 2 GB for example.
```
pip install -r requirements.cuda116.txt	  # CUDA 11.6 
pip install -r requirements.cuda113.txt   # CUDA 11.3
pip install -r requirements.cuda102.txt   # CUDA 10.2
```

**Recommendation:** To avoid clutter of Python libraries on your computer you should use tools like pyenv and/or pipenv.  

## Execute

Login to huggingface.co via the huggingface command line interface. 
```
huggingface-cli login
```
When prompted paste your user token which has been created before. Don't be irritated when the pasted token is not visible on 
the command line. 

**Be warned:** For the initial run gigabytes of data will be downloaded. Take the opportunity and grab some coffee, water or tea. 

### GPU RAM

Based on your amount of GPU RAM there are two options to execute the script. 

a. Create an image with a GPU over 10 GB RAM.
```
./text2image.py "a chair in the shape of an avacado"
```
b. Create an image with a GPU less than 10 GB RAM. 
```
./text2image.py "a chair in the shape of an avacado" --over10gb=False
```
To scale the image with AI support use image2scale.py. See related chapter

### Output

Images are stored as PNG files into the subdirectory **collected**. The used parameter set for the image generation is written 
to CSV. The CSV file resides in the same directory like the images. The prefix of an image file corresponds to the index
in the CSV file. In this way every image is preserved and will not be overwritten. 

Thus it is possible to easily create series of images:
```
for i in $(seq 1 50); do ./text2image.py "a chair in the shape of an avacado" --steps=$i; done
```

### Parameters

The image quality and output can be controlled by parameters:
```
--steps=STEPS	(Default: 15) 	-> Number of Inference Steps
--seed=SEED 	(Default: 1024) -> Manual Generator Seed
--manualseed=MANUALSEED (Default: True) -> Enable or Disable the Manual Generator Seed
--scale=SCALE 	(Default: 7.5) 	-> Guidance Scale
```

Example:
```
./text2image.py "a chair in the shape of an avacado" --steps=50 --scale=2.5 --manualseed=False
```
In reference [^2] the parameters are described in detail. 

## Scale the Images

Use the script `image2scale.py` to increase the size of images with AI support. 
At the first run the models are downloaded. The integrity of the models is verified 
by hash. The expected hashes and source URLs are configured in `share/models.py`.

The script `image2scale.py` is some sort of wrapper around the original script:
https://raw.githubusercontent.com/xinntao/Real-ESRGAN/v0.2.5.0/inference_realesrgan.py 
Adding the integrity check and adapting the output paths to this project. 
Note: The code of the original script are the functions main and parse_args.

In the most cases you only have to execute:
```
./image2scale.py -i collected/00001-a-chair-in-the-shape-of-an-avacado.png
```
The result wil be stored the sub directory `scaled`. 

Execute the script with `-h` to inspect possible arguments.

## References

This script is based on information from the references [^1] [^2] [^3] [^4].

[^1]: https://huggingface.co/CompVis/stable-diffusion-v1-4
[^2]: https://huggingface.co/blog/stable_diffusion
[^3]: https://www.heise.de/news/Text-zu-Bild-Revolution-Stable-Diffusion-ermoeglicht-KI-Bildgenerieren-fuer-alle-7244307.html
[^4]: https://pytorch.org/get-started/locally/
