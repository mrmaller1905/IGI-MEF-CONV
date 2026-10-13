import os
import io
import struct
from .import reader_ilff
from .import mef_struct
from .mef_struct import *
from .reader_ilff import *
import numpy as np

def fromfile(File):


# Reading Data !!!!!

  if (True):
    
    reader = reader_ilff.open(File)

    if reader.find(b'HSEM'):

     hsem = parse_hsem(reader.read(b'HSEM'))

     atta = parse_atta(reader.read(b'ATTA'))

     xtvm = parse_xtvm(reader.read(b'XTVM'))

     trop = parse_trop(reader.read(b'TROP'))

     xvtp = parse_xvtp(reader.read(b'XVTP'))

     cftp = parse_cftp(reader.read(b'CFTP'))

     d3dr = parse_d3dr(reader.read(b'D3DR'),1)

     dner = parse_dner(reader.read(b'DNER'),1)

     xtrv = parse_xtrv(reader.read(b'XTRV'),1)

     ecaf = parse_ecaf(reader.read(b'ECAF'))

    if reader.find(b'HSMC'):
    
     hsmc = parse_hsmc(reader.read(b'HSMC',0))

     xtvc = parse_xtvc(reader.read(b'XTVC',0),1)

     ecfc = parse_ecfc(reader.read(b'ECFC',0))

     tamc = parse_tamc(reader.read(b'TAMC',0))

     hpsc = parse_hpsc(reader.read(b'HPSC',0))
    
     xtvc1= parse_xtvc(reader.read(b'XTVC',1),1)

     ecfc1= parse_ecfc(reader.read(b'ECFC',1))

     tamc1= parse_tamc(reader.read(b'TAMC',1))

     hpsc1= parse_hpsc(reader.read(b'HPSC',1))

    Signs = reader.signatures()


# --------------------------------------------------> SOME NECESSARY CALCULATIONS

  if ( b'HSEM' in Signs ):

   D = hsem['rs'][0][0]
   

  HSEM_DATASIZE_RENDERMESH = 0

  HSEM_DATASIZE_COLLISONMESH = 0
  

  if ( b'D3DR' in Signs ):

    HSEM_DATASIZE_RENDERMESH += 56 + (d3dr['num_face'][0]*6) + (d3dr['num_mesh'][0]*28) + (d3dr['num_verts'][0]*40)

  if ( b'HSMC' in Signs ):

    HSEM_DATASIZE_COLLISONMESH += 32 + (hsmc['num_face_0'][0]*8) + (hsmc['num_vertex_0'][0]*16) + (hsmc['num_material_0'][0]*12) + (hsmc['num_sphere_0'][0]*24)

    HSEM_DATASIZE_COLLISONMESH += 32 + (hsmc['num_face_1'][0]*8) + (hsmc['num_vertex_1'][0]*16) + (hsmc['num_material_1'][0]*12) + (hsmc['num_sphere_1'][0]*24)



  DNER_POS = []

  for R in range ( 0 , len(dner) ):

    Sx = 0
    Sy = 0
    Sz = 0

    for i in range ( dner['off_verts'][R] , dner['off_verts'][R] + dner['num_verts'][R] ):

      Sx += xtrv['px'][i]
      Sy += xtrv['py'][i]
      Sz += xtrv['pz'][i]

    DNER_POS.append([ Sx/dner['num_verts'][R] , Sy/dner['num_verts'][R] , Sz/dner['num_verts'][R] ])

  if max(xtrv['bn']) >  31 :

    I = [ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55 ]

  if max(xtrv['bn']) <= 31 :

    I = [ 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32 ]

  DNER_OFFSET_V1 =  []

  for R in range ( 0 , len(dner) ):

    if ( R != len(dner)-1 ):

      DNER_OFFSET_V1.append((dner['num_face'][R]*3)*2)

    else:

      DNER_OFFSET_V1.append(65535)
      
  

  DNER_OPACITY_V1 = []

  for R in range ( 0 , len(dner) ):

    if ( dner['_opacity'][R] in ( 4, 6, 7, 36, 38, 68, 70, 100, 102 ) ):

      DNER_OPACITY_V1.append(1)

    else:

      DNER_OPACITY_V1.append(0)
      
  

  DNER_EFLAME_V1 = []

  for R in range ( 0 , len(dner) ):

    if ( dner['_opacity'][R] in ( 1, 3, 5, 7, 33, 35, 37, 39, 65, 67, 69, 71 ) ):

      DNER_EFLAME_V1.append(1)

    else:

      DNER_EFLAME_V1.append(0)



# -------------------------------------------------
# -------------------------------------------------
#  FORMAT CONVERSION
#--------------------------------------------------
#--------------------------------------------------


  CHUNKS = []


