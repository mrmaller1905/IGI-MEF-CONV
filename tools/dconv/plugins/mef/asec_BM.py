import os
from utils import fs
import math as m
import numpy as np

def fromfile(meffilename,Data):
    
    meftext = ""

    L = ""+"\n"

    NameOfModel = str(os.path.splitext(os.path.basename(meffilename))[0])        

    ModelName00 = str(os.path.splitext(os.path.basename(meffilename))[0])

    OrginalModel = (ModelName00)

    if True:


# Necessary Calculations ------------------------------

    
        Mts = CalC_Mats(Data[2],Data[4])

        Bnes = CalC_BoneData(Data[4])

        Vts,Nts = CalC_Verts(Data[4])

        Fcs,Tcs = CalC_Faces(Data[4])

        Mag,Gls = CalC_Other(Data[4])

        Atta = CalC_Attachmentinfo(Data[4])

        Do = NecessaryChecks(Data[2],Data[4])


# BoneLinks Data for MEF Conversion -------------------


        Bones = ""

        for i in range ( 0 , len(Bnes) ):

            Bones += "Bone(" + str(Bnes[i][0]) + ",\"" + str(Bnes[i][1]) + "\"," + str(Bnes[i][6]) +","+ str(Bnes[i][2]) +","+ str(Bnes[i][3]) +","+ str(Bnes[i][4]) +");\n"

        Bones += "BuildHierarchy();\n"
        

# Materials Data for MEF Conversion -------------------

    
        Materials = ""

        n = 0
    
        for i in range ( 0, len(Mts) ):

            Mt,n = "",Mts[i][0]

            if ( Mts[i][6] != [] ):
                    Mt += "DiffuseTMap(" + str(n) + "," +"\""+ str(Mts[i][6][2]) +"\""+ ","+str(Mts[i][6][1])+","+str(Mts[i][6][0])+");\n"

            if ( Mts[i][7] != [] ):
                    Mt += "OpacityTMap(" + str(n) + "," +"\""+ str(Mts[i][7][2]) +"\""+ "," +str(Mts[i][7][1])+","+str(Mts[i][7][0])+");\n"

            if ( Mts[i][8] != [] ):
                    Mt += "BumpTMap(" + str(n) + "," + "\"" + str(Mts[i][8][2]) + "\"" + ","+str(Mts[i][8][1])+","+str(Mts[i][8][0])+");\n"

            if ( Mts[i][9] != [] ):
                    Mt += "ReflectionTMap(" + str(n) +","+"\""+ str(Mts[i][9][2]) +"\""+ ","+str(Mts[i][9][1])+","+str(Mts[i][9][0])+");\n"
                    
            Materials += "Material(" + str(n) + ",\"" + str(Mts[i][1]) + "\","+str(Mts[i][11][0])+","+str(Mts[i][11][1])+","+str(Mts[i][11][2])+","+str(Mts[i][12][0])+","+str(Mts[i][12][1])+","+str(Mts[i][12][2])+","+str(Mts[i][13][0])+","+str(Mts[i][13][1])+","+str(Mts[i][13][2])+","+str(Mts[i][2])+","+str(Mts[i][3])+","+str(Mts[i][4])+");" + '\n'           
            Materials += "MaterialShininess(" + str(n) + ","+str(Mts[i][5])+");" + '\n' + str(Mt)

            n += 1
                

# Vertices Data for MEF conversion -------        

    
        Vertices = ""
        
        Normals = ""
                
        for i in range ( 0, len(Vts) ):
        
            Vertices += "Vertex(" + str(i) + "," + str(Vts[i][1]) + "," + str(Vts[i][2]) + "," + str(Vts[i][3]) + ");" + "\n"
            
        for i in range ( 0 , len(Nts) ):

            Normals += "Normal(" + str(i) + "," + str(Nts[i][1]) + "," + str(Nts[i][2]) + "," + str(Nts[i][3]) + ");" + '\n'
            
        
