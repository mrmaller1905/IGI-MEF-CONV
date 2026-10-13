import os 
import numpy as np
from .import reader_form
from .import mtp_struct
from .reader_form import *
from .mtp_struct import *


def fromFile(dir,srcpath):

    qsctext = "\n\\* MTP FILE DECODED DATA \n\n\n"

    reader = reader_form.open(srcpath)

    banm_bytes = reader.read(b'BANM')
    banm = parse_banm(banm_bytes)

    snds_bytes = reader.read(b'SNDS')
    snds = parse_snds(snds_bytes)

    svol_bytes = reader.read(b'SVOL')
    svol = parse_svol(svol_bytes)

    mods_bytes = reader.read(b'MODS')
    mods = parse_mods(mods_bytes)

    vnam_bytes = reader.read(b'VNAM')
    vnam = parse_vnam(vnam_bytes)

    inst_bytes = reader.read(b'INST')
    inst = parse_inst(inst_bytes)

    texf_bytes = reader.read(b'TEXF')
    texf = parse_texf(texf_bytes)

    palf_bytes = reader.read(b'PALF')
    palf = parse_palf(palf_bytes)

    gtts_bytes = reader.read(b'GTT ')
    gtts = parse_gtts(gtts_bytes)

#--------------------------------------------

# Animations     

    qsctext += "\n\\\ Animations (.iff) \n\n"
    qsctext +=  str(banm[0])    
    qsctext += "\n" 
    qsctext +=  str(banm[1]) 
    qsctext += "\n\n\n"

# Sounds    

    qsctext += "\n\\\ Sounds (.wav) \n\n"
    qsctext +=  str(snds[0])   
    qsctext += "\n" 
    qsctext +=  str(snds[1])  
    qsctext += "\n\n\n"

# Shadows    

    qsctext += "\n\\\ Shadows (.mef) \n\n"  
    qsctext +=  str(svol[0])   
    qsctext += "\n" 
    qsctext +=  str(svol[1])  
    qsctext += "\n\n\n"

# Models    

    qsctext += "\n\\\ Models (.mef) \n\n"
    qsctext +=  str(mods[0])    
    qsctext += "\n" 
    qsctext +=  str(mods[1])   
    qsctext += "\n\n\n"

# Virtual names   

    qsctext += "\n\\\ Virtual Names \n\n"
    qsctext +=  str(vnam[0])
    qsctext += "\n" 
    qsctext +=  str(vnam[2])   
    qsctext += "\n\n\n"

# Installed tex info

    qsctext += "\n\\\ Model-Texture Info \n\n"
    qsctext += "["+str(inst[0])+"]" 
    qsctext += "\n" 
    qsctext +=  str(inst[1])   
    qsctext += "\n\n\n"

# Textures  

    qsctext += "\n\\\ Textures (.tex) \n\n"
    qsctext +=  str(texf[0])   
    qsctext += "\n" 
    qsctext +=  str(texf[1])   
    qsctext += "\n\n\n"

# Palletes  

    qsctext += "\n\\\ Palletes (.pal) \n\n"
    qsctext +=  str(palf[0])   
    qsctext += "\n" 
    qsctext +=  str(palf[1])   
    qsctext += "\n\n\n"

# GTT-unknown

    qsctext += "\n\\\ GameTypeTexture (GTT) \n\n"
    qsctext +=  str(gtts[0])   
    qsctext += "\n" 
    qsctext +=  str(gtts[1])   
    qsctext += "\n\n\n"



    return qsctext
