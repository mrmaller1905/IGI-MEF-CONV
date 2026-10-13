import os
from utils import fs
import numpy as np
import math
from math import *
from .import ase_CS

def fromfile(meffilename,Data,Mod,Aid,Po,Ro):
    
    meftext = ""

    L = ""+"\n"

    O = OtherData(Data[4],Data[5],Data[6])

    MainModel = str(os.path.splitext(os.path.basename(Mod))[0])     

    OrginalModel = str(os.path.splitext(os.path.basename(meffilename))[0])        

    ModelName = "attach" + SI(Aid,2) + "_" + OrginalModel #attach00_515_01_1
    
#--------------------- MESH INFO -----------<


    MESH = ""

    Data[4] = TransformedVerts(Data[4],Po,Ro)
    
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

#-------
    
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
    MESH += "	}"+L
        
#--------------------- 3. OBJECT INFO -----------<


    obj = ""

    Ats = [  Sf(Ro[0][0],10), Sf(Ro[0][1],10), Sf(Ro[0][2],10),
             Sf(Ro[1][0],10), Sf(Ro[1][1],10), Sf(Ro[1][2],10),
             Sf(Ro[2][0],10), Sf(Ro[2][1],10), Sf(Ro[2][2],10),
             Sf(Po[0],10),    Sf(Po[1],10),    Sf(Po[2],10)  ]
    
    obj += "*GEOMOBJECT {"+L
    obj += "	*NODE_NAME \""+str(ModelName)+"\""+L
    obj += "	*NODE_PARENT \""+str(MainModel)+"\""+L
    obj += "	*NODE_TM {"+L
    obj += "		*NODE_NAME \""+str(ModelName)+"\""+L
    obj += "		*INHERIT_POS "+str(0)+" "+str(0)+" "+str(0)+L
    obj += "		*INHERIT_ROT "+str(0)+" "+str(0)+" "+str(0)+L
    obj += "		*TM_ROW0 " +Ats[0]+ "	" +Ats[1]+ "	" +Ats[2]+ ""+L
    obj += "		*TM_ROW1 " +Ats[3]+ "	" +Ats[4]+ "	" +Ats[5]+ ""+L
    obj += "		*TM_ROW2 " +Ats[6]+ "	" +Ats[7]+ "	" +Ats[8]+ ""+L
    obj += "		*TM_ROW3 " +Ats[9]+ "	" +Ats[10]+"	" +Ats[11]+""+L
    obj += "		*TM_POS  " +Ats[9]+ "	" +Ats[10]+"	" +Ats[11]+""+L
    obj += "	}"+L
    obj += "" + MESH
    obj += "	*PROP_CASTSHADOW 1"+L
    obj += "	*PROP_RECVSHADOW 1"+L
    obj += "	*MATERIAL_REF "+str(Aid+1)+L
    obj += "}"+L

#---------------------

#---   

    return obj



# ---------------------------------------------------->
# ------------- A. MESH = COLLISION MESH ------------->
# ---------------------------------------------------->




def frommesh(meffilename,Data,Mod,Aid,Po,Ro):
    
    meftext = ""

    L = ""+"\n"

    O = OtherData(Data[4],Data[5],Data[6])

    MainModel = str(os.path.splitext(os.path.basename(meffilename))[0])
    
#--------------------- COLLISION MESH DATA -----------<

    OBJ = ""

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

#-------
    
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
    MESH += "	}"+L
    
    OBJ += "*GEOMOBJECT {"+L
    OBJ += "	*NODE_NAME \"ColMesh01\""+L
    OBJ += "	*NODE_PARENT \""+str(MainModel)+"\""+L
    OBJ += "	*NODE_TM {"+L
    OBJ += "		*NODE_NAME \"ColMesh01\""+L
    OBJ += "		*INHERIT_POS 0 0 0"+L
    OBJ += "		*INHERIT_ROT 0 0 0"+L
    OBJ += "		*TM_ROW0 1.0000000000	0.0000000000	0.0000000000"+L
    OBJ += "		*TM_ROW1 0.0000000000	1.0000000000	0.0000000000"+L
    OBJ += "		*TM_ROW2 0.0000000000	0.0000000000	1.0000000000"+L
    OBJ += "		*TM_ROW3 0.0000000000	0.0000000000	0.0000000000"+L
    OBJ += "		*TM_POS 0.0000000000	0.0000000000	0.0000000000"+L
    OBJ += "	}"+L
    OBJ += "" + MESH
    OBJ += "	*PROP_CASTSHADOW 1"+L
    OBJ += "	*PROP_RECVSHADOW 1"+L
    OBJ += "	*MATERIAL_REF 0"+L
    OBJ += "}"+L

#---------------------
 

    return OBJ



# ----------------------------------------------------
# ------------- OTHER FUNCTIONS ----------------------
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

        R = "0"+str(Num)

    return R


def Conv_Verts(Verts):

    if True:

        assert len(Verts)-1 == Verts[-1][0]

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

            Vrts.append([ 3*i+0 , Verts[i][3] , Verts[i][4] , "0.00000000" ])
            Vrts.append([ 3*i+1 , Verts[i][5] , Verts[i][6] , "0.00000000" ])
            Vrts.append([ 3*i+2 , Verts[i][1] , Verts[i][2] , "0.00000000" ])

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

        Vrts = []

        for i in range ( 0 , len(Verts) ):

            Vrts.append([ 3*i+0 , Verts[i][1] , Verts[i][2]  ])
            Vrts.append([ 3*i+1 , Verts[i][3] , Verts[i][4]  ])
            Vrts.append([ 3*i+2 , Verts[i][5] , Verts[i][6]  ])

        Vts = []
        Vin = []
        for i in range ( 0 , len(Vrts) ):
            E = 0
            for j in range ( 0 , len(Vts) ):
                if Vrts[i][1] == Vts[j][1] and Vrts[i][2] == Vts[j][2] :
                 E = 1
                 Vin.append(j)
                 break
            if E == 0:
                Vin.append(len(Vts))
                Vts.append([ len(Vts) , Vrts[i][1] , Vrts[i][2] , "0.00000000" ])

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


# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------



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


# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------

def Sf(Num,n):

    Num = str(float(Num))

    N = Num.find('.')+11
    
    if len(str(Num)) < N :
        
      while ( len(str(Num)) != N ):

        Num += "0"
    
    elif len(str(Num)) > N :

       Num = float(Num)

       Num = str(round(Num,10))
        
    return Num

def TransformedVerts(Verts,Po,Ro):

    Vts = []

    for i in range ( 0 , len(Verts) ):

        VtX = ((Verts[i][1]*Ro[0][0])+(Verts[i][2]*Ro[1][0])+(Verts[i][3]*Ro[2][0]))+Po[0]

        VtY = ((Verts[i][1]*Ro[0][1])+(Verts[i][2]*Ro[1][1])+(Verts[i][3]*Ro[2][1]))+Po[1]

        VtZ = ((Verts[i][1]*Ro[0][2])+(Verts[i][2]*Ro[1][2])+(Verts[i][3]*Ro[2][2]))+Po[2]

        Vts.append([ Verts[i][0] , VtX , VtY , VtZ ])
        

    return Vts


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