# FORM HEADER HSEM -------------------------------------------------------------------------------------------------------->///////////////


  if ( b'HSEM' in Signs ):

   DATA = b''

   SIZE = 4 + 16

   for i in range ( 0 , len(hsem) ):

    DATA += struct.pack('=1f',0.10)

    DATA += struct.pack('=7I',hsem['Date'][i][0] , hsem['Date'][i][1] , hsem['Date'][i][2] , hsem['Date'][i][3] , hsem['Date'][i][4] , hsem['Date'][i][5] , hsem['Date'][i][6])

    DATA += struct.pack('=4I',hsem['model_type'][i], hsem['reserved_0'][i][0] , hsem['reserved_0'][i][1] , hsem['reserved_0'][i][2])

    DATA += struct.pack('=12f',hsem['vectors'][i][0] , hsem['vectors'][i][1] , hsem['vectors'][i][2] , hsem['vectors'][i][3] , hsem['vectors'][i][4] , hsem['vectors'][i][5] , hsem['vectors'][i][6] , hsem['vectors'][i][7] , hsem['vectors'][i][8] , hsem['vectors'][i][9] , hsem['vectors'][i][10] , hsem['vectors'][i][11])

    DATA += struct.pack('=3I',hsem['num_r_faces'][i], d3dr['num_verts'][0], HSEM_DATASIZE_RENDERMESH) ##
    
    DATA += struct.pack('=3I',hsem['sum_c_faces'][i], hsem['sum_c_verts'][i], HSEM_DATASIZE_COLLISONMESH) ##
    
    DATA += struct.pack('=1f',hsem['model_radius'][i])
    
    DATA += struct.pack('=5H',hsem['num_mverts'][i], hsem['num_attachments'][i], hsem['num_pverts'][i], hsem['num_pfaces'][i], hsem['num_portals'][i])

    DATA += struct.pack('=22B',D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D)

   SKIP = GetSkipBytes(len(DATA)) 

   CHUNKS.append([ b'HSEM' , len(DATA) , 4 , len(DATA)+len(SKIP)+ 16 , DATA+SKIP ])

   SIZE += len(DATA)+len(SKIP) + 16
   


