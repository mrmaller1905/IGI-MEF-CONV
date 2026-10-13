import os 
import numpy as np
from .import reader_ilff
from .import mefc_type_rigid
from .import mefc_type_bone
from .import mefc_type_lightmap
from .import mefc_type_shadow
from .import IGI1_mefc_type_rigid
from .import IGI1_mefc_type_bone
from .import IGI1_mefc_type_lightmap
from .reader_ilff import *
from .mefc_type_rigid import *
from .mefc_type_bone import *
from .mefc_type_lightmap import *
from .mefc_type_shadow import *
from .IGI1_mefc_type_rigid import *
from .IGI1_mefc_type_bone import *
from .IGI1_mefc_type_lightmap import *

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
             meftext = IGI1_mefc_type_rigid.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 1:
            print ("\n * Model Type is Bone Model - " + os.path.basename(meffilename)) 
            meftext = IGI1_mefc_type_bone.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 3:
             print ("\n * Model Type is Lightmap Model - " + os.path.basename(meffilename)) 
             meftext = IGI1_mefc_type_lightmap.fromfile(meffilename,srcpth)

      elif ( len(reader.read(b'HSEM')) != 156 ):
      
        hsem = np.frombuffer(reader.read(b'HSEM'), DTYPE_HSEM_2)
    
        if hsem['model_type'] == 0:
             print ("\n * Model Type is Rigid Model - " + os.path.basename(meffilename)) 
             meftext = mefc_type_rigid.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 1:
            print ("\n * Model Type is Bone Model - " + os.path.basename(meffilename)) 
            meftext = mefc_type_bone.fromfile(meffilename,srcpth)

        elif hsem['model_type'] == 3:
             print ("\n * Model Type is Lightmap Model - " + os.path.basename(meffilename)) 
             meftext = mefc_type_lightmap.fromfile(meffilename,srcpth)
             
    elif reader.find(b'SEMS'):        
            print ("\n * Model Type is Shadow Model - " + os.path.basename(meffilename))
            meftext = mefc_type_shadow.fromfile(meffilename,srcpth)       
        
    return meftext

def fromtype(meffilename):

    qsctext = ""

    NamModel = str(os.path.splitext(os.path.basename(meffilename))[0])
    
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
    
    if ( reader.find(b'HSEM') and reader.find(b'HSMC') ):

      if ( len(reader.read(b'HSEM')) == 156 ):
        
        hsem = np.frombuffer(reader.read(b'HSEM'), DTYPE_HSEM_1)

        Res0 = 1#func.CalC_SavedLightmapResoultion(dner,xtrv,ecaf)
            
        if hsem['model_type'] == 0:
             qsctext += "CreateCompleteModelRigid(\"" + NamModel + "\");\n" 

        elif hsem['model_type'] == 1:          
             qsctext += "CreateCompleteModelBone(\"" + NamModel + "\");\n"

        elif hsem['model_type'] == 3:
             qsctext += "SetLightmapResolution(1" + "/" + str(Res0) + ")" +";"
             qsctext += "CreateCompleteModelLightmap(\"" + NamModel + "\");\n"     
                         
      elif ( len(reader.read(b'HSEM')) != 156 ):
        
        hsem = np.frombuffer(reader.read(b'HSEM'), DTYPE_HSEM_2)

        Res0 = 1#fun.CalC_SavedLightmapResoultion(dner,xtrv,ecaf)
            
        if hsem['model_type'] == 0:
             qsctext += "CreateCompleteModelRigid(\"" + NamModel + "\");\n" 

        elif hsem['model_type'] == 1:          
             qsctext += "CreateCompleteModelBone(\"" + NamModel + "\");\n"

        elif hsem['model_type'] == 3:
             qsctext += "SetLightmapResolution(1" + "/" + str(Res0) + ")" +";"
             qsctext += "CreateCompleteModelLightmap(\"" + NamModel + "\");\n"
             
    elif  reader.find(b'SEMS'):        
             qsctext += "CreateShadowVolume(\"" + NamModel + "\");\n"         

    return qsctext