# Face/UV Data for MEF conversion -------

        
        Faces = ""
            
        UVs = ""
        
        for i in range ( 0 , len(Fcs) ):

            Faces += "Face("+str(i)+","+str(Fcs[i][1])+","+str(Fcs[i][2])+","+str(Fcs[i][3])+","+str(Fcs[i][4])+","+str(Fcs[i][5])+","+str(Fcs[i][6])+","+str(Fcs[i][7])+");" + '\n'
        
        for i in range ( 0 , len(Tcs) ):
    
            UVs += "UV(" + str(i) + ","+str(Tcs[i][1])+","+str(Tcs[i][2])+","+str(Tcs[i][3])+","+str(Tcs[i][4])+","+str(Tcs[i][5])+","+str(Tcs[i][6])+"" + ");" + '\n'
            
            
# Magics/Glows Data for MEF Conversion --------                

                
        mvertices = ""
        
        glows = ""
    
        for i in range ( 0, len(Mag) ):
        
            mvertices += "MagicVertex(" + str(Mag[i][0]) + ","+str(str(Mag[i][1]))+"," + str(Mag[i][2]) + "," + str(Mag[i][3]) + "," + str(Mag[i][4]) + "," + str(Mag[i][5]) + ");\n"
    
        for i in range ( 0, len(Gls) ):
    
            glows += "Glow(" + str(Gls[i][1]) +","+ str(Gls[i][2]) +","+ str(Gls[i][3]) +","+ str(Gls[i][4]) +","+str(Gls[i][5][0]) +","+ str(Gls[i][5][1]) +","+ str(Gls[i][5][2]) + ");\n"



# ---------------------------------------------------------------------------

# Initial text (Newobject)

        meftext += "NewObject(\"" + str(NameOfModel) + "\");" + "\n"
    
# Material    

        meftext +=  str(Materials)
    
# Breakscript

        meftext += "BreakScript();\n"
    
# Bones   

        meftext +=  str(Bones)
    
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

# glows

        meftext +=  str(glows)


    return meftext


# ----------------------------------------------------
# ------------- OTHER FUNCTIONS ----------------------
# ----------------------------------------------------



def CalC_Mats(Mats,Meshes):

    Mti,Mts = [],[]

    MshID = GetTargetMesh(Meshes)[-2]

    for i in range ( 0 , len(Mats) ):

        if ( Mats[i][1] == MshID ):

            Mti += Mats[i]
            break

    if ( len(Mti) == 0 ) and ( MshID != -1 ):
        
        print("!Warning Applied Material not found in Mat. list")

    if ( len(Mti) == 0 ) or ( len(Mats) == 0 ):
                                                return []
                                            
    if ( Mti[18-1] > 0 and Mti[3] == "Multi/Sub-Object" ):

      for i in range ( 0 , Mti[18-1] ):

        M = Mti[i+18]
        Mts.append(ExtData1(M)) ##FF##
    else:
      if 1:
        M = Mti[:18-1]
        Mts.append(ExtData1(M)) ##FF##


    return Mts



def CalC_BoneData(Meshes):

    Bnes = []

    for i in range ( 0 , len(Meshes) ):

      if Meshes[i][0].find("bone") != -1 :

        BString = "\""+str(0)+"\"" ######################################

        Cindex = 0 ######################################

        Bnes.append([ len(Bnes), BString, Msh[5][0], Msh[5][1], Msh[5][2], Cindex ])

    return Bnes
    


def CalC_Verts(Meshes):

    Vts,Nts = [],[]

    Msh,Norms = GetTargetMesh(Meshes), CalC_Norms(GetTargetMesh(Meshes)) ##FF##
    
    MSh,NormS = GetColMesh01(Meshes), CalC_Norms(GetColMesh01(Meshes)) ##FF##

    Verts,Norms,Faces = Msh[8],Norms[0],Msh[10-1]

    for i in range ( 0 , len(Verts) ):

      Vts.append([ len(Vts), round(Verts[i][1],9), round(Verts[i][2],9), round(Verts[i][3],9) ])

    for i in range ( 0 , len(Norms) ):

      Nts.append([ len(Nts), round(Norms[i][0],8), round(Norms[i][1],8), round(Norms[i][2],8) ])

    if ( len(Norms) == 0 and len(Faces) != 0 ):
                                                 Nts += CalC_FNormals(Verts,Faces)[0] ##

    Verts,Norms,Faces = MSh[8],NormS[0],MSh[10-1]

    for i in range ( 0 , len(Verts) ):

      Vts.append([ len(Vts), round(Verts[i][1],9), round(Verts[i][2],9), round(Verts[i][3],9) ])

    for i in range ( 0 , len(Norms) ):

      Nts.append([ len(Nts), round(Norms[i][0],8), round(Norms[i][1],8), round(Norms[i][2],8) ])
      
    if ( len(NormS) == 0 and len(Faces) != 0 ):
                                                 Nts += CalC_FNormals(Verts,Faces)[0] ##
    return Vts,Nts



