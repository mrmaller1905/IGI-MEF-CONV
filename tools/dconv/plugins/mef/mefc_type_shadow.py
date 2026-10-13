import os 
import numpy as np
from .import fun
from .import reader_ilff
from .import mef_struct
from .fun import *
from .mef_struct import *
from .reader_ilff import *

def fromfile(meffilename,srcpth):
    
    
    meftext = ""

    reader = reader_ilff.open(srcpth)    
    
    sems = parse_sems(reader.read(b'SEMS'))
    
    xtvs = parse_xtvs(reader.read(b'XTVS'))
    
    cafs = parse_cafs(reader.read(b'CAFS'))


# Model Info -------------------------------


    NameOfModel = os.path.splitext(os.path.basename(meffilename))[0]
        
    Sc = 40.96

    if ( sems['index_num'][0] == -1 ):
        

# Some Necessary Calculations ------------------------------->


        fun.X, fun.Y  = sems['offset_sfaces'], sems['num_sfaces']

        caf2 = parse_caf2(fun.Correction_Indices_cafs(sems,cafs))


# -----> Simple Shadow Model <------------------------------

# Materials for MEF CONV ----------------------------------


        Materials = ""

        n = 0
    
        for m in range (0 , 1 ):
        
            Materials += "Material(" + str(n) + ",\"" + "ShadowModel_1" + "\"," + "0.5,0.5,0.5,0.5,0.5,0.5,0.9,0.9,0.9" + "," + "0" + "," + "0" + "," + "0" + ");" + '\n'

            n += 1
            

# Vertices for MEF CONV ----------------------------------

    
        Vertices = ""

        n = 0
    
        for i in range ( 0, len(xtvs) ):
        
            Vertices += "Vertex(" + str(n) + "," + str((xtvs['px'][i])/Sc) + "," + str((xtvs['py'][i])/Sc) + "," + str((xtvs['pz'][i])/Sc) + ");" + '\n'

            n += 1


# Normals for MEF CONV ----------------------------------

        
        Normals = ""

        n = 0
        
        for i in range ( 0, len(cafs) ):

          for j in range ( 0 , (1+1+1) ):  
        
            Normals += "Normal(" + str(n) + "," + str(cafs['nx'][i]) + "," + str(cafs['ny'][i]) + "," + str(cafs['nz'][i]) + ");" + '\n'

            n += 1


# Faces for MEF CONV ---------------------------------------


        Faces = ""

        n = 0
        
        for m in range ( 0 , len(sems) ):
        
            Off = sems['offset_sfaces'][m]
            OFF = sems['offset_sverts'][m]
        
            for i in range ( Off, Off + sems['num_sfaces'][m] ):
        
                Faces += "Face(" + str(n) + "," + str(OFF+cafs['a'][i]) + "," + str(OFF+cafs['b'][i]) + "," + str(OFF+cafs['c'][i]) + "," + str(3*n+0) + "," + str(3*n+1) + "," + str(3*n+2) + "," + str(0) + ");" + '\n'

                n += 1


# ---------------------------------------- #
# ---------------------------------------- #
    
#  Name

        meftext += "NewObject(\"" + str(NameOfModel) + "\");" + "\n"
    
#  Materials

        meftext += str(Materials)
    
#  Breakscript

        meftext += "BreakScript();" + '\n'
    
#  Vertices    
    
        meftext += str(Vertices)
    
#  Normals    
    
        meftext += str(Normals)
    
#  Faces        

        meftext += str(Faces)



    else:
        

# Some Necessary Calculations ------------------------------->


        Print=("!")


# -----> Bone Shadow Model <------------------------------


# -----> Bones ----------------------

    
        Bones = ""
    
        for i in range ( 0, (max(sems['index_num'])+1) ):
        
            Bones += "Bone(" + str(i) + "," + "\"Bone # " + str(i) + "\"" + "," + str(i-1) + "," + str(0.00000) + "," + str(0.00000) + "," + str(0.00000) + ");" + '\n'

        Bones += "BuildHierarchy();\n" 

            
# -----> Bone Vertex Influenes ----------------------

    
        VInfluences = ""

        n = 0

        for m in range ( 0, len(sems) ):

            Off = sems['offset_sverts'][m]
    
            for i in range ( Off , Off + sems['num_sverts'][m] ):
        
                VInfluences += "VertexInfluenceRigid(" + str(sems['index_num'][m]) + "," + str(n) + "," + str((xtvs['px'][i])/Sc) + "," + str((xtvs['py'][i])/Sc) + "," + str((xtvs['pz'][i])/Sc) + ");" + '\n'

                n += 1

# Materials for MEF CONV ----------------------------------


        Materials = ""

        n = 0

        for m in range (0 , 1 ):

            Materials += "Material(" + str(n) + ",\"BoneShadow_1\"" + "," + "0.588235,0.588235,0.588235,0.588212,0.588222,0.588212,0.9,0.9,0.9" + "," + "0" + "," + "0" + "," + "0" + ");" + '\n'

            n += 1

                
# -----> Bone Vertices ----------------------

    
        Vertices = ""

        n = 0
    
        for i in range ( 0, len(xtvs) ):
        
            Vertices += "Vertex(" + str(n) + "," + str((xtvs['px'][i])/Sc) + "," + str((xtvs['py'][i])/Sc) + "," + str((xtvs['pz'][i])/Sc) + ");" + '\n'

            n += 1

    
# -----> Bone Normals ----------------------

        
        Normals = ""

        n = 0
        
        for i in range ( 0, len(cafs) ):

          for j in range ( 0 , (1+1+1) ):  
        
            Normals += "Normal(" + str(n) + "," + str(cafs['nx'][i]) + "," + str(cafs['ny'][i]) + "," + str(cafs['nz'][i]) + ");" + '\n'

            n += 1
            
            
# -----> Bone Faces ----------------------


        Faces = ""

        n = 0
        
        for m in range ( 0 , len(sems) ):
        
            Off = sems['offset_sfaces'][m]
            OFF = sems['offset_sverts'][m]
        
            for i in range ( Off, Off + sems['num_sfaces'][m] ):
        
                Faces += "Face(" + str(n) + "," + str(OFF+cafs['a'][i]) + "," + str(OFF+cafs['b'][i]) + "," + str(OFF+cafs['c'][i]) + "," + str(3*n+0) + "," + str(3*n+1) + "," + str(3*n+2) + "," + str(0) + ");" + '\n'

                n += 1
                

# --------------------------- #
# --------------------------- #

    
#  Name

        meftext += "NewObject(\"" + str(os.path.splitext(os.path.basename(meffilename))[0]) + "\");" + "\n"
    
#  Materials

        meftext += str(Materials)
    
#  Breakscript

        meftext += "BreakScript();" + '\n'
    
#  Bone Types

        meftext += str(Bones)

#  Bone Vertices

        meftext += str(Vertices)

#  Bone VertexInfluences

        meftext += str(VInfluences)    

#  Bone Normals

        meftext += str(Normals)

#  Bone Faces

        meftext += str(Faces)    

        
    return meftext
