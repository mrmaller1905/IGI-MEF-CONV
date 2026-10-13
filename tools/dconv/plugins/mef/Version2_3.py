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

     d3dr = parse_d3dr(reader.read(b'D3DR'),3)

     dner = parse_dner(reader.read(b'DNER'),3)

     xtrv = parse_xtrv(reader.read(b'XTRV'),3)

     ecaf = parse_ecaf(reader.read(b'ECAF'))

     pmtl = parse_pmtl(reader.read(b'PMTL'))

    if reader.find(b'HSMC'):
    
     hsmc = parse_hsmc(reader.read(b'HSMC',0))

     xtvc = parse_xtvc(reader.read(b'XTVC',0),3)

     ecfc = parse_ecfc(reader.read(b'ECFC',0))

     tamc = parse_tamc(reader.read(b'TAMC',0))

     hpsc = parse_hpsc(reader.read(b'HPSC',0))
    
     xtvc1= parse_xtvc(reader.read(b'XTVC',1),3)

     ecfc1= parse_ecfc(reader.read(b'ECFC',1))

     tamc1= parse_tamc(reader.read(b'TAMC',1))

     hpsc1= parse_hpsc(reader.read(b'HPSC',1))

    if reader.find(b'TXAN'):

     txan = parse_txan(reader.read(b'TXAN'))

    Signs = reader.signatures()


