import os
import math
import numpy as np
from .import func
from .import reader_ilff
from .import reader_data1
from .import IGI1_mef_struct
from .func import *
from .reader_ilff import *
from .reader_data1 import *
from .IGI1_mef_struct import *

def fromfile(meffilename, srcpth):
    
    meftext = ""
    
    reader = reader_ilff.open(srcpth)

    if reader.find(b'HSEM'):

     hsem = parse_hsem(reader.read(b'HSEM'))

     atta = parse_atta(reader.read(b'ATTA'))

     xtvm = parse_xtvm(reader.read(b'XTVM'))

     trop = parse_trop(reader.read(b'TROP'))

     xvtp = parse_xvtp(reader.read(b'XVTP'))

     cftp = parse_cftp(reader.read(b'CFTP'))

     d3dr = parse_d3dr(reader.read(b'D3DR'),1)

     dner = parse_dner(reader.read(b'DNER'),1)[0]

     ecaf = parse_dner(reader.read(b'DNER'),1)[1]
     
     ecaf = func.IndexCorrection_ecaf1(dner,ecaf)
     
     ecaf = parse_ecaf(reader.find(b'ECAF'),ecaf)

     xtrv = parse_xtrv(reader.read(b'XTRV'),1)

    if reader.find(b'HSMC'):
    
     hsmc = parse_hsmc(reader.read(b'HSMC',0))

     xtvc0 = parse_xtvc(reader.read(b'XTVC',0))

     ecfc0 = parse_ecfc(reader.read(b'ECFC',0))

     tamc0 = parse_tamc(reader.read(b'TAMC',0))

     hpsc0 = parse_hpsc(reader.read(b'HPSC',0))
    
     xtvc1= parse_xtvc(reader.read(b'XTVC',1))

     ecfc1= parse_ecfc(reader.read(b'ECFC',1))

     tamc1= parse_tamc(reader.read(b'TAMC',1))

     hpsc1= parse_hpsc(reader.read(b'HPSC',1))


# MODEL Texture Reading ------------>


    if ( len(dner) != 0 ):
        
       TextureFile = []
        
       if ( (max(dner['_td'])+1) != 0 ):
            
          TextureFile += reader_data1.fromtex(meffilename,(max(dner['_td'])+1))


# Other Info ---------------------->

        
    Sc = 40.96

    Msh0 = [[],[],[],[],[]]
    
    NameOfModel = str(os.path.splitext(os.path.basename(meffilename))[0])

    if reader.find(b'HSMC'):
        

# SOME NECESSARY CALCULATIONS _______________->


        func.NameOfModel = NameOfModel

        Vrts = func.GetBoneVerts02(tamc0,xtvc0)

        func.dner,func.ecaf,func.xtrv = dner,ecaf,xtrv

        func.DNER_OFFFACES= func.CalC_Offset_1(dner,ecaf)

        func.DNER_NUMFACES= func.CalC_nfaces_1(dner,ecaf)

        Msh0 = func.CalC_modeldata0_1(tamc0,ecfc0,xtvc0,len(Msh0[0]),0,0,Msh0)
        
        Msh1 = func.CalC_modeldata0_1(tamc1,ecfc1,xtvc1,len(Msh0[0]),0,1,Msh0)
    
        NameOfModl = NameOfModel[:-1]+"1" # for function below as ( AdditionalData_1 ):
        
        BoneH = func.CalC_BoneOffset(func.AdditionalData_1(NameOfModl,max(xtrv['bn']))[0])
        
        
    
# Materials Data for MEF Conversion ----------

    
        Materials = ""

        Mesh = Msh1

        Mts = Mesh[0]

        n = 0
    
        for i in range ( 0, len(Mts) ):

            Mt = ""
            if ( Mts[i][1] != -1 ):
                    Mt += "MaterialTransparencyType(" + str(n) + ",1);\n"       
            if ( Mts[i][2] != -1 ):
                    Mt += "DiffuseTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][2]]) + ".tga\"" + ",1,0);\n"
            if ( Mts[i][3] != -1 ):
                    Mt += "OpacityTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][3]]) + ".tga\"" + ",1,0);\n"
        
            Materials += "Material(" + str(n) + ",\"" + str(Mts[i][4]) + "\",0.588235,0.588235,0.588235,0.1,0.1,0.1,0.9,0.9,0.9,"+str(Mts[i][5])+","+str(Mts[i][6])+","+str(Mts[i][7])+");" + '\n'         
            Materials += "MaterialShininess(" + str(n) + ","+str(Mts[i][8])+");" + '\n' + str(Mt)

            n += 1


            
