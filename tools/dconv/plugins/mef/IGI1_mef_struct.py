import numpy as np

DTYPE_HSEM = np.dtype([
	('_V',          np.float32),
        ('Date',       (np.uint32, 7)),
	('model_type',  np.uint32),
        ('reserved_0', (np.uint32, 3)),
        ('vectors', (np.float32, 12)),
	('num_r_faces',    np.uint32),
	('num_r_verts',    np.uint32),
	('num_r_buffer',   np.uint32),
	('sum_c_faces',    np.uint32),
	('sum_c_verts',    np.uint32),
	('sum_c_buffer',   np.uint32),
        ('model_radius',   np.float32),
	('num_mverts',     np.uint16),
	('num_attachments',np.uint16),
	('num_pverts',     np.uint16),
	('num_pfaces',     np.uint16),
	('num_portals',    np.uint16),
	('rs',          (np.uint8, 22)), # (dummy.mef,helicol.mef)
        ])

DTYPE_ATTA = np.dtype([
	('name', (np.string_, 16)),
	('px',  np.float32),
	('py',  np.float32),
	('pz',  np.float32),        
	('_00', np.float32),
	('_01', np.float32),
	('_02', np.float32),
	('_03', np.float32),
	('_04', np.float32),
	('_05', np.float32),
	('_06', np.float32),
	('_07', np.float32),
	('_08', np.float32),
	('_09', np.uint32),
	])

DTYPE_XTVM = np.dtype([
	('px', np.float32),
	('py', np.float32),
	('pz', np.float32),     
	('_0', np.int32),
	])

DTYPE_TROP = np.dtype([
        ('o_vertex', np.uint32),
        ('n_vertex', np.uint32),
        ('o_face',   np.uint32),
        ('n_face',   np.uint32),
	('id',       np.uint32),
	])

DTYPE_XVTP = np.dtype([
	('px', np.float32),
	('py', np.float32),
	('pz', np.float32),     
        ])

DTYPE_CFTP = np.dtype([
	('a', np.uint32),
	('b', np.uint32),
	('c', np.uint32),     
        ])

DTYPE_D3DR_0 = np.dtype([
	('_4',        np.uint32),
        ('num_face',  np.uint32),
        ('num_mesh',  np.uint32),
        ('num_verts', np.uint32),
	('reserved', (np.uint32,8)),
	])

DTYPE_D3DR_1 = np.dtype([
	('_4',        np.uint32),
        ('num_face',  np.uint32),
        ('num_mesh',  np.uint32),
        ('verts_0',   np.uint32),
        ('verts_1',   np.uint32),
        ('num_verts', np.uint32),
	('reserved', (np.uint32,8)),
	])

DTYPE_D3DR_3 = np.dtype([
	('_4',           np.uint32),
        ('num_lmap',     np.uint32),
        ('num_face',     np.uint32),
        ('num_mesh',     np.uint32),
        ('num_verts',    np.uint32),
        ('resrved_0',    np.uint32),
        ('_Unknown0',    np.uint32),#????
	('reserved',    (np.uint32,7)),
	])

DTYPE_ECAF = np.dtype([
        ('a', np.uint16),
        ('b', np.uint16),
        ('c', np.uint16),
	])

DTYPE_DNER_0 = np.dtype([
	('px',           np.float32),
	('py',           np.float32),
	('pz',           np.float32),
	('num_face',     np.uint16),
	('nextoffs',     np.uint16),
	('_td',          np.int16),
	('off_verts',    np.uint16),
	('num_verts',    np.uint16),
	('_opacity',     np.uint16),
	('_Eflame',      np.uint8),
	('_mshine',      np.uint8),  
	('_Scolor',      np.uint8),
	('_Opacitd',     np.uint8),      
	])