# --------------------------------------------------> SOME NECESSARY CALCULATIONS

  if ( b'HSEM' in Signs ):

   D = hsem['rs'][0][0]

  HSEM_SUM_C_VERTS = 0
   
  HSEM_DATASIZE_RENDERMESH = 0

  HSEM_DATASIZE_COLLISONMESH = 0

  D3DR_UNKNOWN_V1,DNER_UNKNOWN_V1 = [0],[0]

  Norm = CalC_MeshNormals(xtrv,ecaf,dner)

  if ( b'HSMC' in Signs ):

   Vts0,Vin00 = CalC_UniqueVertsID(xtvc)

   Vts1,Vin1 = CalC_UniqueVertsID(xtvc1)

   HSEM_SUM_C_VERTS = len(Vts0)+len(Vts1)
  
  if ( b'D3DR' in Signs ):

    HSEM_DATASIZE_RENDERMESH += 56 + (d3dr['num_face'][0]*6) + (d3dr['num_mesh'][0]*32) + (d3dr['num_verts'][0]*40)

  if ( b'HSMC' in Signs ):

    HSEM_DATASIZE_COLLISONMESH += 32 + (hsmc['num_face_0'][0]*8) + (len(Vts0)*16) + (hsmc['num_material_0'][0]*12) + (hsmc['num_sphere_0'][0]*24)

    HSEM_DATASIZE_COLLISONMESH += 32 + (hsmc['num_face_1'][0]*8) + (len(Vts1)*16) + (hsmc['num_material_1'][0]*12) + (hsmc['num_sphere_1'][0]*24)

    

  DNER_OFFSET_V1,DNER_OPACITY_V1,DNER_EFLAME_V1 =  [],[],[]

  for R in range ( 0 , len(dner) ):

    if ( R != len(dner)-1 ):

      DNER_OFFSET_V1.append((dner['num_face'][R]*3)*2)
    else:
      DNER_OFFSET_V1.append(65535)

    if ( dner['_opacity'][R] in ( 4, 6, 7, 36, 38, 68, 70, 100, 102 ) ):

      DNER_OPACITY_V1.append(1)
    else:
      DNER_OPACITY_V1.append(0)

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

    DATA += struct.pack('=3I',hsem['num_r_faces'][i], hsem['num_r_verts'][i], HSEM_DATASIZE_RENDERMESH) ##
    
    DATA += struct.pack('=3I',hsem['sum_c_faces'][i], HSEM_SUM_C_VERTS , HSEM_DATASIZE_COLLISONMESH) ##
    
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

   for i in range ( 0 , len(d3dr) ):

    DATA += struct.pack('=7I',d3dr['_4'][i], d3dr['num_lmap'][i], d3dr['num_face'][i], d3dr['num_mesh'][i], d3dr['num_verts'][i], 0, D3DR_UNKNOWN_V1[0]) ##

    DATA += struct.pack('=7I',0,0,0,0,0,0,0)

   CHUNKS.append([ b'D3DR' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(dner) ):

    DATA += struct.pack('=3f2H1h',dner['px'][i], dner['py'][i], dner['pz'][i], dner['num_face'][i]*3, DNER_OFFSET_V1[i], dner['_td'][i])

    DATA += struct.pack('=1h2H1H',dner['_lmap'][i], dner['off_verts'][i], dner['num_verts'][i], DNER_OPACITY_V1[i])

    DATA += struct.pack('=1H4B',DNER_UNKNOWN_V1[0], DNER_EFLAME_V1[i], dner['_mshine'][i], dner['_mcolor'][i], dner['_Opacitd'][i])

    OFF = (dner['off_verts'][i])

    for j in range ( (dner['offset_index'][i] // 3) , (dner['offset_index'][i] // 3) + dner['num_face'][i] ):

     DATA += struct.pack('=3H', ( ecaf['a'][j] - OFF ) , ( ecaf['b'][j] - OFF ) , ( ecaf['c'][j] - OFF ) )

   SKIP = GetSkipBytes(len(DATA)) 

   CHUNKS.append([ b'DNER' , len(DATA) , 4 , len(DATA)+len(SKIP)+ 16 , DATA+SKIP ])

   SIZE += len(DATA)+len(SKIP) + 16

   DATA = b''

   for i in range ( 0 , len(xtrv) ):

    DATA += struct.pack('=10f',xtrv['px'][i], xtrv['py'][i], xtrv['pz'][i], Norm[i][0] , Norm[i][1], Norm[i][2], xtrv['u'][i], xtrv['v'][i], xtrv['u1'][i], xtrv['v1'][i])

   CHUNKS.append([ b'XTRV' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(pmtl) ):

    DATA += struct.pack('=4H',pmtl['_x'][i] , pmtl['_y'][i], pmtl['_z'][i] , pmtl['_w'][i])

   CHUNKS.append([ b'PMTL' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


  if ( b'HSMC' in Signs ): #---------------------------|

   DATA = b''

   for i in range ( 0 , len(hsmc) ):

    DATA += struct.pack('=8I',hsmc['num_face_0'][i] , len(Vts0) , hsmc['num_material_0'][i] , hsmc['num_sphere_0'][i] , 0 , 0 , 0 , 0 )

    DATA += struct.pack('=8I',hsmc['num_face_1'][i] , len(Vts1) , hsmc['num_material_1'][i] , hsmc['num_sphere_1'][i] , 0 , 0 , 0 , 0 )

   CHUNKS.append([ b'HSMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16
   


# COLLISION MESH TYPE 0 ------------------------------- XTVC,ECFC,TAMC,HPSC ----------------------------------------------------------------///////////////



  if ( b'XTVC' in Signs ):

   DATA = b''

   for i in range ( 0 , len(Vts0) ):

        DATA += struct.pack('=3f1I',Vts0[i][0], Vts0[i][1], Vts0[i][2] ,Vts0[i][3])

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(ecfc) ):

        DATA += struct.pack('=4H',Vin00[ecfc['a'][i]], Vin00[ecfc['b'][i]], Vin00[ecfc['c'][i]], ecfc['_mat'][i])

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(tamc) ):

    DATA += struct.pack('=1f1H2h1H',tamc['opacity'][i], tamc['portal'][i], tamc['diffuse'][i], tamc['mat_id'][i], int(0))

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

   for i in range ( 0 , len(Vts1) ):
     
      DATA += struct.pack('=3f1I',Vts1[i][0], Vts1[i][1], Vts1[i][2], Vts1[i][3])

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(ecfc1) ):
     
      DATA += struct.pack('=4H',Vin1[ecfc1['a'][i]], Vin1[ecfc1['b'][i]], Vin1[ecfc1['c'][i]], ecfc1['_mat'][i])

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(tamc1) ):

    DATA += struct.pack('=1f1H2h1H',tamc1['opacity'][i], tamc1['portal'][i], tamc1['diffuse'][i], tamc1['mat_id'][i], int(0))

   CHUNKS.append([ b'TAMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(hpsc1) ):

    DATA += struct.pack('=4f4H',hpsc1['px'][i], hpsc1['py'][i], hpsc1['pz'][i], hpsc1['size'][i], hpsc1['_0'][i] , hpsc1['_1'][i] , hpsc1['_a'][i] , hpsc1['_b'][i])

   CHUNKS.append([ b'HPSC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# TEXTURE BASED ANIM DATA ------------------------------- TXAN ---------------------------------------------------------------------------///////////////



  if ( b'TXAN' in Signs ):

   DATA = b''

   for i in range ( 0 , len(txan) ):

    DATA += struct.pack('=2I',txan['_00'][i],txan['_01'][i])

   CHUNKS.append([ b'TXAN' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

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


def CalC_UniqueVertsID(xtvc):

    Vts = []

    for i in range ( 0 , len(xtvc) ):

      Vts.append([ xtvc['px'][i], xtvc['py'][i], xtvc['pz'][i], 0 ])

    Vts02,Vin02 = [],[]

    for i in range ( 0 , len(Vts) ):

        E = 0
            
        for j in range ( 0 , len(Vts02) ):
                
            if Vts[i] == Vts02[j]:
                    
                Vin02.append(j)
                       
                E = 1
                       
                break
                    
        if E == 0:
                
                Vin02.append(len(Vts02))
                
                Vts02.append(Vts[i])

    return Vts02,Vin02


def CalC_MeshNormals(xtrv,ecaf,dner):

  Fnts,Nts = [],[]

  for i in range ( 0, len(xtrv) ):
                                    Nts.append([ 0.0e+00,0.0e+00,0.0e+00 ])
  for i in range ( 0 , len(ecaf) ):
    
      A,B,C = ecaf['a'][i],ecaf['b'][i],ecaf['c'][i]

      PA = [ xtrv['px'][A], xtrv['py'][A], xtrv['pz'][A] ]
      PB = [ xtrv['px'][B], xtrv['py'][B], xtrv['pz'][B] ]
      PC = [ xtrv['px'][C], xtrv['py'][C], xtrv['pz'][C] ]
            
      Edge1 = [ PC[0]-PA[0] , PC[1]-PA[1] , PC[2]-PA[2] ]
      Edge2 = [ PB[0]-PA[0] , PB[1]-PA[1] , PB[2]-PA[2] ]
      X = np.cross( Edge1, Edge2 )
      
      if ( np.linalg.norm(X) != 0 ):                                  
       NVert = X/np.linalg.norm(X)
       
       Nts[A] = [ Nts[A][0]+NVert[0], Nts[A][1]+NVert[1], Nts[A][2]+NVert[2] ]
       Nts[B] = [ Nts[B][0]+NVert[0], Nts[B][1]+NVert[1], Nts[B][2]+NVert[2] ]
       Nts[C] = [ Nts[C][0]+NVert[0], Nts[C][1]+NVert[1], Nts[C][2]+NVert[2] ]

  for i in range ( 0 , len(xtrv) ):

      if ( np.linalg.norm(Nts[i]) == 0 ): 
                                          Nts[i] = [ 0.0e+00,1.0e+00,0.0e+00 ]
      if ( np.linalg.norm(Nts[i]) != 0 ):
                                          Nts[i] = Nts[i]/np.linalg.norm(Nts[i])
      continue

  return Nts

    
