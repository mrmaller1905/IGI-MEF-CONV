import os
import math
from utils import fs
import numpy as np
from math import *
from .import objS

def fromfile(meffilename,Data,Arg0,Aid,Po,Ro):
    
    objtext = ""

    MatName = str(os.path.splitext(os.path.basename(meffilename))[0])        

    ModelName = "attach"+str(GetID(Aid,2))+"_"+str(os.path.splitext(os.path.basename(meffilename))[0])

    SIZE = GetSizeObject(Data[4])

    Sc,Nr = 1,10


# ----------\\\ GETING DESIRED DATA FORMAT \\\-----------


    Vts = GetMeshVertsData(Data[4]) #F#

    Vts = TransformVertData(Vts,Po,Ro) #F#

    UVs = GetMeshTvertData(Data[6],Data[7]) #F#

    Fces= GetMeshFacesData(Data[6],Data[7]) #F#
    


# ------------------\\\ MESH DATA \\\---------------------


    Verts,Norms,Tverts = "","",""

    for i in range ( 0 , len(Vts) ):

      Verts += "v " + str(GetFNum(Vts[i][1],Nr)) + " " + str(GetFNum(Vts[i][2],Nr)) + " " + str(GetFNum(Vts[i][3],Nr)) + "\n"
    Verts += "# " + str(len(Vts)) + " vertices" + "\n\n" 

    for i in range ( 0 , len(UVs) ):

      Tverts += "vt " + str(GetFNum(UVs[i][1],Nr)) + " " + str(GetFNum(UVs[i][2],Nr)) + " " + str(GetFNum(0.000000,Nr)) + "\n"
    Tverts += "# " + str(len(UVs)) + " texture coords" + "\n\n" 


# ------------------\\\ MESH MAIN DATA \\\-------------------

    Faces = ""

    Mat,Tex = Data[2],Data[3]

    Faces += "g " + str(ModelName) + "\n"

    for i in range ( 0 , len(Fces) ):

        if Fces[i][11] != -1:
           Faces += "usemtl " + str(Mat[Fces[i][10]][1][1:-1])+"_N"+str(GetID(Fces[i][10],2)) + "\n"
           
        Faces += "f -" + str(len(Vts)-Fces[i][3]) + "/-" + str(len(UVs)-Fces[i][9]) ################## AD ########
        Faces +=  " -" + str(len(Vts)-Fces[i][2]) + "/-" + str(len(UVs)-Fces[i][8]) ################## AD ########
        Faces +=  " -" + str(len(Vts)-Fces[i][1]) + "/-" + str(len(UVs)-Fces[i][7]) + " \n" ########## AD ########
        
    Faces += "# " + str(len(Fces)) + " faces" + "\n\n"


    
# -----------------------------------
# /--------- DATA COMPILING --------/
# -----------------------------------



    objtext += "\n"

    objtext += "mtllib mtl\\" + str(MatName) + ".mtl\n"+"\n"+"#\n"

    objtext += "# object " + str(ModelName) + '\n' + "#\n\n"

    objtext += str(Verts)

    objtext += str(Tverts)

    objtext += str(Faces)

    return objtext





# ----------------------------------------------------------------------------------------------------------
# ----------------\\ COLLISION MESH DATA \\-----------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------




def frommesh(meffilename,Data,Arg0,Aid,Po,Ro):
    
    objtext = ""

    MatName = str(os.path.splitext(os.path.basename(meffilename))[0])

    ModelName = str(os.path.splitext(os.path.basename(meffilename))[0]) + "_ColMesh01"

    SIZE = GetSizeObject(Data[4])

    Sc,Nr = 1,10


# ----------\\\ GETING DESIRED DATA FORMAT \\\-----------


    Vts = GetMeshVertsData(Data[4]) #F#
    
    Mat,Tex = Data[2],Data[3]

    Fces= GetMeshFacesData(Data[6],Data[7]) #F#
    

