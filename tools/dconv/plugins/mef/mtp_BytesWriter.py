import os 
import numpy as np
from .import mtp_mtx_reader
from .mtp_mtx_reader import *

def CalSize(Size):
    B = struct.pack('=1I',Size)
    Sz = struct.pack('=4B',B[3],B[2],B[1],B[0])
    return struct.unpack('=1I',Sz)[0]

def CalOff(Size):
    Bytes = b''
    Num = 4-(Size % 4)
    if ( Num != 4 ):
     for i in range ( 0 , Num ):
      Bytes += b'\x00'
    return Bytes


def fromFile(dir,srcpath):

    Bytes = b'FORM'

    DATA = mtp_mtx_reader.read(srcpath)

    banm_data = DATA[0][1]
    banm_size = DATA[0][0]

    snds_data = DATA[1][1]
    snds_size = DATA[1][0]

    svol_data = DATA[2][1]
    svol_size = DATA[2][0]

    mods_data = DATA[3][1]
    mods_size = DATA[3][0]

    vnam_data = DATA[4][1]
    vnam_size = DATA[4][0]

    inst_data = DATA[5][1]
    inst_size = DATA[5][0]

    texf_data = DATA[6][1]
    texf_size = DATA[6][0]

    palf_data = DATA[7][1]
    palf_size = DATA[7][0]

    gtts_data = DATA[8][1]
    gtts_size = DATA[8][0]


# -------------------------------------------- Parsing Data

    Set = []

    for i in range ( 0 , len(gtts_data) // 2 ):

        Set.append([ gtts_data[2*i+0] , gtts_data[2*i+1] ])

    gtts_Data = Set
    

    Set = []

    n = -1

    while ( n+1 < len(inst_data) ):

        n += 1

        S = []

        S.append(inst_data[n])

        S.append(inst_data[n+1])

        for i in range ( 0 , inst_data[n+1] ):

            S.append(inst_data[i+n+2])

        n += inst_data[n+1]+1

        Set.append(S)

    inst_Data = Set

# ---------------------------------------------- Checks

    
    if ( len(banm_data) != banm_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in Anim Header"
                
    if ( len(snds_data) != snds_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in Sounds Header" 
                
    if ( len(svol_data) != svol_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in Shadow models Header" 
                
    if ( len(mods_data) != mods_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in Models Header" 
                
    if ( len(vnam_data) != vnam_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in Virtual Name Header" 
                
    if ( len(inst_Data) != inst_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in Model-Texture Info Header" 
                
    if ( len(texf_data) != texf_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in Textures Header" 
                
    if ( len(palf_data) != palf_size[0]  ):
                assert 0 == 0 , "Wrong Size Given in Palletes Header" 
                
    if ( len(gtts_Data) != gtts_size[0]  ):
                assert 0 != 0 , "Wrong Size Given in GameTypeTexture Header"


#-----------------------------------------------<


# ---------------------------------------------->




#------------------------------------------------>

    form_bytes = b'FORM'

    SIZE = 0

    X = 0
                
#--------------------------------------------Anims


    banm_bytes = b'BANM'

    data = banm_data
    size = banm_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(data) ):

        for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1s', bytes(data[i][j],'utf-8'))

        Bytes += b'\x00'

    Bytes += CalOff(len(Bytes))

    banm_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(banm_bytes)
    
                
#--------------------------------------------Sounds


    snds_bytes = b'SNDS'

    data = snds_data
    size = snds_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(data) ):

        for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1s', bytes(data[i][j],'utf-8'))

        Bytes += b'\x00'

    Bytes += CalOff(len(Bytes))

    snds_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(snds_bytes)

            
#--------------------------------------------Shadows


    svol_bytes = b'SVOL'

    data = svol_data
    size = svol_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(data) ):

        for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1s', bytes(data[i][j],'utf-8'))

        Bytes += b'\x00'

    Bytes += CalOff(len(Bytes))

    svol_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(svol_bytes)

            
#--------------------------------------------Models


    mods_bytes = b'MODS'

    data = mods_data
    size = mods_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(data) ):

        for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1s', bytes(data[i][j],'utf-8'))

        Bytes += b'\x00'

    Bytes += CalOff(len(Bytes))

    mods_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(mods_bytes)

            
#--------------------------------------------Textures


    texf_bytes = b'TEXF'

    data = texf_data
    size = texf_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(data) ):

        for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1s', bytes(data[i][j],'utf-8'))

        Bytes += b'\x00'

    Bytes += CalOff(len(Bytes))

    texf_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(texf_bytes)

            
#--------------------------------------------palletes


    palf_bytes = b'PALF'

    data = palf_data
    size = palf_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(data) ):

        for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1s', bytes(data[i][j],'utf-8'))

        Bytes += b'\x00'

    Bytes += CalOff(len(Bytes))

    palf_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(palf_bytes)

            
#--------------------------------------------GTT


    gtts_bytes = b'GTT '

    data = gtts_Data
    size = gtts_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(data) ):

         Bytes += struct.pack('=1I1i', data[i][0],data[i][1])

    gtts_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(gtts_bytes)

            
#--------------------------------------------Model-Texture Info


    inst_bytes = b'INST'

    data = inst_Data
    size = inst_size[0]

    Bytes = b''

    for i in range ( 0 , len(data) ):

      for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1I', data[i][j])

    inst_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(inst_bytes)
    
                
#--------------------------------------------Virtual Models
 

    vnam_bytes =  b'VNAM'

    data = vnam_data
    size = vnam_size[0]

    Bytes = struct.pack('=1I',size)

    for i in range ( 0 , len(inst_Data) ):

        Bytes += struct.pack('=1I', X)

        X += ((len(inst_Data[i])-1)*4)
                       
    for i in range ( 0 , len(data) ):

        for j in range ( 0 , len(data[i]) ):

         Bytes += struct.pack('=1s', bytes(data[i][j],'utf-8'))

        Bytes += b'\x00'

    Bytes += CalOff(len(Bytes))

    vnam_bytes += struct.pack('=1I',CalSize(len(Bytes))) + Bytes

    SIZE += len(vnam_bytes)
    
                
#--------------------------------------------

    form_bytes += struct.pack('=1I',CalSize(SIZE+4)) + b'MTP '

#--------------------------------------------

    Bytes = form_bytes

# Animations     

    Bytes += banm_bytes

# Sounds      

    Bytes += snds_bytes

# Shadows      

    Bytes += svol_bytes

# Models      

    Bytes += mods_bytes

# Virtual names     

    Bytes += vnam_bytes

# Installed tex info  

    Bytes += inst_bytes

# Textures    

    Bytes += texf_bytes

# Palletes    

    Bytes += palf_bytes

# GameTypeTexture 

    Bytes += gtts_bytes


    return Bytes
