import os
from utils import fs
import numpy as np
import math
from math import *
from .import ase_CS
from .import reader_MEFG
from .reader_MEFG import *

def fromfile(meffilename,Data,Arg0):
    
    meftext = ""

    N,L = 0,""+"\n"

    Bones,Vfts = Data[11],Data[12]

    BonesH = GetBoneHierarchyData(Bones)

    O = OtherData(Data[4],Data[5],Data[6])

    ModelMNam = str(os.path.splitext(os.path.basename(meffilename))[0])        

    ModelName = str(os.path.splitext(os.path.basename(meffilename))[0])

#--------------------- 1. SCENE INFO -------------<


    Info = ""

    Info += "*SCENE {"+L
    Info += "	*SCENE_FILENAME \"\""+L
    Info += "	*SCENE_FIRSTFRAME 0"+L
    Info += "	*SCENE_LASTFRAME 100"+L
    Info += "	*SCENE_FRAMESPEED 30"+L
    Info += "	*SCENE_TICKSPERFRAME 160"+L
    Info += "	*SCENE_BACKGROUND_STATIC 0.0000000000	0.0000000000	0.0000000000"+L
    Info += "	*SCENE_AMBIENT_STATIC 0.0000000000	0.0000000000	0.0000000000"+L
    Info += "}"+L
    
    NORMS = GetNormalsofMesh(Data[4],Data[5],Data[6])
        
        
#--------------------- 2. MATERIALS INFO -----------<


    Mats = ""

    N_Mats,N_tex = len(Data[2]),len(Data[3])

    MATS,Mts = "",Conv_Mats(Data[2],Data[3])

    for i in range ( 0 , N_Mats ):
        
     MATS += "		*SUBMATERIAL "+str(i)+" {"+L
     MATS += "			*MATERIAL_NAME "+str(Mts[i][1])+L
     MATS += "			*MATERIAL_CLASS \""+"Standard"+"\""+L
     MATS += "			*MATERIAL_AMBIENT " +str(Mts[i][2])+Sp(2)+str(Mts[i][3])+Sp(2)+str(Mts[i][4])+L
     MATS += "			*MATERIAL_DIFFUSE " +str(Mts[i][5])+Sp(2)+str(Mts[i][6])+Sp(2)+str(Mts[i][7])+L
     MATS += "			*MATERIAL_SPECULAR " +str(Mts[i][8])+Sp(1)+str(Mts[i][9])+Sp(2)+str(Mts[i][10])+L
     MATS += "			*MATERIAL_SHINE "+str(Mts[i][11])+L
     MATS += "			*MATERIAL_SHINESTRENGTH "+str(Mts[i][12])+L
     MATS += "			*MATERIAL_TRANSPARENCY " +str(Mts[i][13])+L
     MATS += "			*MATERIAL_WIRESIZE " +str(Mts[i][14])+L
     MATS += "			*MATERIAL_SELFILLUM "+str(Mts[i][15])+L
     MATS += ""  +  str(Mts[i][16])
     MATS += "		}"+L
    
    Mats += "*MATERIAL_LIST {"+L
    Mats += "	*MATERIAL_COUNT "+str(1+len(Data[10]))+L
    Mats += "	*MATERIAL 0 {"+L
    Mats += "		*MATERIAL_NAME \""+str(ModelName)+"\""+L
    Mats += "		*MATERIAL_CLASS \"Multi/Sub-Object\""+L
    Mats += "		*NUMSUBMTLS "+str(N_Mats)+L
    Mats += ""  +  (MATS)
    Mats += "   	}"+L

    