DTYPE_DNER_3 = np.dtype([
	('px',          np.float32),
	('py',          np.float32),
	('pz',          np.float32),        
	('num_face',    np.uint16),
	('nextoffs',    np.uint16),
	('_td',         np.int16),
	('_lmap',       np.int16),
        ('off_verts',   np.uint16),
        ('num_verts',   np.uint16),
	('_opacity',    np.uint16),
	('_0',          np.uint16),#????
	('_Eflame',     np.uint8),
	('_mshine',     np.uint8),
	('_mcolor',     np.uint8),
	('_Opacitd',    np.uint8),
	])

DTYPE_XTRV_0 = np.dtype([
	('px', np.float32),
	('py', np.float32),
	('pz', np.float32),
	('nx', np.float32),
	('ny', np.float32),
	('nz', np.float32),
	('u',  np.float32),
	('v',  np.float32),
	])

DTYPE_XTRV_1 = np.dtype([
	('px', np.float32),
	('py', np.float32),
	('pz', np.float32),     
	('nx', np.float32),
	('ny', np.float32),
	('nz', np.float32),
	('u',  np.float32),
	('v',  np.float32),        
        ('w',  np.float32),
        ('vn', np.uint16),
        ('bn', np.uint16),   
	])

DTYPE_XTRV_3 = np.dtype([
	('px', np.float32),
	('py', np.float32),
	('pz', np.float32),     
	('nx', np.float32),
	('ny', np.float32),
	('nz', np.float32),
	('u',  np.float32),
	('v',  np.float32),        
	('u1', np.float32),
	('v1', np.float32), 
	])

DTYPE_PMTL = np.dtype([
        ('_x', np.uint16),
        ('_y', np.uint16),
        ('_z', np.uint16),
        ('_w', np.uint16),
	])

DTYPE_HSMC = np.dtype([
        ('num_face_0' ,      np.uint32),
        ('num_vertex_0' ,    np.uint32),
        ('num_material_0' ,  np.uint32),
        ('num_sphere_0' ,    np.uint32), 
        ('_0',               np.uint32),
        ('_1',               np.uint32),
        ('_2',               np.uint32),
        ('_3',               np.uint32),
        ('num_face_1' ,      np.uint32),
        ('num_vertex_1' ,    np.uint32),
        ('num_material_1' ,  np.uint32),
        ('num_sphere_1' ,    np.uint32),
        ('_4',               np.uint32),
        ('_5',               np.uint32),
        ('_6',               np.uint32),
        ('_7',               np.uint32),     
	])

DTYPE_XTVC = np.dtype([
	('px', np.float32),
	('py', np.float32),
	('pz', np.float32),     
	('bn', np.uint32),
	])

DTYPE_ECFC = np.dtype([
	('a',    np.uint16),
	('b',    np.uint16),
	('c',    np.uint16),
	('_mat', np.uint16),
	])

DTYPE_TAMC = np.dtype([ 
	('opacity',     np.float32),
	('portal',      np.uint16),
	('diffuse',     np.int16),
	('mat_id',      np.int16),
	('unknown',     np.uint16),#Dep.
	])

DTYPE_HPSC = np.dtype([
        ('px',   np.float32),
        ('py',   np.float32),
        ('pz',   np.float32),
        ('size', np.float32),
        ('_0',   np.uint16),
        ('_1',   np.uint16),
        ('_a',   np.uint16),
        ('_b',   np.uint16),
        ])

DTYPE_TXAN = np.dtype([
        ('_00', np.uint32),
        ('_01', np.uint32),
        ])
    
def parse_hsem(hsem_bytes):
    return np.frombuffer(hsem_bytes, DTYPE_HSEM)

def parse_atta(atta_bytes):
    return np.frombuffer(atta_bytes, DTYPE_ATTA)

def parse_xtvm(xtvm_bytes):
    return np.frombuffer(xtvm_bytes, DTYPE_XTVM)

def parse_trop(trop_bytes):
    return np.frombuffer(trop_bytes, DTYPE_TROP)

def parse_xvtp(xvtp_bytes):
    return np.frombuffer(xvtp_bytes, DTYPE_XVTP)

