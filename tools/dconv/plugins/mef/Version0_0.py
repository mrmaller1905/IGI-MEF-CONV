import os 
import numpy as np
from .import Version1_0
from .import Version1_1
from .import Version1_3
from .import Version2_0
from .import Version2_1
from .import Version2_3
from .import Version2_S
from .import reader_ilff
from .reader_ilff import *

def fromtree(File):

    DTYPE_HSEM_1 = np.dtype([
	('_0', np.int32),         # 
	('yy', np.uint32),         # datetime
	('mm', np.uint32),         # datetime
	('dd', np.uint32),         # datetime
	('hh', np.uint32),         # datetime
	('mn', np.uint32),         # datetime
	('ss', np.uint32),         # datetime
	('ms', np.uint32),         # datetime
	('model_type', np.uint32), # modeltype
	('_1', np.uint32),         # 0
	('_2', np.uint32),         # 0
	('_3', np.uint32),         # 0
	('f0', np.float32),        # 
	('f1', np.float32),        # 
	('f2', np.float32),        # 
	('f3', np.float32),        # 
	('f4', np.float32),        # 
	('f5', np.float32),        # 
	('f6', np.float32),        # 
	('f7', np.float32),        # 
	('f8', np.float32),        # 
	('f9', np.float32),        # 
	('fa', np.float32),        # 
	('fb', np.float32),        # 
	('fn', np.uint32),         # render faces count
	('vn', np.uint32),         # render verts count
	('_6', np.uint32),         # 
	('cv', np.uint32),         # collision verts count
	('cf', np.uint32),         # collision faces count
	('_9', np.uint32),         # 
	('fc', np.float32),        # 
	('mg', np.uint16),         # magic verts count
	('an', np.uint16),         # attachments count
	('pv', np.uint16),         # portal verts count
	('pf', np.uint16),         # portal faces count
	('pn', np.uint16),         # portal count
	('_f', np.uint16),         # 0
	('rs', (np.uint8, 20)),    # 
        ])

    DTYPE_HSEM_2 = np.dtype([
        ('_0',         np.float32),
        ('date_time',  [
            ('year',       np.uint32),
            ('month',      np.uint32),
            ('day',        np.uint32),
            ('hour',       np.uint32),
            ('minute',     np.uint32),
            ('second',     np.uint32),
            ('milisecond', np.uint32)
            ]),
        ('model_type', np.uint32),
        ('reserved_0', (np.uint8, 12)),
        ('vectors', ([
            ('x', np.float32),
            ('y', np.float32),
            ('z', np.float32),
            ('w', np.float32)
            ], 3)),
        ('num_r_faces',   np.uint32),
        ('num_r_verts',  np.uint32),
        ('num_r_buffer',         np.uint32),
        ('sum_c_faces',  np.uint32),
        ('sum_c_verts', np.uint32),
        ('sum_c_buffer',         np.uint32),
        ('_3',         np.float32),
        ('num_mverts', np.uint16),
        ('num_attachments', np.uint16),
        ('num_verts', np.uint16),
        ('num_faces',  np.uint16),
        ('num_portals',   np.uint16),
        ('num_bones',  np.uint16),
        ('num_glows',  np.uint16),
        ('reserved_1', (np.uint8, 30)),
        ('reserved_2', (np.uint8, 8))
        ])

    Bytes = b''
    
    reader = reader_ilff.open(File)
    
    if reader.find(b'HSEM'):
        hsem_bytes = reader.read(b'HSEM')

        if ( len(hsem_bytes) == 156 ):
            hsem = np.frombuffer(hsem_bytes, DTYPE_HSEM_1)

        else:
            hsem = np.frombuffer(hsem_bytes, DTYPE_HSEM_2)
        
        if ( len(hsem_bytes) == 156 ) :
            
            if hsem['model_type'] == 0:
                print ("\n * Model Type is Rigid Model , (V1-V2) [Not Recommended] - " + os.path.basename(File)) 
                Bytes += Version1_0.fromfile(File)

            elif hsem['model_type'] == 1:
                print ("\n * Model Type is Bone Model , (V1-V2) [Not Recommended] - " + os.path.basename(File)) 
                Bytes += Version1_1.fromfile(File)

            elif hsem['model_type'] == 3:
                print ("\n * Model Type is Lightmap Model , (V1-V2) [Not Recommended] - " + os.path.basename(File)) 
                Bytes += Version1_3.fromfile(File)
                
        else:
            
            if hsem['model_type'] == 0:
                print ("\n * Model Type is Rigid Model , (V2-V1) - " + os.path.basename(File)) 
                Bytes += Version2_0.fromfile(File)

            elif hsem['model_type'] == 1:
                print ("\n * Model Type is Bone Model , (V2-V1) - " + os.path.basename(File)) 
                Bytes += Version2_1.fromfile(File)

            elif hsem['model_type'] == 3:
                print ("\n * Model Type is Lightmap Model , (V2-V1) - " + os.path.basename(File)) 
                Bytes += Version2_3.fromfile(File)        

    elif  reader.find(b'SEMS'):        
                print("\n Model Type is Shadow Model , (V2-V1) (NOT SUPPORTED) - " + os.path.basename(File))
                Bytes += Version2_S.fromfile(File)  
        
    return Bytes