#--------------------- MESH INFO -----------<


    MESH = ""

    VERTS,Vts = "",Conv_Verts(Data[4])

    for i in range ( 0 , len(Vts) ):

        VERTS += Spc(3)+"*MESH_VERTEX  "+Vts[i][0] + Sp(6)+Vts[i][1] + Sp(3)+Vts[i][2] + Sp(3)+Vts[i][3] +L

    FACES,Fcs = "",Conv_Faces(Data[6],O)

    for i in range ( 0 , len(Fcs) ):

        FACES += Spc(3)+"*MESH_FACE  "+Fcs[i][0] +"   "+ " "+Fcs[i][1] + " "+Fcs[i][2] + " "+Fcs[i][3] + " "
        FACES += "" + Fcs[i][4] + " " + Fcs[i][5] + " "+Fcs[i][6] + Sp(3) + Fcs[i][7] + Spc(1) + Fcs[i][8] +L

    TVERTS,Tcs = "",Conv_UVs(Data[7])

    for i in range ( 0 , len(Tcs) ):

        TVERTS += Spc(3)+"*MESH_TVERT  "+Tcs[i][0] + Sp(4)+Tcs[i][1] + Sp(2)+Tcs[i][2] + Sp(2)+Tcs[i][3] +L

    TFACES,Tfs = "",Conv_Tfaces(Data[7])

    for i in range ( 0 , len(Tfs) ):

        TFACES += Spc(3)+"*MESH_TFACE  "+Tfs[i][0] + Sp(4)+Tfs[i][1] + Sp(2)+Tfs[i][2] + Sp(2)+Tfs[i][3] +L
    
    MESH += "	*MESH {"+L
    MESH += "		*TIMEVALUE "+str(0)+L
    MESH += "		*MESH_NUMVERTEX "+str(len(Vts))+L
    MESH += "		*MESH_NUMFACES "+str(len(Fcs))+L
    MESH += "		*MESH_VERTEX_LIST {"+L
    MESH += "" + (VERTS)
    MESH += "		}"+L
    MESH += "		*MESH_FACE_LIST {"+L
    MESH += "" + (FACES)
    MESH += "		}"+L
    MESH += "		*MESH_NUMTVERTEX "+str(len(Tcs))+L
    MESH += "		*MESH_TVERTLIST {"+L
    MESH += "" + (TVERTS)
    MESH += "		}"+L
    MESH += "		*MESH_NUMTVFACES "+str(len(Tfs))+L
    MESH += "		*MESH_TFACELIST {"+L
    MESH += "" + (TFACES)
    MESH += "		}"+L
    MESH += "		*MESH_NUMCVERTEX "+str(0)+L
    MESH += "		*MESH_NORMALS {"+L
    MESH += "" + (NORMS)
    MESH += "		}"+L
    MESH += "	}"+L

    obj = ""
    
    obj += "*GEOMOBJECT {"+L
    obj += "	*NODE_NAME \""+str(ModelName)+"\""+L
    obj += "	*NODE_TM {"+L
    obj += "		*NODE_NAME \""+str(ModelName)+"\""+L
    obj += "		*INHERIT_POS 0 0 0"+L
    obj += "		*INHERIT_ROT 0 0 0"+L
    obj += "		*TM_ROW0 1.0000000000	0.0000000000	0.0000000000"+L
    obj += "		*TM_ROW1 0.0000000000	1.0000000000	0.0000000000"+L
    obj += "		*TM_ROW2 0.0000000000	0.0000000000	1.0000000000"+L
    obj += "		*TM_ROW3 0.0000000000	0.0000000000	0.0000000000"+L
    obj += "	}"+L
    obj += "" + MESH
    obj += "	*PROP_CASTSHADOW 1"+L
    obj += "	*PROP_RECVSHADOW 1"+L
    obj += "	*MATERIAL_REF 0"+L
    obj += "}"+L

#--------------------- 3. BONES INFO -----------<

    bnes = ""

    for i in range ( 0 , len(Bones) ):

      Nm = "Bone"+str(SI(i,2))+"_"+str(Bones[i][1][1:-1])
      Nc = "Bone"+str(SI(Bones[i][2],2))+"_"+str(Bones[Bones[i][2]][1][1:-1])
      
      Vs = BoneVertCData(Bones,BonesH[i])
      Fs = BoneFaceFData(Bones,BonesH[i])

      bnes += "*GEOMOBJECT {" +L
      bnes += "	*NODE_NAME \""+str(Nm)+"\"" +L
      bnes += "	*NODE_PARENT \""+str(Nc)+"\""+L
      bnes += "	*NODE_TM {" +L
      bnes += "		*NODE_NAME \""+str(Nm)+"\"" +L
      bnes += "		*TM_ROW0 "+str(Sf(1.000000000,10))+" "+str(Sf(0.000000000,10))+" "+str(Sf(0.000000000,10)) +L
      bnes += "		*TM_ROW1 "+str(Sf(0.000000000,10))+" "+str(Sf(1.000000000,10))+" "+str(Sf(0.000000000,10)) +L
      bnes += "		*TM_ROW2 "+str(Sf(0.000000000,10))+" "+str(Sf(0.000000000,10))+" "+str(Sf(1.000000000,10)) +L
      bnes += "		*TM_ROW3 "+str(Sf(BonesH[i][0][0],10))+" "+str(Sf(BonesH[i][0][1],10))+" "+str(Sf(BonesH[i][0][2],10)) +L
      bnes += "	}" +L
      bnes += "	*WIREFRAME_COLOR 0.8823529601	0.8294117808	0.8960785031" +L
      bnes += "	*MESH {" +L
      bnes += "		*TIMEVALUE 0" +L
      bnes += "		*MESH_NUMVERTEX 9" +L
      bnes += "		*MESH_NUMFACES 14" +L
      bnes += "		*MESH_VERTEX_LIST {" +L
      bnes += "" +str(Vs)
      bnes += "		}" +L
      bnes += "		*MESH_FACE_LIST {" +L
      bnes += "" +str(Fs)
      bnes += "		}" +L
      bnes += "	}" +L
      bnes += "}" +L

    Mats += "}"+L


