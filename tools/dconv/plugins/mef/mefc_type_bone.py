import os 
import numpy as np
import math
from .import fun
from .import reader_ilff
from .import mef_struct
from .import reader_data2
from math import *
from .fun import *
from .mef_struct import *
from .reader_ilff import *
from .reader_data2 import *

def fromfile(meffilename, srcpth):
    
    meftext = ""
    
    reader = reader_ilff.open(srcpth)        
    
    hsem = parse_hsem(reader.read(b'HSEM'))
    
    manb = parse_manb(reader.read(b'MANB'))

    atta = parse_atta(reader.read(b'ATTA'))

    xtvm = parse_xtvm(reader.read(b'XTVM'))

    trop = parse_trop(reader.read(b'TROP'))

    xvtp = parse_xvtp(reader.read(b'XVTP'))

    cftp = parse_cftp(reader.read(b'CFTP'))

    ecaf = parse_ecaf(reader.read(b'ECAF'))
 
    d3dr = parse_d3dr(reader.read(b'D3DR'),1)    

    dner = parse_dner(reader.read(b'DNER'),1)

    xtrv = parse_xtrv(reader.read(b'XTRV'),1)

    reih1 = parse_reih(reader.read(b'REIH'))[0]

    reih2 = parse_reih(reader.read(b'REIH'))[1]
    
    if reader.find(b'WOLG'):
        
        wolg = parse_wolg(reader.read(b'WOLG'))
    
    if reader.find(b'HSMC'):
    
        hsmc = parse_hsmc(reader.read(b'HSMC'))    
    
        xtvc0 = parse_xtvc(reader.read(b'XTVC',0),1)
    
        ecfc0 = parse_ecfc(reader.read(b'ECFC',0))
    
        tamc0 = parse_tamc(reader.read(b'TAMC',0))
    
        hpsc0 = parse_hpsc(reader.read(b'HPSC',0))

        xtvc1 = parse_xtvc(reader.read(b'XTVC',1),1)
        
        ecfc1 = parse_ecfc(reader.read(b'ECFC',1))

        tamc1 = parse_tamc(reader.read(b'TAMC',1))

        hpsc1 = parse_hpsc(reader.read(b'HPSC',1))

    if reader.find(b'HPRM'):

        hprm1 = parse_hprm(reader.read(b'HPRM'))[0]
        
        hprm2 = parse_hprm(reader.read(b'HPRM'))[1]


# MODEL Texture Reading ------------>


    if ( len(dner) != 0 ):

       Tm,Tb,Tr = max(dner['_td'])+1,max(dner['_tb'])+1,max(dner['_tr'])+1

       TextureFile = []

       if ( Tm < Tb ):
                        Tm = Tb
       if ( Tm < Tr ): 
                        Tm = Tr
       if ( Tm != 0 ):
                        TextureFile += reader_data2.fromtex(meffilename,Tm)


# Other Info ---------------------->

        
    Sc = 40.96

    Msh0 = [[],[],[],[],[]]

    dx,dy,dz = d3dr['verts_1'][0],d3dr['verts_0'][0],d3dr['num_verts'][0]
    
    NameOfModel = str(os.path.splitext(os.path.basename(meffilename))[0])

    if reader.find(b'HSMC'):
        

# SOME NECESSARY CALCULATIONS _______________->


        fun.NameOfModel = NameOfModel

        Vrts= GetBoneVerts(len(xtvc0),xtvc0)

        fun.DNER_NUMFACES = dner['num_face']

        fun.DNER_OFFFACES = dner['offset_index']//3

        fun.dner,fun.ecaf,fun.xtrv = dner,ecaf,xtrv

        Msh0 = CalC_modeldata1_1(tamc0,ecfc0,xtvc0,len(Msh0[0]),0,0,Msh0)
        
        Msh1 = CalC_modeldata1_1(tamc1,ecfc1,xtvc1,len(Msh0[0]),0,1,Msh0)
        
        
    
