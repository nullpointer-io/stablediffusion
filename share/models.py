#!/usr/bin/env python3

from dataclasses import dataclass, field
import hashlib
import importlib
from pathlib import Path
import requests
import shutil


@dataclass
class ModelData:
    name: str
    type: str
    url: str
    hash: str
    projfile: str = field(init=False) 
    modfile: str = field(init=False)

    def _projfile(self):
        currentmod = Path(__file__)
        return currentmod.parent / self.type / f"{self.name}.pth"
    
    def _modfile(self):
        mod = importlib.import_module(self.type)
        modpath = Path(mod.__file__)
        moddir = modpath.parent / 'experiments' / 'pretrained_models'
        moddir.mkdir(parents=True, exist_ok=True)
        return moddir / f"{self.name}.pth"

    def __post_init__(self):
        self.projfile = self._projfile()
        self.modfile = self._modfile() 

## ------------- EDIT ----------------- ##

MODELS = [  ModelData('RealESRGAN_x4plus',
                      'realesrgan', 
                      'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
                      '4fa0d38905f75ac06eb49a7951b426670021be3018265fd191d2125df9d682f1'), 
            ModelData('RealESRGAN_x4plus_anime_6B',
                      'realesrgan',
                      'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth',
                      'f872d837d3c90ed2e05227bed711af5671a6fd1c9f7d7e91c911a61f155e99da'),
            ModelData('GFPGANv1.3',
                      'gfpgan',
                      'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
                      'c953a88f2727c85c3d9ae72e2bd4846bbaf59fe6972ad94130e23e7017524a70')
    ]

## --------------------------------- ##

def setup():

    for model in MODELS:
        model.projfile.parent.mkdir(parents=True, exist_ok=True)
        if not model.projfile.exists():
            print(f"Download missing model: {model.name}")
            with requests.get(model.url, stream=True) as r:
                with open(model.projfile, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print(f"Successfully downloaded: {model.name}")
        m = hashlib.sha256()
        m.update(model.projfile.read_bytes())
        if model.hash != m.hexdigest():
            raise SystemExit(f"Wrong digest: {model.projfile}")
        model.modfile.unlink(missing_ok=True)
        model.modfile.symlink_to(model.projfile)
        print(f"Model linked to: {model.modfile.parent}")

            
        

# FACEXLIB_FILES=(
#  'detection_Resnet50_Final.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth 6d1de9c2944f2ccddca5f5e010ea5ae64a39845a86311af6fdf30841b0a5a16d'  
#  'parsing_parsenet.pth https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth 3d558d8d0e42c20224f13cf5a29c79eba2d59913419f945545d8cf7b72920de2'
# )
