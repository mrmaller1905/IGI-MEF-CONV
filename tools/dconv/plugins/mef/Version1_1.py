import os
import io
import struct
from .import reader_ilff
from .import IGI1_mef_struct
from .IGI1_mef_struct import *
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

     dner = parse_dner(reader.read(b'DNER'),1)[0]

     xtrv = parse_xtrv(reader.read(b'XTRV'),1)

     ecaf = parse_dner(reader.read(b'DNER'),1)[1]

    if reader.find(b'HSMC'):
    
     hsmc = parse_hsmc(reader.read(b'HSMC',0))

     xtvc = parse_xtvc(reader.read(b'XTVC',0))

     ecfc = parse_ecfc(reader.read(b'ECFC',0))

     tamc = parse_tamc(reader.read(b'TAMC',0))

     hpsc = parse_hpsc(reader.read(b'HPSC',0))
    
     xtvc1= parse_xtvc(reader.read(b'XTVC',1))

     ecfc1= parse_ecfc(reader.read(b'ECFC',1))

     tamc1= parse_tamc(reader.read(b'TAMC',1))

     hpsc1= parse_hpsc(reader.read(b'HPSC',1))

    if reader.find(b'TXAN'):

     txan = parse_txan(reader.read(b'TXAN'))

    Signs = reader.signatures()

    NameOfModel = str(os.path.splitext(os.path.basename(File))[0])