# OTHER MODEL_INFO ------------------------------- ATTA,XTVM,WOLG ----------------------------------------------------------------///////////////


  if ( b'ATTA' in Signs ):

   DATA = b''

   for i in range ( 0 , len(atta) ):

    DATA += struct.pack('=16s6f',atta['name'][i], atta['px'][i], atta['py'][i], atta['pz'][i], atta['_00'][i], atta['_01'][i], atta['_02'][i])

    DATA += struct.pack('=6f1I',atta['_03'][i], atta['_04'][i], atta['_05'][i], atta['_06'][i], atta['_07'][i], atta['_08'][i], atta['_09'][i])
    
   CHUNKS.append([ b'ATTA' , len(DATA) , 4 , len(DATA) + 16 , DATA ])   

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(xtvm) ):

    DATA += struct.pack('=3f1i',xtvm['px'][i], xtvm['py'][i], xtvm['pz'][i], xtvm['_0'][i])

   CHUNKS.append([ b'XTVM' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16
                


# PORTAL MESH DEFS ------------------------------- TROP,XVTP,CFTP ----------------------------------------------------------------///////////////


  if ( b'TROP' in Signs ):

   DATA = b''

   for i in range ( 0 , len(trop) ):

    DATA += struct.pack('=5I',trop['o_vertex'][i], trop['n_vertex'][i],
                   trop['o_face'][i], trop['n_face'][i], trop['id'][i])

   CHUNKS.append([ b'TROP' , len(DATA) , 4 , len(DATA) + 16 , DATA ])  

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(xvtp) ):

    DATA += struct.pack('=3f',xvtp['px'][i] , xvtp['py'][i] , xvtp['pz'][i])

   CHUNKS.append([ b'XVTP' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(cftp) ):

    DATA += struct.pack('=3I',cftp['a'][i] , cftp['b'][i] , cftp['c'][i])

   CHUNKS.append([ b'CFTP' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# RENDER MESH DEF. ------------------------------- DNER,ECAF,XTRV ----------------------------------------------------------------/////////////// !!!!!!!!!!!!



# D3DR --------------------------------|


  if ( b'D3DR' in Signs ):

   DATA = b''

   DATA += struct.pack('=14I',d3dr['_4'][0],d3dr['num_face'][0],d3dr['num_mesh'][0],d3dr['verts_0'][0],d3dr['verts_1'][0],d3dr['num_verts'][0],0,0,0,0,0,0,0,0)

   CHUNKS.append([ b'D3DR' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(dner) ):

    DATA += struct.pack('=3f2H1h2H',DNER_POS[i][0], DNER_POS[i][1], DNER_POS[i][2], dner['num_face'][i]*3, DNER_OFFSET_V1[i], dner['_td'][i], dner['off_verts'][i], dner['num_verts'][i])

    DATA += struct.pack('=1H4B',DNER_OPACITY_V1[i], DNER_EFLAME_V1[i], dner['_mshine'][i], dner['_Scolor'][i], dner['_Opacitd'][i])

    OFF = (dner['off_verts'][i])

    for j in range ( (dner['offset_index'][i] // 3) , (dner['offset_index'][i] // 3) + dner['num_face'][i] ):

     DATA += struct.pack('=3H', ( ecaf['a'][j] - OFF ) , ( ecaf['b'][j] - OFF ) , ( ecaf['c'][j] - OFF ) )

   SKIP = GetSkipBytes(len(DATA)) 

   CHUNKS.append([ b'DNER' , len(DATA) , 4 , len(DATA)+len(SKIP)+ 16 , DATA+SKIP ])

   SIZE += len(DATA)+len(SKIP) + 16

   DATA = b''

   for i in range ( 0 , len(xtrv) ):

    DATA += struct.pack('=6f',xtrv['px'][i], xtrv['py'][i], xtrv['pz'][i], xtrv['nx'][i], xtrv['ny'][i], xtrv['nz'][i])

    DATA += struct.pack('=3f2H',xtrv['u'][i], xtrv['v'][i], xtrv['w'][i], xtrv['vn'][i], I[xtrv['bn'][i]])

   CHUNKS.append([ b'XTRV' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


  if ( b'HSMC' in Signs ): # ----------------------------------------|

   DATA = b''

   for i in range ( 0 , len(hsmc) ):

    DATA += struct.pack('=8I',hsmc['num_face_0'][i] , hsmc['num_vertex_0'][i] , hsmc['num_material_0'][i] , hsmc['num_sphere_0'][i] , 0 , 0 , 0 , 0 )

    DATA += struct.pack('=8I',hsmc['num_face_1'][i] , hsmc['num_vertex_1'][i] , hsmc['num_material_1'][i] , hsmc['num_sphere_1'][i] , 0 , 0 , 0 , 0 )

   CHUNKS.append([ b'HSMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# COLLISION MESH TYPE 0 ------------------------------- XTVC,ECFC,TAMC,HPSC ----------------------------------------------------------------///////////////



  if ( b'XTVC' in Signs ):

   DATA = b''

   for i in range ( 0 , len(xtvc) ):

    DATA += struct.pack('=3f1I',xtvc['px'][i], xtvc['py'][i], xtvc['pz'][i] , I[xtvc['bn'][i]])

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(ecfc) ):

    DATA += struct.pack('=4H',ecfc['a'][i], ecfc['b'][i], ecfc['c'][i], ecfc['_mat'][i])

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(tamc) ):

    DATA += struct.pack('=1f1H2h1H',tamc['opacity'][i], tamc['portal'][i], tamc['diffuse'][i], tamc['mat_id'][i], tamc['unknown'][i])

   CHUNKS.append([ b'TAMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(hpsc) ):

    DATA += struct.pack('=4f4H',hpsc['px'][i] , hpsc['py'][i] , hpsc['pz'][i] , hpsc['size'][i], hpsc['_0'][i] , hpsc['_1'][i] , hpsc['_a'][i] , hpsc['_b'][i])

   CHUNKS.append([ b'HPSC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# COLLISION MESH TYPE 1 ------------------------------- XTVC,ECFC,TAMC,HPSC ----------------------------------------------------------------///////////////



  if ( b'XTVC' in Signs ):

   DATA = b''

   for i in range ( 0 , len(xtvc1) ):

    DATA += struct.pack('=3f1I',xtvc1['px'][i] , xtvc1['py'][i] , xtvc1['pz'][i] , I[xtvc1['bn'][i]])

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(ecfc1) ):

    DATA += struct.pack('=4H',ecfc1['a'][i], ecfc1['b'][i], ecfc1['c'][i], ecfc1['_mat'][i])

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(tamc1) ):

    DATA += struct.pack('=1f1H2h1H',tamc1['opacity'][i], tamc1['portal'][i], tamc1['diffuse'][i], tamc1['mat_id'][i], tamc1['unknown'][i])

   CHUNKS.append([ b'TAMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(hpsc1) ):

    DATA += struct.pack('=4f4H',hpsc1['px'][i], hpsc1['py'][i], hpsc1['pz'][i], hpsc1['size'][i], hpsc1['_0'][i] , hpsc1['_1'][i] , hpsc1['_a'][i] , hpsc1['_b'][i])

   CHUNKS.append([ b'HPSC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16
   


# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------


# Data Writing !!


  Bytes = b''

  Bytes += struct.pack('=4s',b'ILFF')

  Bytes += struct.pack('=1I',SIZE)

  Bytes += struct.pack('=1I',4)

  Bytes += struct.pack('=1I',0)

  Bytes += struct.pack('=4s',b'OCEM')

  for i in range ( 0 , len(CHUNKS) ):

    Bytes += struct.pack('=4s',CHUNKS[i][0])

    Bytes += struct.pack('=1I',CHUNKS[i][1])

    Bytes += struct.pack('=1I',CHUNKS[i][2])

    if ( i != len(CHUNKS)-1 ):

     Bytes += struct.pack('=1I',CHUNKS[i][3])

    if ( i == len(CHUNKS)-1 ):

     Bytes += struct.pack('=1I',0)

    Bytes += CHUNKS[i][4]


      
# -------------------------------------------------
        
  return Bytes



def GetSkipBytes(Size):

  Bytes = b''

  while ( Size%4 != 0 ):

   Bytes += b'\x00'

   Size += 1

  return Bytes

    