def CalC_Faces(Meshes):

    Fcs,Tcs = [],[]

    Msh,Nin = GetTargetMesh(Meshes), GetNormsIndex(GetTargetMesh(Meshes)) ##FF##

    MSh,NiN = GetColMesh01(Meshes), GetNormsIndex(GetColMesh01(Meshes)) ##FF##
    
    Faces,UVs,UVf = Msh[10-1],Msh[10+2],Msh[10+3]
    
    for i in range ( 0 , len(Faces) ):

      Fcs.append([ len(Fcs), Faces[i][1], Faces[i][3], Faces[i][2], Nin[i][1], Nin[i][3], Nin[i][2], Faces[i][-1] ])

    for i in range ( 0 , len(UVf) ):

      A,B,C = UVf[i][1],UVf[i][3],UVf[i][2]
      
      Tcs.append([ len(Tcs), round(UVs[A][1],9), round(UVs[A][2],9), round(UVs[B][1],9), round(UVs[B][2],9), round(UVs[C][1],9), round(UVs[C][2],9) ])
    
    Faces,UVs,UVf = MSh[10-1],MSh[10+2],MSh[10+3] ##

    OFF,off = len(Msh[8]),GetMaxValue(Nin)+1 ##

    for i in range ( 0 , len(Faces) ):

      Fcs.append([ len(Fcs), OFF+Faces[i][1], OFF+Faces[i][3], OFF+Faces[i][2], off+NiN[i][1], off+NiN[i][3], off+NiN[i][2], 0+Faces[i][-1] ])

    for i in range ( 0 , len(UVf) ):

      A,B,C = UVf[i][1],UVf[i][3],UVf[i][2]
      
      Tcs.append([ len(Tcs), round(UVs[A][1],9), round(UVs[A][2],9), round(UVs[B][1],9), round(UVs[B][2],9), round(UVs[C][1],9), round(UVs[C][2],9) ])

    return Fcs,Tcs



def CalC_Other(Meshes):

    Mags,Glws = [],[]

    for i in range ( 0 , len(Meshes) ):

      if ( Meshes[i][0].find("magic") != -1 ):

          Mags.append([ len(Mags), 0, round(Meshes[i][5][0],6), round(Meshes[i][5][1],6), round(Meshes[i][5][2],6), GetMValue(Meshes[i][0]) ])

      elif ( Meshes[i][0].find("glow") != -1 ):

          Glws.append([ len(Glws), round(Meshes[i][5][0],6), round(Meshes[i][5][1],6), round(Meshes[i][5][2],6), GetSize(Meshes[i][8]), Meshes[i][-1] ])


    return Mags,Glws
    


def CalC_Attachmentinfo(Meshes):

    Atta,exts = [],[]

    for i in range ( 0 , len(Meshes) ):

      if ( Meshes[i][0].find("attach") != -1 ):

        Atta.append([ len(Atta), Meshes[i][0][10-1:], Meshes[i][2], Meshes[i][3], Meshes[i][4], Meshes[i][5], -1 ])


    return Atta

    

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ MAJOR FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



def NecessaryChecks(Mats,Meshes):

    assert 0 == 0, "\n\n ->"

    assert 0 == 0, "\n\n ->"

    assert 0 == 0, "\n\n ->"

    assert 0 == 0, "\n\n ->"

    return 0



