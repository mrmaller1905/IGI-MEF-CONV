import os
import math
from utils import fs
import numpy as np
from math import *
from .import objS

def fromfile(meffilename,Data,Arg0):
    
    objtext = ""

    CreateMatLib(meffilename,Data,Arg0) 

    MatName = str(os.path.splitext(os.path.basename(meffilename))[0])        

    ModelName = str(os.path.splitext(os.path.basename(meffilename))[0])

    SIZE = GetSizeObject(Data[4])

    Sc,Nr = 1,10


# ----------\\\ GETING DESIRED DATA FORMAT \\\-----------


    Vts = GetMeshVertsData(Data[4]) #F#

    Atta= GetLinkedObjData(Data[10]) #F#

    UVs = GetMeshTvertData(Data[6],Data[7]) #F#

    Fces= GetMeshFacesData(Data[6],Data[7]) #F#

    Mag,Gls = GetOtherInfo(Data[8],Data[9]) #F#
    


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


# -------\\\ MESH LINKED OBJS DATA + MAGIC/GLOW OBJS DATA \\\-------


    attachments = ""

    for i in range ( 0 , len(Atta) ):

        Arg0 = str(os.path.dirname(meffilename))
        
        FILE = Arg0+"\\"+str(Data[10][i][0])[1:-1]+".MEF"
            
        Po = [ Atta[i][11],Atta[i][12],Atta[i][13]]
        Rx = [ Atta[i][2], Atta[i][3], Atta[i][4] ]
        Ry = [ Atta[i][5], Atta[i][6], Atta[i][7] ]
        Rz = [ Atta[i][8], Atta[i][9], Atta[i][10]]
        Po,Ro = [ Po[0],Po[1],Po[2] ], [ Rx,Ry,Rz ]

        if (os.path.exists(FILE)) == True :

             attachments += objS.fromtree(FILE,i,Po,Ro,[])
        else:
             attachments += Cr_Ao(i,FILE,ModelName,Po,Ro,SIZE) #F
             
        continue


    Mverts,glows = "\n","\n"

    for i in range ( 0 , len(Mag) ):

        ID,Pos,Radius = GetID(i,len(Mag))+Mag[i][4],[Mag[i][1],Mag[i][2],Mag[i][3]],SIZE

        Mverts += "\n"
        Mverts += "#" + "\n"
        Mverts += "# object magic" + str(ID) + " \n"
        Mverts += "#" + "\n"
        Mverts += "\n"
        Mverts += str(SphVrt(Pos,Radius)) #F
        Mverts += "# 62 vertices" + "\n"
        Mverts += "\n"
        Mverts += "g magic" + str(ID) + "\n"
        Mverts += "usemtl Magic_Object\n"
        Mverts += str(FixedFaceInfo())

    for i in range ( 0 , len(Gls) ):

        ID,Pos,Radius = GetID(i,len(Gls)),[Gls[i][1],Gls[i][2],Gls[i][3]],Gls[i][4]

        glows += "\n"
        glows += "#" + "\n"
        glows += "# object glow" + str(ID) + " \n"
        glows += "#" + "\n"
        glows += "\n"
        glows += str(SphVrt(Pos,Radius)) #F
        glows += "# 62 vertices" + "\n"
        glows += "\n"
        glows += "g glow" + str(ID) + "\n"
        glows += "usemtl glow" + str(ID) + "\n"  
        glows += str(FixedFaceInfo())


    
# -----------------------------------
# /--------- DATA COMPILING --------/
# -----------------------------------




    objtext += "# 3ds Max Wavefront OBJ Exporter v0.94b - (c)2007 guruware\n"

    objtext += "# IGI MESH EXPORTED FILE\n" 

    objtext += "\n"

    objtext += "mtllib mtl\\" + str(MatName) + ".mtl\n"+"\n"+"#\n"

    objtext += "# object " + str(ModelName) + '\n' + "#\n\n"

    objtext += str(Verts)

    objtext += str(Tverts)

    objtext += str(Faces)

    objtext += str(Mverts)

    objtext += str(glows)

    objtext += str(attachments) 

    return objtext





