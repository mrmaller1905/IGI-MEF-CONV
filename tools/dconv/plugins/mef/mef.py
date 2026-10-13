import os 
import numpy as np
from .import reader_ilff
from .import mef_type_rigid
from .import mef_type_bone
from .import mef_type_lightmap
from .import mef_type_shadow
from .import IGI1_mef_type_rigid
from .import IGI1_mef_type_bone
from .import IGI1_mef_type_lightmap
from .reader_ilff import *
from .mef_type_rigid import *
from .mef_type_bone import *
from .mef_type_lightmap import *
from .mef_type_shadow import *
from .IGI1_mef_type_rigid import *
from .IGI1_mef_type_bone import *
from .IGI1_mef_type_lightmap import *

def fromtree(meffilename):
    
    reader = reader_ilff.open(srcpth)

    DTYPE_HSEM_1 = np.dtype([
	('_00',    (np.uint32,8)),
	('model_type', np.uint32),
	('_01',   (np.uint32,30)),
        ])
    
    DTYPE_HSEM_2 = np.dtype([
	('_00',    (np.uint32,8)),
	('model_type', np.uint32),
	('_01',   (np.uint32,35)),
        ])
    
    if reader.find(b'HSEM'):

      if ( len(reader.read(b'HSEM')) == 156 ):
      
        hsem = np.frombuffer(reader.read(b'HSEM'), DTYPE_HSEM_1)
    
        if hsem['model_type'] == 0:
             print ("\n * Model Type is Rigid Model - " + os.path.basename(meffilename)) 
             meftext = IGI1_mef_type_rigid.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 1:
            print ("\n * Model Type is Bone Model - " + os.path.basename(meffilename)) 
            meftext = IGI1_mef_type_bone.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 3:
             print ("\n * Model Type is Lightmap Model - " + os.path.basename(meffilename)) 
             meftext = IGI1_mef_type_lightmap.fromfile(meffilename,srcpth)

      elif ( len(reader.read(b'HSEM')) != 156 ):
      
        hsem = np.frombuffer(reader.read(b'HSEM'), DTYPE_HSEM_2)
    
        if hsem['model_type'] == 0:
             print ("\n * Model Type is Rigid Model - " + os.path.basename(meffilename)) 
             meftext = mef_type_rigid.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 1:
             print ("\n * Model Type is Bone Model - " + os.path.basename(meffilename)) 
             meftext = mef_type_bone.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 3:
             print ("\n * Model Type is Lightmap Model - " + os.path.basename(meffilename)) 
             meftext = mef_type_lightmap.fromfile(meffilename,srcpth)
             
    elif reader.find(b'SEMS'):
        print ("\n * Model Type is Shadow Model - " + os.path.basename(meffilename))
        meftext = mef_type_shadow.fromfile(meffilename,srcpth)
        
        
    return meftext
    