# Bone Data for MEF conversion -----------


        Bones = ""  

        Bone = func.AdditionalData_1(NameOfModel,max(xtrv['bn']))[0]

        if max(xtrv['bn']) != 48 :
                                    Bone,I = CalC_IGI2BONEH(Bone),GET_BONEREF(Bone)
        if max(xtrv['bn']) == 48 :
                                    Bone,I = CalC_IGI2BONEH0(Bone),GET_BONEREF0(Bone)

        for i in range ( 0 , len(Bone) ):

          Bones += "Bone(" + str(i) + ",\"" + str(Bone[i][0]) + "\"," + str(Bone[i][1]) + "," + str(Bone[i][2]/Sc) + "," + str(Bone[i][3]/Sc) + "," + str(Bone[i][4]/Sc) + ");\n"
          #Bones += "Bone(" + str(i) + ",\"BONE_UNDEFINED\"," + str(i-1) + "," + str(88888888) + "," + str(88888888) + "," + str(88888888) + "); \\ IN IGI 1, BONEINFO IS IN ANIM FILE\n"

        Bones += "BuildHierarchy();\n"

                
           
# Vertices Data for MEF conversion -------

    
        Vertices = ""

        Vts = Mesh[1]
    
        for i in range ( 0, len(Vrts) ):
        
            Vertices += "Vertex(" + str(i) + "," + str((Vrts[i][0]+BoneH[0][Vrts[i][3]])/Sc) + "," + str((Vrts[i][1]+BoneH[1][Vrts[i][3]])/Sc) + "," + str((Vrts[i][2]+BoneH[2][Vrts[i][3]])/Sc) + ");" + '\n'
        
        Vtsi = func.CalC_BoneEffects(d3dr,xtrv,Vrts)

        if max(xtrv['bn']) != 48 :
                                    Vtsi = SumTheBones06(Vtsi,func.AdditionalData_1(NameOfModel,max(xtrv['bn']))[0],I)
        if max(xtrv['bn']) == 48 :
                                    Vtsi = SumTheBones05(Vtsi,func.AdditionalData_1(NameOfModel,max(xtrv['bn']))[0],I)

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
    
            attachments +="AttachObject(\"" + str((str(atta['name'][i]))[2:-1]) + "\"," + str(i) + "," + str(atta['_00'][i]) + "," + str(atta['_01'][i]) + "," + str(atta['_02'][i]) + "," + str(atta['_03'][i]) + "," + str(atta['_04'][i]) + "," + str(atta['_05'][i]) + "," + str(atta['_06'][i]) + "," + str(atta['_07'][i]) + "," + str(atta['_08'][i]) + "," + str((atta['px'][i])/Sc) + "," + str((atta['py'][i])/Sc) + "," + str((atta['pz'][i])/Sc) + ");" + '\n'

            attachments +="AttachObjectBoneID(" + str(i) + "," + str(-1) + ");" + '\n'
            
    
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
        

    else:

# SOME NECESSARY CALCULATIONS _______________->

    
        NameOfModl = NameOfModel[:-1]+"1" # for function below as ( AdditionalData_1 ):
        
        BoneH = func.CalC_BoneOffset(func.AdditionalData_1(NameOfModl,max(xtrv['bn']))[0])
     
        xtrx = parse_xtrx(reader.find(b'XTRV'),func.PostCorrection_xtrv1(d3dr,xtrv,BoneH))

        Vrts = func.GetBoneVerts(d3dr,xtrv)

        DNER_OFFFACES = func.CalC_Offset_1(dner,ecaf)

        DNER_NUMFACES = func.CalC_nfaces_1(dner,ecaf)
        
        func.x,func.y = trop['o_face'],trop['n_face']

        Msh0 = func.CalC_meshdata0_1(trop,cftp,xvtp,Msh0)
        
        func.x,func.y = DNER_OFFFACES,DNER_NUMFACES
        
        Msh1 = func.CalC_meshdata0_1(dner,ecaf,xtrx,Msh0)
        
    