#--------------------------------------------------------------------------------------------------------------
#---------------------/ MATERIAL INFO OF MODEL (.MTL FILE) /---------------------------------------------------
#--------------------------------------------------------------------------------------------------------------




def CreateMatLib(meffilename,Data,Pth):
    
    mtltext = ""

    Mats,Texs = Data[2],Data[3]

    MatName = str(os.path.splitext(os.path.basename(meffilename))[0])           

    ModelName = str(os.path.splitext(os.path.basename(meffilename))[0])

    Mags,Gls = Data[8],GetMatGlsInfo(Data[9])

    Sp = "\t\t\t"

        
# Materials of Target Model(.MEF)
#-------------------------------
         

    Materials = ""

    for i in range ( 0 , len(Mats) ):

        Mat,Ss = GetModMatInfo(Mats[i],Texs),"_N"+str(GetID(i,2)) #F

        M  = "newmtl "+str(Mat[1]+Ss)+ "\n"
        M += Sp + "Ns " +str(Mat[12])+ "\n"
        M += Sp + "Ni " +str(Mat[13])+ "\n"
        M += Sp + "d "  +str(Mat[11])+ "\n"
        M += Sp + "Tr " +str(Mat[10])+ "\n"
        M += Sp + "Tf " +str(Mat[11])+" " +str(Mat[11])+" " +str(Mat[11])+" " + "\n"+ Sp + "illum 2 \n"
        M += Sp + "Ka " +str(Mat[2])+ " " +str(Mat[3])+ " " +str(Mat[4])+ " " + "\n"
        M += Sp + "Kd " +str(Mat[2])+ " " +str(Mat[3])+ " " +str(Mat[4])+ " " + "\n"
        M += Sp + "Ks " +str(Mat[8])+ " " +str(Mat[8])+ " " +str(Mat[8])+ " " + "\n"
        M += Sp + "Ke " +str(Mat[9])+ " " +str(Mat[9])+ " " +str(Mat[9])+ " " + "\n"
        
        if ( Mat[14] != "" ):
                              M += Sp + "map_ka " + str(Mat[14]) + "\n" + Sp + "map_kd " + str(Mat[14]) + "\n"
        if ( Mat[15] != "" ):
                              M += Sp + "map_d "  + str(Mat[15]) + "\n"
        if ( Mat[16] != "" ):
                              M += Sp + "map_refl " + str(Mat[16]) + "\n"
        if ( Mat[17] != "" ):
                              M += Sp + "map_bump " + str(Mat[17]) + "\n" + Sp + "bump " + str(Mat[17]) + "\n"

        Materials += M + Sp + "\n"

        
# Material for Magic Objs and Light Objs
#----------------------------------------


    MMaterials,GMaterials = "",""

    if ( len(Mags) > 0 ) :

        MMaterials += "newmtl Magic_Object" + "\n"
        MMaterials += Sp + "Ns 25.000000000" + "\n"
        MMaterials += Sp + "Ni 1.0000000000" + "\n"
        MMaterials += Sp + "d 0.9000000000" + "\n"
        MMaterials += Sp + "Tr 0.100000000" + "\n"
        MMaterials += Sp + "Tf 0.900000000 0.900000000 0.900000000" + "\n" + Sp + "illum 2" + "\n"
        MMaterials += Sp + "Ka 0.499999999 0.000000000 0.000000000" + "\n"
        MMaterials += Sp + "Kd 0.499999999 0.000000000 0.000000000" + "\n"
        MMaterials += Sp + "Ks 0.000000000 0.000000000 0.000000000" + "\n"
        MMaterials += Sp + "\n" 

    if ( len(Gls) > 0 ):
      for i in range ( 0 , len(Gls) ):

        GMaterials += "newmtl glow" + str(GetID(i,len(Gls))) + "\n" #F
        GMaterials += Sp + "Ns 10.000000000" + "\n"
        GMaterials += Sp + "Ni 1.0000000000" + "\n"
        GMaterials += Sp + "d 1.0000000000" + "\n"
        GMaterials += Sp + "Tr 0.000000000" + "\n"
        GMaterials += Sp + "Tf 1.0000000000 1.0000000000 1.0000000000 " + "\n" + Sp + "illum 2" + "\n"
        GMaterials += Sp + "Ka " + str(Gls[i][1]) +" "+ str(Gls[i][2]) +" "+ str(Gls[i][3]) + "\n"
        GMaterials += Sp + "Kd " + str(Gls[i][1]) +" "+ str(Gls[i][3]) +" "+ str(Gls[i][3]) + "\n"
        GMaterials += Sp + "Ke " + "0.1250000000" +" "+ "0.1250000000" +" "+ "0.1250000000" + "\n"
        GMaterials += Sp + "\n"

        

