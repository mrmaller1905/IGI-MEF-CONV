import os 
import numpy as np
from .import reader_ilff
from .import mef_struct
from .mef_struct import *
from .reader_ilff import *

def fromfile(meffilename, srcpth):
    
    meftext = ""
    
    reader = reader_ilff.open(srcpth)


# Model Name

    meftext += "\n\\\ Model Name \n\n"   
    meftext +=  "[(\"" + str(os.path.basename(meffilename)) + "\")]"   
    meftext += "\n\n"     
    
    hsem = parse_hsem(reader.read(b'HSEM'))

# Mesh info

    meftext += "\n\\\ Mesh info \n\n"   
    meftext +=  str(hsem)   
    meftext += "\n\n"
    
    atta = str(parse_atta(reader.read(b'ATTA'))).replace(") ",")\n ")

# attachments

    meftext += "\n\\\ Attachments \n\n"   
    meftext +=  str(atta)   
    meftext += "\n\n"       
    
    xtvm = str(parse_xtvm(reader.read(b'XTVM'))).replace(") ",")\n ")

# Magic Vertices     

    meftext += "\n\\\ Magic vertices \n\n"   
    meftext +=  str(xtvm)   
    meftext += "\n\n"
    
    trop = str(parse_trop(reader.read(b'TROP'))).replace(") ",")\n ")

# Portal Define

    meftext += "\n\\\ Portal defs \n\n"   
    meftext +=  str(trop)   
    meftext += "\n\n"   
    
    xvtp = str(parse_xvtp(reader.read(b'XVTP'))).replace(") ",")\n ")

# Portal Vertices

    meftext += "\n\\\ Portal Vertices \n\n"   
    meftext +=  str(xvtp)   
    meftext += "\n\n"           
    
    cftp = str(parse_cftp(reader.read(b'CFTP'))).replace(") ",")\n ")

# Portal Faces

    meftext += "\n\\\ Portal Faces \n\n"   
    meftext +=  str(cftp)   
    meftext += "\n\n"

    if reader.find(b'WOLG'):
        
        wolg = str(parse_wolg(reader.read(b'WOLG'))).replace(") ",")\n ")

#  Glows            

        meftext += "\n\\\ Glow Sprites \n\n"   
        meftext +=  str(wolg)   
        meftext += "\n\n"
    
    d3dr = parse_d3dr(reader.read(b'D3DR'),0)

# Render Mesh 

    meftext += "\n\\\ Render Mesh \n\n"   
    meftext +=  str(d3dr)   
    meftext += "\n\n"
    
    dner = str(parse_dner(reader.read(b'DNER'),0)).replace(") ",")\n ")

# Render Mesh Define

    meftext += "\n\\\ Render Mesh Define \n\n"   
    meftext +=  str(dner)   
    meftext += "\n\n"               

    ecaf = parse_ecaf(reader.read(b'ECAF'))

# Render Mesh Faces

    meftext += "\n\\\ Render Mesh Faces \n\n"   
    meftext +=  str(ecaf)   
    meftext += "\n\n"
    
    xtrv = str(parse_xtrv(reader.read(b'XTRV'),0)).replace(") ",")\n ")

# Render Mesh Vertices

    meftext += "\n\\\ Render Mesh Vertices \n\n"   
    meftext +=  str(xtrv)   
    meftext += "\n\n"                       
    
    if reader.find(b'HSMC'):
    
        hsmc = parse_hsmc(reader.read(b'HSMC'))

# Collision Mesh 

        meftext += "\n\\\ Collision Mesh \n\n"   
        meftext +=  str(hsmc)   
        meftext += "\n\n"                
    
        xtvc = str(parse_xtvc(reader.read(b'XTVC'),0)).replace(") ",")\n ")

# Collision Mesh Vertices - 0

        meftext += "\n\\\ Collision Mesh Vertices - 0 \n\n"   
        meftext +=  str(xtvc)   
        meftext += "\n\n"                            
    
        ecfc = parse_ecfc(reader.read(b'ECFC'))

# Collision Mesh Faces - 0

        meftext += "\n\\\ Collision Mesh Faces - 0 \n\n"   
        meftext +=  str(ecfc)   
        meftext += "\n\n"        
    
        tamc = str(parse_tamc(reader.read(b'TAMC'))).replace(") ",")\n ")

# Collision Mesh Materials - 0

        meftext += "\n\\\ Collision Mesh Materials - 0 \n\n"   
        meftext +=  str(tamc)   
        meftext += "\n\n"
     
        hpsc = str(parse_hpsc(reader.read(b'HPSC'))).replace(") ",")\n ")
                
# Collision Mesh Sphere - 0

        meftext += "\n\\\ Collision Mesh Sphere - 0 \n\n"   
        meftext +=  str(hpsc)   
        meftext += "\n\n"                             
        
        xtvc1 = str(parse_xtvc(reader.read(b'XTVC',1),0)).replace(") ",")\n ")

# Collision Mesh Vertices - 1

        meftext += "\n\\\ Collision Mesh Vertices - 1 \n\n"   
        meftext +=  str(xtvc1)   
        meftext += "\n\n"      
    
        ecfc1 = parse_ecfc(reader.read(b'ECFC',1))

# Collision Mesh Faces - 1

        meftext += "\n\\\ Collision Mesh Faces - 1 \n\n"   
        meftext +=  str(ecfc1)   
        meftext += "\n\n"                                  
    
        tamc1 = str(parse_tamc(reader.read(b'TAMC',1))).replace(") ",")\n ")

# Collision Mesh Materials - 1

        meftext += "\n\\\ Collision Mesh Materials - 1 \n\n"   
        meftext +=  str(tamc1)   
        meftext += "\n\n"                         
    
        hpsc1 = str(parse_hpsc(reader.read(b'HPSC',1))).replace(") ",")\n ")

# Collision Mesh Sphere - 1

        meftext += "\n\\\ Collision Mesh Sphere - 1 \n\n"   
        meftext +=  str(hpsc1)   
        meftext += "\n\n"

# Morph Vertices

    if reader.find(b'HPRM'):

        hprm1 = parse_hprm(reader.read(b'HPRM'))[0]
        hprm2 = parse_hprm(reader.read(b'HPRM'))[1]
        hprm2 = str(hprm2).replace(") ",")\n ")

        meftext += "\n\\\ Morph Vertices \n\n"
        meftext +=  str(hprm1)
        meftext += "\n"
        meftext +=  str(hprm2)
        meftext += "\n\n"
        
# Unknown symbol TXAN

    if reader.find(b'TXAN'):
         
        txan = parse_txan(reader.read(b'TXAN'))    

        meftext += "\n\\\ TXAN \n\n"
        meftext +=  str(txan)
        meftext += "\n\n"
    
    return meftext
