import os 
import numpy as np

D_COUNT = np.dtype([
	('count', np.uint32),
	])

D_INST = np.dtype([
	('_001', np.uint32),
	])

D_INFT = np.dtype([
	('_001', np.uint32),
	('_002', np.uint32),
	])

D_GTTS = np.dtype([
	('id', np.uint32),
	('typ', np.int32),
	])

def parse_banm(banm_bytes):
    
    R1 = np.frombuffer(banm_bytes[:4],D_COUNT)                       
    R2 = []
    Tp = ""           
    for i in range ( 4 , len(banm_bytes) ):  
     if ( banm_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R2.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(banm_bytes[i:i+1],(np.string_, 1)))[3:-2]
    return R1['count'],R2

def parse_snds(snds_bytes):
    
    R1 = np.frombuffer(snds_bytes[:4],D_COUNT)             
    R2 = []
    Tp = ""             
    for i in range ( 4 , len(snds_bytes) ):
     if ( snds_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R2.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(snds_bytes[i:i+1],(np.string_, 1)))[3:-2]
    return R1['count'],R2

def parse_svol(svol_bytes):
    
    R1 = np.frombuffer(svol_bytes[:4],D_COUNT)          
    R2 = []
    Tp = ""          
    for i in range ( 4 , len(svol_bytes) ):
     if ( svol_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R2.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(svol_bytes[i:i+1],(np.string_, 1)))[3:-2]
    return R1['count'],R2

def parse_mods(mods_bytes):
    
    R1 = np.frombuffer(mods_bytes[:4],D_COUNT)            
    R2 = []
    Tp = ""            
    for i in range ( 4 , len(mods_bytes) ):
     if ( mods_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R2.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(mods_bytes[i:i+1],(np.string_, 1)))[3:-2]
    return R1['count'],R2


def parse_vnam(vnam_bytes):

    R1 = np.frombuffer(vnam_bytes[:4],D_COUNT)
    X1 = R1['count'][0]
    R2 = np.frombuffer(vnam_bytes[4:4+(4*X1)],D_COUNT)
    X2 = 4+(4*X1)
    R3 = []
    Tp = ""            
    for i in range ( X2 , len(vnam_bytes) ):
     if ( vnam_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R3.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(vnam_bytes[i:i+1],(np.string_, 1)))[3:-2]
    return R1['count'],R2,R3

def parse_inst(inst_bytes):

    R = ""
    X = 0
    Rn = 0
    Rx = []
    Ry = []
    while ( X != len(inst_bytes) ):
        
        R1 = np.frombuffer(inst_bytes[X:X+8],D_INFT)
        Y = R1['_002'][0]
        R2 = np.frombuffer(inst_bytes[X+8:X+(Y*4)+8],D_INST)
        X = X+(Y*4)+8
        R += str(R1) + str(R2) + '\n'
        Rx.append(R1)
        Ry.append(R2)
        Rn += 1
    if ( R == "" ):
        R = "[]"
    return Rn,R,Rx,Ry

def parse_texf(texf_bytes):
    
    R1 = np.frombuffer(texf_bytes[:4],D_COUNT)          
    R2 = []
    Tp = ""             
    for i in range ( 4 , len(texf_bytes) ):
     if ( texf_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R2.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(texf_bytes[i:i+1],(np.string_, 1)))[3:-2]
    return R1['count'],R2

def parse_palf(palf_bytes):
    
    R1 = np.frombuffer(palf_bytes[:4],D_COUNT)         
    R2 = []
    Tp = ""                      
    for i in range ( 4 , len(palf_bytes) ):
        
     if ( palf_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R2.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(palf_bytes[i:i+1],(np.string_, 1)))[3:-2]     
    return R1['count'],R2

def parse_inst0(inst_bytes):

    R = ""
    X = 0
    Rn = 0
    Rx = []
    Ry = []
    while ( X != len(inst_bytes) ):
        
        R1 = np.frombuffer(inst_bytes[X:X+8],D_INFT)
        Y = R1['_002'][0]
        R2 = np.frombuffer(inst_bytes[X+8:X+(Y*4)+8],(np.uint32))
        X = X+(Y*4)+8
        R += str(R1) + str(R2) + '\n'
        Rx.append(R1)
        Ry.append(R2)
        Rn += 1
    return Rn,R,Rx,Ry

def parse_vnam0(vnam_bytes):

    R1 = np.frombuffer(vnam_bytes[:4],D_COUNT)
    X1 = R1['count'][0]
    R2 = np.frombuffer(vnam_bytes[4:4+(4*X1)],(np.uint32))
    X2 = 4+(4*X1)
    R3 = []
    Tp = ""            
    for i in range ( X2 , len(vnam_bytes) ):
     if ( vnam_bytes[i:i+1] == b'\x00' ):
          if ( Tp != "" ):
              R3.append(Tp)
          Tp = ""
     else:
          Tp += str(np.frombuffer(vnam_bytes[i:i+1],(np.string_, 1)))[3:-2]
    return R1['count'],R2,R3

def parse_gtts(gtts_bytes):
    
    R1 = np.frombuffer(gtts_bytes[:4],D_COUNT)
    R2 = ""
    X = 4
    while ( X != len(gtts_bytes) ):
        R = np.frombuffer(gtts_bytes[X:X+8],D_GTTS)
        X = X + 8
        R2 += str(R) + "\n"
    if ( R2 == "" ):
        R2 = "[]"
    return R1['count'],R2