#---------------------

    if ( True ):

     meftext += "*3DSMAX_ASCIIEXPORT	200"+"\n"
    
     meftext += "*COMMENT \"AsciiExport Version  2.00 - dd mm yy dd\""+"\n"
    
     meftext += str(Info)

     meftext += str(Mats)

     meftext += str(obj)

     meftext += str(bnes)

#---   

    return meftext



# ----------------------------------------------------
# ------------- FUNCTIONS ----------------------------
# ----------------------------------------------------


def Spc(N):
    
    Space = ""
    for i in range ( 0 , N ):
        Space += "	"
        
    return Space

def Sp(N):
    
    Space = ""
    for i in range ( 0 , N ):
        Space += " "
        
    return Space

def SI(Num,N):

    R = str(Num)
    assert len(R) <= N , "Digits must be less than the required"
    while len(R) < N :
        R = "0"+R

    return R

def Sf(Num,n):

    Num = round(Num,10)
    Num = str(float(Num))
    N = Num.find('.')+11
    assert len(str(Num)) <= N , "PROGRAM ERROR"
    while ( len(str(Num)) != N ):
        Num += "0"
    if Num[0] != "-" :
                        Num = " "+Num
    return Num


def SS(Num,n):

    N = len(str(n))
    Num = str(Num)
    assert len(Num) <= N,"Error Required WhitSpace not in range"
    while ( len(str(Num)) != N ):
        Num = Num+" "

    return Num



# ----------------------------------------------------


def Conv_Verts(Verts):

    if True:

        Length = len(str(len(Verts)-1))

        for i in range ( 0 , len(Verts) ):

          Verts[i][0] = str(Verts[i][0])  

          while ( len(Verts[i][0]) < Length ):

            Verts[i][0] = " "+Verts[i][0]

    if True:

        for i in range ( 0 , len(Verts) ):

          Verts[i][1],Verts[i][2],Verts[i][3] = str(Verts[i][1]),str(Verts[i][2]),str(Verts[i][3])

          if Verts[i][1][0] != "-":
                                    Verts[i][1] = " "+Verts[i][1]
          if Verts[i][2][0] != "-":
                                    Verts[i][2] = " "+Verts[i][2]
          if Verts[i][3][0] != "-":
                                    Verts[i][3] = " "+Verts[i][3]
                                    
        Length_1,Length_2,Length_3 = 0,0,0

        for i in range ( 0 , len(Verts) ):

            if Length_1 < len(Verts[i][1]) :
                                            Length_1 = len(Verts[i][1])
            if Length_2 < len(Verts[i][2]) :
                                            Length_2 = len(Verts[i][2])
            if Length_3 < len(Verts[i][3]) :
                                            Length_3 = len(Verts[i][3])
        for i in range ( 0 , len(Verts) ):

            while Length_1 > len(Verts[i][1]) :
                                            Verts[i][1] += "0"
            while Length_2 > len(Verts[i][2]) :
                                            Verts[i][2] += "0"
            while Length_3 > len(Verts[i][3]) :
                                            Verts[i][3] += "0"
    

    return Verts