# Materials Data for MEF Conversion ----------

    
        Materials = ""

        Mesh = Msh1

        Mts = Mesh[0]

        n = 0
    
        for i in range ( 0, len(Mts) ):

            Mt = ""
            
            if ( Mts[i][1][0] == 1 ):
                    Mt += "MaterialTransparencyType(" + str(n) + ","+str(Mts[i][1][1])+");\n"       
            if ( Mts[i][2][0] != -1 ):
                    Mt += "DiffuseTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][2][0]]) + ".tga\"" + ","+str(Mts[i][2][1])+","+str(Mts[i][2][2])+");\n"
            if ( Mts[i][3][0] == 1 ):
                    Mt += "OpacityTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][2][0]]) + ".tga\"" + ","+str(Mts[i][3][1])+","+str(Mts[i][3][2])+");\n"
            if ( Mts[i][4][0] != -1 ):
                    Mt += "BumpTMap(" + "" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][4][0]]) + ".tga\"" + ","+str(Mts[i][4][1])+","+str(Mts[i][4][2])+");\n"
            if ( Mts[i][5][0] != -1 ):
                    Mt += "ReflectionTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][5][0]]) + ".tga\"" + ","+str(Mts[i][5][1])+","+str(Mts[i][5][2])+");\n"
        
            Mts[i][6] = Mts[i][6].replace("Material", "BONE")
            Mts[i][6] = Mts[i][6].replace(NameOfModel,"BONE")
                    
            Materials += "Material(" + str(n) + ",\"" + str(Mts[i][6]) + "\",0.588235,0.588235,0.588235,0.1,0.1,0.1,0.9,0.9,0.9,"+str(Mts[i][7])+","+str(Mts[i][8])+","+str(Mts[i][9])+");" + '\n'           
            Materials += "MaterialShininess(" + str(n) + ","+str(Mts[i][10])+");" + '\n' + str(Mt)

            n += 1


            
# Bone Data for MEF conversion -----------

  
        Bones = ""
        
        Bind = CalC_BoneLinks([-1],reih1)

        BneH = CalC_BoneOffset(Bind,reih2)

        for i in range ( 0 , len(manb) ):

            Bones += "Bone(" + str(i) + ",\"" + str(str(manb['bone_name'][i]))[2:-1] + "\"," + str(Bind[i]) + "," + str(reih2['px'][i]/Sc) + "," + str(reih2['py'][i]/Sc) + "," + str(reih2['pz'][i]/Sc) + ");\n"

        Bones += "BuildHierarchy();\n"

                
           
# Vertices Data for MEF conversion -------

    
        Vertices = ""

        Vts = Mesh[1]
    
        for i in range ( 0, len(Vrts) ):
        
            Vertices += "Vertex(" + str(i) + "," + str((Vrts[i][0]+BneH[0][Vrts[i][3]])/Sc) + "," + str((Vrts[i][1]+BneH[1][Vrts[i][3]])/Sc) + "," + str((Vrts[i][2]+BneH[2][Vrts[i][3]])/Sc) + ");" + '\n'
        
        Vtsi,Vin = CalC_BoneEffects(d3dr,xtrv,Vrts)

        for i in range ( 0 , len(Vtsi) ):
        
            Vertices += "VertexInfluenceRigid(" + str(Vtsi[i][0]) + "," + str(Vtsi[i][1]) + "," + str((Vtsi[i][2])/Sc) + "," + str((Vtsi[i][3])/Sc) + "," + str((Vtsi[i][4])/Sc) + "," + str(Vtsi[i][5]) + ");" + '\n'        

        
    
# Normal Vertices Data for MEF conversion -------


        Normals = ""

        n = 0

        Nts = Mesh[2]

        for i in range ( 0 , len(Nts) ):

            Normals += "Normal(" + str(n) + "," + str(Nts[i][0]) + "," + str(Nts[i][1]) + "," + str(Nts[i][2]) + ");" + '\n'

            n += 1
            
        
