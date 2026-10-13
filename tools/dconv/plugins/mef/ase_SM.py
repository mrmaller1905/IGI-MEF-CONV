import os
import math
from utils import fs
import numpy as np
from math import *
from .import ase_CS
from .import reader_MEFG
from .reader_MEFG import *

def fromfile(meffilename,Data,Arg0):
    
    meftext = ""

    L = ""+"\n"
    
    Sz = CalC_Size(Data[4])*2

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
    
    Mvt = Conv_Mverts(Data[8],Data[4])
    Gls = Conv_Glows (Data[9],Data[4])
    
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
        
#--------------------- 3. OBJECT INFO -----------<


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

#--------------------- 4. MAGIC/GLOW SP. -----------<

    mvert = ""

    for i in range ( 0 , len(Mvt) ):

      mvert += "*GEOMOBJECT {" +L
      mvert += "	*NODE_NAME \""+str(Mvt[i][0])+"\"" +L
      mvert += "	*NODE_PARENT \""+str(ModelName)+"\""+L
      mvert += "	*NODE_TM {" +L
      mvert += "		*NODE_NAME \""+str(Mvt[i][0])+"\"" +L
      mvert += "		*INHERIT_POS 0 0 0" +L
      mvert += "		*INHERIT_ROT 0 0 0" +L
      mvert += "		*TM_ROW0 "+str(Mvt[i][11])+" 0.0000000000 0.0000000000" +L
      mvert += "		*TM_ROW1 0.0000000000 "+str(Mvt[i][11])+" 0.0000000000" +L
      mvert += "		*TM_ROW2 0.0000000000 0.0000000000 "+str(Mvt[i][11])+"" +L
      mvert += "		*TM_ROW3 "+str(Mvt[i][1])+" "+str(Mvt[i][2])+" "+str(Mvt[i][3]) +L
      mvert += "		*TM_POS  "+str(Mvt[i][1])+" "+str(Mvt[i][2])+" "+str(Mvt[i][3]) +L
      mvert += "	}" +L
      mvert += "	*MESH {" +L
      mvert += "		*MESH_NUMVERTEX "+str(Mvt[i][4]) +L
      mvert += "		*MESH_NUMFACES "+str(Mvt[i][5]) +L
      mvert += "		*MESH_VERTEX_LIST {" +L
      mvert += "" + str(Mvt[i][6])
      mvert += "		}" +L
      mvert += "		*MESH_FACE_LIST {" +L
      mvert += "" + str(Mvt[i][7])
      mvert += "		}" +L
      mvert += "	}" +L
      mvert += "	*WIREFRAME_COLOR "+str(Mvt[i][8])+" "+str(Mvt[i][9])+" "+str(Mvt[i][10])+"" +L
      mvert += "}" +L

    glows = ""

    for i in range ( 0 , len(Gls) ):

      glows += "*GEOMOBJECT {" +L
      glows += "	*NODE_NAME \""+str(Gls[i][0])+"\"" +L
      glows += "	*NODE_PARENT \""+str(ModelName)+"\""+L
      glows += "	*NODE_TM {" +L
      glows += "		*NODE_NAME \""+str(Gls[i][0])+"\"" +L
      glows += "		*INHERIT_POS 0 0 0" +L
      glows += "		*INHERIT_ROT 0 0 0" +L
      glows += "		*TM_ROW0 "+str(Gls[i][11])+" 0.0000000000 0.0000000000" +L
      glows += "		*TM_ROW1 0.0000000000 "+str(Gls[i][11])+" 0.0000000000" +L
      glows += "		*TM_ROW2 0.0000000000 0.0000000000 "+str(Gls[i][11])+"" +L
      glows += "		*TM_ROW3 "+str(Gls[i][1])+" "+str(Gls[i][2])+" "+str(Gls[i][3]) +L
      glows += "		*TM_POS  "+str(Gls[i][1])+" "+str(Gls[i][2])+" "+str(Gls[i][3]) +L
      glows += "	}" +L
      glows += "	*MESH {" +L
      glows += "		*MESH_NUMVERTEX "+str(Gls[i][4]) +L
      glows += "		*MESH_NUMFACES "+str(Gls[i][5]) +L
      glows += "		*MESH_VERTEX_LIST {" +L
      glows += "" + str(Gls[i][6])
      glows += "		}" +L
      glows += "		*MESH_FACE_LIST {" +L
      glows += "" + str(Gls[i][7])
      glows += "		}" +L
      glows += "	}" +L
      glows += "	*WIREFRAME_COLOR "+str(Gls[i][8])+" "+str(Gls[i][9])+" "+str(Gls[i][10])+"" +L
      glows += "}" +L