def Conv_UVs(Verts):

    if True:

        Vrts = []

        for i in range ( 0 , len(Verts) ):

            Vrts.append([ 3*i+0 , Verts[i][3] , Verts[i][4] , "0.00000000"  ])
            Vrts.append([ 3*i+1 , Verts[i][5] , Verts[i][6] , "0.00000000"  ])
            Vrts.append([ 3*i+2 , Verts[i][1] , Verts[i][2] , "0.00000000"  ])

        Verts,Length = Vrts,len(str(len(Vrts)-1))
        
        for i in range ( 0 , len(Verts) ):

          Verts[i][0] = str(Verts[i][0])  

          while ( len(Verts[i][0]) < Length ):

            Verts[i][0] = Verts[i][0]+" "

    if True:

        for i in range ( 0 , len(Verts) ):

          Verts[i][1],Verts[i][2],Verts[i][3] = str(Verts[i][1]),str(Verts[i][2]),str(Verts[i][3])

          if Verts[i][1][0] != "-":
                                    Verts[i][1] = " "+Verts[i][1]
          if Verts[i][2][0] != "-":
                                    Verts[i][2] = " "+Verts[i][2]
          if Verts[i][3][0] != "-":
                                    Verts[i][3] = " "+Verts[i][3]
                                    
        Length_1,Length_2,Length_3 = 0,0,0

        for i in range ( 0 , len(Verts) ):

            if Length_1 < len(Verts[i][1]) :
                                            Length_1 = len(Verts[i][1])
            if Length_2 < len(Verts[i][2]) :
                                            Length_2 = len(Verts[i][2])
            if Length_3 < len(Verts[i][3]) :
                                            Length_3 = len(Verts[i][3])
        for i in range ( 0 , len(Verts) ):

            while Length_1 > len(Verts[i][1]) :
                                            Verts[i][1] += "0"
            while Length_2 > len(Verts[i][2]) :
                                            Verts[i][2] += "0"
            while Length_3 > len(Verts[i][3]) :
                                            Verts[i][3] += "0"
    

    return Verts




def Conv_Tfaces(Verts):

    if True:

        Faces = []

        for i in range ( 0 , len(Verts) ):

            Faces.append([ i , 3*i+2, 3*i+1, 3*i+0 ])

        Length = len(str(len(Faces)-1))
        
        for i in range ( 0 , len(Faces) ):

           Faces[i][0] = str(Faces[i][0])  

           while ( len(Faces[i][0]) < Length ):

             Faces[i][0] = Faces[i][0]+" "

    if True:
                                    
        Length_1,Length_2,Length_3 = 0,0,0

        for i in range ( 0 , len(Faces) ):

            Faces[i][1],Faces[i][2],Faces[i][3] = str(Faces[i][1]),str(Faces[i][2]),str(Faces[i][3])

            if Length_1 < len(Faces[i][1]) :
                                            Length_1 = len(Faces[i][1])
            if Length_2 < len(Faces[i][2]) :
                                            Length_2 = len(Faces[i][2])
            if Length_3 < len(Faces[i][3]) :
                                            Length_3 = len(Faces[i][3])
        for i in range ( 0 , len(Verts) ):

            while Length_1 > len(Faces[i][1]) :
                                            Faces[i][1] += " "
            while Length_2 > len(Faces[i][2]) :
                                            Faces[i][2] += " "
            while Length_3 > len(Faces[i][3]) :
                                            Faces[i][3] += " "
    
    return Faces