# --------------------------------------------------> NECESSARY ADDITIONAL DATA

    if (True):

        Bone = []

        T = 0

        if ( max(xtrv['bn']) in ( 30 , 31 ) ):

          if ( NameOfModel in ("000_01_1","009_02_1","008_01_1") ):
                                                       T = 0
          if ( NameOfModel in ("001_01_1","001_02_1","003_01_1","003_02_1","004_01_1","004_02_1","006_01_1","009_01_1","009_02_1","011_01_1","011_02_1","011_03_1","013_01_1","014_01_1","014_02_1","016_01_1","018_01_1","019_01_1","020_01_1","021_01_1","022_01_1") ):
                                                       T = 1
          if ( NameOfModel in ("012_01_1","015_01_1","028_01_1") ):
                                                       T = 6
                                                       
          if ( T == 0 ): # Type 0
              
            Bone.append([  [b'center',-1,0.00000000,0.00000000,3990.4000000],
                           [b'lower body',0,-5.13892293e-01,1.83352112e+02,553.558],
                           [b'upper body',1,1.52358502e-01,-3.77480377e+02,1280.4136],
                           [b'shoulders',2,7.41089210e-02,9.60487366e+01,631.042],
                           [b'head',3,-3.96711912e-05,1.03258926e+02,352.9273],
                           [b'head_lower',4,-1.01815081e+00,9.77469406e+01,891.61316],
                           [b'head_upper',4,-1.13468617e-01,7.63609085e+01,121.43697],
                           [b'head_end',6,3.71010319e-05,4.54250488e+02,-358.70023],
                           [b'upper left arm',3,-8.73770996e+02,1.80327621e+02,-380.14197],
                           [b'lower left arm',8,-4.98601959e+02,-2.20046127e+02,-1074.86],
                           [b'left hand',9,-4.76041199e+02,2.13745651e+02,-980.41034],
                           [b'upper left finge',10,-2.31919205e+02,-2.96972692e-03,-439.61548],
                           [b'lower left finge',11,-1.12167320e+01,1.05587096e-04,-200.45413],
                           [b'left fingers end',12,-1.51359072e+01,-5.44903160e-05,-306.64743],
                           [b'upper right arm',3,8.77789124e+02,1.80327209e+02,-380.14032],
                           [b'lower right arm',14,4.94149628e+02,-2.20123535e+02,-1074.8108],
                           [b'right hand',15,4.68049896e+02,2.13821838e+02,-985.94403],
                           [b'upper right fing',16,2.32673676e+02,-1.04437349e-04,-433.71722],
                           [b'lower right fing',17,1.36010542e+01,3.24469962e-04,-200.1371],
                           [b'right fingers en',18,2.63072968e+00,-1.09073611e-04,-307.542],
                           [b'none00',1,5.44034815e+00,7.25950439e+02,-228.98277],
                           [b'none01',20,9.46663422e-05,2.10357861e+03,392.49387],
                           [b'none02',21,8.08206314e-05,1.61433179e+03,1297.793],
                           [b'upper left leg',0,-4.30378998e+02,9.49665756e+01,-44.375652],
                           [b'lower left leg',23,-8.46106589e-01,2.08386444e+02,-1737.646],
                           [b'left foot',24,7.99461365e+01,-3.63005524e+02,-1827.7457],
                           [b'left toe',25,-2.31287994e+01,3.90893158e+02,-163.4263],
                           [b'left toe end',26,-3.08275185e+01,7.38062317e+02,-258.84998],
                           [b'upper right leg',0,4.35314667e+02,9.49653473e+01,-44.375652],
                           [b'lower right leg',28,3.45443940e+00,2.08386444e+02,-1737.6501],
                           [b'right foot',29,-7.91121902e+01,-3.63005524e+02,-1827.7416],
                           [b'right toe',30,1.66293087e+01,3.90893158e+02,-163.4263],
                           [b'right toe end',31,1.02110405e+01,7.38062317e+02,-258.84998] ])


          if ( T == 1 ):  # Type 1/2/3
              
            Bone.append([  [b'center',-1,0.00000000,0.00000000,3990.40000000],
                           [b'lower body',0,-5.13904631e-01,1.8335211e+02,553.558],
                           [b'upper body',1,1.52365461e-01,-3.6878210e+02,1027.4037],
                           [b'shoulders',2,7.40687847e-02,9.6049149e+01,686.4855],
                           [b'head',3,9.28120812e-07,8.1288391e+01,371.17868],
                           [b'head_lower',4,-1.01816308e+00,9.7746941e+01,891.61316],
                           [b'head_upper',4,-1.13495238e-01,7.6360909e+01,121.437386],
                           [b'head_end',6,1.59762021e-05,4.5425049e+02,-358.6998],
                           [b'upper left arm',3,-8.52697083e+02,1.8032762e+02,-389.19165],
                           [b'lower left arm',8,-5.05782257e+02,-1.2448235e+02,-947.757],
                           [b'left hand',9,-4.51174377e+02,3.6357815e+01,-831.19714],
                           [b'upper left finge',10,-1.74661209e+02,-3.1095438e-03,-306.36646],
                           [b'lower left finge',11,-5.47590141e+01,-2.6617035e-05,-246.78154],
                           [b'left fingers end',12,-1.52120523e+01,-3.5429046e-05,-385.1272],
                           [b'upper right arm',3,8.17057739e+02,1.8032721e+02,-389.19003],
                           [b'lower right arm',14,5.05384949e+02,-1.2455936e+02,-928.3666],
                           [b'right hand',15,4.01260132e+02,3.6434246e+01,-848.47],
                           [b'upper right fing',16,1.70200256e+02,1.5114690e-04,-307.54242],
                           [b'lower right fing',17,5.92297974e+01,2.4149237e-04,-237.6237],
                           [b'right fingers en',18,8.28260326e+00,-2.1982698e-05,-377.2043],
                           [b'none00',1,1.12996347e-01,7.2239508e+02,-229.50092],
                           [b'none01',20,8.60274668e-05,2.1035786e+03,392.49387],
                           [b'none02',21,7.42084594e-05,1.6143318e+03,1297.793],
                           [b'upper left leg',0,-4.30378998e+02,9.4966164e+01,-44.375244],
                           [b'lower left leg',23,-8.46045136e-01,-4.2745033e+01,-1789.1041],
                           [b'left foot',24,7.99461365e+01,-1.6188129e+02,-1850.7448],
                           [b'left toe',25,-2.31287594e+01,3.9089316e+02,-163.4263],
                           [b'left toe end',26,-3.08275604e+01,7.3806232e+02,-258.84998],
                           [b'upper right leg',0,4.35314667e+02,9.4965347e+01,-44.375652],
                           [b'lower right leg',28,3.45439839e+00,-4.2745033e+01,-1789.1082],
                           [b'right foot',29,-7.91121902e+01,-1.6188129e+02,-1850.7448],
                           [b'right toe',30,1.66292667e+01,3.9089316e+02,-163.4263],
                           [b'right toe end',31,1.02110405e+01,7.3806232e+02,-258.84998] ])


          if ( T == 6 ):  # Type 6
              
            Bone.append([  [b'center',-1,0.00000000,0.00000000,3990.40000000],
                           [b'lower body',0,-5.13896406e-01,1.83352112e+02,489.6645],
                           [b'upper body',1,1.52378157e-01,-2.18227097e+02,1046.5403],
                           [b'shoulders',2,7.40782022e-02,5.87649002e+01,513.7039],
                           [b'head',3,3.28596684e-06,8.12888031e+01,371.17828],
                           [b'head_lower',4,-1.01817131e+00,9.77469406e+01,891.61316],
                           [b'head_upper',4,-1.13495238e-01,7.63609085e+01,121.4378],
                           [b'head_end',6,1.15636631e-05,4.54250488e+02,-358.70023],
                           [b'upper left arm',3,-5.83679993e+02,5.83929825e+01,-389.19165],
                           [b'lower left arm',8,-4.66862061e+02,-2.15144844e+01,-868.36017],
                           [b'left hand',9,-4.37157867e+02,3.63582230e+01,-852.6479],
                           [b'upper left finge',10,-1.99647629e+02,-3.04460176e-03,-260.6461],
                           [b'lower left finge',11,-2.45681343e+01,-9.16303816e-06,-210.57986],
                           [b'left fingers end',12,9.49948349e+01,-4.26356710e-05,-318.0638],
                           [b'upper right arm',3,5.80255737e+02,5.83925743e+01,-389.19003],
                           [b'lower right arm',14,4.63294434e+02,-2.15915298e+01,-874.6844],
                           [b'right hand',15,4.35507172e+02,3.64342461e+01,-844.1979],
                           [b'upper right fing',16,1.94484619e+02,4.95280110e-05,-241.98267],
                           [b'lower right fing',17,5.74742508e+01,-5.37550841e-05,-190.76791],
                           [b'right fingers en',18,-4.76352501e+01,5.51038975e-05,-375.40042],
                           [b'none00',1,1.12985700e-01,7.22395081e+02,-229.50092],
                           [b'none01',20,8.78370774e-05,2.10357861e+03,392.49344],
                           [b'none02',21,4.90893290e-05,1.61433179e+03,1297.793],
                           [b'upper left leg',0,-3.28154297e+02,9.49665756e+01,-44.375652],
                           [b'lower left leg',23,-8.46086085e-01,-7.94472427e+01,-1660.7231],
                           [b'left foot',24,7.99461365e+01,-1.13308464e+02,-1689.0879],
                           [b'left toe',25,-2.31287594e+01,3.90893158e+02,-342.1192],
                           [b'left toe end',26,-3.08275604e+01,7.38062317e+02,-258.84998],
                           [b'upper right leg',0,3.30613129e+02,9.49653473e+01,-44.375652],
                           [b'lower right leg',28,3.45442700e+00,-7.94472427e+01,-1660.7273],
                           [b'right foot',29,-7.91121902e+01,-1.13308464e+02,-1689.0879],
                           [b'right toe',30,1.66293087e+01,3.90893158e+02,-342.1192],
                           [b'right toe end',31,1.02111225e+01,7.38062317e+02,-258.84998] ])

            
        elif ( max(xtrv['bn']) == 48 ):
            

            Bone.append([  [b'center shoulders',-1,0.0000000,0.0000000,0.0000000],
                           [b'none11',0,-1.1343995e-01,808.52167,-384.8368],
                           [b'none12',1,6.1222905e-05,1066.7172,-1691.1564],
                           [b'none13',2,5.0344344e-05,1576.28,1174.8434],
                           [b'upper right arm',0,8.4967010e+02,180.32721,132.39622],
                           [b'lower right arm',4,4.3388925e+02,-149.5171,-779.57935],
                           [b'right hand',5,-9.7083801e+01,-978.6327,3.3235476],
                           [b'upper right fore',6,-3.1386255e+01,-467.02182,-19.283188],
                           [b'lower right fore',7,-2.8277719e+00,-197.48618,17.174404],
                           [b'right forefinger',8,-3.0587697e+00,-95.37372,13.356072],
                           [b'none01',9,4.5676541e-05,-172.4121,14.865039],
                           [b'upper right litt',6,1.7049968e+02,-422.55972,-6.261186],
                           [b'lower right litt',11,4.4212223e+01,-121.56846,24.181145],
                           [b'right little fin',12,2.2205603e+01,-75.37213,2.3467457],
                           [b'none02',13,3.6761887e+01,-172.4121,14.86508],
                           [b'upper right midd',6,7.1074196e+01,-446.1445,-21.541477],
                           [b'lower right midd',15,2.8278374e+01,-174.86356,17.174322],
                           [b'right middle fin',16,1.6271030e+01,-92.138695,13.121167],
                           [b'none03',17,1.9012526e+01,-182.83273,14.350663],
                           [b'upper right ring',6,-1.4618254e+02,-462.87256,-23.310581],
                           [b'lower right ring',19,-4.3129650e+01,-145.90894,25.17295],
                           [b'right ring finge',20,-2.2678118e+01,-89.71755,13.356154],
                           [b'none04',21,-3.9589764e+01,-155.44524,14.865039],
                           [b'upper right thum',6,-9.8684921e+01,-161.50813,45.1543],
                           [b'lower right thum',23,-7.9162163e+01,95.27623,-83.39865],
                           [b'right thumb tip',24,-2.1998058e+01,-120.164345,64.02785],
                           [b'none05',25,1.5249572e+01,-162.13974,53.904995],
                           [b'upper left arm',0,-8.5407739e+02,180.32721,132.39622],
                           [b'lower left arm',27,-4.3388925e+02,149.5171,779.57935],
                           [b'left hand',28,9.7083801e+01,978.6327,-3.3235393],
                           [b'upper left foref',29,-7.1074608e+01,446.4312,12.079514],
                           [b'lower left foref',30,-2.8278456e+01,172.79057,-13.583974],
                           [b'left forefinger ',31,-1.6120094e+01,90.7436,-12.373688],
                           [b'none06',32,-1.9012402e+01,182.83273,-14.350581],
                           [b'upper left littl',29,3.1386295e+01,467.30853,9.821224],
                           [b'lower left littl',34,2.8277595e+00,198.48232,-8.268759],
                           [b'left little fing',35,2.8405800e+00,93.8242,-12.595568],
                           [b'none07',36,-3.3972385e-05,172.4121,-14.864957],
                           [b'upper left middl',29,-1.7049968e+02,419.45905,3.8814964],
                           [b'lower left middl',38,-4.4212223e+01,128.28795,-17.394156],
                           [b'left middle fing',39,-2.2205521e+01,76.166756,-9.846415],
                           [b'none08',40,-3.6761887e+01,172.4121,-14.864998],
                           [b'upper left ring',29,1.4618254e+02,463.15927,13.848699],
                           [b'lower left ring',42,4.3129650e+01,147.39537,-11.426856],
                           [b'left ring finger',43,2.4544132e+01,92.61793,-10.2587185],
                           [b'none09',44,3.9589642e+01,155.44524,-14.865121],
                           [b'upper left thumb',29,9.8684921e+01,161.50813,-45.1543],
                           [b'lower left thumb',46,8.9203506e+01,-95.27623,84.01346],
                           [b'left thumb tip',47,2.1998140e+01,121.58238,-60.84649],
                           [b'none10',48,-1.5249531e+01,154.34587,-60.435658],
                           [b'none20',0,-1.1341291e-01,808.52167,156.95953],
                           [b'none21',50,7.7520075e-05,1992.581,-165.84662],
                           [b'none22',51,6.6365435e-05,1962.6721,-113.23023],
                           [b'none30',0,-1.1346616e-01,808.52167,730.6076],
                           [b'none31',53,1.3104209e-04,1875.9844,691.7939],
                           [b'none32',54,-4.8148479e-05,1831.6246,-714.1867] ])
            