def GetTargetMesh(Meshes): #

    Mshes = []

    for i in range ( 0 , len(Meshes) ):

      if Meshes[i][0].find("glow") == -1 and Meshes[i][0].find("attach") == -1 :

       if Meshes[i][0].find("magic") == -1 and Meshes[i][0].find("bone") == -1 :

        if Meshes[i][0].find("Portal") == -1 and Meshes[i][0].find("ColMesh01") == -1 :

           Mshes.append(Meshes[i])

    if ( len(Mshes) == 0 ):
                          print("!Warning, No object found in file")
    if ( len(Mshes) >= 2 ):
                          print("!Warning, More than one object found in file")
    if ( len(Mshes) == 0 ):
                          Mshes.append(["","",[],[],[],[],0,0,[],[],0,0,[],[],0,[],-1,[]])
    return Mshes[0]



def GetColMesh01(Meshes):

    Mshes = []

    for i in range ( 0 , len(Meshes) ):

       if Meshes[i][0].find("ColMesh01") != -1 :

           Mshes.append(Meshes[i])
           
    if ( len(Mshes) >= 2 ):
                          print("!Warning, More than one object found in file")
    if ( len(Mshes) == 0 ):
                          Mshes.append(["","",[],[],[],[],0,0,[],[],0,0,[],[],0,[],-1,[]])
    return Mshes[0]



def ExtData1(Mt):

    Mat = [Mt[1],Mt[2],Mt[13],Mt[14],Mt[15],Mt[16],[],[],[],[],0,Mt[4:7],Mt[7:10],Mt[10:13]]

    Mat[11] = [ round(Mat[11][0],3),round(Mat[11][1],3),round(Mat[11][2],3) ]

    Mat[12] = [ round(Mat[12][0],1),round(Mat[12][1],1),round(Mat[12][2],1) ]

    Mat[13] = [ round(Mat[13][0],1),round(Mat[13][1],1),round(Mat[13][2],1) ]

    if ( Mt[2].find("Transparent") != -1 or Mt[2].find("collision01") != -1 ) and Mt[15] != 1.0 :

     print("!Warning! Transparent mesh faces are not made hidden")

    Mat[2],Mat[3] = CalC_Sfloat(Mat[2]),CalC_Sfloat(Mat[3]) ##FF##

    Mat[4],Mat[5] = CalC_Sfloat(Mat[4]),CalC_Sfloat(Mat[5]) ##FF##

    Mat[6],Mat[7] = GetTextureinf(Mt,0),GetTextureinf(Mt,1) ##FF##

    Mat[8],Mat[9] = GetTextureinf(Mt,2),GetTextureinf(Mt,3) ##FF##

    return Mat



def CalC_FNormals(Verts,Faces): #

    Nts,Nin = [],[]

    if ( len(Faces) > 0 ):

        for i in range ( 0 , len(Faces) ):

            A,C,B= Faces[i][1],Faces[i][2],Faces[i][3]

            PA = [Verts[A][1],Verts[A][2],Verts[A][3]]
            PB = [Verts[B][1],Verts[B][2],Verts[B][3]]
            PC = [Verts[C][1],Verts[C][2],Verts[C][3]]
            
            Edge1 = [ PC[0]-PA[0] , PC[1]-PA[1] , PC[2]-PA[2] ]
            NVert = [ 0.000000001 , 0.000000001 , 0.000000001 ]
            Edge2 = [ PB[0]-PA[0] , PB[1]-PA[1] , PB[2]-PA[2] ]

            if ( np.linalg.norm(np.cross(Edge1,Edge2)) != 0 ):
             NVert = (np.cross(Edge1,Edge2))/np.linalg.norm(NVert)

            Nts.append([ NVert[0], NVert[1], NVert[2], PA[0], PA[1], PA[2] ])
            Nts.append([ NVert[0], NVert[1], NVert[2], PB[0], PB[1], PB[2] ])
            Nts.append([ NVert[0], NVert[1], NVert[2], PC[0], PC[1], PC[2] ])
            

    return CalC_UniqueItems(Nts,Nin) ##FF##