def Conv_Faces(Fces,Fcs):

    if True:

        Faces = []

        for i in range ( 0 , len(Fces) ):

            Faces.append([ i , Fces[i][1] , Fces[i][3] , Fces[i][2] , Fcs[i][0], Fcs[i][1], Fcs[i][2], "1", Fces[i][7] ])

        Length = len(str(len(Faces)-1))
        
        for i in range ( 0 , len(Faces) ):

           Faces[i][0] = str(Faces[i][0])  

           while ( len(Faces[i][0]) < Length ):
                                                 Faces[i][0] = " "+Faces[i][0]
           Faces[i][0] += ":" 
                                                 
    if True:
                                    
        Length_1,Length_2,Length_3 = 0,0,0

        for i in range ( 0 , len(Faces) ):

            Faces[i][1],Faces[i][2],Faces[i][3] = str(Faces[i][1]),str(Faces[i][2]),str(Faces[i][3])

            if Length_1 < len(Faces[i][1]) :
                                            Length_1 = len(Faces[i][1])
            if Length_2 < len(Faces[i][2]) :
                                            Length_2 = len(Faces[i][2])
            if Length_3 < len(Faces[i][3]) :
                                            Length_3 = len(Faces[i][3])
            if True :  #UNK1
                               Faces[i][4] = "AB:    "+str(Faces[i][4])
            if True :  #UNK2        
                               Faces[i][5] = "BC:    "+str(Faces[i][5])
            if True :  #UNK3                     
                               Faces[i][6] = "CA:    "+str(Faces[i][6])
                      
        for i in range ( 0 , len(Faces) ):

            while Length_1 > len(Faces[i][1]) :
                                            Faces[i][1] = " "+Faces[i][1]
            while Length_2 > len(Faces[i][2]) :
                                            Faces[i][2] = " "+Faces[i][2]
            while Length_3 > len(Faces[i][3]) :
                                            Faces[i][3] = " "+Faces[i][3]
            if True :
                      Faces[i][1] = "A:   "+Faces[i][1]
            if True :         
                      Faces[i][2] = "B:   "+Faces[i][2]
            if True :                     
                      Faces[i][3] = "C:   "+Faces[i][3]
                                                 
    if True:
                                    
        Length_1,Length_2 = 0,0

        for i in range ( 0 , len(Faces) ):

            Faces[i][7],Faces[i][8] = str(Faces[i][7]),str(Faces[i][8])

            if Length_1 < len(Faces[i][7]) :
                                            Length_1 = len(Faces[i][7])
            if Length_2 < len(Faces[i][8]) :
                                            Length_2 = len(Faces[i][8])
        for i in range ( 0 , len(Faces) ):

            while Length_1 > len(Faces[i][1]) :
                                            Faces[i][7] += " "
            while Length_2 > len(Faces[i][2]) :
                                            Faces[i][8] += " "
            if True :
                      Faces[i][7] = "*MESH_SMOOTHING "+Faces[i][7]
            if True :         
                      Faces[i][8] = ""+ "*MESH_MTLID "+Faces[i][8]
    
    return Faces


# ------------------------------------------------------------------------------------
# -----------------------------//////////////////////////////-------------------------
# ------------------------------------------------------------------------------------


def Conv_Mats(Mats,Tex):

    if True:

        Mts = []

        for i in range ( 0 , len(Mats) ):

            TxStr = ""

            for j in range ( 0 , len(Tex) ):

              if Mats[i][0] == Tex[j][1][0] :  
            
                TxStr += "			*MAP_"+str(Tex[j][0])+" {"+"\n"
                TxStr += "				*MAP_NAME \"Map # "+str(SI(j,2))+"\""+"\n"
                TxStr += "				*MAP_CLASS \"Bitmap\""+"\n"
                TxStr += "				*MAP_AMOUNT "+str(Sf(Tex[j][1][2],10))+"\n"
                TxStr += "				*BITMAP "+str(Tex[j][1][1]) +"\n"
                TxStr += "			}"+"\n"

            if ( Mats[i][1] == "\"collision01_m21\"" ):
                 Mats[i][2],Mats[i][3],Mats[i][4] = 0.3500, 0.5000, 0.6500

            if ( Mats[i][1] == "\"Transparent\"" ):
                 Mats[i][2],Mats[i][3],Mats[i][4] = 0.4800, 0.5000, 0.5200

            Mts.append([ i,Mats[i][1],
                         Sf(Mats[i][2],10),Sf(Mats[i][3],10),Sf(Mats[i][4],10),
                         Sf(Mats[i][5],10),Sf(Mats[i][6],10),Sf(Mats[i][7],10),
                         Sf(Mats[i][8],10),Sf(Mats[i][9],10),Sf(Mats[i][10],10),
                         Sf(Mats[i][15],10),
                         Sf(Mats[i][11],10),
                         Sf(Mats[i][13],10),
                         Sf(1-Mats[i][13],10),
                         Sf(Mats[i][12],10),
                         TxStr ])
    return Mts