# Face Data for MEF conversion -------

        
        Faces = ""    
    
        n = 0

        Fces = Mesh[3]
        
        for i in range ( 0 , len(Fces) ):

            Faces += "Face(" + str(n) +","+str(Fces[i][0])+","+str(Fces[i][1])+","+str(Fces[i][2])+","+str(Fces[i][3])+","+str(Fces[i][4])+","+str(Fces[i][5])+","+str(Fces[i][6])+");" + '\n' 
   
            n = n + 1
                
            
# UV Data for MEF conversion -------

            
        UVs = ""
    
        n = 0

        Tcs = Mesh[4]
        
        for i in range ( 0 , len(Tcs) ):
    
            UVs += "UV(" + str(n) + ","+str(Tcs[i][0])+","+str(Tcs[i][3])+","+str(Tcs[i][1])+","+str(Tcs[i][4])+","+str(Tcs[i][2])+","+str(Tcs[i][5])+"" + ");" + '\n'
                    
            n = n + 1
                        
            
# Magic Vertices Data for MEF Conversion --------

                
        mvertices = ""  
    
        for i in range ( 0, len(xtvm) ):
        
            mvertices += "MagicVertex(" + str(i) + "," + "0" + "," + str((xtvm['px'][i])/Sc) + "," + str((xtvm['py'][i])/Sc) + "," + str((xtvm['pz'][i])/Sc) + "," + str(xtvm['_0'][i]) + ");" + '\n'
            
        
# Attachments Data for MEF Conversion --------

            
        attachments = ""
            
        for i in range ( 0, len(atta )):
    
            attachments += "AttachObject(\"" + str((str(atta['name'][i]))[2:-1]) + "\"," + str(i) + "," + str(atta['_00'][i]) + "," + str(atta['_01'][i]) + "," + str(atta['_02'][i]) + "," + str(atta['_03'][i]) + "," + str(atta['_04'][i]) + "," + str(atta['_05'][i]) + "," + str(atta['_06'][i]) + "," + str(atta['_07'][i]) + "," + str(atta['_08'][i]) + "," + str((atta['px'][i])/Sc) + "," + str((atta['py'][i])/Sc) + "," + str((atta['pz'][i])/Sc) + ");" + '\n'

            attachments += "AttachObjectBoneID(" + str(i) + "," + str(atta['_an'][i]) + ");" + '\n'

                

# Morph Data for MEF Conversion --------


        morphs = ""

        if reader.find(b'HPRM'):

          for m in range ( 0 , len(hprm1) ):                

            if ( hprm1['count_00'][m] != 0 ):

                morphs += "MorphChannel(" + str(m) + ",\"" + "Channel_0" + str(m+1) + "\");\n"
                

          Morph_list = []

          Off = 0

          for m in range ( 0 , len(hprm1) ):

             x = Off

             for i in range ( x , x + hprm1['count_00'][m] ):

                Morph_list.append([ m , Vin[hprm2['_Vn'][i]] , hprm2['_px'][i]/Sc , hprm2['_py'][i]/Sc , hprm2['_pz'][i]/Sc ])

                Off += 1

          Morphes = []

          for x in range ( 0 , len(Morph_list) ):

              E = 0

              for y in range ( 0 , len(Morphes) ):

                  if ( Morph_list[x][0] == Morphes[y][0] and Morph_list[x][1] == Morphes[y][1] and Morph_list[x][2] == Morphes[y][2] and Morph_list[x][3] == Morphes[y][3] and Morph_list[x][4] == Morphes[y][4] ):

                   E = 1

              if ( E == 0 ) :

                  Morphes.append([ Morph_list[x][0] , Morph_list[x][1] , Morph_list[x][2] , Morph_list[x][3] , Morph_list[x][4] ])
                  
          for i in range ( 0 , len(Morphes) ):

             morphs += "MorphVertex(" + str(Morphes[i][0]) + "," + str(Morphes[i][1]) + "," + str(Morphes[i][2]) + "," + str(Morphes[i][3]) + "," + str(Morphes[i][4]) + ");" + '\n'  
      

# ------------------------------------------

    
# Initial text (Newobject)

        meftext += "NewObject(\""+str(NameOfModel)+"\");\n"
    