#-------------------------------
# <<------ Mtl file data ----->>
#-------------------------------


    mtltext += "# 3ds Max Wavefront OBJ Exporter v0.94b - (c)2007 guruware\n"

    mtltext += "# IGI MESH EXPORTED FILE (Material info)\n"

    mtltext += "\n"
    
    mtltext += str(Materials) 
    
    mtltext += str(MMaterials)
    
    mtltext += str(GMaterials)

    Tgt_file = (str(Pth)+"\\mtl\\"+(ModelName))+".mtl"
        
    os.makedirs(os.path.dirname(Tgt_file), exist_ok=True)
    
    with open(Tgt_file, 'w') as o:
        
     o.write(mtltext)
    
    return None






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



def GetMatGlsInfo(Gls):

    Glw = []

    Nr = 10

    for i in range ( 0 , len(Gls) ):

     Glw.append([ i, GetFNum(Gls[i][4],Nr), GetFNum(Gls[i][5],Nr), GetFNum(Gls[i][6],Nr) ])

    return Glw



def Cr_Ao(i,File,Model,Po,Ro,Sz):

    Str = "\n\n"

    Model = str(os.path.splitext(os.path.basename(File))[0])

    X,Y,Z,R,N = Po[0],Po[1],Po[2], Sz, "attach"+GetID(i,2)+"_"+Model #F
    
    Str += "#\n"
    Str += "# object "+str(N)+"\n"
    Str += "#\n\n"
    Str += "v "+str(X-R)+" "+str(Y-R)+" "+str(Z-R)+" \n"
    Str += "v "+str(X+R)+" "+str(Y-R)+" "+str(Z-R)+" \n"
    Str += "v "+str(X-R)+" "+str(Y+R)+" "+str(Z-R)+" \n"
    Str += "v "+str(X+R)+" "+str(Y+R)+" "+str(Z-R)+" \n"
    Str += "v "+str(X-R)+" "+str(Y-R)+" "+str(Z+R)+" \n"
    Str += "v "+str(X+R)+" "+str(Y-R)+" "+str(Z+R)+" \n"
    Str += "v "+str(X-R)+" "+str(Y+R)+" "+str(Z+R)+" \n"
    Str += "v "+str(X+R)+" "+str(Y+R)+" "+str(Z+R)+" \n"
    Str += "# 8 vertices\n\n"
    Str += "g "+str(N)+"\ns1\n"
    Str += "f -1 -4 -3 \n"+"f -4 -1 -2 \n"+"f -5 -8 -6 \n"
    Str += "f -8 -5 -7 \n"+"f -1 -6 -2 \n"+"f -6 -1 -5 \n"
    Str += "f -2 -8 -4 \n"+"f -8 -2 -6 \n"+"f -4 -7 -3 \n"
    Str += "f -7 -4 -8 \n"+"f -3 -5 -1 \n"+"f -5 -3 -7 \n"
    Str += "# 12 faces\n"

    return Str
               