def GetNormalsofMesh(Verts,Norms,Faces):

    Normals,L = "","\n"

    for i in range ( 0 , len(Faces) ):

        No = max([len(Faces),len(Verts)])

        a,b,c = Faces[i][1],Faces[i][2],Faces[i][3]
        d,e,f = Faces[i][4],Faces[i][5],Faces[i][6]

        PA = [Verts[a][1],Verts[a][2],Verts[a][3]]
        PB = [Verts[b][1],Verts[b][2],Verts[b][3]]
        PC = [Verts[c][1],Verts[c][2],Verts[c][3]]
            
        Edge1 = [ PC[0]-PA[0] , PC[1]-PA[1] , PC[2]-PA[2] ]
        Edge2 = [ PB[0]-PA[0] , PB[1]-PA[1] , PB[2]-PA[2] ]
        NVert = [ 0.000000001 , 0.000000001 , 0.000000001 ]

        Norm1 = [ Sf(Norms[d][1],10), Sf(Norms[d][2],10), Sf(Norms[d][3],10) ]
        Norm3 = [ Sf(Norms[e][1],10), Sf(Norms[e][2],10), Sf(Norms[e][3],10) ]
        Norm2 = [ Sf(Norms[f][1],10), Sf(Norms[f][2],10), Sf(Norms[f][3],10) ]
        
        if ( np.linalg.norm(np.cross( Edge1, Edge2 )) != 0 ):                                  
         NVert = np.cross( Edge1, Edge2 )/np.linalg.norm(np.cross( Edge1, Edge2 ))
        NVert = [ Sf(NVert[0],10), Sf(NVert[1],10), Sf(NVert[2],10) ]

        Normals += "			*MESH_FACENORMAL "+str(SS(i,No))+"               "+str(NVert[0])+"	"+str(NVert[1])+"	"+str(NVert[2]) +L
        Normals += "				*MESH_VERTEXNORMAL "+str(SS(a,No))+"     "+str(Norm1[0])+"	"+str(Norm1[1])+"	"+str(Norm1[2]) +L
        Normals += "				*MESH_VERTEXNORMAL "+str(SS(c,No))+"     "+str(Norm2[0])+"	"+str(Norm2[1])+"	"+str(Norm2[2]) +L
        Normals += "				*MESH_VERTEXNORMAL "+str(SS(b,No))+"     "+str(Norm3[0])+"	"+str(Norm3[1])+"	"+str(Norm3[2]) +L

    return Normals




