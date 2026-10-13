import os 
import numpy as np
from .import reader_form
from .import mtp_struct
from .reader_form import *
from .mtp_struct import *


def FromData(Mtp_file,ModelNames,ModelTypes,ModelLODs):

    assert os.path.exists(Mtp_file), " .MTP file is missing " + str(Mtp_file)

# -------------------------------------------

    data = ""

    reader = reader_form.open(Mtp_file)

    banm_bytes = reader.read(b'BANM')
    banm = parse_banm(banm_bytes)

    svol_bytes = reader.read(b'SVOL')
    svol = parse_svol(svol_bytes)

    mods_bytes = reader.read(b'MODS')
    mods = parse_mods(mods_bytes)

    vnam_bytes = reader.read(b'VNAM')
    vnam = parse_vnam0(vnam_bytes)

    texf_bytes = reader.read(b'TEXF')
    texf = parse_texf(texf_bytes)

    inst_bytes = reader.read(b'INST')
    inst = parse_inst0(inst_bytes)

#--------------------------------------------


#---<VIRTUALMODELS>


    VModels = []

    Temp = []

    for i in range ( 0 , len(inst[2]) ):

      if inst[2][i][0][0] not in Temp:

        Temp.append(inst[2][i][0][0])

      elif inst[2][i][0][0] not in VModels:

        VModels.append(inst[2][i][0][0])


    Er = 0

    if ( len(ModelNames) != len(mods[1]) ):

        assert 0!=0, "Error! Data File and MTP file Looks Different"

    for i in range ( 0 , len(mods[1]) ):

        assert ModelNames[i] != mods[1][i] , "Error! Data File and MTP file Looks Different"



    Tex = []

    Temp = []

    for i in range ( 0 , len(inst[3]) ):

      if inst[2][i][0][0] not in Temp:

        Temp.append(inst[2][i][0][0])

        Tex.append(inst[3][i])


        
    Vtex = []

    for i in range ( 0 , len(inst[2]) ):

        if ( inst[2][i][0][0] not in VModels ):

            Vtex.append([])

        else:

            Temp = []

            k = inst[2][i][0][0]

            for j in range ( 0 , inst[2][i][0][1] ):

             if (  inst[3][i][j] != Tex[k][j] ):

              Temp.append([ texf[1][inst[3][i][j]] , texf[1][Tex[k][j]] ])

            Vtex.append(Temp)
        

    SModels = []

    for i in range ( 0 , len(inst[2]) ):

        V = 0

        if ( inst[2][i][0][0] in VModels ):
            
         V = 1
            
        SModels.append([ vnam[2][i] , mods[1][inst[2][i][0][0]] , V , ModelTypes[inst[2][i][0][0]] , len(Vtex[i]) , ModelLODs[inst[2][i][0][0]] ])
        

#-------------------------------

# Anims ---->


    Anims = ""

    for i in range ( 0 , len(banm[1]) ):

     Anims += "CreateAnim(\""+str(banm[1][i])+"\");\n"

     if ( i == len(banm[1])-1 ):

      Anims += "\n"

    
# Shadows ---->


    Shades = ""

    for i in range ( 0 , len(svol[1]) ):

     Shades += "CreateShadowVolume(\""+str(svol[1][i])+"\");\n"

     if ( i == len(svol[1])-1 ):

      Shades += "\n"


# Virtual Models ---->


    Vmods = ""

    for i in range ( 0 , len(VModels) ):

     Vmods += "CreateModelBoneNotVirtual(\""+str(mods[1][VModels[i]])+"\");\n"

     if ( i == len(VModels)-1 ):

      Vmods += "\n"


# Models Definition ---->


    Mods = ""

    for i in range ( 0 , len(SModels) ):

        if ( SModels[i][2] == 0 ):

          if ( SModels[i][5] == 1 ):

            if ( SModels[i][3] == 0 ):

                Mods += "CreateCompleteModelRigid(\"" + str(SModels[i][0]) + "\");\n" 

            if ( SModels[i][3] == 1 ):

                Mods += "CreateCompleteModelBone(\"" + str(SModels[i][0]) + "\");\n" 

            if ( SModels[i][3] == 3 ):

                Mods += "SetLightmapResolution(1);CreateCompleteModelLightmap(\"" + str(SModels[i][0]) + "\");\n" 

        if ( SModels[i][2] == 1 ):

            if ( SModels[i][3] == 1 ):

                Mods += "CreateVirtualModel(\"" + str(SModels[i][0]) + "\",\"" + str(SModels[i][1]) + "\");"

                for j in range ( 0 ,  SModels[i][4] ):

                  Mods += "DefineVirTex(\"" + str(Vtex[i][j][1]) + "\",\"" + str(Vtex[i][j][0]) + "\",\"\");"

                Mods += "\n"

        if ( i == len(SModels)-1 ):

         Mods += "\n"


#-------------------<

    return Anims,Shades,Vmods,Mods
                