# ------------------\\\ MESH DATA \\\---------------------


    Verts,Faces = "",""

    for i in range ( 0 , len(Vts) ):

      Verts += "v " + str(GetFNum(Vts[i][1],Nr)) + " " + str(GetFNum(Vts[i][2],Nr)) + " " + str(GetFNum(Vts[i][3],Nr)) + "\n"
    Verts += "# " + str(len(Vts)) + " vertices" + "\n\n"

    Faces += "g " + str(ModelName) + "\n"

    for i in range ( 0 , len(Fces) ):

        if Fces[i][11] != -1:
           Faces += "usemtl " + str(Mat[Fces[i][10]][1][1:-1])+"_N"+str(GetID(Fces[i][10],2)) + "\n"
           
        Faces += "f -" + str(len(Vts)-Fces[i][3]) + " -" + str(len(Vts)-Fces[i][2]) + " -" + str(len(Vts)-Fces[i][1]) + " \n"  ################## AD ########
        
    Faces += "# " + str(len(Fces)) + " faces" + "\n\n"


    
# -----------------------------------
# /--------- DATA COMPILING --------/
# -----------------------------------



    objtext += "\n"

    objtext += "mtllib mtl\\" + str(MatName) + ".mtl\n"+"\n"+"#\n"

    objtext += "# object " + str(ModelName) + '\n' + "#\n\n"

    objtext += str(Verts)

    objtext += str(Faces)

    return objtext




# ---------------------------------------------------------------------------------------------------------------------------
# ----------------\\ IMPORTANT FUNCTIONS \\----------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------


# ------- GENERIC FUNCTIONS ---------



def GetSizeObject(Verts):

    LENGTH = 1.0

    PX,PY,PZ = 0.0,0.0,0.0

    for i in range ( 0 , len(Verts) ):

        PX += Verts[i][1]
        PY += Verts[i][2]
        PZ += Verts[i][3]

    if len(Verts) > 0 :

        PX /= len(Verts)
        PY /= len(Verts)
        PZ /= len(Verts)

    for i in range ( 0 , len(Verts) ):

     if Dist([PX,PY,PZ],[Verts[i][1],Verts[i][2],Verts[i][3]]) > LENGTH :

        LENGTH = Dist([PX,PY,PZ],[Verts[i][1],Verts[i][2],Verts[i][3]])

    LENGTH = 0.08 * LENGTH

    return LENGTH
    
               

def GetFNum(Num,Ds):

    if abs(Num) > 1000000000000:
                                return str(Num)

    Num = str(float(round(Num,Ds)))

    N = Num.find('.')+1+ Ds
    
    assert len(str(Num)) <= N , "\n\n Error! Target Number Digits are more than Required"
        
    while ( len(str(Num)) != N ):

        Num += "0"
        
    return Num



def GetID(i,TLengthNum):

    ID = str(i)

    TLength = str(TLengthNum)

    if len(TLength) == 1:
                          TLength = "02"

    assert len(ID) <= len(TLength), "\n\n Error! Target Number Digits are more than Required"

    while ( len(ID) < len(TLength) ):

     ID = "0"+ID

    return ID




# ------- SPECIFIC FUNCTIONS ---------



def GetMeshVertsData(Verts): 

    Vts = []

    for i in range ( 0 , len(Verts) ):

     assert i == Verts[i][0], "\n\n - Indexing not following Sequence"

     Vts.append([ 0, Verts[i][1], Verts[i][2], Verts[i][3]  ])
     
    #assert len(GetUniqueItems(Vts)[0]) == len(Vts), "\n\n - Duplicate Vertices found"

    return Vts



