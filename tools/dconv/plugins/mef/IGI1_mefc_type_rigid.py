import os 
import numpy as np
import math
from math import *
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

     d3dr = parse_d3dr(reader.read(b'D3DR'),0)

     dner = parse_dner(reader.read(b'DNER'),0)[0]

     ecaf = parse_dner(reader.read(b'DNER'),0)[1]
     
     ecaf = func.IndexCorrection_ecaf1(dner,ecaf)
     
     ecaf = parse_ecaf(reader.find(b'ECAF'),ecaf)

     xtrv = parse_xtrv(reader.read(b'XTRV'),0)  

    if reader.find(b'HSMC'):
    
     hsmc = parse_hsmc(reader.read(b'HSMC',0))

     xtvc0 = parse_xtvc(reader.read(b'XTVC',0))

     ecfc0 = parse_ecfc(reader.read(b'ECFC',0))

     tamc0 = parse_tamc(reader.read(b'TAMC',0))

     hpsc0 = parse_hpsc(reader.read(b'HPSC',0))
    
     xtvc1 = parse_xtvc(reader.read(b'XTVC',1))

     ecfc1 = parse_ecfc(reader.read(b'ECFC',1))

     tamc1 = parse_tamc(reader.read(b'TAMC',1))

     hpsc1 = parse_hpsc(reader.read(b'HPSC',1))
    
    NameOfModel = str(os.path.splitext(os.path.basename(meffilename))[0])


# MODEL Texture Reading ------------>


    if ( len(dner) != 0 ):
        
       TextureFile = []
        
       if ( (max(dner['_td'])+1) != 0 ):
            
          TextureFile += reader_data1.fromtex(meffilename,(max(dner['_td'])+1))


# Other Info ------------------------->

        
    Sc = 40.96

    Msh0 = [[],[],[],[],[]]
    
    NameOfModel = str(os.path.splitext(os.path.basename(meffilename))[0])

    if reader.find(b'HSMC'):
        


# SOME NECESSARY CALCULATIONS ---------->


        func.NameOfModel = NameOfModel

        func.dner,func.ecaf,func.xtrv = dner,ecaf,xtrv

        func.DNER_OFFFACES= func.CalC_Offset_1(dner,ecaf)

        func.DNER_NUMFACES= func.CalC_nfaces_1(dner,ecaf)

        Msh0 = func.CalC_modeldata0_1(tamc0,ecfc0,xtvc0,len(Msh0[0]),0,0,Msh0)
        
        Msh1 = func.CalC_modeldata0_1(tamc1,ecfc1,xtvc1,len(Msh0[0]),0,1,Msh0)

    
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
            
            
# Vertices Data for MEF conversion -------

    
        Vertices = ""

        n = 0

        Vts = Mesh[1]
                
        for i in range ( 0, len(Vts) ):
        
            Vertices += "Vertex(" + str(n) + "," + str(Vts[i][0]/Sc) + "," + str(Vts[i][1]/Sc) + "," + str(Vts[i][2]/Sc) + ");" + "\n"

            n += 1
            
    
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

        meftext += "NewObject(\"" + str(NameOfModel) + "\");\n"
    
# Material    

        meftext +=  str(Materials)       
    
# Breakscript

        meftext += "BreakScript();\n"
    
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


        DNER_OFFFACES = func.CalC_Offset_1(dner,ecaf)

        DNER_NUMFACES = func.CalC_nfaces_1(dner,ecaf)
        
        func.x,func.y = trop['o_face'],trop['n_face']

        Msh0 = func.CalC_meshdata0_1(trop,cftp,xvtp,Msh0)
        
        func.x,func.y = DNER_OFFFACES,DNER_NUMFACES
        
        Msh1 = func.CalC_meshdata0_1(dner,ecaf,xtrv,Msh0)

    
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
            
            
# Vertices Data for MEF conversion -------

    
        Vertices = ""

        n = 0

        Vts = Mesh[1]
                
        for i in range ( 0, len(Vts) ):
        
            Vertices += "Vertex(" + str(n) + "," + str(Vts[i][0]/Sc) + "," + str(Vts[i][1]/Sc) + "," + str(Vts[i][2]/Sc) + ");" + "\n"

            n += 1
            
    
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

        meftext += "NewObject(\"" + str(NameOfModel) + "\");\n"
    
# Material    

        meftext +=  str(Materials)       
    
# Breakscript

        meftext += "BreakScript();\n" 
    
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
