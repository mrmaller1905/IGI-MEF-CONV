import os
import math
import struct
import numpy as np
from math import *


# --------------------------------------------------------------------------------------------------------------------------------- RENDER MESH FUNCTIONS



def CalC_Offset_1(dner,ecaf):

        Off = []

        if ( len(dner) > 0 ):

          n = 0

          Off.append(n)

          for R in range ( 0 , len(dner)-1 ):

            n += dner['num_face'][R]//3

            Off.append(n)

        return Off
    


def CalC_nfaces_1(dner,ecaf):

        Fce = []

        if ( len(dner) > 0 ):

          for R in range ( 0 , len(dner) ):

            Fce.append(dner['num_face'][R]//3)

        return Fce

    

def CalC_Index(dner):

        Ns = []

        Off = 0

        for R in range ( 0 , len(dner) ):

            for i in range ( Off , Off + (dner['num_face'][R]//3) ):

               Ns.append(R)

               Off += 1

        return Ns

    

def CalC_Index02(dner):

        Ns = []

        for R in range ( 0 , len(dner) ):

            x = dner['off_verts'][R]

            y = dner['num_verts'][R]

            for i in range ( x , x + y ):

               Ns.append(R)

        return Ns

    

def IndexCorrection_ecaf1(dner,ecaf):

        Faces = b''

        Off = 0

        for R in range ( 0 , len(dner) ):

            OFF = dner['off_verts'][R]

            for i in range ( Off , Off + (dner['num_face'][R]//3) ):

               Faces += struct.pack('=3H' ,ecaf['a'][i]+OFF,ecaf['b'][i]+OFF,ecaf['c'][i]+OFF)

               Off += 1

        return Faces

    

def PostCorrection_xtrv1(d3dr,xtrv,BoneH):

        Verts = b''

        Off = 0

        for i in range ( 0 , d3dr['verts_1'][0] ):

            B = xtrv['bn'][i]

            Off = [BoneH[0][B],BoneH[1][B],BoneH[2][B]]

            Px,Nx = xtrv['px'][i]+Off[0],xtrv['nx'][i]

            Py,Ny = xtrv['py'][i]+Off[1],xtrv['ny'][i]

            Pz,Nz = xtrv['pz'][i]+Off[2],xtrv['nz'][i]

            Utc,Vtc = xtrv['u'][i],xtrv['v'][i]

            Verts += struct.pack('=8f' , Px, Py, Pz, Nx, Ny, Nz, Utc, Vtc)
            
        return Verts


# --------------------------------------------------------------------------------------------------------------------------------- MATERIAL PROPERTIES FUNCTIONS


def GetIndex(Vt,Vts,Vtn):

        for i in range ( 0 , len(Vts) ):

           if ( Vts[i] == Vt ):

              Vtn.append(i)

        return Vtn


def Check_RenderMesh(dner):

        Index = 0
        
        for R in range ( 0 , len(dner) ):

            if ( dner['_td'][R] < Index ):
                                           Index += 0
            elif dner['_td'][R] == Index :
                                           Index += 1
            elif  dner['_td'][R] > Index :
                                           return 1 # CORRECTION NEEDED
        return 0



def CalC_digits(N):

        Num = 0
        if ( N == 0 ):
            Num += 1
        while ( N > 0 ): 
            Num += 1   
            N //= 10    
        return Num



def CalC_Zeros(N,n):

        if ( CalC_digits(N) <= n ):
            Num = str(N)
            for i in range ( 0 , n-CalC_digits(N) ):
              Num = str(0)+str(Num)
            return Num
        else:
            assert False , "Digits are Exceeding their limit"
    


def CalC_float8(N):

        if ( N > 0 and N < 255 ):
                        V = round((((N)+1)/256),2)
        elif ( N == 255 ):
                        V = 1                
        elif ( N == 0 ):
                        V = 0
        else:
            assert False , "Number must be ( 0 <= N <= 255 ) "
            
        return V


def GetMaterial(Mi,Tex,Opd,Type):

        Name = "Material-Undefined"

        Nm = NameOfModel

        if ( Type == 0 ):

                if  (  Mi == -1 and Tex == -1 and Opd == 1.0 ):
                                                                Name = "Transparent"
                elif ( Mi == -1 and Tex == -1 and Opd != 1.0 ):
                                                                Name = "Material_Undefined"
                elif ( Mi == -1 and Tex != -1 and Opd == 1.0 ):
                                                                Name = "Material -Hidden"
                elif ( Mi == -1 and Tex != -1 and Opd != 1.0 ):
                                                                Name = "Material -Default"
                elif ( Mi != -1 and Tex == -1 and Opd == 1.0 ):
                                                                Name = "Hidden_m"+str(CalC_Zeros(Mi,2))
                elif ( Mi != -1 and Tex == -1 and Opd != 1.0 ):
                                                                Name = "Material_m"+str(CalC_Zeros(Mi,2))
                elif ( Mi != -1 and Tex != -1 and Opd == 1.0 ):
                                                                Name = "Hidden_m"+str(CalC_Zeros(Mi,2))
                elif ( Mi != -1 and Tex != -1 and Opd != 1.0 ):
                                                                Name = str(Nm)+"_m"+str(CalC_Zeros(Mi,2))
                else:
                                                                Name = input("Exception of Mat-Definition")
        if ( Type == 1 ):

                if  (  Mi == -1 and Tex == -1 and Opd == 1.0 ):
                                                                Name = "collision01 -Default"
                elif ( Mi == -1 and Tex == -1 and Opd != 1.0 ):
                                                                Name = "collision01_Undefined"
                elif ( Mi == -1 and Tex != -1 and Opd == 1.0 ):
                                                                Name = "collision01 -Undefined"
                elif ( Mi == -1 and Tex != -1 and Opd != 1.0 ):
                                                                Name = "collision01_Default" 
                elif ( Mi != -1 and Tex == -1 and Opd == 1.0 ):
                                                                Name = "collision01_m"+str(CalC_Zeros(Mi,2))
                elif ( Mi != -1 and Tex == -1 and Opd != 1.0 ):
                                                                Name = "collision01"+"_m"+str(CalC_Zeros(Mi,2))
                elif ( Mi != -1 and Tex != -1 and Opd == 1.0 ):
                                                                Name = "collision01_m"+str(CalC_Zeros(Mi,2))
                elif ( Mi != -1 and Tex != -1 and Opd != 1.0 ):
                                                                Name = "collision01"+"_m"+str(CalC_Zeros(Mi,2))
                else:
                                                                Name = input("Exception of Mat-Definition")     
        return Name


# --------------------------------------------------------------------------------------------------------------------------------- BONE FUNCTIONS


def GetBoneVerts(d3dr,xtrv):
        
        Vrts = []

        for i in range ( 0 , d3dr['verts_1'][0] ):

            Vt = [ xtrv['px'][i] , xtrv['py'][i] , xtrv['pz'][i] , xtrv['bn'][i] ]

            if Vt not in Vrts:

                Vrts.append(Vt)

        return Vrts


def GetBoneVerts02(tamc,xtvc):
        
        Vrts = []

        for i in range ( 0 , len(xtvc) ):

            Vt = [ xtvc['px'][i] , xtvc['py'][i] , xtvc['pz'][i] , xtvc['bn'][i] ]

            if Vt not in Vrts:

                Vrts.append(Vt)

        return Vrts


    
def CalC_BoneOffset(Bone):
    
        BxHierarchy = []
        ByHierarchy = []
        BzHierarchy = []      

        for i in range ( 0 , len(Bone) ):

          if ( Bone[i][1] == -1 ):

            BxHierarchy.append(Bone[i][2])
            ByHierarchy.append(Bone[i][3])
            BzHierarchy.append(Bone[i][4])
                
          else:

            Bc = Bone[i][1]

            Px = 0.0
            Py = 0.0
            Pz = 0.0                

            while ( Bc != -1 ):

                Px += Bone[Bc][2]
                Py += Bone[Bc][3]
                Pz += Bone[Bc][4]

                Bc = Bone[Bc][1]

            Px += Bone[i][2]
            Py += Bone[i][3]
            Pz += Bone[i][4]

            BxHierarchy.append(Px)
            ByHierarchy.append(Py)
            BzHierarchy.append(Pz)
                
        return BxHierarchy,ByHierarchy,BzHierarchy



def CalC_BoneEffects(d3dr,xtrv,Vrts):

        Vts = []

        Vin = []
        
        for i in range ( 0 , len(Vrts) ):

          for j in range ( 0 , d3dr['verts_1'][0] ):

            if ( Vrts[i][0] == xtrv['px'][j] and Vrts[i][1] == xtrv['py'][j] and Vrts[i][2] == xtrv['pz'][j] and  Vrts[i][3] == xtrv['bn'][j] ):

                Vts.append([ xtrv['px'][j] , xtrv['py'][j] , xtrv['pz'][j] , xtrv['w'][j] , xtrv['bn'][j] , i ])
                
                Vin.append(j)

                break
            
          assert len(Vts) == (i+1), "ERROR IN INDEXING"
          
        Vtz = []    
        
        for i in range ( d3dr['verts_1'][0] , len(xtrv) ):

          for j in range ( 0 , len(Vin) ):

            if ( xtrv['vn'][i] == Vin[j] ):

                Vtz.append([ xtrv['px'][i] , xtrv['py'][i] , xtrv['pz'][i] , xtrv['w'][i] , xtrv['bn'][i] , xtrv['vn'][i] ])

                break

        
# indexing ##---------------------


        Vin = []

        for j in range ( 0 , d3dr['verts_1'][0] ):

            for i in range ( 0 , len(Vrts) ):

                if ( Vrts[i][0] == (xtrv['px'][j]) and Vrts[i][1] == (xtrv['py'][j]) and Vrts[i][2] == (xtrv['pz'][j]) and Vrts[i][3] == xtrv['bn'][j] ):
                        
                    Vin.append(i)

        Vti = []

        for i in range ( 0 , len(Vtz) ):

            for j in range ( 0 , len(Vts) ):

                if Vin[Vtz[i][5]] == Vts[j][5] :

                    Vti.append(j)

                    break
        
        Vtzs = []

        for i in range ( 0 , len(Vts) ):

                Vtzs.append([ Vts[i][4], Vts[i][5], Vts[i][0], Vts[i][1], Vts[i][2], Vts[i][3] ])

        for i in range ( 0 , len(Vtz) ):

                Vtzs.append([ Vtz[i][4], Vti[i], Vtz[i][0], Vtz[i][1], Vtz[i][2], Vtz[i][3] ])
                
        return Vtzs



# --------------------------------------------------------------------------------------------------------------------------------- RENDER MODEL FUNCTIONS



def CalC_meshdata0_1(M,F,V,Msh):

        Mts,Vts,Nts,Fcs,Tcs = Msh[0],Msh[1],Msh[2],Msh[3],Msh[4]

        for m in range ( 0 , len(M) ):

           Mti = Add_Material(Mts,M[m])

           Mts,Mtn = Mti[0],Mti[1]

           for i in range ( x[m] , x[m]+y[m] ):

              Vti = Add_Vertex(Vts,F[i],V)

              Nti = Add_Normal(Nts,F[i],V)

              Tcs = Add_TexCrd(Tcs,F[i],V)

              Fcs = Add_Face(Fcs,Vti[1],Nti[1],Mti[1])

              Vts,Vtn,Nts,Ntn = Vti[0],Vti[1],Nti[0],Nti[1]
                
        return Mts,Vts,Nts,Fcs,Tcs



def Add_Material(Mts,Mat):

        Mtn = []

        if ( len(Mat) == 5 ): # Portals
                    
             if ( True ):

                        MAT_NAME = "portal"+str(CalC_Zeros(Mat['id'],3))

             Mt = ([ 0, -1, -1, -1, MAT_NAME, 0, 0, 0, 0 ])
             
             Mtn.append(len(Mts))

             Mts.append(Mt)

        if ( len(Mat) != 5 ): # Render
                    
             if ( True ):

                        N1,N2,N3,Sc,Mc = -1,-1,-1,0,0

                        Opd = CalC_float8(Mat['_Opacitd'])

                        Ms = CalC_float8(Mat['_mshine'])

                        if ( len(Mat) == 13 ):#
                                                    Sc = CalC_float8(Mat['_Scolor'])
                        if ( len(Mat) == 15 ):#
                                                    Mc = CalC_float8(Mat['_mcolor']) 
                        if ( Mat['_Eflame'] != 0 ):
                                                    N1 = Mat['_td']     
                        if ( Mat['_td'] != -1 ):
                                                    N2 = Mat['_td']
                        if ( Mat['_opacity'] != 0 ):
                                                    N3 = Mat['_td']
                                            
             Mt = ([ 1 , N1 , N2 , N3 , GetMaterial(-1,N2,0.0,0) , Sc, Mc, Opd, Ms ])

             if Mt not in Mts or (N3 == -1) :
                    
               Mtn.append(len(Mts))
              
               Mts.append(Mt)
              
             else:
                    
               Mtn = GetIndex(Mt,Mts,Mtn)

        return Mts,Mtn



def Add_Vertex(Vts,Face,Verts):

        Vtn = []

        if ( True ):

            Vt = ([ Verts['px'][Face['a']] , Verts['py'][Face['a']] , Verts['pz'][Face['a']] ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

            Vt = ([ Verts['px'][Face['b']] , Verts['py'][Face['b']] , Verts['pz'][Face['b']] ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

            Vt = ([ Verts['px'][Face['c']] , Verts['py'][Face['c']] , Verts['pz'][Face['c']] ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

        return Vts,Vtn



def Add_Normal(Nts,Face,Verts):

        Ntn = []

        if ( len(Verts[0]) > 4 ):

            Nt = ([ Verts['nx'][Face['a']] , Verts['ny'][Face['a']] , Verts['nz'][Face['a']] , Verts['px'][Face['a']] , Verts['py'][Face['a']] , Verts['pz'][Face['a']] ])

            if Nt not in Nts:
                    
                Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)

            Nt = ([ Verts['nx'][Face['b']] , Verts['ny'][Face['b']] , Verts['nz'][Face['b']]  , Verts['px'][Face['b']] , Verts['py'][Face['b']] , Verts['pz'][Face['b']] ])

            if Nt not in Nts:
                    
                Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)

            Nt = ([ Verts['nx'][Face['c']] , Verts['ny'][Face['c']] , Verts['nz'][Face['c']]  , Verts['px'][Face['c']] , Verts['py'][Face['c']] , Verts['pz'][Face['c']] ])

            if Nt not in Nts:
                    
                Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)

        else:
            Nts,Ntn = Cal_Normal(Nts,Face,Verts)

        return Nts,Ntn



def Add_TexCrd(Tcs,Face,Verts):

        if ( len(Verts[0]) > 4 ):

            Tcs.append([ Verts['u'][Face['a']] ,
                         
                         Verts['u'][Face['b']] ,
                         
                         Verts['u'][Face['c']] ,
                         
                         round(1-Verts['v'][Face['a']],8) ,
                         
                         round(1-Verts['v'][Face['b']],8) ,
                         
                         round(1-Verts['v'][Face['c']],8) ])

        else:

            Tcs.append([ 0.1357911 , 0.9111357753119 , 0.24681012 , 0.810122468864221 , 0.82534752 , 0.97786012366821 ]) # Random Value

        return Tcs



def Add_Face(Fcs,Vtn,Ntn,Mtn):

        if ( True ):

            Fcs.append([ Vtn[0] , Vtn[1] , Vtn[2] , Ntn[0] , Ntn[1] , Ntn[2] , Mtn[0] ])

        return Fcs



# --------------------------------------------------------------------------------------------------------------------------------- OTHER FUNCTIONS



def CalC_UniqueMaterialsData_1(Msh):

        Mts,Vts,Nts,Fcs,Tcs = Msh[0],Msh[1],Msh[2],Msh[3],Msh[4]

        if ( True ):  # Searching for duplicate materials

          Mts02,Min = [],[]

          for m in range ( 0 , len(Mts) ):

              E = 0

              for M in range ( 0 , len(Mts02) ):

                  if ( Mts02[M] == Mts[m] and Mts[m][3] != -1 ):

                        Min.append(M)  

                        E = 1

                        break

              if ( E == 0 ):

                   Min.append(len(Mts02))

                   Mts02.append(Mts[m])

                   continue

        if ( True ): # Changing Index to New One

            if ( len(Mts) != len(Mts02) ):

               Mts = Mts02

               for i in range ( 0 , len(Fcs) ):

                   Fcs[i][6] = Min[Fcs[i][6]]

                   continue
                
        return Mts,Vts,Nts,Fcs,Tcs


def RenderMeshCorrectOrder(dner,ecaf,xtrv): ###### UNUSED FUNCTION

        Mats = []

        if ( True ): # Creating Additional MESH

             X,Y = DNER_OFFFACES,DNER_NUMFACES

             x,y = dner['off_verts'], dner['num_verts']

             for R in range ( 0 , len(dner) ):

                Verts,Faces = [],[]

                for i in range ( x[R] ,x[R]+y[R] ):
                                                    Verts.append(xtrv[i])
                for i in range ( X[R] ,X[R]+Y[R] ):
                                                    Faces.append(ecaf[i])
                Mats.append([dner[R],Faces,Verts])

        New = []

        if ( True ): # Sorting that MESH in ascending

           for R in range ( -1 , max(dner['_td'])+1 ): 

             for M in range ( 0 , len(Mats) ):

                 if ( Mats[M][0][5] == R ):

                     New.append(Mats[M])

        Mesh = []

        if ( True ): # Compiling New Data in One

             Data0,Data1,Data2 = [],[],[]

             for m in range ( 0 , len(New) ):

                Data0.append(New[m][0])

                for i in range ( 0, len(New[m][1]) ):
                                                      Data1.append(New[m][1][i])
                for i in range ( 0, len(New[m][2]) ):
                                                      Data2.append(New[m][2][i])
             Mesh = [Data0,Data1,Data2]
                     
        return Mesh

        

def Cal_Normal(Nts,Face,Verts):

        Ntn = []

        if ( True ):

            PA = [Verts['px'][Face['a']],Verts['py'][Face['a']],Verts['pz'][Face['a']]]
            PB = [Verts['px'][Face['b']],Verts['py'][Face['b']],Verts['pz'][Face['b']]]
            PC = [Verts['px'][Face['c']],Verts['py'][Face['c']],Verts['pz'][Face['c']]]
            
            Edge1 = [ PC[0]-PA[0] , PC[1]-PA[1] , PC[2]-PA[2] ]
            Edge2 = [ PB[0]-PA[0] , PB[1]-PA[1] , PB[2]-PA[2] ]
            
            NVert = np.cross( Edge1 , Edge2 )
            if ( np.linalg.norm(NVert) == 0 ):
                                                 NVert[0],NVert[1],NVert[2] = 0.000000001,0.000000001,0.000000001
            NVert = NVert/np.linalg.norm(NVert)
            
            Nt = ([NVert[0],NVert[1],NVert[2],Verts['px'][Face['a']],Verts['py'][Face['a']],Verts['pz'][Face['a']]])
            if Nt not in Nts:
                 Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)
                
            Nt = ([NVert[0],NVert[1],NVert[2],Verts['px'][Face['b']],Verts['py'][Face['b']],Verts['pz'][Face['b']]])
            if Nt not in Nts:
                 Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)
                
            Nt = ([NVert[0],NVert[1],NVert[2],Verts['px'][Face['c']],Verts['py'][Face['c']],Verts['pz'][Face['c']]])
            if Nt not in Nts:
                 Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)

        return Nts,Ntn



def GetLineFaceVerts(M,F,V,i,FACE):

               P = [ [V['px'][F['a'][i]], V['py'][F['a'][i]], V['pz'][F['a'][i]]] ,
                     
                     [V['px'][F['b'][i]], V['py'][F['b'][i]], V['pz'][F['b'][i]]] ,
                     
                     [V['px'][F['c'][i]], V['py'][F['c'][i]], V['pz'][F['c'][i]]] ]
        
               for R in range ( 0 , len(dner) ):

                  Vts = []

                  FACE = []

                  if ( dner['_td'][R] == M['diffuse'][F['_mat'][i]] ): 

                     for k in range ( dner['off_verts'][R] , dner['off_verts'][R] + dner['num_verts'][R] ):

                        Vts.append([xtrv['px'][k],xtrv['py'][k],xtrv['pz'][k]])
                        
                  for x in range ( 0 , len(P) ):

                    for y in range ( 0 , len(Vts) ):
                             
                      if ( P[x] == Vts[y] ): # Match Vertex

                        FACE.append(y+(dner['off_verts'][R]))

                        break

                  if ( len(FACE) != 3 and NameOfModel == "489_01_1" ):

                     if ( F['a'][i] == 260 ):
                                              FACE = [ 793, 793, 792 ] ### 489_01_1 EXCEPTIONAL CASE
                     if ( F['a'][i] == 261 ):
                                              FACE = [ 792, 792, 793 ] ### 489_01_1 EXCEPTIONAL CASE
                
                  if (len(FACE) == 3):

                       FACE = [ FACE[0], FACE[1], FACE[2] ]

                       break

               assert len(FACE) == 3, "Hidden Face Vertex Not Found in Render MESH"

               return FACE



# --------------------------------------------------------------------------------------------------------------------------------- THAT DATA IS FROM IGI 1 anims/anim.iff



def AdditionalData_1(NameOfModel,BoneID):

        Bone = []

        N = 0

        if ( BoneID in ( 30 , 31 ) ):

          if ( NameOfModel in ("000_01_1","009_02_1","008_01_1") ):
                                                       N = 0
          if ( NameOfModel in ("001_01_1","001_02_1","003_01_1","003_02_1","004_01_1","004_02_1","006_01_1","009_01_1","009_02_1","011_01_1","011_02_1","011_03_1","013_01_1","014_01_1","014_02_1","016_01_1","018_01_1","019_01_1","020_01_1","021_01_1","022_01_1") ):
                                                       N = 1
          if ( NameOfModel in ("012_01_1","015_01_1","028_01_1") ):
                                                       N = 6                                                      
          if ( N == 0 ): # Type 0
              
            Bone.append([  ["center",-1,0.00000000,0.00000000,3990.4000000],
                           ["lower body",0,-5.13892293e-01,1.83352112e+02,553.558],
                           ["upper body",1,1.52358502e-01,-3.77480377e+02,1280.4136],
                           ["shoulders",2,7.41089210e-02,9.60487366e+01,631.042],
                           ["head",3,-3.96711912e-05,1.03258926e+02,352.9273],
                           ["head lower",4,-1.01815081e+00,9.77469406e+01,891.61316],
                           ["head upper",4,-1.13468617e-01,7.63609085e+01,121.43697],
                           ["head end",6,3.71010319e-05,4.54250488e+02,-358.70023],
                           ["upper left arm",3,-8.73770996e+02,1.80327621e+02,-380.14197],
                           ["lower left arm",8,-4.98601959e+02,-2.20046127e+02,-1074.86],
                           ["left hand",9,-4.76041199e+02,2.13745651e+02,-980.41034],
                           ["upper left finge",10,-2.31919205e+02,-2.96972692e-03,-439.61548],
                           ["lower left finge",11,-1.12167320e+01,1.05587096e-04,-200.45413],
                           ["left fingers end",12,-1.51359072e+01,-5.44903160e-05,-306.64743],
                           ["upper right arm",3,8.77789124e+02,1.80327209e+02,-380.14032],
                           ["lower right arm",14,4.94149628e+02,-2.20123535e+02,-1074.8108],
                           ["right hand",15,4.68049896e+02,2.13821838e+02,-985.94403],
                           ["upper right fing",16,2.32673676e+02,-1.04437349e-04,-433.71722],
                           ["lower right fing",17,1.36010542e+01,3.24469962e-04,-200.1371],
                           ["right fingers en",18,2.63072968e+00,-1.09073611e-04,-307.542],
                           ["none00",1,5.44034815e+00,7.25950439e+02,-228.98277],
                           ["none01",20,9.46663422e-05,2.10357861e+03,392.49387],
                           ["none02",21,8.08206314e-05,1.61433179e+03,1297.793],
                           ["upper left leg",0,-4.30378998e+02,9.49665756e+01,-44.375652],
                           ["lower left leg",23,-8.46106589e-01,2.08386444e+02,-1737.646],
                           ["left foot",24,7.99461365e+01,-3.63005524e+02,-1827.7457],
                           ["left toe",25,-2.31287994e+01,3.90893158e+02,-163.4263],
                           ["left toe end",26,-3.08275185e+01,7.38062317e+02,-258.84998],
                           ["upper right leg",0,4.35314667e+02,9.49653473e+01,-44.375652],
                           ["lower right leg",28,3.45443940e+00,2.08386444e+02,-1737.6501],
                           ["right foot",29,-7.91121902e+01,-3.63005524e+02,-1827.7416],
                           ["right toe",30,1.66293087e+01,3.90893158e+02,-163.4263],
                           ["right toe end",31,1.02110405e+01,7.38062317e+02,-258.84998] ])


          if ( N == 1 ):  # Type 1/2/3
              
            Bone.append([  ["center",-1,0.00000000,0.00000000,3990.40000000],
                           ["lower body",0,-5.13904631e-01,1.8335211e+02,553.558],
                           ["upper body",1,1.52365461e-01,-3.6878210e+02,1027.4037],
                           ["shoulders",2,7.40687847e-02,9.6049149e+01,686.4855],
                           ["head",3,9.28120812e-07,8.1288391e+01,371.17868],
                           ["head lower",4,-1.01816308e+00,9.7746941e+01,891.61316],
                           ["head upper",4,-1.13495238e-01,7.6360909e+01,121.437386],
                           ["head end",6,1.59762021e-05,4.5425049e+02,-358.6998],
                           ["upper left arm",3,-8.52697083e+02,1.8032762e+02,-389.19165],
                           ["lower left arm",8,-5.05782257e+02,-1.2448235e+02,-947.757],
                           ["left hand",9,-4.51174377e+02,3.6357815e+01,-831.19714],
                           ["upper left finge",10,-1.74661209e+02,-3.1095438e-03,-306.36646],
                           ["lower left finge",11,-5.47590141e+01,-2.6617035e-05,-246.78154],
                           ["left fingers end",12,-1.52120523e+01,-3.5429046e-05,-385.1272],
                           ["upper right arm",3,8.17057739e+02,1.8032721e+02,-389.19003],
                           ["lower right arm",14,5.05384949e+02,-1.2455936e+02,-928.3666],
                           ["right hand",15,4.01260132e+02,3.6434246e+01,-848.47],
                           ["upper right fing",16,1.70200256e+02,1.5114690e-04,-307.54242],
                           ["lower right fing",17,5.92297974e+01,2.4149237e-04,-237.6237],
                           ["right fingers en",18,8.28260326e+00,-2.1982698e-05,-377.2043],
                           ["none00",1,1.12996347e-01,7.2239508e+02,-229.50092],
                           ["none01",20,8.60274668e-05,2.1035786e+03,392.49387],
                           ["none02",21,7.42084594e-05,1.6143318e+03,1297.793],
                           ["upper left leg",0,-4.30378998e+02,9.4966164e+01,-44.375244],
                           ["lower left leg",23,-8.46045136e-01,-4.2745033e+01,-1789.1041],
                           ["left foot",24,7.99461365e+01,-1.6188129e+02,-1850.7448],
                           ["left toe",25,-2.31287594e+01,3.9089316e+02,-163.4263],
                           ["left toe end",26,-3.08275604e+01,7.3806232e+02,-258.84998],
                           ["upper right leg",0,4.35314667e+02,9.4965347e+01,-44.375652],
                           ["lower right leg",28,3.45439839e+00,-4.2745033e+01,-1789.1082],
                           ["right foot",29,-7.91121902e+01,-1.6188129e+02,-1850.7448],
                           ["right toe",30,1.66292667e+01,3.9089316e+02,-163.4263],
                           ["right toe end",31,1.02110405e+01,7.3806232e+02,-258.84998] ])


          if ( N == 6 ):  # Type 6
              
            Bone.append([  ["center",-1,0.00000000,0.00000000,3990.40000000],
                           ["lower body",0,-5.13896406e-01,1.83352112e+02,489.6645],
                           ["upper body",1,1.52378157e-01,-2.18227097e+02,1046.5403],
                           ["shoulders",2,7.40782022e-02,5.87649002e+01,513.7039],
                           ["head",3,3.28596684e-06,8.12888031e+01,371.17828],
                           ["head lower",4,-1.01817131e+00,9.77469406e+01,891.61316],
                           ["head upper",4,-1.13495238e-01,7.63609085e+01,121.4378],
                           ["head end",6,1.15636631e-05,4.54250488e+02,-358.70023],
                           ["upper left arm",3,-5.83679993e+02,5.83929825e+01,-389.19165],
                           ["lower left arm",8,-4.66862061e+02,-2.15144844e+01,-868.36017],
                           ["left hand",9,-4.37157867e+02,3.63582230e+01,-852.6479],
                           ["upper left finge",10,-1.99647629e+02,-3.04460176e-03,-260.6461],
                           ["lower left finge",11,-2.45681343e+01,-9.16303816e-06,-210.57986],
                           ["left fingers end",12,9.49948349e+01,-4.26356710e-05,-318.0638],
                           ["upper right arm",3,5.80255737e+02,5.83925743e+01,-389.19003],
                           ["lower right arm",14,4.63294434e+02,-2.15915298e+01,-874.6844],
                           ["right hand",15,4.35507172e+02,3.64342461e+01,-844.1979],
                           ["upper right fing",16,1.94484619e+02,4.95280110e-05,-241.98267],
                           ["lower right fing",17,5.74742508e+01,-5.37550841e-05,-190.76791],
                           ["right fingers en",18,-4.76352501e+01,5.51038975e-05,-375.40042],
                           ["none00",1,1.12985700e-01,7.22395081e+02,-229.50092],
                           ["none01",20,8.78370774e-05,2.10357861e+03,392.49344],
                           ["none02",21,4.90893290e-05,1.61433179e+03,1297.793],
                           ["upper left leg",0,-3.28154297e+02,9.49665756e+01,-44.375652],
                           ["lower left leg",23,-8.46086085e-01,-7.94472427e+01,-1660.7231],
                           ["left foot",24,7.99461365e+01,-1.13308464e+02,-1689.0879],
                           ["left toe",25,-2.31287594e+01,3.90893158e+02,-342.1192],
                           ["left toe end",26,-3.08275604e+01,7.38062317e+02,-258.84998],
                           ["upper right leg",0,3.30613129e+02,9.49653473e+01,-44.375652],
                           ["lower right leg",28,3.45442700e+00,-7.94472427e+01,-1660.7273],
                           ["right foot",29,-7.91121902e+01,-1.13308464e+02,-1689.0879],
                           ["right toe",30,1.66293087e+01,3.90893158e+02,-342.1192],
                           ["right toe end",31,1.02111225e+01,7.38062317e+02,-258.84998] ])

            
        elif ( BoneID == 48 ):
            

            Bone.append([  ["center shoulders",-1,0.0000000,0.0000000,0.0000000],
                           ["none11",0,-1.1343995e-01,808.52167,-384.8368],
                           ["none12",1,6.1222905e-05,1066.7172,-1691.1564],
                           ["none13",2,5.0344344e-05,1576.28,1174.8434],
                           ["upper right arm",0,8.4967010e+02,180.32721,132.39622],
                           ["lower right arm",4,4.3388925e+02,-149.5171,-779.57935],
                           ["right hand",5,-9.7083801e+01,-978.6327,3.3235476],
                           ["upper right midd",6,-3.1386255e+01,-467.02182,-19.283188],
                           ["lower right midd",7,-2.8277719e+00,-197.48618,17.174404],
                           ["right middle fin",8,-3.0587697e+00,-95.37372,13.356072],
                           ["none03",9,4.5676541e-05,-172.4121,14.865039],
                           ["upper right litt",6,1.7049968e+02,-422.55972,-6.261186],
                           ["lower right litt",11,4.4212223e+01,-121.56846,24.181145],
                           ["right little fin",12,2.2205603e+01,-75.37213,2.3467457],
                           ["none05",13,3.6761887e+01,-172.4121,14.86508],
                           ["upper right ring",6,7.1074196e+01,-446.1445,-21.541477],
                           ["lower right ring",15,2.8278374e+01,-174.86356,17.174322],
                           ["right ring finge",16,1.6271030e+01,-92.138695,13.121167],
                           ["none04",17,1.9012526e+01,-182.83273,14.350663],
                           ["upper right fore",6,-1.4618254e+02,-462.87256,-23.310581],
                           ["lower right fore",19,-4.3129650e+01,-145.90894,25.17295],
                           ["right forefinger",20,-2.2678118e+01,-89.71755,13.356154],
                           ["none02",21,-3.9589764e+01,-155.44524,14.865039],
                           ["upper right thum",6,-9.8684921e+01,-161.50813,45.1543],
                           ["lower right thum",23,-7.9162163e+01,95.27623,-83.39865],
                           ["right thumb tip",24,-2.1998058e+01,-120.164345,64.02785],
                           ["none01",25,1.5249572e+01,-162.13974,53.904995],
                           ["upper left arm",0,-8.5407739e+02,180.32721,132.39622],
                           ["lower left arm",27,-4.3388925e+02,149.5171,779.57935],
                           ["left hand",28,9.7083801e+01,978.6327,-3.3235393],
                           ["upper left ring ",29,-7.1074608e+01,446.4312,12.079514],
                           ["lower left ring ",30,-2.8278456e+01,172.79057,-13.583974],
                           ["left ring finger",31,-1.6120094e+01,90.7436,-12.373688],
                           ["none08",32,-1.9012402e+01,182.83273,-14.350581],
                           ["upper left middl",29,3.1386295e+01,467.30853,9.821224],
                           ["lower left middl",34,2.8277595e+00,198.48232,-8.268759],
                           ["left middle fing",35,2.8405800e+00,93.8242,-12.595568],
                           ["none06",36,-3.3972385e-05,172.4121,-14.864957],
                           ["upper left littl",29,-1.7049968e+02,419.45905,3.8814964],
                           ["lower left littl",38,-4.4212223e+01,128.28795,-17.394156],
                           ["left little fing",39,-2.2205521e+01,76.166756,-9.846415],
                           ["none07",40,-3.6761887e+01,172.4121,-14.864998],
                           ["upper left foref",29,1.4618254e+02,463.15927,13.848699],
                           ["lower left foref",42,4.3129650e+01,147.39537,-11.426856],
                           ["left forefinger ",43,2.4544132e+01,92.61793,-10.2587185],
                           ["none09",44,3.9589642e+01,155.44524,-14.865121],
                           ["upper left thumb",29,9.8684921e+01,161.50813,-45.1543],
                           ["lower left thumb",46,8.9203506e+01,-95.27623,84.01346],
                           ["left thumb tip",47,2.1998140e+01,121.58238,-60.84649],
                           ["none10",48,-1.5249531e+01,154.34587,-60.435658],
                           ["none20",0,-1.1341291e-01,808.52167,156.95953],
                           ["none21",50,7.7520075e-05,1992.581,-165.84662],
                           ["none22",51,6.6365435e-05,1962.6721,-113.23023],
                           ["none30",0,-1.1346616e-01,808.52167,730.6076],
                           ["none31",53,1.3104209e-04,1875.9844,691.7939],
                           ["none32",54,-4.8148479e-05,1831.6246,-714.1867] ])

        return Bone



# --------------------------------------------------------------------------------------------------------------------------------- RENDER FACE TRACING FUNCTIONS


def FindFaceID(M,F,V,i,Ext):

        N = -1

        m = F['_mat'][i]

        if ( M['opacity'][m] != 1.0 and M['portal'][m] == 65535 ):

          for I in range ( 0 , len(Ext) ):

            if ( Ext[I] == i ): # for Render face

                N = I # render face index for face

                break

        return N



def FindFaceType(M,F,V,Extra,i,j):

        m = F['_mat'][i]

        if True :

         if ( M['opacity'][m] != 1.0 and M['portal'][m] != 65535 ):
                                                                     Type = 0
         if ( M['opacity'][m] != 1.0 and M['portal'][m] == 65535 ):
                                                                     Type = 1
         if ( M['opacity'][m] == 1.0 and M['portal'][m] == 65535 ):
                                                                     Type = 2
         if ( M['opacity'][m] == 1.0 and M['portal'][m] != 65535 ):
                                                                     Type = 0
         if ( Type == 1 and  j == -1 ):
                                                                     Type = 4
        return Type


def FindFacesHidden(M,F,V,i,j,Type):

        FACE = []

        if ( Type == 1 and j != -1 ):

               FACE = [ ecaf['a'][j],ecaf['b'][j],ecaf['c'][j] ]

        elif ( Type == 4 and j == -1 ):

               FACE = GetLineFaceVerts(M,F,V,i,[])
        else:
               FACE = [ -1, -1, -1 ]

        return FACE


def FindFaceRenderIndex(i,j,Face2,Type):

        N = -1

        if ( Type == 1 and j != -1 ):

           N = CalC_Index(dner)[j] # for face

        elif ( Type == 4 and j == -1 ):

           N = CalC_Index02(dner)[Face2[0]] # for vertex

           print("Warning! Line Face occurence found in model")

        return N


def INDEX(Mats,Offset,Face,Face02,Cat):

        N = -1

        if ( True ):

          for i in range ( 0 , len(Mats) ):

            if ( Face['_mat'] == Mats[i][0] and Face02 == Mats[i][1] and Cat == Mats[i][2] ):

               N = i + Offset # Material connected to this face index

               break

        assert N != -1, "Material Definition Not Found of Face"

        return [[N]]



# ---------------------------------------------------------------------------------------------------------------------------------  REAL MODEL FUNCTIONS



def CalC_modeldata0_1(M,F,V,O,t,Cat,Msh):

        Mts,Vts,Nts,Fcs,Tcs = Msh[0],Msh[1],Msh[2],Msh[3],Msh[4]

        Mat = CalC_Materials(M,F,V,t,Cat)

        Mts = ADD_Materials(Mts,Mat[0],M)

        for i in range ( 0 , len(F) ):

            j = FindFaceID(M,F,V,i,Mat[1])

            T = FindFaceType(M,F,V,0,i,j)#Tp

            f = FindFacesHidden(M,F,V,i,j,T)

            I = FindFaceRenderIndex(i,j,f,T)

            Mtn = INDEX(Mat[0],O,F[i],I,Cat)

            Vti = ADD_Vertex(Vts,V,F[i],f,T)

            Nti = ADD_Normal(Nts,V,F[i],f,T)
            
            Tcs = ADD_TexCrd(Tcs,V,F[i],f,T)

            Fcs = ADD_Face(Fcs,Vti[1],Nti[1],Mtn[0])

            Vts,Vtn,Nts,Ntn = Vti[0],Vti[1],Nti[0],Nti[1]

        return Mts,Vts,Nts,Fcs,Tcs



def ADD_Materials(Mts,M,Mat):
        

        for i in range ( 0 , len(M) ):

            m,R,T = M[i][0],M[i][1],M[i][2]
            

            if  ( R == -1 and Mat['portal'][m] != 65535 and Mat['opacity'][m] != 1.0 ):  # PORTALS ---------------------
                    

               if ( True ):

                                MAT_NAME = "portal"+str(CalC_Zeros(Mat['portal'][m],3))
                  

               Mt = ([ 0, -1, -1, -1, MAT_NAME, 0, 0, 0, 0 ])

               Mts.append(Mt)
               

            elif ( R != -1 and Mat['portal'][m] == 65535 and Mat['opacity'][m] != 1.0 ):  # RENDER MESH ----------------
                    

               if ( True ):

                                N1,N2,N3,Sc,Mc = -1,-1,-1,0,0

                                Opd = CalC_float8(dner['_Opacitd'][R])

                                Ms = CalC_float8(dner['_mshine'][R])

                                if ( len(dner[R]) == 13 ):#
                                                                      Sc = CalC_float8(dner['_Scolor'][R])
                                if ( len(dner[R]) == 15 ):#
                                                                      Mc = CalC_float8(dner['_mcolor'][R]) 
                                if ( dner['_Eflame'][R] != 0 ):
                                                                      N1 = dner['_td'][R]
                                if ( dner['_td'][R] != -1 ):
                                                                      N2 = dner['_td'][R]
                                if ( dner['_opacity'][R] != 0 ):
                                                                      N3 = dner['_td'][R]

               if ( True ):

                                M0 = Mat['diffuse'][m]
                      
                                Op = Mat['opacity'][m]

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                      
                                            
               Mt = ([ 1 , N1 , N2 , N3 , MAT_NAME , Sc, Mc, Opd, Ms ])
              
               Mts.append(Mt)
                  

            elif ( R == -1 and Mat['portal'][m] == 65535 and ( Mat['opacity'][m] == 1.0 ) and T == 0 ):  # COLLISION MESH 0 ----------------
                    

               if ( True ):

                                M0 = Mat['diffuse'][m]

                                Op = Mat['opacity'][m]

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                  

               Mt = ([ 2, -1, M0, -1, MAT_NAME , 0, 0, 1, 0.01 ])
              
               Mts.append(Mt)
                  

            elif ( R == -1 and Mat['portal'][m] == 65535 and ( Mat['opacity'][m] == 1.0 ) and T == 1 ):  # COLLISION MESH 1 ---------------------
                    

               if ( True ):

                                M0 = Mat['diffuse'][m]

                                Op = Mat['opacity'][m]

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                  

               Mt = ([ 3, -1, M0, -1, MAT_NAME , 0, 0, 1, 0 ])
              
               Mts.append(Mt)
               

        return Mts



def ADD_Vertex(Vts,Verts,Face,Face2,Type):

        Vtn = []

        if ( True ):

            Verts,Face = Verts,[Face['a'],Face['b'],Face['c']] # Bringing Data from COL MESH

            Vt = ([ Verts['px'][Face[0]] , Verts['py'][Face[0]] , Verts['pz'][Face[0]] ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

            Vt = ([ Verts['px'][Face[1]] , Verts['py'][Face[1]] , Verts['pz'][Face[1]] ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

            Vt = ([ Verts['px'][Face[2]] , Verts['py'][Face[2]] , Verts['pz'][Face[2]] ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

        return Vts,Vtn



def ADD_Normal(Nts,Verts,Face,Face2,Type):

        Ntn = []

        if ( Type in (1,4) ):
                
            Verts,Face = xtrv,[Face2[0],Face2[1],Face2[2]] # Bringing Data from RENDER MESH

            Nt = ([ Verts['nx'][Face[0]] , Verts['ny'][Face[0]] , Verts['nz'][Face[0]] , Verts['px'][Face[0]] , Verts['py'][Face[0]] , Verts['pz'][Face[0]] ])

            if Nt not in Nts:
                    
                Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)

            Nt = ([ Verts['nx'][Face[1]] , Verts['ny'][Face[1]] , Verts['nz'][Face[1]]  , Verts['px'][Face[1]] , Verts['py'][Face[1]] , Verts['pz'][Face[1]] ])

            if Nt not in Nts:
                    
                Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)

            Nt = ([ Verts['nx'][Face[2]] , Verts['ny'][Face[2]] , Verts['nz'][Face[2]]  , Verts['px'][Face[2]] , Verts['py'][Face[2]] , Verts['pz'][Face[2]] ])

            if Nt not in Nts:
                    
                Nts.append(Nt)

            Ntn = GetIndex(Nt,Nts,Ntn)

        else:
            Nts,Ntn = Cal_Normal(Nts,Face,Verts)

        return Nts,Ntn



def ADD_TexCrd(Tcs,Verts,Face,Face2,Type):

        if ( Type in (1,4) ):
                
            Verts,Face = xtrv,[Face2[0],Face2[1],Face2[2]] # Bringing Data from RENDER MESH

            Tcs.append([ Verts['u'][Face[0]] ,
                         
                         Verts['u'][Face[1]] ,
                         
                         Verts['u'][Face[2]] ,
                         
                         round(1-Verts['v'][Face[0]],8) ,
                         
                         round(1-Verts['v'][Face[1]],8) ,
                         
                         round(1-Verts['v'][Face[2]],8) ])

        else:
            Tcs.append([ 0.1357911 , 0.9111357 , 0.24681012 , 0.8101224 , 0.82534752 , 0.9778677 ]) # Random Value

        return Tcs



def ADD_Face(Fcs,Vtn,Ntn,Mtn):

        if ( True ):

            Fcs.append([ Vtn[0] , Vtn[1] , Vtn[2] , Ntn[0] , Ntn[1] , Ntn[2] , Mtn[0] ])

        return Fcs




#################################################################################################################################################
######################################################################### MATERIALS FUNCTIONS ###################################################
#################################################################################################################################################




def CalC_Materials(tamc,ecfc,xtvc,Type,Cat):
        

## DNER DOMAINANCY ----------------------
        

        Net0 = []

        Ext0 = []

        for R in range ( 0 , len(dner) ):

          for i in range ( DNER_OFFFACES[R] , DNER_OFFFACES[R] + DNER_NUMFACES[R] ):

            for j in range ( 0 , len(ecfc) ):

               if j not in Ext0 and tamc['diffuse'][ecfc['_mat'][j]] == dner['_td'][R] :

                    if ( xtrv['px'][ecaf['a'][i]] == xtvc['px'][ecfc['a'][j]] and xtrv['px'][ecaf['b'][i]] == xtvc['px'][ecfc['b'][j]] and xtrv['px'][ecaf['c'][i]] == xtvc['px'][ecfc['c'][j]] and xtrv['py'][ecaf['a'][i]] == xtvc['py'][ecfc['a'][j]] and xtrv['py'][ecaf['b'][i]] == xtvc['py'][ecfc['b'][j]] and xtrv['py'][ecaf['c'][i]] == xtvc['py'][ecfc['c'][j]] and xtrv['pz'][ecaf['a'][i]] == xtvc['pz'][ecfc['a'][j]] and xtrv['pz'][ecaf['b'][i]] == xtvc['pz'][ecfc['b'][j]] and xtrv['pz'][ecaf['c'][i]] == xtvc['pz'][ecfc['c'][j]] ):

                        Ext0.append(j)
                        
                        if ([ ecfc['_mat'][j] , R ]) not in Net0:
                      
                          Net0.append([ ecfc['_mat'][j] , R ])

                        break
                

## TAMC DOMAINANCY ----------------------
                

        Net1 = []

        Ext1 = []

        for m in range ( 0 , len(tamc) ):   

         for i in range ( 0 , len(ecfc) ):

            if ( ( tamc['opacity'][m] == 1.0 or tamc['portal'][m] != 65535 ) and ecfc['_mat'][i] == m ):

              Ext1.append(-1)      

              if ([ m , -1 ]) not in Net1:
                      
                Net1.append([ m , -1 ])

            elif ( ( tamc['opacity'][m] != 1.0 and tamc['portal'][m] == 65535 ) and ecfc['_mat'][i] == m ):

               for R in range ( 0 , len(dner) ):

                 for j in range ( DNER_OFFFACES[R] , DNER_OFFFACES[R] + DNER_NUMFACES[R] ):

                   if j not in Ext1 and tamc['diffuse'][m] == dner['_td'][R] :   

                      if ( xtvc['px'][ecfc['a'][i]] == xtrv['px'][ecaf['a'][j]] and xtvc['px'][ecfc['b'][i]] == xtrv['px'][ecaf['b'][j]] and xtvc['px'][ecfc['c'][i]] == xtrv['px'][ecaf['c'][j]] and xtvc['py'][ecfc['a'][i]] == xtrv['py'][ecaf['a'][j]] and xtvc['py'][ecfc['b'][i]] == xtrv['py'][ecaf['b'][j]] and xtvc['py'][ecfc['c'][i]] == xtrv['py'][ecaf['c'][j]] and xtvc['pz'][ecfc['a'][i]] == xtrv['pz'][ecaf['a'][j]] and xtvc['pz'][ecfc['b'][i]] == xtrv['pz'][ecaf['b'][j]] and xtvc['pz'][ecfc['c'][i]] == xtrv['pz'][ecaf['c'][j]] ):

                        Ext1.append(j)
                        
                        if ([ ecfc['_mat'][i] , R ]) not in Net1:
                      
                          Net1.append([ ecfc['_mat'][i] , R ])

                        break
                

## COMPILING BOTH RESULTS ---------------

                          
        Net = []

        N1,N2 = [0],[0]

        if ( Type == 1 ):

          while ( len(Net1) != 0 ):
                      
              Net.append([ Net1[0][0] , Net1[0][1] , Cat ])

              del Net1[0]

        else:

          while ( len(Net0) != 0 or len(Net1) != 0 ):

            if ( Net1[0][1] == -1 and len(Net0) != len(Net1) ):

                   Net.append([ Net1[0][0] , Net1[0][1] , Cat ])

                   N1.append(Net1[0][0]+1)

                   N2.append(Net1[0][1]+0)

                   del Net1[0]


            elif ( Net0[0][0] == Net1[0][0] and Net0[0][1] == Net1[0][1] ):

                   Net.append([ Net1[0][0] , Net1[0][1] , Cat ])

                   N1.append(Net0[0][0]+1)

                   N2.append(Net1[0][1]+1)

                   del Net0[0],Net1[0]

            else:

              if ( ( Net0[0][0] > max(N1) or Net0[0][1] > max(N2) ) and (Net1[0][0] <= max(N1)) and (Net1[0][1] <= max(N2)) ):

                 for j in range ( 0 , len(Net0) ):

                  if ( Net1[0][0] == Net0[j][0] and Net1[0][1] == Net0[j][1] ):

                   Net.append([ Net1[0][0] , Net1[0][1] , Cat ])

                   N1.append(Net1[0][0]+1)

                   N2.append(Net1[0][1]+1)

                   del Net0[j],Net1[0]

                   break

              elif ( (Net1[0][0] > max(N1) or Net1[0][1] > max(N2)) and (Net0[0][0] <= max(N1)) and (Net0[0][1] <= max(N2)) ):
                  
                 for j in range ( 0 , len(Net1) ):

                  if ( Net0[0][0] == Net1[j][0] and Net0[0][1] == Net1[j][1] ):

                   Net.append([ Net0[0][0] , Net0[0][1] , Cat ])

                   N1.append(Net0[0][0]+1)

                   N2.append(Net0[0][1]+1)

                   del Net0[0],Net1[j]

                   break

              elif ( Net0[0][0] > max(N1) or Net0[0][1] > max(N2) and Net1[0][0] > max(N1) or Net1[0][1] > max(N2) ):
                  
                 for j in range ( 0 , len(Net1) ):  

                  if ( Net1[j][0] == max(N1) and Net1[j][1] == -1 ):
                      
                   Net.append([ Net1[j][0] , Net1[j][1] , Cat ])

                   N1.append(Net1[j][0]+1)

                   N1.append(Net1[j][1]+0)

                   del Net1[j]

                   break
                
                  
        return Net,Ext0