#--------------------- 5. ATTACHMENT INFO -----------<

    attas = ""

    for i in range ( 0 , len(Data[10]) ):

        FILE = Arg0+"\\"+str(Data[10][i][0])[1:-1]+".MEF"
            
        Po = [ Data[10][i][11], Data[10][i][12], Data[10][i][13] ]

        Rx = [ Data[10][i][2], Data[10][i][3], Data[10][i][4] ]

        Ry = [ Data[10][i][5], Data[10][i][6], Data[10][i][7] ]

        Rz = [ Data[10][i][8], Data[10][i][9], Data[10][i][10] ]

        Mats += ExtractMaterials(FILE,i,(os.path.exists(FILE)))

        Ro = [ Rx, Ry, Rz ]

        if (os.path.exists(FILE)) == True :

         attas += ase_CS.fromtree(FILE,i,Po,Ro,[])

        else:

         attas += CreateDummyObject(i,FILE,ModelName,Po,Ro,Sz)

         E=input("\n-ERROR- Attachment Model Not Found in directory ??")
         
    Mats += "}"+L

#---------------------

    if ( True ):

     meftext += "*3DSMAX_ASCIIEXPORT	200"+"\n"
    
     meftext += "*COMMENT \"AsciiExport Version  2.00 - dd mm yy dd\""+"\n"
    
     meftext += str(Info)

     meftext += str(Mats)

     meftext += str(obj)

     meftext += str(attas)

     meftext += str(mvert)

     meftext += str(glows)

     meftext += str()

#---   

    return meftext



# ----------------------------------------------------------------------------------------------------------------------------------------
# ------------- OTHER FUNCTIONS ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------


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

    if N == 1:
                N += 1
    R=str(Num)

    assert len(R) <= N , "Digits must be less than the required"

    while len(R) < N :

        R = "0"+str(R)

    return R


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

            Faces.append([ i , Fces[i][1] , Fces[i][3] , Fces[i][2] , Fcs[i][0], Fcs[i][1], Fcs[i][2], Fcs[i][3], Fces[i][7] ])

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


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------//////////////////////////////-------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
                 Mats[i][2],Mats[i][3],Mats[i][4] = 0.2550, 0.4990, 0.7550
                 Mats[i][5],Mats[i][6],Mats[i][7] = 0.2550, 0.4990, 0.7550

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


def ExtractMaterials(FILE,I,Type):

    Mats = ""

    L = ""+"\n"

    if ( Type == False ):

        NAME = str(os.path.splitext(os.path.basename(FILE))[0])
        
        Mats += "	*MATERIAL "+str(I+1)+" {"+L
        Mats += "		*MATERIAL_NAME \"attach"+str(SI(I,2))+"_"+str(NAME)+"\""+L
        Mats += "		*MATERIAL_CLASS \"Standard\""+L
        Mats += "		*MATERIAL_AMBIENT  0.5882353187	0.5882353187	0.5882353187"+L
        Mats += "		*MATERIAL_DIFFUSE  0.5882353187	0.5882353187	0.5882353187"+L
        Mats += "		*MATERIAL_SPECULAR 0.899999976	0.8999999762	0.8999999762"+L
        Mats += "		*MATERIAL_SHINE 0.1000000000"+L
        Mats += "		*MATERIAL_SHINESTRENGTH 0.0000000000"+L
        Mats += "		*MATERIAL_TRANSPARENCY 0.0000000000"+L
        Mats += "		*MATERIAL_WIRESIZE 1.0000000000"+L
        Mats += "		*MATERIAL_SELFILLUM 0.0000000000"+L
        Mats += "	}"+L

    else:

        Data = reader_MEFG.read(FILE)

        N_Mats,N_tex = len(Data[2]),len(Data[3])

        MATS,Mts = "",Conv_Mats(Data[2],Data[3])

        NAME = str(os.path.splitext(os.path.basename(FILE))[0])

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
    
        Mats += "	*MATERIAL "+str(I+1)+" {"+L
        Mats += "		*MATERIAL_NAME \"attach"+str(SI(I,2))+"_"+str(NAME)+"\""+L
        Mats += "		*MATERIAL_CLASS \"Multi/Sub-Object\""+L
        Mats += "		*NUMSUBMTLS "+str(N_Mats)+L
        Mats += ""  +  (MATS)
        Mats += "   	}"+L

    return Mats