def SphVrt(Pos,Radius):

    Points = ""

    PX,PY,PZ,RD,Oa = Pos[0],Pos[1],Pos[2],Radius,90

    Points += "v " + str((PX)+(RD*0)) + " " + str((PY)+(RD*0)) + " " + str((PZ)+(1*RD)) + " " + "\n"

    if True:
               
        while ( Oa != -90+30 ):
            Oa,Ob,Oc = Oa-30,0,360
            while ( Ob != 360 and Oc != 0 ):
                Pcx = math.sin(math.radians(Oc)) * math.cos(math.radians(Oa))
                Pcy = math.cos(math.radians(Ob)) * math.cos(math.radians(Oa))
                Pcz = math.sin(math.radians(Oa)) * math.sin(math.radians(90))
                Points += "v " + str(PX+(Pcx*RD)) + " " + str(PY+(Pcy*RD)) + " " + str(PZ+(Pcz*RD)) + " " + "\n"
                Ob,Oc = Ob+30,Oc-30
               
    Points += "v " + str(PX+(0*RD)) + " " + str(PY+(0*RD)) + " " + str(PZ+(-1*RD)) + " " + "\n"

    return Points

              

def FixedFaceInfo():

    return GetSphFaceData()




# ------- SPECIFIC FUNCTIONS ---------



def GetMeshVertsData(Verts): 

    Vts = []

    for i in range ( 0 , len(Verts) ):

     assert i == Verts[i][0], "\n\n - Indexing not following Sequence"

     Vts.append([ 0, Verts[i][1], Verts[i][2], Verts[i][3]  ])
     
    #assert len(GetUniqueItems(Vts)[0]) == len(Vts), "\n\n - Duplicate Vertices found"

    return Vts



def GetMeshNormsData(Norms): 

    Nts = []

    for i in range ( 0 , len(Norms) ):

     assert i == Norms[i][0], "\n\n - Indexing not following Sequence"

     Nts.append([ 0, Norms[i][1], Norms[i][2], Norms[i][3]  ])

    return Nts



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




def GetOtherInfo(Mgs,Gls): 

    Mag,Glw = [],[]

    for i in range ( 0 , len(Mgs) ):

     N = ""
     if Mgs[i][5]!=-1:
                       N += "A"
     assert i == Mgs[i][0], "\n\n - Indexing not following Sequence"

     Mag.append([ 0, Mgs[i][2], Mgs[i][3], Mgs[i][4], N ])

    for i in range ( 0 , len(Gls) ):

     assert i == i, "\n\n - Indexing not following Sequence"

     Glw.append([ 0, Gls[i][0], Gls[i][1], Gls[i][2], Gls[i][3] ])

    return Mag,Glw
               
               

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



def GetModMatInfo(Mat,Texs):

    Mts = []

    Nr = 10

    Mat[15] = Mat[15]*100

    map_D,map_O,map_R,map_B = "","","",""

    for i in range ( 0 , len(Texs) ):

        if Mat[0] == Texs[i][1][0] and Texs[i][0] == "DIFFUSE" :
                                                      map_D = str(Texs[i][1][1])
        if Mat[0] == Texs[i][1][0] and Texs[i][0] == "OPACITY" :
                                                      map_O = str(Texs[i][1][1])
        if Mat[0] == Texs[i][1][0] and Texs[i][0] == "REFLECT" :
                                                      map_R = str(Texs[i][1][1])
        if Mat[0] == Texs[i][1][0] and Texs[i][0] == "BUMP" :
                                                      map_B = str(Texs[i][1][1])
    Mts = [ 0,Mat[1][1:-1],
            
            GetFNum(Mat[2],Nr),GetFNum(Mat[3],Nr),GetFNum(Mat[4],Nr),
            
            GetFNum(Mat[8],Nr),GetFNum(Mat[9],Nr),GetFNum(Mat[10],Nr),
            
            GetFNum(Mat[11],Nr),GetFNum(Mat[12],Nr),GetFNum(Mat[13],Nr),
            
            GetFNum(1.0-Mat[13],Nr),GetFNum(Mat[15],Nr),GetFNum(1.5,Nr),
            
            map_D[1:-1],map_O[1:-1],map_R[1:-1],map_B[1:-1] ]
    
    return Mts
        


