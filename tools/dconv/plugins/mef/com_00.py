import os 
import numpy as np
from .import com_02
from .com_02 import *
from .import mef_struct
from .import reader_ilff
from .mef_struct import *
from .reader_ilff import *

def fromtree(srcpth1,srcpth2):
    
    reader = reader_ilff.open(srcpth1)

    Et = ""

    disc = ""

    E = 1

    M1 = -1
    
    if reader.find(b'HSEM') and E == 1 :
        
        hsem_bytes = reader.read(b'HSEM')
        
        if ( len(hsem_bytes) != 156 ):

            hsem = np.frombuffer(hsem_bytes, DTYPE_HSEM)
            
            if hsem['model_type'] == 0:
                                            M1 = 0
            elif hsem['model_type'] == 1:
                                            M1 = 1
            elif hsem['model_type'] == 3:
                                            M1 = 3
        else:
            print( " \n - Irrelevant MEF Model File Version ")
            E = 0

    elif  reader.find(b'SEMS'):
                                            M1 = 2
                   
    M2 = -1

    reader = reader_ilff.open(srcpth2)

    if reader.find(b'HSEM') and E == 1 :
        
        hsem_bytes = reader.read(b'HSEM')
        
        if ( len(hsem_bytes) != 156 ):

            hsem = np.frombuffer(hsem_bytes, DTYPE_HSEM)
            
            if hsem['model_type'] == 0:
                                            M2 = 0
            elif hsem['model_type'] == 1:
                                            M2 = 1
            elif hsem['model_type'] == 3:
                                            M2 = 3
        else:
            print( " \n - Irrelevant MEF Model File Version ")
            E = 0

    elif  reader.find(b'SEMS'):
                                            M2 = 2

    if ( E == 1 ):

        if ( M1 != M2 ):

            print( " \n - Model Type Not Matching ")

            disc = ""

        else:

            M = M1
            
            if (M == 0):
                      disc = com_02.fromM0(srcpth1,srcpth2,M)
            elif M == 1:
                      disc = com_02.fromM1(srcpth1,srcpth2,M)
            elif M == 3:
                      disc = com_02.fromM0(srcpth1,srcpth2,M)
            elif M == 2:
                      disc = com_02.fromM2(srcpth1,srcpth2,M)
                   
    return Et,disc