def CalC_Norms(Msh):

    Nts,Nin = [],[]

    Verts,Faces,Norms = Msh[8],Msh[9],Msh[15]

    if ( len(Norms) > 0 ):

      for i in range ( 0 , len(Faces) ):

          A,C,B= (3*i+0),(3*i+1),(3*i+2)
          D,F,E= Faces[i][1],Faces[i][2],Faces[i][3]

          PA = [Verts[D][1],Verts[D][2],Verts[D][3]]
          PB = [Verts[E][1],Verts[E][2],Verts[E][3]]
          PC = [Verts[F][1],Verts[F][2],Verts[F][3]]

          NA = [Norms[A][1],Norms[A][2],Norms[A][3]]
          NB = [Norms[B][1],Norms[B][2],Norms[B][3]]
          NC = [Norms[C][1],Norms[C][2],Norms[C][3]]

          Nts.append([ NA[0], NA[1], NA[2], PA[0], PA[1], PA[2] ])
          Nts.append([ NB[0], NB[1], NB[2], PB[0], PB[1], PB[2] ])
          Nts.append([ NC[0], NC[1], NC[2], PC[0], PC[1], PC[2] ])
            

    return CalC_UniqueItems(Nts,Nin) ##FF##


def GetNormsIndex(Msh):

    Nin = []

    Verts,Faces,Norms = Msh[8],Msh[9],Msh[15]

    if ( len(Norms) != 0 and len(Faces) != 0 ):

      Nin2 = CalC_Norms(Msh)[1] ##ff##

    else:

      Nin2 = CalC_FNormals(Verts,Faces)[1] ##ff##

    for i in range ( 0 , len(Faces) ):

      Nin.append([ i, Nin2[3*i+0], Nin2[3*i+2], Nin2[3*i+1] ])


    return Nin



def GetMValue(StringName): ##

    if StringName[-1] == "A":
                            return 0
    if StringName[-1] == "B":
                            return 1
    return -1


def GetSize(Verts):

    Amp,Mean = 0,[0,0.0,0.0,0.0]

    for i in range ( 0 , len(Verts) ):

     Mean[1] += Verts[i][1]
        
     Mean[2] += Verts[i][2]
        
     Mean[3] += Verts[i][3]

    Mean[1],Mean[2],Mean[3] = Mean[1]/len(Verts),Mean[2]/len(Verts),Mean[3]/len(Verts)

    for i in range ( 0 , len(Verts) ):

       if CalC_Dist(Verts[i],Mean) > Amp:

           Amp = CalC_Dist(Verts[i],Mean)  ##FF##

    return Amp


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ MINOR FUNCTIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\



def CalC_Sfloat(N):

    if ( N == 0.0 ):
                    return 0
    if ( N == 1.0 ):
                    return 1
    return N


def GetTextureinf(M,N):

    Mps = []

    Tts = [ "MAP_DIFFUSE","MAP_OPACITY","MAP_REFLECT","MAP_BUMP" ]

    for i in range ( 0 , len(M) ):

      if ( M[i] == Tts[N] ):

        Mps += ([ 0, M[i+3], M[i+4] ])

        Mps[-2] = CalC_Sfloat(Mps[-2])

    if ( len(Mps) >= 4):
                        print("\n!Warning! Mapinfo found more than one")
    if ( len(Mps) >= 4):
                        Mps = Mps[:4-1]
    return Mps


def CalC_Dist(V,M):

    V = [ 0,V[1]-M[1], V[2]-M[2], V[3]-M[3] ]

    V = [ V[1]*V[1], V[2]*V[2], V[3]*V[3] ]

    return (V[0]+V[1]+V[2])**(1/2)


def CalC_UniqueItems(Nts,Nin):

    Nts02,Nin02 = [],[]

    for i in range ( 0 , len(Nts) ):

        E = 0
            
        for j in range ( 0 , len(Nts02) ):
                
            if Nts[i] == Nts02[j]:
                    
                Nin02.append(j)
                       
                E = 1
                       
                break
                    
        if E == 0:
                
                Nin02.append(len(Nts02))
                
                Nts02.append(Nts[i+0])

    return Nts02,Nin02


def GetMaxValue(Nin):

    R = -1

    for i in range ( 0 , len(Nin) ):

     R = max(Nin[i][1], Nin[i][2], Nin[i][3])

    return R
    


def SI(Num,N):

    R = str(Num)

    assert len(R) <= N , "Digits must be less than the required"

    while len(R) < N :

        R = "0"+str(Num)

    return R

    