# Materials Data for MEF Conversion ----------

    
        Materials = ""

        Mesh = Msh1

        Mts = Mesh[0]

        n = 0
    
        for i in range ( 0, len(Mts) ):

            Mt = ""
            if ( Mts[i][1] != -1 ):
                    Mt += "MaterialTransparencyType(" + str(n) + ",1);\n"       
            if ( Mts[i][2] != -1 ):
                    Mt += "DiffuseTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][2]]) + ".tga\"" + ",1,0);\n"
            if ( Mts[i][3] != -1 ):
                    Mt += "OpacityTMap(" + str(n) + "," + "\"textures/" + str(TextureFile[Mts[i][3]]) + ".tga\"" + ",1,0);\n"
        
            Mts[i][4] = Mts[i][4].replace("Material","BONE -Undefined")
            
            Materials += "Material(" + str(n) + ",\"" + str(Mts[i][4]) + "\",0.588235,0.588235,0.588235,0.1,0.1,0.1,0.9,0.9,0.9,"+str(Mts[i][5])+","+str(Mts[i][6])+","+str(Mts[i][7])+");" + '\n'         
            Materials += "MaterialShininess(" + str(n) + ","+str(Mts[i][8])+");" + '\n' + str(Mt)

            n += 1

            
# Bone Data for MEF conversion -----------


        Bones = ""

        Bone = func.AdditionalData_1(NameOfModel,max(xtrv['bn']))[0]

        if max(xtrv['bn']) != 48 :
                                    Bone,I = CalC_IGI2BONEH(Bone),GET_BONEREF(Bone)
        if max(xtrv['bn']) == 48 :
                                    Bone,I = CalC_IGI2BONEH0(Bone),GET_BONEREF0(Bone)

        for i in range ( 0 , len(Bone) ):

          Bones += "Bone(" + str(i) + ",\"" + str(Bone[i][0]) + "\"," + str(Bone[i][1]) + "," + str(Bone[i][2]/Sc) + "," + str(Bone[i][3]/Sc) + "," + str(Bone[i][4]/Sc) + ");\n"
          #Bones += "Bone(" + str(i) + ",\"BONE_UNDEFINED\"," + str(i-1) + "," + str(88888888) + "," + str(88888888) + "," + str(88888888) + "); \\ IN IGI 1, BONEINFO IS IN ANIM FILE\n"          

        Bones += "BuildHierarchy();\n"
                
        
# Vertices Data for MEF conversion -------

    
        Vertices = ""

        Vts = Mesh[1]
    
        for i in range ( 0, len(Vts) ):
        
            Vertices += "Vertex(" + str(i) + "," + str(Vts[i][0]/Sc) + "," + str(Vts[i][1]/Sc) + "," + str(Vts[i][2]/Sc) + ");" + '\n'
        
        Vtsi = func.CalC_BoneEffects(d3dr,xtrv,Vrts)

        if max(xtrv['bn']) != 48 :
                                    Vtsi = SumTheBones06(Vtsi,func.AdditionalData_1(NameOfModel,max(xtrv['bn']))[0],I)
        if max(xtrv['bn']) == 48 :
                                    Vtsi = SumTheBones05(Vtsi,func.AdditionalData_1(NameOfModel,max(xtrv['bn']))[0],I)

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
            
        for i in range ( 0, len(atta) ):
    
            attachments += "AttachObject(\"" + str((str(atta['name'][i]))[2:-1]) + "\"," + str(i) + "," + str(atta['_00'][i]) + "," + str(atta['_01'][i]) + "," + str(atta['_02'][i]) + "," + str(atta['_03'][i]) + "," + str(atta['_04'][i]) + "," + str(atta['_05'][i]) + "," + str(atta['_06'][i]) + "," + str(atta['_07'][i]) + "," + str(atta['_08'][i]) + "," + str((atta['px'][i])/Sc) + "," + str((atta['py'][i])/Sc) + "," + str((atta['pz'][i])/Sc) + ");" + '\n'

            attachments += "AttachObjectBoneID(" + str(i) + "," + str(-1) + ");" + '\n'

                
# ----------------------------------------
    
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




# ----------------------------------------------------------------

# ----------------------------------------------------------------

# ----------------------------------------------------------------






