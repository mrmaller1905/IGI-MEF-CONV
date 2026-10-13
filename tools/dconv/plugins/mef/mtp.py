import os 
import numpy as np
from .import mtp_dconv
from .import reader_ilff
from .import mtp_dat_reader
from .mtp_dconv import *
from .reader_ilff import *
from .mtp_dat_reader import *

DTYPE_HSEM1 = np.dtype([
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

DTYPE_HSEM2 = np.dtype([
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



def fromFile(dir,srcpath):

    qsctext = ""

    srcpth = (str(os.path.split(srcpath)[0])) + "\\models\\"

    Func = mtp_dat_reader.fromdat(srcpath,srcpth) # TO READ DAT FILE

    ModelNames = Func[0] # MODEL IDS

    ModelTypes = [] # [ 0,1,3 ]

    ModelLODs = [] # [ 1 means model, 0 means model_LOD ]

    for i in range ( 0 , len(ModelNames) ):

        reader = reader_ilff.open(srcpth + ModelNames[i])
    
        if ( reader.find(b'HSEM') ):
            hsem_bytes = reader.read(b'HSEM')

            if ( reader.find(b'HSMC') ):

              ModelLODs.append(1)

            else:

              ModelLODs.append(0)

            if ( len(hsem_bytes) == 156 ):
                hsem = np.frombuffer(hsem_bytes, DTYPE_HSEM1)
            else:
                hsem = np.frombuffer(hsem_bytes, DTYPE_HSEM2)           
    
            if hsem['model_type'] == 0:
                    ModelTypes.append(0)
            elif hsem['model_type'] == 1:  
                    ModelTypes.append(1)
            elif hsem['model_type'] == 3:
                    ModelTypes.append(3)


    Mtp_file = (str(srcpath).replace(".dat",".mtp")) # TO READ MTP FILE

    Func = mtp_dconv.FromData(Mtp_file,ModelNames,ModelTypes,ModelLODs)

    qsctext += Func[0] # ANIMATIONS (.IFF)

    qsctext += Func[1] # SHADOW MODELS (.MEF)

    qsctext += Func[2] # VIRTUAL MODELS (.VNAM)

    qsctext += Func[3] # ORGINAL MODELS (.MEF) 


    
    return qsctext