def OtherData(Verts,Norms,Faces):

    NormsF = []

    Faceinfo = []

    N = 0

    for i in range ( 0 , len(Faces) ):

        PA = [Verts[Faces[i][1]][1],Verts[Faces[i][1]][2],Verts[Faces[i][1]][3]]
        PB = [Verts[Faces[i][2]][1],Verts[Faces[i][2]][2],Verts[Faces[i][2]][3]]
        PC = [Verts[Faces[i][3]][1],Verts[Faces[i][3]][2],Verts[Faces[i][3]][3]]
        Edge1 = [ PC[0]-PA[0] , PC[1]-PA[1] , PC[2]-PA[2] ]
        Edge2 = [ PB[0]-PA[0] , PB[1]-PA[1] , PB[2]-PA[2] ]
        NVert = [ 0.000000001 , 0.000000001 , 0.000000001 ]
        if ( np.linalg.norm(np.cross( Edge1, Edge2 )) != 0 ):                                  
         NVert = np.cross( Edge1, Edge2 )/np.linalg.norm(np.cross( Edge1, Edge2 ))
        NormsF.append([ (NVert[0]), (NVert[1]), (NVert[2]) ])

    for i in range ( 0 , len(Faces) ):

        N += 1
        Info = [ 1,1,1,N ]
        for j in range ( i-1, -1, -1  ):
            Fce1,Fce2 = [ Faces[i][1], Faces[i][3], Faces[i][2], -Faceinfo[j][3] ], [ Faces[j][1], Faces[j][3], Faces[j][2], -Faceinfo[j][3] ]
            AB,BA = ( Fce1[0] in Fce2 and Fce1[1] in Fce2 ),( Fce2[0] in Fce1 and Fce2[1] in Fce1 )
            BC,CB = ( Fce1[1] in Fce2 and Fce1[2] in Fce2 ),( Fce2[1] in Fce1 and Fce2[2] in Fce1 )
            AC,CA = ( Fce1[0] in Fce2 and Fce1[2] in Fce2 ),( Fce2[0] in Fce1 and Fce2[2] in Fce1 )
            
            if ( AB and BA and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[0],Faceinfo[j][0]=0,0
            if ( AB and CB and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[0],Faceinfo[j][1]=0,0
            if ( AB and CA and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[0],Faceinfo[j][2]=0,0
            if ( BC and BA and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[1],Faceinfo[j][0]=0,0
            if ( BC and CB and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[1],Faceinfo[j][1]=0,0
            if ( BC and CA and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[1],Faceinfo[j][2]=0,0
            if ( AC and BA and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[2],Faceinfo[j][0]=0,0
            if ( AC and CB and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[2],Faceinfo[j][1]=0,0
            if ( AC and CA and np.dot(NormsF[i],NormsF[j]) > 0.985 ):
                                                               Info[2],Faceinfo[j][2]=0,0
                                                               
        for j in range ( i-1, -1, -1  ):                                        
            Fce1,Fce2 = [ Faces[i][4], Faces[i][6], Faces[i][5], -Faceinfo[j][3] ],[ Faces[j][4], Faces[j][6], Faces[j][5], -Faceinfo[j][3] ]
            if ( (Fce1[0] in Fce2 and Fce1[1] in Fce2) or (Fce1[1] in Fce2 and Fce1[2] in Fce2) or (Fce1[0] in Fce2 and Fce1[2] in Fce2) ):
             Info[3],N = Faceinfo[j][3],N-1
             break
             
        Faceinfo.append(Info)

    return Faceinfo




# --------------------------------------------------------------------------------------\\\\\\\\\\\
# --------------------------------------------------------------------------------------\\\\\\\\\\\ BONE Funcs
# --------------------------------------------------------------------------------------\\\\\\\\\\\


def GetBoneObjectLength(Bones):

    Lengths = []

    for i in range ( 0 , len(Bones) ):

        Lengths.append(1.0) # Default Length

        for j in range ( i+1 , len(Bones) ):

            if ( Bones[i][0] == Bones[j][2] ):

                Lengths[-1] = ((Bones[j][3]**2)+(Bones[j][4]**2)+(Bones[j][5]**2))**(1/2)

                if Lengths[-1] < 0.1 :
                                       Lengths[-1] = 8.0

                for k in range ( j+1 , len(Bones) ):

                    if ( Bones[i][0] == Bones[k][2] ):

                        Lengths[-1] = 8.0

                        break
                break

    return Lengths


def GetBoneHierarchyData(Bones):

    BHierarchy = []

    Blength = GetBoneObjectLength(Bones)

    for i in range ( 0 , len(Bones) ):

        Bc = Bones[i][2]
        Px,Py,Pz = 0.0,0.0,0.0         
        while ( Bc != -1 ):
          Px += Bones[Bc][3]
          Py += Bones[Bc][4]
          Pz += Bones[Bc][5]
          Bc  = Bones[Bc][2]
        Px += Bones[i][3]
        Py += Bones[i][4]
        Pz += Bones[i][5]

        BHierarchy.append([ Px,Py,Pz ])

    BnesData = []

    BRotMatrix = GetBRMatrix(Bones)

    for i in range ( 0 , len(Bones) ):

        Ro = BRotMatrix[i] #Rotation Matrix for BoneLink

        Po = [ BHierarchy[i][0],BHierarchy[i][1],BHierarchy[i][2] ]

        BnesData.append([ Po, Ro, Blength[i]/24, Blength[i] ])

    return BnesData



def BoneVertCData(Bones,BonesH):

    Str = ""

    SZ = BonesH[2] # Size (Fixed/calculated)

    LG = BonesH[3]  # Length (Calculated One)
    
    Po = [ BonesH[0][0],BonesH[0][1],BonesH[0][2] ]

    Ro = GetVertsCorrection(SZ,LG,[BonesH[1][0],BonesH[1][1],BonesH[1][2]])

    Vts = [[ SZ, -SZ, +SZ ],[ SZ, +SZ, +SZ ],[ SZ, +SZ, -SZ ],[ SZ, -SZ, -SZ ],
           [ LG, -SZ, +SZ ],[ LG, +SZ, +SZ ],[ LG, +SZ, -SZ ],[ LG, -SZ, -SZ ] ]

    Vts.append([ 0.0, 0.0, 0.0 ])

    for i in range ( 0 , len(Vts) ):

        VtX = ((Vts[i][0]*Ro[0][0])+(Vts[i][1]*Ro[1][0])+(Vts[i][2]*Ro[2][0]))+Po[0]

        VtY = ((Vts[i][0]*Ro[0][1])+(Vts[i][1]*Ro[1][1])+(Vts[i][2]*Ro[2][1]))+Po[1]

        VtZ = ((Vts[i][0]*Ro[0][2])+(Vts[i][1]*Ro[1][2])+(Vts[i][2]*Ro[2][2]))+Po[2]
    
        Str += "\t\t\t\t\t\t*MESH_VERTEX    "+str(i)+"\t"+str(VtX)+" "+str(VtY)+" "+str(VtZ)+"\n"

    return Str



def BoneFaceFData(Bones,BonesH):

    Str = ""
    Str += "	    \t\t\t*MESH_FACE    0:    A:    4 B:    5 C:    7 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 1 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    1:    A:    6 B:    7 C:    5 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 1 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    2:    A:    1 B:    2 C:    5 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 2 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    3:    A:    6 B:    5 C:    2 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 2 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    4:    A:    0 B:    1 C:    4 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 3 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    5:    A:    5 B:    4 C:    1 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 3 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    6:    A:    7 B:    6 C:    3 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 4 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    7:    A:    2 B:    3 C:    6 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 4 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    8:    A:    4 B:    7 C:    0 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 5 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE    9:    A:    3 B:    0 C:    7 AB:    1 BC:    0 CA:    1	 *MESH_SMOOTHING 5 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE   10:    A:    8 B:    1 C:    0 AB:    1 BC:    1 CA:    1	 *MESH_SMOOTHING 6 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE   11:    A:    8 B:    2 C:    1 AB:    1 BC:    1 CA:    1	 *MESH_SMOOTHING 7 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE   12:    A:    8 B:    3 C:    2 AB:    1 BC:    1 CA:    1	 *MESH_SMOOTHING 8 	*MESH_MTLID 0"+"\n"
    Str += "	    \t\t\t*MESH_FACE   13:    A:    8 B:    0 C:    3 AB:    1 BC:    1 CA:    1	 *MESH_SMOOTHING 9 	*MESH_MTLID 0"+"\n"

    return Str



# ---------------------------


def GetVertsCorrection(SZ,LG,RTx):

    RTx = RTx/np.linalg.norm(RTx)

    if (abs(RTx[0])) > 1e-6:

     X = RTx[0]*(math.cos(math.radians(90)))-RTx[2]*(math.sin(math.radians(90)))

     Z = RTx[0]*(math.sin(math.radians(90)))+RTx[2]*(math.cos(math.radians(90)))

     RTy,RTz = [ X,RTx[1],Z ],np.cross([ X,RTx[1],Z ],RTx)

    elif abs(RTx[1]) > 1e-6:

     X = RTx[0]*(math.cos(math.radians(90)))-RTx[1]*(math.sin(math.radians(90)))

     Y = RTx[0]*(math.sin(math.radians(90)))+RTx[1]*(math.cos(math.radians(90)))

     RTz,RTy = [ X,Y,RTx[2] ],np.cross(RTx,[ X,Y,RTx[2] ])

    elif abs(RTx[2]) > 1e-6:

     X = RTx[0]*(math.cos(math.radians(90)))-RTx[2]*(math.sin(math.radians(90)))

     Z = RTx[0]*(math.sin(math.radians(90)))+RTx[2]*(math.cos(math.radians(90)))

     RTy,RTz = [ X,RTx[1],Z ],np.cross([ X,RTx[1],Z ],RTx)

    else:
     E=input("ERROR")

    return RTx,RTy,RTz




def GetBRMatrix(Bones):

    Ro = []

    for i in range ( 0 , len(Bones) ):

        Ro.append([ 0.0,0.0,1.0 ])

        if len(Ro) > 2:
                               Ro[-1]=Ro[Bones[i][2]]
        if Bones[i][2] == -1:
                               continue 

        for j in range ( i+1 , len(Bones) ):

            if ( Bones[i][0] == Bones[j][2] ):

                V = [ Bones[j][3] , Bones[j][4] , Bones[j][5] ]

                if np.linalg.norm(V) != 0:
                                           Ro[-1] = V

                for k in range ( j+1 , len(Bones) ):

                    if ( Bones[i][0] == Bones[k][2] ):

                        Ro[-1] = Ro[Bones[i][2]]

                        break
                
                break

    return Ro