# Material    

        meftext +=  str(Materials)

# Breakscript

        meftext += "BreakScript();\n"

# Bones

        meftext += str(Bones)
    
# Vertices     

        meftext +=  str(Vertices)   
    
# Normals     

        meftext +=  str(Normals)   
    
# Faces     

        meftext +=  str(Faces)   
    
# UV     

        meftext +=  str(UVs)   

# Morph Vertices

        meftext +=  str(morphs)
    
# magic vertices     

        meftext +=  str(mvertices)   
    
# attachments   

        meftext +=  str(attachments)
        

    else:

# SOME NECESSARY CALCULATIONS _______________->


        fun.NameOfModel = NameOfModel

        Vrts = fun.GetBoneVerts(dx,xtrv)
        
        fun.X,fun.Y = trop['o_face'],trop['n_face']

        Msh0 = fun.CalC_meshdata1_1(trop,cftp,xvtp,Msh0)

        fun.X,fun.Y = dner['offset_index']//3,dner['num_face']
        
        Msh1 = fun.CalC_meshdata1_1(dner,ecaf,xtrv,Msh0)
        
    
# Materials Data for MEF Conversion ----------    

    
        Materials = ""

        Mesh = Msh1

        Mts = Mesh[0]

        n = 0
    
        for i in range ( 0, len(Mts) ):

            Mt = ""
            
            if ( Mts[i][1][0] == 1 ):
                    Mt += "MaterialTransparencyType(" + str(n) + ","+str(Mts[i][1][1])+");\n"
            if ( Mts[i][2][0] != -1 ):
                    Mt += "DiffuseTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][2][0]]) + ".tga\"" + ","+str(Mts[i][2][1])+","+str(Mts[i][2][2])+");\n"
            if ( Mts[i][3][0] == 1 ):
                    Mt += "OpacityTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][2][0]]) + ".tga\"" + ","+str(Mts[i][3][1])+","+str(Mts[i][3][2])+");\n"
            if ( Mts[i][4][0] != -1 ):
                    Mt += "BumpTMap(" + "" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][4][0]]) + ".tga\"" + ","+str(Mts[i][4][1])+","+str(Mts[i][4][2])+");\n"
            if ( Mts[i][5][0] != -1 ):
                    Mt += "ReflectionTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][5][0]]) + ".tga\"" + ","+str(Mts[i][5][1])+","+str(Mts[i][5][2])+");\n"
        
            Mts[i][6] = Mts[i][6].replace("Material","BONE")
                    
            Materials += "Material(" + str(n) + ",\"" + str(Mts[i][6]) + "\",0.588235,0.588235,0.588235,0.1,0.1,0.1,0.9,0.9,0.9,"+str(Mts[i][7])+","+str(Mts[i][8])+","+str(Mts[i][9])+");" + '\n'           
            Materials += "MaterialShininess(" + str(n) + ","+str(Mts[i][10])+");" + '\n' + str(Mt)

            n += 1
            


# Bone Hierarchy for MEF Conversion ----------

  
        Bones = ""
        
        Bind = CalC_BoneLinks([-1],reih1)

        BneH = CalC_BoneOffset(Bind,reih2)

        for i in range ( 0 , len(manb) ):

            Bones += "Bone(" + str(i) + ",\"" + str(str(manb['bone_name'][i]))[2:-1] + "\"," + str(Bind[i]) + "," + str(reih2['px'][i]/Sc) + "," + str(reih2['py'][i]/Sc) + "," + str(reih2['pz'][i]/Sc) + ");\n"

        Bones += "BuildHierarchy();\n"
                
        
