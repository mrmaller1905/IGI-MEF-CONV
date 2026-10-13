import os 
import numpy as np
from .import asec_SM
from .import asec_BM
from .import reader_MASE
from .reader_MASE import *
from .asec_SM import *
from .asec_BM import *

def fromtree(meffilename):

    meftext = ""

    print ("\n * Model is " + os.path.basename(meffilename))
    
    Data = reader_MASE.read(meffilename)

    if ( len(Data) > 0 ):

        Type_Model = Data[0] 
        
        if ( Type_Model == 0 ) : 
            meftext = asec_SM.fromfile(meffilename,Data)
            
        
        if ( Type_Model == 1 ) :
            meftext = asec_BM.fromfile(meffilename,Data)
            
        
        if ( Type_Model == 2 ) :
            meftext = asec_SM.fromfile(meffilename,Data)


    if ( len(Data) > 0 ): # CHECKS

        assert 0==0, "Error found?"
             
        
    return meftext    