def GetMeshFacesData(Faces,UVs): 

    Fces = []

    UvIDs = CalC_UVFaces(Faces,UVs) #F

    for i in range ( 0 , len(Faces) ):

     N = 0
     if i >= 1:
        if Faces[i][7] == Faces[i-1][7] :
                                        N = -1

     assert i == Faces[i][0], "\n\n - Indexing not following Sequence"

     Fces.append([ 0,
                   Faces[i][1], Faces[i][2], Faces[i][3],
                   Faces[i][4], Faces[i][5], Faces[i][6],
                   UvIDs[i][0], UvIDs[i][1], UvIDs[i][2],
                   Faces[i][7], N  ])
    return Fces



def GetMeshTvertData(FACES,UVS): 

    UVs = []

    if len(UVS) > 0:

      for i in range ( 0, len(UVS) ):

        UVs.append([ 0, 1-UVS[i][1], UVS[i][2] ])
        
        UVs.append([ 0, 1-UVS[i][3], UVS[i][4] ])
        
        UVs.append([ 0, 1-UVS[i][5], UVS[i][6] ])

    else:

      for i in range ( 0, len(FACES) ):

        UVs.append([ 0, 0.50000000, 0.50000000 ]) 

    UVs = GetUniqueItems(UVs)[0]

    return UVs 



def GetLinkedObjData(Ao): 

    Atta = []

    for i in range ( 0, len(Ao) ):

     assert i == Ao[i][1], "\n\n - Indexing not following Sequence"

     Atta.append([ Ao[i][0], Ao[i][1],
                   
                   Ao[i][2], Ao[i][3], Ao[i][4],
                   
                   Ao[i][5], Ao[i][6], Ao[i][7],
                   
                   Ao[i][8], Ao[i][9], Ao[i][10],
                   
                   Ao[i][11], Ao[i][12], Ao[i][13] ])

    return Atta



def TransformVertData(Verts,Po,Ro): 

    Vts = []

    for i in range ( 0 , len(Verts) ):

        VtX = ((Verts[i][1]*Ro[0][0])+(Verts[i][2]*Ro[1][0])+(Verts[i][3]*Ro[2][0]))+Po[0]

        VtY = ((Verts[i][1]*Ro[0][1])+(Verts[i][2]*Ro[1][1])+(Verts[i][3]*Ro[2][1]))+Po[1]

        VtZ = ((Verts[i][1]*Ro[0][2])+(Verts[i][2]*Ro[1][2])+(Verts[i][3]*Ro[2][2]))+Po[2]

        Vts.append([ Verts[i][0] , VtX , VtY , VtZ ])
     
    return Vts
               
               

# ---------- SUBFUNCTIONS ---------------



def Dist(A,B):

    Dx,Dy,Dz = (A[0]-B[0])**2,(A[1]-B[1])**2,(A[2]-B[2])**2

    Dt = (Dx+Dy+Dz)**(0.5)

    return Dt


def GetUniqueItems(Vts02):

    Vts,Vin = [],[]

    for i in range ( 0 , len(Vts02) ):

        E = 0
        for j in range ( 0 , len(Vts) ):

            if ( Vts02[i] == Vts[j] ):
                Vin.append(j)
                E = 1
                break

        if E == 0 :
                Vts.append(Vts02[i])
                Vin.append(len(Vts)-1)
                continue

    return Vts,Vin



def CalC_UVFaces(FACES,UVS): 

    UVs,Uin = [],[]

    if len(UVS) > 0:

      for i in range ( 0, len(UVS) ):

        Uin.append([ 3*i+0, 3*i+1, 3*i+2 ])

        UVs.append([ 0, 1-UVS[i][1], UVS[i][2] ])

        UVs.append([ 0, 1-UVS[i][3], UVS[i][4] ])

        UVs.append([ 0, 1-UVS[i][5], UVS[i][6] ])

    else:

      for i in range ( 0, len(FACES) ):

          Uin.append([ i, i, i ])

          UVs.append([ 0, 0.50000000, 0.50000000 ]) 

    I = GetUniqueItems(UVs)[1]

    for i in range ( 0, len(Uin) ):

      Uin[i] = [ I[Uin[i][0]],I[Uin[i][1]],I[Uin[i][2]] ]

    return Uin