# Vertices Data for MEF conversion -------

    
        Vertices = ""

        Vts = Mesh[1]
    
        for i in range ( 0, len(Vrts) ):
        
            Vertices += "Vertex(" + str(i) + "," + str((Vrts[i][0]+BneH[0][Vrts[i][3]])/Sc) + "," + str((Vrts[i][1]+BneH[1][Vrts[i][3]])/Sc) + "," + str((Vrts[i][2]+BneH[2][Vrts[i][3]])/Sc) + ");" + '\n'
        
        Vtsi,Vin = fun.CalC_BoneEffects(d3dr,xtrv,Vrts)

        for i in range ( 0 , len(Vtsi) ):
        
            Vertices += "VertexInfluenceRigid(" + str(Vtsi[i][0]) + "," + str(Vtsi[i][1]) + "," + str((Vtsi[i][2])/Sc) + "," + str((Vtsi[i][3])/Sc) + "," + str((Vtsi[i][4])/Sc) + "," + str(Vtsi[i][5]) + ");" + '\n'

        
    
# Normal Vertices Data for MEF conversion -------


        Normals = ""

        n = 0

        Nts = Mesh[2]

        for i in range ( 0 , len(Nts) ):

            Normals += "Normal(" + str(n) + "," + str(Nts[i][0]) + "," + str(Nts[i][1]) + "," + str(Nts[i][2]) + ");" + '\n'

            n += 1
            
        
# Face Data for MEF conversion -------

        
        Faces = ""    
    
        n = 0

        Fces = Mesh[3]
        
        for i in range ( 0 , len(Fces) ):

            Faces += "Face(" + str(n) +","+str(Fces[i][0])+","+str(Fces[i][1])+","+str(Fces[i][2])+","+str(Fces[i][3])+","+str(Fces[i][4])+","+str(Fces[i][5])+","+str(Fces[i][6])+");" + '\n' 
   
            n = n + 1
                
            
# UV Data for MEF conversion -------

            
        UVs = ""
    
        n = 0

        Tcs = Mesh[4]
        
        for i in range ( 0 , len(Tcs) ):
    
            UVs += "UV(" + str(n) + ","+str(Tcs[i][0])+","+str(Tcs[i][3])+","+str(Tcs[i][1])+","+str(Tcs[i][4])+","+str(Tcs[i][2])+","+str(Tcs[i][5])+"" + ");" + '\n'
                    
            n = n + 1
                
            
# Magic Vertices Data for MEF Conversion --------                

                
        mvertices = ""  
    
        for i in range ( 0, len(xtvm) ):
        
            mvertices += "MagicVertex(" + str(i) + "," + "0" + "," + str((xtvm['px'][i])/Sc) + "," + str((xtvm['py'][i])/Sc) + "," + str((xtvm['pz'][i])/Sc) + "," + str(xtvm['_0'][i]) + ");" + '\n'

        
# Attachments Data for MEF Conversion --------

            
        attachments = ""
            
        for i in range ( 0 , len(atta) ):
    
                attachments += "AttachObject(\"" + str(str(atta['name'][i])[2:-1]) + "\"," + str(i) + "," + str(atta['_00'][i]) + "," + str(atta['_01'][i]) + "," + str(atta['_02'][i]) + "," + str(atta['_03'][i]) + "," + str(atta['_04'][i]) + "," + str(atta['_05'][i]) + "," + str(atta['_06'][i]) + "," + str(atta['_07'][i]) + "," + str(atta['_08'][i]) + "," + str((atta['px'][i])/Sc) + "," + str((atta['py'][i])/Sc) + "," + str((atta['pz'][i])/Sc) + ");" + '\n'

                attachments += "AttachObjectBoneID(" + str(i) + "," + str(atta['_an'][i]) + ");" + '\n'
                
                    
#_____________________________________________________
                
                
# Initial text (Newobject)

        meftext += "NewObject(\""+str(NameOfModel)+"\");\n"
    
# Material    

        meftext +=  str(Materials)

# Breakscript

        meftext += "BreakScript();\n"     

# Bones

        meftext += str(Bones)  
    
# Vertices     

        meftext +=  str(Vertices)   
    
# Normals     

        meftext +=  str(Normals)   
    
# Faces     

        meftext +=  str(Faces)   
    
# UV     

        meftext +=  str(UVs)   
    
# magic vertices     

        meftext +=  str(mvertices)   
    
# attachments   

        meftext +=  str(attachments)
        
    
    return meftext