def GetNormalsofMesh(Verts,Norms,Faces):

    Normals,L = "","\n"

    for i in range ( 0 , len(Faces) ):

        No = max([len(Faces),len(Verts)])

        a,b,c = Faces[i][1],Faces[i][2],Faces[i][3]
        d,e,f = Faces[i][4],Faces[i][5],Faces[i][6]

        PA = [Verts[a][1],Verts[a][2],Verts[a][3]]
        PC = [Verts[c][1],Verts[c][2],Verts[c][3]]
        PB = [Verts[b][1],Verts[b][2],Verts[b][3]]
            
        Edge1 = [ PC[0]-PA[0] , PC[1]-PA[1] , PC[2]-PA[2] ]
        Edge2 = [ PB[0]-PA[0] , PB[1]-PA[1] , PB[2]-PA[2] ]
        NVert = [ 0.000000001 , 0.000000001 , 0.000000001 ]

        Norm1 = [ Sf(Norms[d][1],10), Sf(Norms[d][2],10), Sf(Norms[d][3],10) ]
        Norm2 = [ Sf(Norms[f][1],10), Sf(Norms[f][2],10), Sf(Norms[f][3],10) ]
        Norm3 = [ Sf(Norms[e][1],10), Sf(Norms[e][2],10), Sf(Norms[e][3],10) ]
        
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


def CreateDummyObject(Aid,File,MainModel,Po,Ro,Sz): 
    
    obj = ""

    L = ""+"\n"

    Px,Py,Pz = Po[0],Po[1],Po[2]

    Model = str(os.path.splitext(os.path.basename(File))[0])

    ModelName = "attach"+SI(Aid,2)+"_"+Model #attach00_515_01_1

    Ats = [ Sf(Ro[0][0],10), Sf(Ro[0][1],10), Sf(Ro[0][2],10),
            Sf(Ro[1][0],10), Sf(Ro[1][1],10), Sf(Ro[1][2],10),
            Sf(Ro[2][0],10), Sf(Ro[2][1],10), Sf(Ro[2][2],10),
            Sf(Po[0],10),    Sf(Po[1],10),    Sf(Po[2],10) ]
    
    obj += "*HELPEROBJECT {"+L
    obj += "	*NODE_NAME \""+str(ModelName)+"\""+L
    obj += "	*NODE_PARENT \""+str(MainModel)+"\""+L
    obj += "	*NODE_TM {"+L
    obj += "	*NODE_NAME \""+str(ModelName)+"\""+L
    obj += "	*TM_ROW0 " +Ats[0]+ "	" +Ats[1]+ "	" +Ats[2]+ ""+L
    obj += "	*TM_ROW1 " +Ats[3]+ "	" +Ats[4]+ "	" +Ats[5]+ ""+L
    obj += "	*TM_ROW2 " +Ats[6]+ "	" +Ats[7]+ "	" +Ats[8]+ ""+L
    obj += "	*TM_ROW3 " +Ats[9]+ "	" +Ats[10]+"	" +Ats[11]+""+L
    obj += "	}"+L
    obj += "	*BOUNDINGBOX_MIN "+str(Px-Sz)+" "+str(Py-Sz)+" "+str(Pz-Sz) +L
    obj += "	*BOUNDINGBOX_MAX "+str(Px+Sz)+" "+str(Py+Sz)+" "+str(Pz+Sz) +L
    obj += "}"+L

    return obj

    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------//////////////////////////////-------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def Dist(A,B):

    Dx,Dy,Dz = (A[0]-B[0])**2,(A[1]-B[1])**2,(A[2]-B[2])**2

    Dt = (Dx+Dy+Dz)**(0.5)

    return Dt


def CalC_Size(Verts):

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

    LENGTH = 0.025 * LENGTH

    return LENGTH

    
