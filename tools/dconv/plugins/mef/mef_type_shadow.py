import os 
import numpy as np
from .import reader_ilff
from .import mef_struct
from .mef_struct import *
from .reader_ilff import *

def fromfile(meffilename,srcpth):
    
    meftext = ""
    
    reader = reader_ilff.open(srcpth)

    NameOfModel = str(os.path.basename(meffilename))

# NameOfModel

    meftext += "\n\\\ Model Name \n\n"   
    meftext += "[(\"" + str(NameOfModel) + "\")]"   
    meftext += "\n\n"
    
    sems = str(parse_sems(reader.read(b'SEMS'))).replace(") ",")\n ")

# Mesh Info 

    meftext += "\n\\\ Mesh Info \n\n"   
    meftext +=  str(sems)   
    meftext += "\n\n"
    
    xtvs = str(parse_xtvs(reader.read(b'XTVS'))).replace(") ",")\n ")

# Vertices  

    meftext += "\n\\\ Vertices \n\n"   
    meftext +=  str(xtvs)   
    meftext += "\n\n" 
    
    cafs = str(parse_cafs(reader.read(b'CAFS'))).replace(") ",")\n ")

# Faces

    meftext += "\n\\\ Faces \n\n"   
    meftext +=  str(cafs)   
    meftext += "\n\n"

    egde = parse_egde(reader.read(b'EGDE'))
    
# Egdes
    
    meftext += "\n\\\ Egdes \n\n"   
    meftext +=  str(egde)   
    meftext += "\n\n"
    
    
    return meftext