def GET_BONEREF(Bone):

    return [ 0,1,4,7,15,15,15,20,16,21,23,25,27,29,17,22,24,26,28,30,1,1,1,2,5,8,13,18,3,6,9,14,19 ]


def CalC_IGI2BONEH(Bone):
    Bnes = [ ["center",-1],
             ["lower body",0], ["upper left leg",0], ["upper right leg",0],
             ["upper body",1], ["lower left leg",2], ["lower right leg",3],
             ["shoulders",4], ["left foot",5], ["right foot",6],
             ["rotate_head",7], ["rotate_left",7], ["rotate_right",7], ["left toe",8], ["right toe",9],
             ["head",10], ["upper left arm",11], ["upper right arm",12], ["left toe end",13], ["right toe end",14],
             ["head end",15], ["lower left arm",16], ["lower right arm",17], ["left hand",21], ["right hand",22],
             ["upper left finge",23], ["upper right fing",24],
             ["lower left finge",25], ["lower right fing",26],
             ["left fingers end",27], ["right fingers en",28] ]

    for i in range ( 0 , len(Bnes) ):

        V = [ 0.0e+00, 0.0e+00, 0.0e+00 ]

        for j in range ( 0 , len(Bone) ):

         if ( Bnes[i][0] == Bone[j][0] ):

          V = [ Bone[j][2], Bone[j][3], Bone[j][4] ]

          break

        Bnes[i] += [ V[0],V[1],V[2] ]

    return Bnes


def SumTheBones06(Vtsi,Bone,I):

    for i in range ( 0 , len(Vtsi) ):

        if Vtsi[i][0] == 5:
                                 Vtsi[i][2],Vtsi[i][3],Vtsi[i][4] = Vtsi[i][2]+Bone[5][2],Vtsi[i][3]+Bone[5][3],Vtsi[i][4]+Bone[5][4]
        if Vtsi[i][0] == 6:
                                 Vtsi[i][2],Vtsi[i][3],Vtsi[i][4] = Vtsi[i][2]+Bone[6][2],Vtsi[i][3]+Bone[6][3],Vtsi[i][4]+Bone[6][4]     
        Vtsi[i][0]=I[Vtsi[i][0]]

    return Vtsi



# -------------------------------------


def GET_BONEREF0(Bone):

    return [ 0,0,0,0,2,4,6,14,24,34,44,13,23,33,43,15,25,35,45,12,22,32,42,16,26,36,46,1,3,5,10,20,30,40,9,19,29,39,8,18,28,38,7,17,27,37,11,21,31,41,0,0,0,0,0,0 ]


def CalC_IGI2BONEH0(Bone):
    
    Bnes = [ ["center shoulders",-1],
             ["upper left arm",0 ],  ["upper right arm",0],  ["lower left arm",1 ],  ["lower right arm",2],  ["left hand",3], ["right hand",4],
             ["upper left foref",5], ["upper left littl",5], ["upper left middl",5], ["upper left ring ",5], ["upper left thumb",5],
             ["upper right fore",6], ["upper right litt",6], ["upper right midd",6], ["upper right ring",6], ["upper right thum",6],
             ["lower left foref",7], ["lower left littl",8], ["lower left middl",9], ["lower left ring ",10],["lower left thumb",11],
             ["lower right fore",12],["lower right litt",13],["lower right midd",14],["lower right ring",15],["lower right thum",16],
             ["left forefinger ",17],["left little fing",18],["left middle fing",19],["left ring finger",20],["left thumb tip",21],
             ["right forefinger",22],["right little fin",23],["right middle fin",24],["right ring finge",25],["right thumb tip",26],
             ["none09",27],["none07",28],["none06",29],["none08",30],["none10",31],["none02",32],["none05",33],["none03",34],["none04",35],["none01",36]]

    for i in range ( 0 , len(Bnes) ):

        V = [ 0.0e+00, 0.0e+00, 0.0e+00 ]
        for j in range ( 0 , len(Bone) ):
         if ( Bnes[i][0] == Bone[j][0] ):
          V = [ Bone[j][2], Bone[j][3], Bone[j][4] ]
          break
        Bnes[i] += [ V[0],V[1],V[2] ]

    return Bnes


def SumTheBones05(Vtsi,Bone,I):

    for i in range ( 0 , len(Vtsi) ):

        Vtsi[i][0]=I[Vtsi[i][0]]

    return Vtsi