def parse_cftp(cftp_bytes):
    return np.frombuffer(cftp_bytes, DTYPE_CFTP)

def parse_d3dr(d3dr_bytes, model_type):
    if model_type == 0:
        return np.frombuffer(d3dr_bytes, DTYPE_D3DR_0)
    elif model_type == 1:
        return np.frombuffer(d3dr_bytes, DTYPE_D3DR_1)
    elif model_type == 3:
        return np.frombuffer(d3dr_bytes, DTYPE_D3DR_3)  

def parse_xtrv(xtrv_bytes, model_type):
    if model_type == 0:
        return np.frombuffer(xtrv_bytes, DTYPE_XTRV_0)
    elif model_type == 1:
        return np.frombuffer(xtrv_bytes, DTYPE_XTRV_1)
    elif model_type == 3:
        return np.frombuffer(xtrv_bytes, DTYPE_XTRV_3)

def parse_dner(dner_bytes, model_type):
    if model_type == 0:
            return load_dner(dner_bytes,0)
    elif model_type == 1:
            return load_dner(dner_bytes,1)   
    elif model_type == 3:
            return load_dner(dner_bytes,3) 

def parse_xtrx(NONE,xtrx_bytes):
    return np.frombuffer(xtrx_bytes, DTYPE_XTRV_0)

def parse_ecaf(NONE,ecaf_bytes):
    return np.frombuffer(ecaf_bytes, DTYPE_ECAF)

def parse_pmtl(pmtl_bytes):
    return np.frombuffer(pmtl_bytes, DTYPE_PMTL)

def parse_hsmc(hsmc_bytes):
    return np.frombuffer(hsmc_bytes, DTYPE_HSMC)

def parse_xtvc(xtvc_bytes):
    return np.frombuffer(xtvc_bytes, DTYPE_XTVC)

def parse_ecfc(ecfc_bytes):
    return np.frombuffer(ecfc_bytes, DTYPE_ECFC)

def parse_tamc(tamc_bytes):
    return np.frombuffer(tamc_bytes, DTYPE_TAMC)

def parse_hpsc(hpsc_bytes):
    return np.frombuffer(hpsc_bytes, DTYPE_HPSC)

def parse_txan(txan_bytes):
    return np.frombuffer(txan_bytes, DTYPE_TXAN)

def load_dner(dner_bytes,model_type):
    X = 0
    Y = 0
    dner_bytes01 = dner_bytes[0:0]
    dner_bytes02 = dner_bytes[0:0]
    if ( model_type == 0 or model_type == 1 ):
        while (1):
            if ( X < (len(dner_bytes)) ):
                dner1 = dner_bytes[X:28+X]
                dner = np.frombuffer(dner1,DTYPE_DNER_0)
                Y = 2 * dner['num_face'][0] + (28 + X)
                dner2 = dner_bytes[28+X:Y]
                X = Y
                dner_bytes01 += dner1
                dner_bytes02 += dner2            
                if ( dner['nextoffs'][0] == -1 ):
                 break
            else:
                 break            
        dner = np.frombuffer(dner_bytes01,DTYPE_DNER_0)
        ecaf = np.frombuffer(dner_bytes02,DTYPE_ECAF)
        
    if ( model_type == 3 ):
        while (1):
            if ( X < (len(dner_bytes)) ):
                dner1 = dner_bytes[X:32+X]
                dner = np.frombuffer(dner1,DTYPE_DNER_3)
                Y = 2 * dner['num_face'][0] + (32 + X)
                dner2 = dner_bytes[32+X:Y]
                X = Y
                dner_bytes01 += dner1
                dner_bytes02 += dner2   
                if ( dner['nextoffs'][0] == -1 ):
                 break
            else:
                 break            
        dner = np.frombuffer(dner_bytes01,DTYPE_DNER_3)
        ecaf = np.frombuffer(dner_bytes02,DTYPE_ECAF)
        
    return dner,ecaf
    