def Conv_Mverts(Items,Verts):

    Mvt = []

    N = len(str(len(Items)))

    SIZE = CalC_Size(Verts)
    
    for i in range ( 0 , len(Items) ):

        X = ""
        
        if (Items[i][5]) == 0:
                              X = "A"
        if (Items[i][5]) == 1:
                              X = "B"

        Vrts = FData01([ Items[i][2], Items[i][3], Items[i][4], SIZE ])

        Fces = FData02([ Items[i][2], Items[i][3], Items[i][4], SIZE ])
                                
        Mvt.append([ "magic"+SI(i,N)+str(X), Sf(Items[i][2],10), Sf(Items[i][3],10), Sf(Items[i][4],10), 62, 120,
                     Vrts, Fces, Sf(0.99000000,10), Sf(0.01000000,10), Sf(0.01000000,10), Sf(SIZE/100,10) ])
    return Mvt

    
def Conv_Glows(Items,Verts):

    Gls = []

    N = len(str(len(Items)))
    
    for i in range ( 0 , len(Items) ):

        Vrts = FData01(Items[i])

        Fces = FData02(Items[i])

        Gls.append([ "glow"+SI(i,N), Sf(Items[i][0],10), Sf(Items[i][1],10), Sf(Items[i][2],10), 62, 120,
                     Vrts, Fces, Sf(Items[i][4],10), Sf(Items[i][5],10), Sf(Items[i][6],10), Sf(Items[i][3]/100,10)  ])
    return Gls


def FData01(Item):
    
    Str,N,L,S = "",0,"\n",Item[3]

    if True:

        Str += "			*MESH_VERTEX    "+str(0)+"	"+str(Item[0])+"  "+str(Item[1])+"  "+str(Item[2]+S)+"" +L
        Oa = 90
        while ( Oa != -90+30 ):
          Oa -= 30
          Ob = 0
          Oc = 360
            
          while ( Ob != 360 and Oc != 0 ):
            Pox = math.sin(math.radians(Oc)) * math.cos(math.radians(Oa))*S
            Poy = math.cos(math.radians(Ob)) * math.cos(math.radians(Oa))*S
            Poz = math.sin(math.radians(Oa)) * math.sin(math.radians(90))*S
            Ob,Oc = Ob+30,Oc-30
            N += 1
            Str += "			*MESH_VERTEX    "+str(N)+"	"+str(Item[0]+Pox)+"  "+str(Item[1]+Poy)+"  "+str(Item[2]+Poz)+"" +L
        Str += "			*MESH_VERTEX    "+str(61)+"	"+str(Item[0])+"  "+str(Item[1])+"  "+str(Item[2]-S)+"" +L
        

    return Str