def GetSphFaceData():

    Mverts = ""

    if True:

        Mverts += "f -62 -61 -60 " + "\n" 
        Mverts += "f -62 -60 -59 " + "\n"
        Mverts += "f -62 -59 -58 " + "\n"
        Mverts += "f -62 -58 -57 " + "\n"
        Mverts += "f -62 -57 -56 " + "\n"
        Mverts += "f -62 -56 -55 " + "\n"
        Mverts += "f -62 -55 -54 " + "\n"
        Mverts += "f -62 -54 -53 " + "\n"
        Mverts += "f -62 -53 -52 " + "\n"
        Mverts += "f -62 -52 -51 " + "\n"
        Mverts += "f -62 -51 -50 " + "\n"
        Mverts += "f -62 -50 -61 " + "\n"
        Mverts += "f -61 -49 -48 " + "\n"
        Mverts += "f -61 -48 -60 " + "\n"
        Mverts += "f -60 -48 -47 " + "\n"
        Mverts += "f -60 -47 -59 " + "\n"
        Mverts += "f -59 -47 -46 " + "\n"
        Mverts += "f -59 -46 -58 " + "\n"
        Mverts += "f -58 -46 -45 " + "\n"
        Mverts += "f -58 -45 -57 " + "\n"
        Mverts += "f -57 -45 -44 " + "\n"
        Mverts += "f -57 -44 -56 " + "\n"
        Mverts += "f -56 -44 -43 " + "\n"
        Mverts += "f -56 -43 -55 " + "\n"
        Mverts += "f -55 -43 -42 " + "\n"
        Mverts += "f -55 -42 -54 " + "\n"
        Mverts += "f -54 -42 -41 " + "\n"
        Mverts += "f -54 -41 -53 " + "\n"
        Mverts += "f -53 -41 -40 " + "\n"
        Mverts += "f -53 -40 -52 " + "\n"
        Mverts += "f -52 -40 -39 " + "\n"
        Mverts += "f -52 -39 -51 " + "\n"
        Mverts += "f -51 -39 -38 " + "\n"
        Mverts += "f -51 -38 -50 " + "\n"
        Mverts += "f -50 -38 -49 " + "\n"
        Mverts += "f -50 -49 -61 " + "\n"
        Mverts += "f -49 -37 -36 " + "\n"
        Mverts += "f -49 -36 -48 " + "\n"
        Mverts += "f -48 -36 -35 " + "\n"
        Mverts += "f -48 -35 -47 " + "\n"
        Mverts += "f -47 -35 -34 " + "\n"
        Mverts += "f -47 -34 -46 " + "\n"
        Mverts += "f -46 -34 -33 " + "\n"
        Mverts += "f -46 -33 -45 " + "\n"
        Mverts += "f -45 -33 -32 " + "\n"
        Mverts += "f -45 -32 -44 " + "\n"
        Mverts += "f -44 -32 -31 " + "\n"
        Mverts += "f -44 -31 -43 " + "\n"
        Mverts += "f -43 -31 -30 " + "\n"
        Mverts += "f -43 -30 -42 " + "\n"
        Mverts += "f -42 -30 -29 " + "\n"
        Mverts += "f -42 -29 -41 " + "\n"
        Mverts += "f -41 -29 -28 " + "\n"
        Mverts += "f -41 -28 -40 " + "\n"
        Mverts += "f -40 -28 -27 " + "\n"
        Mverts += "f -40 -27 -39 " + "\n"
        Mverts += "f -39 -27 -26 " + "\n"
        Mverts += "f -39 -26 -38 " + "\n"
        Mverts += "f -38 -26 -37 " + "\n"
        Mverts += "f -38 -37 -49 " + "\n"
        Mverts += "f -37 -25 -24 " + "\n"
        Mverts += "f -37 -24 -36 " + "\n"
        Mverts += "f -36 -24 -23 " + "\n"
        Mverts += "f -36 -23 -35 " + "\n"
        Mverts += "f -35 -23 -22 " + "\n"
        Mverts += "f -35 -22 -34 " + "\n"
        Mverts += "f -34 -22 -21 " + "\n"
        Mverts += "f -34 -21 -33 " + "\n"
        Mverts += "f -33 -21 -20 " + "\n"
        Mverts += "f -33 -20 -32 " + "\n"
        Mverts += "f -32 -20 -19 " + "\n"
        Mverts += "f -32 -19 -31 " + "\n"
        Mverts += "f -31 -19 -18 " + "\n"
        Mverts += "f -31 -18 -30 " + "\n"
        Mverts += "f -30 -18 -17 " + "\n"
        Mverts += "f -30 -17 -29 " + "\n"
        Mverts += "f -29 -17 -16 " + "\n"
        Mverts += "f -29 -16 -28 " + "\n"
        Mverts += "f -28 -16 -15 " + "\n"
        Mverts += "f -28 -15 -27 " + "\n"
        Mverts += "f -27 -15 -14 " + "\n"
        Mverts += "f -27 -14 -26 " + "\n"
        Mverts += "f -26 -14 -25 " + "\n"
        Mverts += "f -26 -25 -37 " + "\n"
        Mverts += "f -25 -13 -12 " + "\n"
        Mverts += "f -25 -12 -24 " + "\n"
        Mverts += "f -24 -12 -11 " + "\n"
        Mverts += "f -24 -11 -23 " + "\n"
        Mverts += "f -23 -11 -10 " + "\n"
        Mverts += "f -23 -10 -22 " + "\n"
        Mverts += "f -22 -10 -9 " + "\n"
        Mverts += "f -22 -9 -21 " + "\n"
        Mverts += "f -21 -9 -8 " + "\n"
        Mverts += "f -21 -8 -20 " + "\n"
        Mverts += "f -20 -8 -7 " + "\n"
        Mverts += "f -20 -7 -19 " + "\n"
        Mverts += "f -19 -7 -6 " + "\n"
        Mverts += "f -19 -6 -18 " + "\n"
        Mverts += "f -18 -6 -5 " + "\n"
        Mverts += "f -18 -5 -17 " + "\n"
        Mverts += "f -17 -5 -4 " + "\n"
        Mverts += "f -17 -4 -16 " + "\n"
        Mverts += "f -16 -4 -3 " + "\n"
        Mverts += "f -16 -3 -15 " + "\n"
        Mverts += "f -15 -3 -2 " + "\n"
        Mverts += "f -15 -2 -14 " + "\n"
        Mverts += "f -14 -2 -13 " + "\n"
        Mverts += "f -14 -13 -25 " + "\n"
        Mverts += "f -1 -12 -13 " + "\n"
        Mverts += "f -1 -11 -12 " + "\n"
        Mverts += "f -1 -10 -11 " + "\n"
        Mverts += "f -1 -9 -10 " + "\n"
        Mverts += "f -1 -8 -9 " + "\n"
        Mverts += "f -1 -7 -8 " + "\n"
        Mverts += "f -1 -6 -7 " + "\n"
        Mverts += "f -1 -5 -6 " + "\n"
        Mverts += "f -1 -4 -5 " + "\n"
        Mverts += "f -1 -3 -4 " + "\n"
        Mverts += "f -1 -2 -3 " + "\n"
        Mverts += "f -1 -13 -2 " + "\n"
        Mverts += "# 120 faces" + "\n"

    return Mverts