# Bone CONVERSION ------->


  B = Bone[0]
  
  if (len(B)) == 56:
                    ID = [ 0,27,4, 28,5, 29,6, 30,34,38,42,46,7,11,15,19,23, 31,35,39,43,47,8,12,16,20,24, 32,36,40,44,48,9,13,17,21,25, 33,37,41,45,49,10,14,18,22,26 ]
                    ID = [ 0,1,4,27,50,53,2,5,28,51,54,3,6,29,52,55,7,11,15,19,23,30,34,38,42,46,8,12,16,20,24,31,35,39,43,47,9,13,17,21,25,32,36,40,44,48,10,14,18,22,26,33,37,41,45,49 ]
  elif len(B) == 33:
                    ID = [ 0,1,23,28, 2,24,29, 3,25,30, 4,-1,-2,26,31, 5+(6-6),8,14,27,32, 7,9,15, 10,16, 11,17, 12,18, 13,19 ]
                    ID = [ 0,1,23,28,20,2,24,29,21,3,25,30,22,4,8,14,26,31,5,6,9,15,27,32,7,10,16,11,17,12,18,13,19 ]
  else:
                    E=input("ERROR")
  I,Bone = [],[]

  BONELINK = []

  for i in range ( 0, len(B) ):

    I.append(-1)

    for j in range( 0, len(ID) ):

       if ( i == ID[j] ):
                         I[-1] = j+0

  for i in range ( 0 , len(ID) ):

    Bone.append([ B[ID[i]][0], I[B[ID[i]][1]],B[ID[i]][2], B[ID[i]][3], B[ID[i]][4]  ])

  Bone[0][1] = -1

  for i in range ( 0 , len(Bone) ):

    N = 0
    for j in range ( 0 , len(Bone) ):

      if ( i == Bone[j][1] ):
                              N += 1
    BONELINK.append(N)