def FData02(Item):

    Str = ""
    Str += "			*MESH_FACE    0:    A:    0 B:    1 C:    2 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    1:    A:    0 B:    2 C:    3 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    2:    A:    0 B:    3 C:    4 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    3:    A:    0 B:    4 C:    5 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    4:    A:    0 B:    5 C:    6 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    5:    A:    0 B:    6 C:    7 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    6:    A:    0 B:    7 C:    8 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    7:    A:    0 B:    8 C:    9 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    8:    A:    0 B:    9 C:   10 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE    9:    A:    0 B:   10 C:   11 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   10:    A:    0 B:   11 C:   12 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   11:    A:    0 B:   12 C:    1 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   12:    A:    1 B:   13 C:   14 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   13:    A:    1 B:   14 C:    2 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   14:    A:    2 B:   14 C:   15 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   15:    A:    2 B:   15 C:    3 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   16:    A:    3 B:   15 C:   16 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   17:    A:    3 B:   16 C:    4 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   18:    A:    4 B:   16 C:   17 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   19:    A:    4 B:   17 C:    5 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   20:    A:    5 B:   17 C:   18 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   21:    A:    5 B:   18 C:    6 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   22:    A:    6 B:   18 C:   19 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   23:    A:    6 B:   19 C:    7 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   24:    A:    7 B:   19 C:   20 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   25:    A:    7 B:   20 C:    8 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   26:    A:    8 B:   20 C:   21 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   27:    A:    8 B:   21 C:    9 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   28:    A:    9 B:   21 C:   22 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   29:    A:    9 B:   22 C:   10 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   30:    A:   10 B:   22 C:   23 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   31:    A:   10 B:   23 C:   11 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   32:    A:   11 B:   23 C:   24 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   33:    A:   11 B:   24 C:   12 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   34:    A:   12 B:   24 C:   13 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   35:    A:   12 B:   13 C:    1 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   36:    A:   13 B:   25 C:   26 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   37:    A:   13 B:   26 C:   14 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   38:    A:   14 B:   26 C:   27 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   39:    A:   14 B:   27 C:   15 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   40:    A:   15 B:   27 C:   28 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   41:    A:   15 B:   28 C:   16 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   42:    A:   16 B:   28 C:   29 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   43:    A:   16 B:   29 C:   17 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   44:    A:   17 B:   29 C:   30 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   45:    A:   17 B:   30 C:   18 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   46:    A:   18 B:   30 C:   31 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   47:    A:   18 B:   31 C:   19 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   48:    A:   19 B:   31 C:   32 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   49:    A:   19 B:   32 C:   20 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   50:    A:   20 B:   32 C:   33 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   51:    A:   20 B:   33 C:   21 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   52:    A:   21 B:   33 C:   34 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   53:    A:   21 B:   34 C:   22 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   54:    A:   22 B:   34 C:   35 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   55:    A:   22 B:   35 C:   23 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   56:    A:   23 B:   35 C:   36 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   57:    A:   23 B:   36 C:   24 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   58:    A:   24 B:   36 C:   25 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   59:    A:   24 B:   25 C:   13 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   60:    A:   25 B:   37 C:   38 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   61:    A:   25 B:   38 C:   26 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   62:    A:   26 B:   38 C:   39 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   63:    A:   26 B:   39 C:   27 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   64:    A:   27 B:   39 C:   40 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   65:    A:   27 B:   40 C:   28 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   66:    A:   28 B:   40 C:   41 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   67:    A:   28 B:   41 C:   29 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   68:    A:   29 B:   41 C:   42 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   69:    A:   29 B:   42 C:   30 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   70:    A:   30 B:   42 C:   43 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   71:    A:   30 B:   43 C:   31 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   72:    A:   31 B:   43 C:   44 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   73:    A:   31 B:   44 C:   32 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   74:    A:   32 B:   44 C:   45 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   75:    A:   32 B:   45 C:   33 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   76:    A:   33 B:   45 C:   46 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   77:    A:   33 B:   46 C:   34 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   78:    A:   34 B:   46 C:   47 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   79:    A:   34 B:   47 C:   35 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   80:    A:   35 B:   47 C:   48 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   81:    A:   35 B:   48 C:   36 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   82:    A:   36 B:   48 C:   37 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   83:    A:   36 B:   37 C:   25 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   84:    A:   37 B:   49 C:   50 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   85:    A:   37 B:   50 C:   38 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   86:    A:   38 B:   50 C:   51 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   87:    A:   38 B:   51 C:   39 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   88:    A:   39 B:   51 C:   52 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   89:    A:   39 B:   52 C:   40 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   90:    A:   40 B:   52 C:   53 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   91:    A:   40 B:   53 C:   41 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   92:    A:   41 B:   53 C:   54 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   93:    A:   41 B:   54 C:   42 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   94:    A:   42 B:   54 C:   55 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   95:    A:   42 B:   55 C:   43 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   96:    A:   43 B:   55 C:   56 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   97:    A:   43 B:   56 C:   44 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   98:    A:   44 B:   56 C:   57 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE   99:    A:   44 B:   57 C:   45 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  100:    A:   45 B:   57 C:   58 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  101:    A:   45 B:   58 C:   46 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  102:    A:   46 B:   58 C:   59 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  103:    A:   46 B:   59 C:   47 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  104:    A:   47 B:   59 C:   60 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  105:    A:   47 B:   60 C:   48 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  106:    A:   48 B:   60 C:   49 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  107:    A:   48 B:   49 C:   37 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  108:    A:   61 B:   50 C:   49 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  109:    A:   61 B:   51 C:   50 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  110:    A:   61 B:   52 C:   51 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  111:    A:   61 B:   53 C:   52 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  112:    A:   61 B:   54 C:   53 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  113:    A:   61 B:   55 C:   54 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  114:    A:   61 B:   56 C:   55 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  115:    A:   61 B:   57 C:   56 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  116:    A:   61 B:   58 C:   57 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  117:    A:   61 B:   59 C:   58 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  118:    A:   61 B:   60 C:   59 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"
    Str += "			*MESH_FACE  119:    A:   61 B:   49 C:   60 AB:    0 BC:    0 CA:    0	 *MESH_SMOOTHING 1 	*MESH_MTLID 1" +"\n"

    return Str
