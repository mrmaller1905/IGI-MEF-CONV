import os
import math
import struct
import numpy as np
from math import *
from .import mef_struct
from .mef_struct import *


# --------------------------------------------------------------------------------------------------------------------------------- RENDER MESH FUNCTIONS


def CalC_Index(dner):

        Ns = []

        for R in range ( 0 , len(dner) ):

            for i in range ( (dner['offset_index'][R]//3) , (dner['offset_index'][R]//3) + (dner['num_face'][R]) ):

               Ns.append(R)

        return Ns

    

def CalC_Index02(dner):

        Ns = []

        for R in range ( 0 , len(dner) ):

            for i in range ( dner['off_verts'][R] , dner['off_verts'][R] + dner['num_verts'][R] ):

               Ns.append(R)

        return Ns


def Remove_Duplicates(List):

         Lst,Ext = [],[]

         for i in range ( 0 , len(List) ):

            Listid=([List[i][0],List[i][1]])
             
            if Listid not in Ext:

                Ext.append(Listid)
                
                Lst.append(List[i])

         return Lst


def CalC_References(xtrv,Vts):

        Links = []

        for x in range ( 0 , len(xtrv) ):

            E = 0

            for y in range ( 0 , len(Vts) ):

              if ( Vts[y][0]==xtrv['px'][x] and Vts[y][1]==xtrv['py'][x] and Vts[y][2]==xtrv['pz'][x] ):

                Links.append(y)

                E = 1

            assert E == 1 , "Something Wrong With the MEF file"

        return Links


def Correction_Indices_cafs(sems,cafs):

        Faces = b''

        for i in range ( 0 , len(sems) ):

            for j in range ( X[i], X[i]+Y[i] ):

                Faces += struct.pack('=3I',sems['offset_sverts'][i]+cafs['a'][j],sems['offset_sverts'][i]+cafs['b'][j],sems['offset_sverts'][i]+cafs['c'][j])

        return Faces


def Find_ReflectionMap(dner):
        
        Texs,Rfts = [],[]

        N = 0

        for R in range ( 0 , len(dner) ):

          if ( dner['_td'][R] < N ):

             Texs.append(dner['_td'][R])
             Rfts.append(-1)
             N += 0

          if ( dner['_td'][R] == N ):

             Texs.append(dner['_td'][R])
             Rfts.append(-1)
             N += 1

          if ( dner['_td'][R] > N ):

             Rfts[R-1],N = N,N+1
             if ( dner['_td'][R] == N ):
                Texs.append(dner['_td'][R])
                Rfts.append(-1)
                N += 1

             else:
                assert 0 != 0 , "Wrong Texture ids assignment found in model!"

        Rfs = []

        N = 0

        for R in range ( 0 , len(dner) ):

            Rfs.append(Rfts[R])

            F = CalC_Bools_08(dner['_opacity'][R])

            if ( N < Texs[R] ):
                                 assert 0!=0, "Invalid Tex. ids found"
            if ( N == Texs[R] ):
                                        N = 1 + Texs[R]
            if ( Rfts[R] != -1 ):
                                        N = 1 + Rfts[R]
            elif ( F[0][5] == 1 ):
                                        Rfs[R] = N + 0
            elif ( F[0][2] == 1 ):

                for r in range ( 0 , len(dner) ):
                    if ( (dner['_opacity'][r],dner['_mshine'][r],dner['_mcolor'][r],dner['_Opacitd'][r],dner['_td'][r]) == (dner['_opacity'][R],dner['_mshine'][R],dner['_mcolor'][R],dner['_Opacitd'][R],dner['_td'][R]) ):
                        if ( Rfts[r] != -1 ):
                             Rfs[R] = Rfts[r]
                             
                             break
                
        return Rfs


# --------------------------------------------------------------------------------------------------------------------------------- CHECK FUNCTIONS


def GetSmoothVerts(Nts02,Vs):

        Sets = []
        
        while ( len(Vs) != 0 ):

            V = [Vs[0]]

            for i in range ( 1 , len(Vs) ):

                if ( Check1(Nts02,Vs[0],Vs[i]) == 1 ):

                    V.append(Vs[i])

            Sets.append(V)

            for i in range ( 0 , len(V) ):
                    
              for j in range ( 0 , len(Vs) ):
                      
                if ( Vs[j] == V[i] ):
                        
                    del Vs[j]
                    
                    break
            
        return Sets



def Check1(Nts,A,B):

        O = 50

        if ( True ):

           A = [ Nts[A][0], Nts[A][1], Nts[A][2] ]

           B = [ Nts[B][0], Nts[B][1], Nts[B][2] ]

           C = np.dot(A,B) # Angle between Na & Nb

           if C >= +1.0 :
                           C = +1.0
           if C <= -1.0 :
                           C = -1.0

           if ( math.degrees(math.acos(C)) < O ):  

                           return 1
        return 0


def Check2(Na,Nb):

        O = 0.0008

        if ( True ):

            if ( (Na[3],Na[4],Na[5]) == (Nb[3],Nb[4],Nb[5]) ):

                if ( abs(Na[0]-Nb[0]) < O and abs(Na[1]-Nb[1]) < O and abs(Na[2]-Nb[2]) < O ):

                        return 1
        return 0


def Check3(xtvc,xtrv):

        O = 0.0000001

        if ( True ):

            if ( (xtvc[0],xtvc[1],xtvc[2]) == (xtrv[0],xtrv[1],xtrv[2]) ):
                    
                if ( abs(xtvc[3]-xtrv[3]) < O and abs(xtvc[4]-xtrv[4]) == 0 ):
                                                                               return 1
                if ( abs(xtvc[4]-xtrv[4]) < O and abs(xtvc[3]-xtrv[3]) == 0 ):
                                                                               return 1
        return 0


def Check_RenderMeshFaces(dner,ecaf,xtrv):

        Num = 0

        for i in range ( 0 , len(ecaf)):

            X = [ecaf['a'][i],ecaf['b'][i],ecaf['c'][i]]
            if X[0] == Num :
                            Num += 1
            if X[1] == Num :
                            Num += 1
            if X[2] == Num :
                            Num += 1
            if X[0] > Num or X[1] > Num or X[2] > Num:
                                                  return 1
        return 0


def Check_RenderMeshVerts(dner,ecaf,xtrv):

        Num = []

        for i in range ( 0 , len(ecaf)):

            if ecaf['a'][i] not in Num:
                                        Num.append(ecaf['a'][i])
            if ecaf['b'][i] not in Num:
                                        Num.append(ecaf['b'][i])
            if ecaf['c'][i] not in Num:
                                        Num.append(ecaf['c'][i])
        NaN = []

        if ( len(xtrv) != len(Num) ):

            for i in range ( 0 , len(xtrv) ):

                if i not in Num:

                    NaN.append(i)

        return NaN


# --------------------------------------------------------------------------------------------------------------------------------- MATERIAL PROPERTIES FUNCTIONS


def GetIndex(Vt,Vts,Vtn):

        for i in range ( 0 , len(Vts) ):

           if ( Vts[i] == Vt ):

               Vtn.append(i)

        return Vtn


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
    

def CalC_Numdef(N):

        if ( N > 0.0 and N < 1.0 ):
                        V = round(N,2)
        elif ( N == 1.0 ):
                        V = 1                
        elif ( N == 0.0 ):
                        V = 0
        else:
            assert False , "Number must be ( 0.0 <= N <= 1.0 ) "
            
        return V


def CalC_Bools_08(Num):

        Bin = str(bin(Num))[2:]

        while ( len(Bin) != 8 ):
                                Bin = "0" + Bin
                                
        return [[int(Bin[7]),int(Bin[6]),int(Bin[5]),int(Bin[4]),
                 int(Bin[3]),int(Bin[2]),int(Bin[1]),int(Bin[0])]]


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
                                                                Name = "collision01 -Undefined"
                elif ( Mi == -1 and Tex != -1 and Opd == 1.0 ):
                                                                Name = "collision01 -Undefined"
                elif ( Mi == -1 and Tex != -1 and Opd != 1.0 ):
                                                                Name = "collision01 -Default" 
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


def GetBoneVerts(Length,Verts):
        
        Vrts = []

        for i in range ( 0 , Length ):

            Vt = [ Verts['px'][i] , Verts['py'][i] , Verts['pz'][i] , Verts['bn'][i] ]

            if Vt not in Vrts:

                Vrts.append(Vt)

        return Vrts


def CalC_BoneLinks(Bind,reih1):

        for i in range ( 1 , len(reih1) ):

            for j in range ( 0 , reih1['num_child'][i-1] ):

                Bind.append(i-1)

        return Bind

    
def CalC_BoneOffset(Bind,reih2):

        BxHierarchy = []
        ByHierarchy = []
        BzHierarchy = []        

        for i in range ( 0 , len(reih2) ):

            Bc = Bind[i]

            if ( Bind[i] == -1 ):

                Px = reih2['px'][i]
                Py = reih2['py'][i]
                Pz = reih2['pz'][i]

                BxHierarchy.append(Px)
                ByHierarchy.append(Py)
                BzHierarchy.append(Pz)
                
            else:

                Px = 0.0
                Py = 0.0
                Pz = 0.0                

                while ( Bc != -1 ):

                  Px += reih2['px'][Bc]
                  Py += reih2['py'][Bc]
                  Pz += reih2['pz'][Bc]

                  Bc = Bind[Bc]

                Px += reih2['px'][i]
                Py += reih2['py'][i]
                Pz += reih2['pz'][i]

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

                Vin.append(j)

                E = 1

                break

          if ( E == 1 ):

            Vts.append([ Vrts[i][0] , Vrts[i][1] , Vrts[i][2] , xtrv['w'][j] , Vrts[i][3] , i ])

          else:

            Vts.append([ Vrts[i][0] , Vrts[i][1] , Vrts[i][2] , 1.0000000000 , Vrts[i][3] , i ])

          
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
                
        return Vtzs,Vin



# --------------------------------------------------------------------------------------------------------------------------------- RENDER MODEL FUNCTIONS



def CalC_meshdata1_1(M,F,V,Msh):

        Mts,Vts,Nts,Fcs,Tcs = Msh[0],Msh[1],Msh[2],Msh[3],Msh[4]

        for m in range ( 0 , len(M) ):

           Mti = Add_Material(Mts,M[m])

           Mts,Mtn = Mti[0],Mti[1]

           for i in range ( X[m] , X[m]+Y[m] ):

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

             Mt = ([ 0, [-1], [-1], [-1], [-1], [-1], MAT_NAME, 0, 0, 0, 0 ])
             
             Mtn.append(len(Mts))

             Mts.append(Mt)

        if ( len(Mat) != 5 ): # Render
                    
             if ( True ):

                  if ( len(Mat) == 16 ):  

                        Bmp = CalC_Bools_08(Mat['_opacity'])

                        Mc = str(Bmp[0][1]*0.1) # ilumination

                        Ms = CalC_float8(Mat['_mshine'])

                        Sc = CalC_float8(Mat['_Scolor'])

                        Opd = CalC_float8(Mat['_Opacitd'])

                        Mat_tt = [ Bmp[0][0] , 1, Bmp[0][3] ]

                        Tex_df = [ Mat['_td'], 1, Bmp[0][6] ]

                        Tex_op = [ Bmp[0][2] , 1, Bmp[0][7] ]

                        Tex_bp = [ Mat['_tb'], CalC_float8(Mat['_tbd']), Bmp[0][4] ]

                        Tex_rf = [ Mat['_tr'], CalC_float8(Mat['_trd']), Bmp[0][5] ]

                  else:

                        Bmp = CalC_Bools_08(Mat['_opacity'])

                        Sc = 0 # Default Value for type 3

                        Ms = CalC_float8(Mat['_mshine'])

                        Mc = CalC_float8(Mat['_mcolor'])

                        Opd = CalC_float8(Mat['_Opacitd'])

                        Bmp_R_map = Ref_tex_map[0]

                        del Ref_tex_map[0]

                        Mat_tt = [ Bmp[0][0], 1, Bmp[0][3] ]

                        Tex_df = [ Mat['_td'],1, Bmp[0][6] ]

                        Tex_op = [ Bmp[0][2], 1, Bmp[0][7] ]

                        Tex_bp = [ Bmp[0][4], 1, Bmp[0][4] ]

                        Tex_rf = [ Bmp_R_map, 1, Bmp[0][5] ]

                        
             Mt = ([ 1 , Mat_tt , Tex_df , Tex_op , Tex_bp , Tex_rf , GetMaterial(-1,Tex_df[0],0.0,0) , Sc , Mc , Opd , Ms ])

             if Mt not in Mts or (Bmp[0][2] == 0) :
                    
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

            Vt = ([ Verts['px'][Face['b']] , Verts['py'][Face['b']] , Verts['pz'][Face['b']]  ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

            Vt = ([ Verts['px'][Face['c']] , Verts['py'][Face['c']] , Verts['pz'][Face['c']]  ])

            if Vt not in Vts:
                    
                Vts.append(Vt)

            Vtn = GetIndex(Vt,Vts,Vtn)

        return Vts,Vtn



def Add_Normal(Nts,Face,Verts):

        Ntn = []

        if ( len(Verts[0]) >= 8 ):

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

        if ( len(Verts[0]) > 5 ):

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

                  if ( Mts02[M] == Mts[m] and Mts[m][3][0] == 1 ):

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
        

def CalC_MeshNormals(xtrv,ecaf,dner):

        Vts,Nts = b'',[]

        for i in range ( 0, len(xtrv) ):
                                            Nts.append([ 0.0e+00,0.0e+00,0.0e+00 ])
        for i in range ( 0 , len(ecaf) ):
    
              A,B,C = ecaf['a'][i],ecaf['b'][i],ecaf['c'][i]

              PA = [ xtrv['px'][A], xtrv['py'][A], xtrv['pz'][A] ]
              PB = [ xtrv['px'][B], xtrv['py'][B], xtrv['pz'][B] ]
              PC = [ xtrv['px'][C], xtrv['py'][C], xtrv['pz'][C] ]
            
              Edge1 = [ PC[0]-PA[0] , PC[1]-PA[1] , PC[2]-PA[2] ]
              Edge2 = [ PB[0]-PA[0] , PB[1]-PA[1] , PB[2]-PA[2] ]
              X = np.cross( Edge1, Edge2 )
      
              if ( np.linalg.norm(X) != 0 ):                                  
               NVert = X/np.linalg.norm(X)
       
               Nts[A] = [ Nts[A][0]+NVert[0], Nts[A][1]+NVert[1], Nts[A][2]+NVert[2] ]
               Nts[B] = [ Nts[B][0]+NVert[0], Nts[B][1]+NVert[1], Nts[B][2]+NVert[2] ]
               Nts[C] = [ Nts[C][0]+NVert[0], Nts[C][1]+NVert[1], Nts[C][2]+NVert[2] ]

        for i in range ( 0 , len(xtrv) ):

              if ( np.linalg.norm(Nts[i]) == 0 ): 
                                                  Nts[i] = [ 0.0e+00,1.0e+00,0.0e+00 ]
              if ( np.linalg.norm(Nts[i]) != 0 ):
                                                  Nts[i] = Nts[i]/np.linalg.norm(Nts[i])

              Vts += struct.pack('=10f',xtrv['px'][i], xtrv['py'][i], xtrv['pz'][i], Nts[i][0],

                Nts[i][1], Nts[i][2], xtrv['u'][i], xtrv['v'][i], xtrv['u1'][i], xtrv['v1'][i])
              
        return Vts
        

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

               P= [[V['px'][F['a'][i]], V['py'][F['a'][i]], V['pz'][F['a'][i]]],
                    
                   [V['px'][F['b'][i]], V['py'][F['b'][i]], V['pz'][F['b'][i]]],
                     
                   [V['px'][F['c'][i]], V['py'][F['c'][i]], V['pz'][F['c'][i]]]]

               if ( len(FACE) != 3 ):
        
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
                
                  if (len(FACE) == 3):

                       FACE = [ FACE[0], FACE[1], FACE[2] ]

                       break

               assert len(FACE) == 3, "Hidden Face Vertex Not Found in Render MESH"

               return FACE


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
         if ( Type == 1 and  j == -1 ):
                                                                     Type = 4
        return Type



def FindFaceType02(M,F,V,i,j):

        m = F['_mat'][i]

        if True :

         if ( (M['opacity'][m] != 1.0 or  M['diffuse'][m] == -1) and M['portal'][m] != 65535 ):
                                                                                                Type = 0
         if ( (M['opacity'][m] != 1.0 and M['diffuse'][m] != -1) and M['portal'][m] == 65535 ):
                                                                                                Type = 1
         if ( (M['opacity'][m] == 1.0 or  M['diffuse'][m] == -1) and M['portal'][m] == 65535 ):
                                                                                                Type = 2
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


def FindFaceHidden2(M,F,V,i,j,Type):

        FACE = []

        if ( Type == 1 and j != -1 ):

               FACE = [ ecaf['a'][j],ecaf['b'][j],ecaf['c'][j] ]

        elif ( Type == 4 and j == -1 ):

               FACE = GetLineFaceVrt03(M,F,V,i,[])
        else:
               FACE = [ -1, -1, -1 ]

        return FACE


def FindFaceRenderIndex(i,j,Face2,Type):

        N = -1

        if ( Type == 1 and j != -1 ):

           N = CalC_Index(dner)[j] # for face

        elif ( Type == 4 and j == -1 ):

           N = CalC_Index02(dner)[Face2[0]] # for vertex

        return N


def INDEX(Mats,Offset,Face,Face02,Cat):

        N = -1

        if ( True ):

          for i in range ( 0 , len(Mats) ):

            if ( Face['_mat'] == Mats[i][0] and Face02 == Mats[i][1] and Cat == Mats[i][2] ):

               N = i + Offset # Material connected to this face index

               break

        assert N != -1, "Material Definition Not Found of Face\n\n"+str(([ Face['_mat'] , Face02 , Cat ]))

        return [[N]]



# ---------------------------------------------------------------------------------------------------------------------------------  REAL MODEL FUNCTIONS



def CalC_modeldata0_1(M,F,V,O,t,Cat,Msh):

        Mts,Vts,Nts,Fcs,Tcs = Msh[0],Msh[1],Msh[2],Msh[3],Msh[4]

        Mat = CalC_Materials(M,F,V,1,Cat)

        Mts = ADD_Material03(Mts,Mat[0],M)

        for i in range ( 0 , len(F) ):

            j = FindFaceID(M,F,V,i,Mat[1])

            T = FindFaceType02(M,F,V,i,j)#Tp

            f = FindFaceHidden2(M,F,V,i,j,T)

            I = FindFaceRenderIndex(i,j,f,T)

            Mtn = INDEX(Mat[0],O,F[i],I,Cat)

            Vti = ADD_Vertex(Vts,V,F[i],f,T)

            Nti = ADD_Normal(Nts,V,F[i],f,T)

            Tcs = ADD_TexCrd(Tcs,V,F[i],f,T)

            Fcs = ADD_Face(Fcs,Vti[1],Nti[1],Mtn[0])

            Vts,Vtn,Nts,Ntn = Vti[0],Vti[1],Nti[0],Nti[1]

        return Mts,Vts,Nts,Fcs,Tcs



def CalC_modeldata1_1(M,F,V,O,t,Cat,Msh):

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
            

            if  ( R == -1 and Mat['portal'][m] != 65535 ):  # PORTALS ---------------------
                    

               if ( True ):

                                MAT_NAME = "portal"+str(CalC_Zeros(Mat['portal'][m],3))
                  

               Mt = ([ 0 , [-1] , [-1] , [-1] , [-1] , [-1] , MAT_NAME, 0 , 0 , 0 , 0 ])

               Mts.append(Mt)
               

            elif ( R != -1 and Mat['portal'][m] == 65535 and Mat['opacity'][m] != 1.0 ):  # RENDER MESH ----------------
                    

               if ( True ):

                                Bmp = CalC_Bools_08(dner['_opacity'][R])

                                Mc = str(Bmp[0][1]*0.1) # ilumination

                                Ms = CalC_float8(dner['_mshine'][R])

                                Sc = CalC_float8(dner['_Scolor'][R])

                                Opd = CalC_float8(dner['_Opacitd'][R])

                                Mat_tt = [ Bmp[0][0], 1, 0 ]

                                Tex_op = [ Bmp[0][2], 1, 0 ]

                                Tex_df = [ dner['_td'][R], 1, Bmp[0][6] ]

                                Tex_bp = [ dner['_tb'][R], CalC_float8(dner['_tbd'][R]), Bmp[0][4] ]

                                Tex_rf = [ dner['_tr'][R], CalC_float8(dner['_trd'][R]), Bmp[0][5] ]

               if ( True ):

                                M0 = Mat['diffuse'][m]
                      
                                Op = Mat['opacity'][m]

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                      
                                            
               Mt = ([ 1 , Mat_tt , Tex_df , Tex_op , Tex_bp , Tex_rf , MAT_NAME , Sc , Mc , Opd , Ms ])
              
               Mts.append(Mt)
                  

            elif ( R == -1 and Mat['portal'][m] == 65535 and ( Mat['opacity'][m] == 1.0 ) and T == 0 ):  # COLLISION MESH 0 ----------------
                    

               if ( True ):

                                M0 = Mat['diffuse'][m]

                                Op = Mat['opacity'][m]

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                  

               Mt = ([ 2, [-1] , [M0,1,0] , [-1] , [-1] , [-1] , MAT_NAME , 0, 0, 1, 0.01 ])
              
               Mts.append(Mt)
                  

            elif ( R == -1 and Mat['portal'][m] == 65535 and ( Mat['opacity'][m] == 1.0 ) and T == 1 ):  # COLLISION MESH 1 ---------------------
                    

               if ( True ):

                                M0 = Mat['diffuse'][m]

                                Op = Mat['opacity'][m]

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                  

               Mt = ([ 3, [-1], [M0,1,0] , [-1] , [-1] , [-1] , MAT_NAME , 0, 0, 1, 0 ])
              
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



def ADD_Material03(Mts,M,Mat):
        

        for i in range ( 0 , len(M) ):

            m,R,T = M[i][0],M[i][1],M[i][2]
            

            if  ( R == -1 and Mat['portal'][m] != 65535 ):  # PORTALS ---------------------
                    

               if ( True ):

                                M0,Opd = Mat['diffuse'][m],CalC_Numdef(Mat['opacity'][m])

                                MAT_NAME = "portal"+str(CalC_Zeros(Mat['portal'][m],3))
                  

               Mt = ([ 0 , [-1] , [M0,1,0] , [-1] , [-1] , [-1] , MAT_NAME, 0 , 0 , Opd , 0.1 ])

               Mts.append(Mt)
               

            elif ( R != -1 and Mat['portal'][m] == 65535 and Mat['opacity'][m] != 1.0 and Mat['diffuse'][m] != -1 ):  # RENDER MESH ----------------
                    

               if ( True ):

                                Bmp = CalC_Bools_08(dner['_opacity'][R])

                                Sc = 0 # Default Value for type 3

                                Ms = CalC_float8(dner['_mshine'][R])
        
                                Mc = CalC_float8(dner['_mcolor'][R])

                                Opd = CalC_float8(dner['_Opacitd'][R])

                                Mat_tt = [ Bmp[0][0], 1, 0 ]

                                Tex_op = [ Bmp[0][2], 1, 0 ]

                                Tex_df = [ dner['_td'][R], 1, Bmp[0][6] ]

                                Tex_bp = [ Bmp[0][4], 1, Bmp[0][4] ]

                                Tex_rf = [ Ref_tex_map[R], 1, Bmp[0][5] ]

               if ( True ):

                                M0 = Mat['diffuse'][m]
                      
                                Op = CalC_Numdef(Mat['opacity'][m])

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                      
                                            
               Mt = ([ 1 , Mat_tt , Tex_df , Tex_op , Tex_bp , Tex_rf , MAT_NAME , Sc , Mc , Opd , Ms ])
              
               Mts.append(Mt)
                  

            elif ( R == -1 and Mat['portal'][m] == 65535 and ( Mat['opacity'][m] == 1.0 or Mat['diffuse'][m] == -1 ) and T == 0 ):  # COLLISION MESH 0 ----------------
                    

               if ( True ):

                                M0 = Mat['diffuse'][m]

                                Op = CalC_Numdef(Mat['opacity'][m])

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                  

               Mt = ([ 2, [-1] , [M0,1,0] , [-1] , [-1] , [-1] , MAT_NAME , 0, 0, Op, 0.01 ])
              
               Mts.append(Mt)
                  

            elif ( R == -1 and Mat['portal'][m] == 65535 and ( Mat['opacity'][m] == 1.0 or Mat['diffuse'][m] == -1 ) and T == 1 ):  # COLLISION MESH 1 ---------------------
                    

               if ( True ):

                                M0 = Mat['diffuse'][m]

                                Op = CalC_Numdef(Mat['opacity'][m])

                                MAT_NAME = GetMaterial(Mat['mat_id'][m],M0,Op,T)
                  

               Mt = ([ 3, [-1], [M0,1,0] , [-1] , [-1] , [-1] , MAT_NAME , 0, 0, Op, 0 ])
              
               Mts.append(Mt)
               

        return Mts



#################################################################################################################################################
######################################################################### MATERIALS FUNCTIONS ###################################################
#################################################################################################################################################




def CalC_Materials(tamc,ecfc,xtvc,Type,Cat):
        

## DNER DOMAINANCY ----------------------
        

        Net0 = []

        Ext0 = []

        for R in range ( 0 , len(dner) ):

          for i in range ( DNER_OFFFACES[R] , DNER_OFFFACES[R] + DNER_NUMFACES[R] ):

            Ext0.append(-1) # Exceptional Case 741_01_1.mef

            for j in range ( 0 , len(ecfc) ):

               if tamc['diffuse'][ecfc['_mat'][j]] == dner['_td'][R] :  
                    
                  if j not in Ext0 :

                    if ( xtrv['px'][ecaf['a'][i]] == xtvc['px'][ecfc['a'][j]] and xtrv['px'][ecaf['b'][i]] == xtvc['px'][ecfc['b'][j]] and xtrv['px'][ecaf['c'][i]] == xtvc['px'][ecfc['c'][j]] and xtrv['py'][ecaf['a'][i]] == xtvc['py'][ecfc['a'][j]] and xtrv['py'][ecaf['b'][i]] == xtvc['py'][ecfc['b'][j]] and xtrv['py'][ecaf['c'][i]] == xtvc['py'][ecfc['c'][j]] and xtrv['pz'][ecaf['a'][i]] == xtvc['pz'][ecfc['a'][j]] and xtrv['pz'][ecaf['b'][i]] == xtvc['pz'][ecfc['b'][j]] and xtrv['pz'][ecaf['c'][i]] == xtvc['pz'][ecfc['c'][j]] ):
                        
                        if ([ ecfc['_mat'][j] , R ]) not in Net0:
                      
                         Net0.append([ ecfc['_mat'][j] , R ])

                        Ext0[-1]=(j)
                        
                        break

                       
                
                

## TAMC DOMAINANCY TYPE 0 ----------------------
                
        if Type == 0 :
                
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

                   if tamc['diffuse'][m] == dner['_td'][R] :      

                     if j not in Ext1 :   

                      if ( xtvc['px'][ecfc['a'][i]] == xtrv['px'][ecaf['a'][j]] and xtvc['px'][ecfc['b'][i]] == xtrv['px'][ecaf['b'][j]] and xtvc['px'][ecfc['c'][i]] == xtrv['px'][ecaf['c'][j]] and xtvc['py'][ecfc['a'][i]] == xtrv['py'][ecaf['a'][j]] and xtvc['py'][ecfc['b'][i]] == xtrv['py'][ecaf['b'][j]] and xtvc['py'][ecfc['c'][i]] == xtrv['py'][ecaf['c'][j]] and xtvc['pz'][ecfc['a'][i]] == xtrv['pz'][ecaf['a'][j]] and xtvc['pz'][ecfc['b'][i]] == xtrv['pz'][ecaf['b'][j]] and xtvc['pz'][ecfc['c'][i]] == xtrv['pz'][ecaf['c'][j]] ):

                        Ext1.append(j)
                        
                        if ([ ecfc['_mat'][i] , R ]) not in Net1:
                      
                          Net1.append([ ecfc['_mat'][i] , R ])

                        break

                       
                
                

## TAMC DOMAINANCY TYPE 1 ----------------------
                
        else:

         Net1 = []

         Ext1 = []

         for m in range ( 0 , len(tamc) ):   

          for i in range ( 0 , len(ecfc) ):

            if ( ( tamc['opacity'][m] == 1.0 or tamc['portal'][m] != 65535 or tamc['diffuse'][m] == -1 ) and ecfc['_mat'][i] == m ):

              Ext1.append(-1)      

              if ([ m , -1 ]) not in Net1:
                      
                Net1.append([ m , -1 ])

            elif ( ( tamc['opacity'][m] != 1.0 and tamc['portal'][m] == 65535 and tamc['diffuse'][m] != -1 ) and ecfc['_mat'][i] == m ):

               for R in range ( 0 , len(dner) ):

                 for j in range ( DNER_OFFFACES[R] , DNER_OFFFACES[R] + DNER_NUMFACES[R] ):

                   if tamc['diffuse'][m] == dner['_td'][R] :      

                     if j not in Ext1 :   

                      if ( xtvc['px'][ecfc['a'][i]] == xtrv['px'][ecaf['a'][j]] and xtvc['px'][ecfc['b'][i]] == xtrv['px'][ecaf['b'][j]] and xtvc['px'][ecfc['c'][i]] == xtrv['px'][ecaf['c'][j]] and xtvc['py'][ecfc['a'][i]] == xtrv['py'][ecaf['a'][j]] and xtvc['py'][ecfc['b'][i]] == xtrv['py'][ecaf['b'][j]] and xtvc['py'][ecfc['c'][i]] == xtrv['py'][ecaf['c'][j]] and xtvc['pz'][ecfc['a'][i]] == xtrv['pz'][ecaf['a'][j]] and xtvc['pz'][ecfc['b'][i]] == xtrv['pz'][ecaf['b'][j]] and xtvc['pz'][ecfc['c'][i]] == xtrv['pz'][ecaf['c'][j]] ):

                        Ext1.append(j)
                        
                        if ([ ecfc['_mat'][i] , R ]) not in Net1:
                      
                          Net1.append([ ecfc['_mat'][i] , R ])

                        break
                

## COMPILING BOTH RESULTS ---------------

                          
        Net = []

        N1,N2 = [0],[0]

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



# ---------------------------------------------------------------------------------------------------------------------------------  LMAP MODEL FUNCTIONS



def Add_CorrectOrder(dner,ecaf,xtrv):
        
                
        Fcs,n = [],0

        Mti,Mtn = CalC_Index(dner),CalC_Index02(dner)

        for i in range ( 0 , len(ecaf) ):

         Fcs.append([ ecaf['a'][i] , ecaf['b'][i] , ecaf['c'][i] , Mti[i] ])


        Fces = []

        while ( len(Fcs) != 0 ):

          N = len(Fcs)

          for i in range ( 0 , len(Fcs) ):  

           if ( Fcs[i][0] > n+0 or Fcs[i][0] > n+1 or Fcs[i][0] > n+2 ):
                  continue
                
           elif ( Fcs[i][0] == n+0 and Fcs[i][1] == n+1 and Fcs[i][2] == n+2 ):
                  n += 3
                  Fces.append([ Fcs[i][0] , Fcs[i][1] , Fcs[i][2] , Fcs[i][3] ])
                  del Fcs[i]
                  break
                
           elif ( Fcs[i][0] < n+0 and Fcs[i][1] < n+0 and Fcs[i][2] < n+0 ):
                  n += 0
                  Fces.append([ Fcs[i][0] , Fcs[i][1] , Fcs[i][2] , Fcs[i][3] ])
                  del Fcs[i]
                  break
                
           elif ( Fcs[i][0] == n+0 and Fcs[i][1] <= n+0 and Fcs[i][2] <= n+0 ) or ( Fcs[i][0] <= n+0 and Fcs[i][1] == n+0 and Fcs[i][2] <= n+0 ) or ( Fcs[i][0] <= n+0 and Fcs[i][1] <= n+0 and Fcs[i][2] == n+0 ):
                  n += 1
                  Fces.append([ Fcs[i][0] , Fcs[i][1] , Fcs[i][2] , Fcs[i][3] ])
                  del Fcs[i]
                  break
                
           elif ( Fcs[i][0] == n+0 and Fcs[i][1] == n+1 and Fcs[i][2] <= n+1 ) or ( Fcs[i][0] == n+0 and Fcs[i][1] <= n+1 and Fcs[i][2] == n+1 ) or ( Fcs[i][0] <= n+0 and Fcs[i][1] == n+0 and Fcs[i][2] == n+1 ):
                  n += 2
                  Fces.append([ Fcs[i][0] , Fcs[i][1] , Fcs[i][2] , Fcs[i][3] ])
                  del Fcs[i]
                  break
                
          if ( N == len(Fcs) ):
                  n += 1
                  Fces.append([ n-1 , n-0 , n-0 , Mtn[n-1] ])
                  Fces.append([ n-0 , n-1 , n-1 , Mtn[n-1] ])

                                  
        dner_bts,ecaf_bytes = b'',b''
                
        FACES,n = [],0

        for R in range ( 0 , len(dner) ):

            N = 0
            for i in range ( 0 , len(Fces) ):
                if ( Fces[i][3] == R ):
                     N += 1
            FACES.append(N)
        
        for R in range ( 0 , len(dner) ):

            dner_bts += struct.pack('=4B3f4H2h', dner['_opacity'][R], dner['_mshine'][R], dner['_mcolor'][R], dner['_Opacitd'][R], dner['px'][R], dner['py'][R], dner['pz'][R],n*(3),FACES[R], dner['off_verts'][R], dner['num_verts'][R], dner['_td'][R], dner['_lmap'][R])
            n += FACES[R]
                
        for i in range ( 0 , len(Fces) ):

            ecaf_bytes += struct.pack('=3H', Fces[i][0],Fces[i][1],Fces[i][2])
            
        dner,ecaf = parse_dner(dner_bts,3),parse_ecaf(ecaf_bytes)

        return dner,ecaf



def GetLineFaceVrt03(M,F,V,i,FACE):

               P= [[V['px'][F['a'][i]], V['py'][F['a'][i]], V['pz'][F['a'][i]],  V['u1'][F['a'][i]],  V['v1'][F['a'][i]]],
                    
                   [V['px'][F['b'][i]], V['py'][F['b'][i]], V['pz'][F['b'][i]],  V['u1'][F['b'][i]],  V['v1'][F['b'][i]]],
                     
                   [V['px'][F['c'][i]], V['py'][F['c'][i]], V['pz'][F['c'][i]],  V['u1'][F['c'][i]],  V['v1'][F['c'][i]]]]

               if ( len(FACE) != 3 ):
        
                for R in range ( 0 , len(dner) ):

                  Vts,FACE = [],[]

                  if ( dner['_td'][R] == M['diffuse'][F['_mat'][i]] ): 

                     for k in range ( dner['off_verts'][R] , dner['off_verts'][R] + dner['num_verts'][R] ):

                        Vts.append([xtrv['px'][k],xtrv['py'][k],xtrv['pz'][k],xtrv['u1'][k],xtrv['v1'][k]])
                        
                  for x in range ( 0 , len(P) ):

                    for y in range ( 0 , len(Vts) ):
                             
                      if ( Check3(P[x],Vts[y]) == 1 ): # Match Vertex

                        FACE.append(y+(dner['off_verts'][R]))

                        break
                
                  if (len(FACE) == 3):
                                        break

               assert len(FACE) == 3, "Hidden Face Vertex Not Found in Render MESH"

               return FACE


def Add_ExtraFace(dner,ecaf,xtrv,NaN):

        dner2,ecaf2 = b'',b''

        n = 0

        if ( len(NaN) > 0 ):

          FACES = []

          for R in range ( 0 , len(dner) ):

              N = 0

              for i in range ( dner['offset_index'][R]//3 , dner['offset_index'][R]//3 + dner['num_face'][R] ):

                  if ( len(NaN) > 0 ): # to ignore check for empty array NaN in program

                     if ( NaN[0] <= ecaf['a'][i] or NaN[0] <= ecaf['b'][i] or NaN[0] <= ecaf['c'][i] ):

                        if ( NaN[0]+1 not in NaN ):
                            ecaf2 += struct.pack('=3H', NaN[0]-1 , NaN[0]-1 , NaN[0] ) # EXTRA FACE
                            N += 2
                            del NaN[0]
                            ecaf2 += struct.pack('=3H', ecaf['a'][i] , ecaf['b'][i] , ecaf['c'][i] )

                        else:
                            ecaf2 += struct.pack('=3H', NaN[0] , NaN[0] , NaN[0]+1 ) # EXTRA FACE
                            N += 2
                            del NaN[0],NaN[0]
                            ecaf2 += struct.pack('=3H', ecaf['a'][i] , ecaf['b'][i] , ecaf['c'][i] )
                            
                     else:
                          ecaf2 += struct.pack('=3H', ecaf['a'][i] , ecaf['b'][i] , ecaf['c'][i] )
                          N += 1
                          continue
                  else:
                       ecaf2 += struct.pack('=3H', ecaf['a'][i] , ecaf['b'][i] , ecaf['c'][i] )
                       N += 1
                       continue

              if True:
                       FACES.append(N)

          for R in range ( 0 , len(dner) ):

                dner2 += struct.pack('=4B3f4H3h2B', dner['_opacity'][R], dner['_mshine'][R], dner['_Scolor'][R], dner['_Opacitd'][R], dner['px'][R], dner['py'][R], dner['pz'][R],n*(3),FACES[R], dner['off_verts'][R], dner['num_verts'][R], dner['_td'][R], dner['_tb'][R], dner['_tr'][R], dner['_trd'][R], dner['_tbd'][R] )

                n += FACES[R]

          ecaf = parse_ecaf(ecaf2)

          dner = parse_dner(dner2,0)

        return dner,ecaf



#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