# --------------------------------------------------> SOME NECESSARY CALCULATIONS

  if ( b'HSEM' in Signs ):

   D = hsem['rs'][0][0]

  HSEM_DATASIZE_RENDERMESH = 0

  HSEM_DATASIZE_COLLISONMESH = 0

  NUMBER_OF_BONES = 0

  if ( b'D3DR' in Signs ):

    HSEM_DATASIZE_RENDERMESH += 40 + (d3dr['num_face'][0]*6) + (d3dr['num_mesh'][0]*32) + (d3dr['num_verts'][0]*40)

  if ( b'HSMC' in Signs ):

    HSEM_DATASIZE_COLLISONMESH += 32 + (hsmc['num_face_0'][0]*12) + (hsmc['num_vertex_0'][0]*20) + (hsmc['num_material_0'][0]*16) + (hsmc['num_sphere_0'][0]*24)

    HSEM_DATASIZE_COLLISONMESH += 32 + (hsmc['num_face_1'][0]*12) + (hsmc['num_vertex_1'][0]*20) + (hsmc['num_material_1'][0]*16) + (hsmc['num_sphere_1'][0]*24)

  if ( b'XTRV' in Signs ):

    if ( max(xtrv['bn']) in ( 30 , 31 ) ):

        NUMBER_OF_BONES = 33

    if ( max(xtrv['bn']) in ( 47 , 48 ) ):

        NUMBER_OF_BONES = 56

  DNER_OFFSET_V1 = [0]

  for R in range ( 0 , len(dner)-1 ):

      DNER_OFFSET_V1.append(DNER_OFFSET_V1[-1]+dner['num_face'][R])
      

  FACES = []

  for R in range ( 0 , len(dner) ):

    OFF = dner['off_verts'][R]

    for i in range ( (DNER_OFFSET_V1[R] // 3) , (DNER_OFFSET_V1[R] // 3) + (dner['num_face'][R] // 3) ):

      FACES.append([ ecaf['a'][i]+OFF , ecaf['b'][i]+OFF , ecaf['c'][i]+OFF ])
  

  DNER_OPACITY_V1 = []

  for R in range ( 0 , len(dner) ):

    N = 0
    
    if ( dner['_opacity'][R] == 1 ):
                                      N += 4
    if ( dner['_Eflame'][R] == 1 ):
                                      N += 3
    DNER_OPACITY_V1.append(N)

    

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

    DATA += struct.pack('=1f',0.16)

    DATA += struct.pack('=7I',hsem['Date'][i][0] , hsem['Date'][i][1] , hsem['Date'][i][2] , hsem['Date'][i][3] , hsem['Date'][i][4] , hsem['Date'][i][5] , hsem['Date'][i][6])

    DATA += struct.pack('=4I',hsem['model_type'][i], hsem['reserved_0'][i][0] , hsem['reserved_0'][i][1] , hsem['reserved_0'][i][2])

    DATA += struct.pack('=12f',hsem['vectors'][i][0] , hsem['vectors'][i][1] , hsem['vectors'][i][2] , hsem['vectors'][i][3] , hsem['vectors'][i][4] , hsem['vectors'][i][5] , hsem['vectors'][i][6] , hsem['vectors'][i][7] , hsem['vectors'][i][8] , hsem['vectors'][i][9] , hsem['vectors'][i][10] ,hsem['vectors'][i][11])

    DATA += struct.pack('=3I',hsem['num_r_faces'][i], d3dr['verts_1'][0], HSEM_DATASIZE_RENDERMESH) ##
    
    DATA += struct.pack('=3I',hsem['sum_c_faces'][i], hsem['sum_c_verts'][i], HSEM_DATASIZE_COLLISONMESH) ##
    
    DATA += struct.pack('=1f',hsem['model_radius'][i])
    
    DATA += struct.pack('=7H', hsem['num_mverts'][i], hsem['num_attachments'][i], hsem['num_pverts'][i], hsem['num_pfaces'][i], hsem['num_portals'][i], int(NUMBER_OF_BONES), int(0))

    DATA += struct.pack('=38B',D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D)

   CHUNKS.append([ b'HSEM' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


# OTHER MODEL_INFO ------------------------------- ATTA,XTVM,WOLG ----------------------------------------------------------------///////////////


  if ( b'ATTA' in Signs ):

   DATA = b''

   for i in range ( 0 , len(atta) ):

    DATA += struct.pack('=16s6f',atta['name'][i], atta['px'][i], atta['py'][i], atta['pz'][i], atta['_00'][i], atta['_01'][i], atta['_02'][i])

    DATA += struct.pack('=6f1I1i',atta['_03'][i],atta['_04'][i],atta['_05'][i], atta['_06'][i],atta['_07'][i],atta['_08'][i], atta['_09'][i],-1)
    
   CHUNKS.append([ b'ATTA' , len(DATA) , 4 , len(DATA) + 16 , DATA ])   

   SIZE += len(DATA) + 16
  

# BONE LINKS INFO ------------------------------- REIH,MANB,HPRM ----------------------------------------------------------------///////////////


  if ( b'HSEM' in Signs ):

   DATA = b''

   for i in range ( 0 , len(Bone) ):

    DATA += struct.pack('=1B',BONELINK[i]) ##

   DATA += struct.pack('=1B',0)

   for i in range ( 0 , len(Bone) ):

    DATA += struct.pack('=3f',Bone[i][2],Bone[i][3],Bone[i][4]) 
    
   SKIP = GetSkipBytes(len(DATA)) 

   CHUNKS.append([ b'REIH' , len(DATA) , 4 , len(DATA)+len(SKIP) + 16 , DATA+SKIP ])

   SIZE += len(DATA)+len(SKIP) + 16

   DATA = b''

   for i in range ( 0 , len(Bone) ):

    DATA += struct.pack('=16s',Bone[i][0]) ##
    
   CHUNKS.append([ b'MANB' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# XTVM ----------------------->


  if ( b'XTVM' in Signs ):

   DATA = b''

   for i in range ( 0 , len(xtvm) ):

    DATA += struct.pack('=3f1i',xtvm['px'][i] , xtvm['py'][i] , xtvm['pz'][i], xtvm['_0'][i])

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


   if ( b'D3DR' in Signs ): # ----------------------------------------|

    DATA = b''

    for i in range ( 0 , len(d3dr) ):

     DATA += struct.pack('=10I',d3dr['_4'][i], d3dr['num_face'][i], d3dr['num_mesh'][i], d3dr['verts_0'][i], d3dr['verts_1'][i], d3dr['num_verts'][i], 0, 0, 0, 0)

   CHUNKS.append([ b'D3DR' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(FACES) ):

    DATA += struct.pack('=3H',FACES[i][0],FACES[i][1],FACES[i][2]) ##

   SKIP = GetSkipBytes(len(DATA)) 

   CHUNKS.append([ b'ECAF' , len(DATA) , 4 , len(DATA)+len(SKIP) + 16 , DATA+SKIP ])

   SIZE += len(DATA)+len(SKIP) + 16

   DATA = b''

   for i in range ( 0 , len(dner) ):

    DATA += struct.pack('=4B3f1H',DNER_OPACITY_V1[i], dner['_mshine'][i], dner['_Scolor'][i], dner['_Opacitd'][i], 0.0, 0.0, 0.0, DNER_OFFSET_V1[i])

    DATA += struct.pack('=3H3h2B',dner['num_face'][i]//3, dner['off_verts'][i], dner['num_verts'][i], dner['_td'][i], -1, -1, 0, 0)
    
   CHUNKS.append([ b'DNER' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(xtrv) ):

    DATA += struct.pack('=6f',xtrv['px'][i], xtrv['py'][i], xtrv['pz'][i], xtrv['nx'][i], xtrv['ny'][i], xtrv['nz'][i])

    DATA += struct.pack('=3f2H',xtrv['u'][i], xtrv['v'][i], xtrv['w'][i], xtrv['vn'][i], I[xtrv['bn'][i]])

   CHUNKS.append([ b'XTRV' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


  if ( b'HSMC' in Signs ): # ----------------------------------------|

   DATA = b''

   DATA += struct.pack('=8I',hsmc['num_face_0'][0] , hsmc['num_vertex_0'][0] , hsmc['num_material_0'][0] , hsmc['num_sphere_0'][0] , 0 , 0 , 0 , 0 )

   DATA += struct.pack('=8I',hsmc['num_face_1'][0] , hsmc['num_vertex_1'][0] , hsmc['num_material_1'][0] , hsmc['num_sphere_1'][0] , 0 , 0 , 0 , 0 )

   CHUNKS.append([ b'HSMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   

# COLLISION MESH TYPE 0 ------------------------------- XTVC,ECFC,TAMC,HPSC ----------------------------------------------------------------///////////////


  if ( b'XTVC' in Signs ):

   DATA = b''

   for i in range ( 0 , len(xtvc) ):

    DATA += struct.pack('=3f1Q',xtvc['px'][i], xtvc['py'][i], xtvc['pz'][i], I[xtvc['bn'][i]])

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(ecfc) ):

    DATA += struct.pack('=6H',ecfc['a'][i] , ecfc['b'][i] , ecfc['c'][i], ecfc['_mat'][i], 65535, int(0)) 

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(tamc) ):

    DATA += struct.pack('=1f1H1h1i1h1H',tamc['opacity'][i], tamc['portal'][i], tamc['diffuse'][i], int(0), tamc['mat_id'][i], tamc['unknown'][i]) 

   CHUNKS.append([ b'TAMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(hpsc) ):

    DATA += struct.pack('=4f4H',hpsc['px'][i] , hpsc['py'][i] , hpsc['pz'][i] , hpsc['size'][i], hpsc['_0'][i] , hpsc['_1'][i] , hpsc['_a'][i] , hpsc['_b'][i] )

   CHUNKS.append([ b'HPSC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# COLLISION MESH TYPE 1 ------------------------------- XTVC,ECFC,TAMC,HPSC ----------------------------------------------------------------///////////////


  if ( b'XTVC' in Signs ):

   DATA = b''

   for i in range ( 0 , len(xtvc1) ):

    DATA += struct.pack('=3f1Q',xtvc1['px'][i], xtvc1['py'][i], xtvc1['pz'][i], I[xtvc1['bn'][i]])

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(ecfc1) ):

    DATA += struct.pack('=6H',ecfc1['a'][i] , ecfc1['b'][i] , ecfc1['c'][i], ecfc1['_mat'][i], 65535, int(0))

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(tamc1) ):

    DATA += struct.pack('=1f1H1h1i1h1H',tamc1['opacity'][i], tamc1['portal'][i], tamc1['diffuse'][i], int(0), tamc1['mat_id'][i], tamc1['unknown'][i])

   CHUNKS.append([ b'TAMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

   DATA = b''

   for i in range ( 0 , len(hpsc1) ):

    DATA += struct.pack('=4f4H',hpsc1['px'][i] , hpsc1['py'][i] , hpsc1['pz'][i] , hpsc1['size'][i], hpsc1['_0'][i] , hpsc1['_1'][i] , hpsc1['_a'][i] , hpsc1['_b'][i])

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

    
  
