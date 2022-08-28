#!/usr/bin/env python3

import csv
from pathlib import Path
import re
import shutil
from time import localtime, strftime, time 

from diffusers import StableDiffusionPipeline
import fire
import pandas as pd
import torch
import unicodedata

MODEL = "CompVis/stable-diffusion-v1-4"
GPU = "cuda"
CSV_FILENAME = "stablediffusion.info.csv"
OUTDIR = Path.cwd() / 'collected'

def get_imgfile_from_prompt(idx, textinput):
    return OUTDIR / f"{idx:05}-{slugify(textinput)}.png"

def save_info(**params):
    
    csvfile = OUTDIR / CSV_FILENAME
    write_mode = 'a' if csvfile.exists() else 'w'  
    header = False if write_mode == 'a' else True
    
    col2params = {'prompt': 'textinput', 'num_inference_steps': 'steps', 
                  'manual_seed': 'manualseed', 'generator_seed': 'seed',
                  'guidance_scale': 'scale'}
    
    if csvfile.exists():
        current = pd.read_csv(csvfile)
        idx = int(current.idx.max()) + 1
    else:
        idx = 0
    
    imgfile = get_imgfile_from_prompt(idx, params['textinput'])
    
    data = dict()
    data['idx'] = idx 
    data['filename'] = imgfile.name
    for colname in col2params.keys(): 
        paramname = col2params[colname]
        data[colname] = [params[paramname]]
    data['timestamp'] = int(time())
    
    df = pd.DataFrame(data)
    df.to_csv(csvfile, header=header, index=False, mode=write_mode, quoting=csv.QUOTE_NONNUMERIC)
    
    csv_status = "created" if write_mode == 'w' else "updated"
    print(f"CSV {csv_status}: {csvfile}")

    return imgfile
    

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def main(textinput, steps=15, manualseed=True, seed=1024, scale=7.5, over10gb=True):

    #import pydevd; pydevd.settrace()
    params = dict(**locals())   # needed for saving into info file

    if not over10gb:
        params.update({"torch_dtype": torch.float16, "revision": "fp16"})  # pylint: disable=no-member
        params.pop(over10gb)    # should not be in info file

    OUTDIR.mkdir(exist_ok=True)

    if not manualseed:
        generator = torch.Generator(GPU).seed() # pylint: disable=no-member
    else:
        generator = torch.Generator(GPU).manual_seed(seed)  # pylint: disable=no-member
    pipe = StableDiffusionPipeline.from_pretrained(MODEL, generator=generator, use_auth_token=True, **params)
    pipe = pipe.to(GPU)

    with torch.autocast(GPU):
        result = pipe(textinput) 
        print(f"Result: {result}")
        img = result["sample"][0]

    imgfile = save_info(**params)
    img.save(imgfile)
    print(f"SUCCESS: {imgfile}")

if __name__ == '__main__':
    fire.Fire(main)
