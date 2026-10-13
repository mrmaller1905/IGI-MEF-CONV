import os 
import numpy as np
from .import ase_SM
from .import ase_BM
from .import ase_AM
from .import reader_MEFG
from .reader_MEFG import *
from .ase_SM import *
from .ase_BM import *
from .ase_AM import *

def fromtree(meffilename,Aid,Po,Ro,Hr):

    objtext = ""

    if ( Aid == -1 ):

     print ("\n * Model is " + os.path.basename(meffilename))
    
    Data  = MAINMESHOFMODEL(reader_MEFG.read(meffilename))

    Data1 = COLLMESHOFMODEL(reader_MEFG.read(meffilename))

    if ( len(Data) > 0 and Aid == -1 ):

        Type_Model = Data[0] 
        
        if ( Type_Model == 0 ) : 
            objtext = ase_SM.fromfile(meffilename,Data,Arg0)
            
        
        if ( Type_Model == 1 ) :
            objtext = ase_BM.fromfile(meffilename,Data,Arg0)

    if ( len(Data[6]) > 0 and Aid != -1 ):
        
        if (1): 
            objtext = ase_AM.fromfile(meffilename,Data,srcpth,Aid,Po,Ro)

    if ( len(Data1[6]) > 0 and Aid == -1 ):
        
        if (1): 
            objtext += ase_AM.frommesh(meffilename,Data1,srcpth,Aid,Po,Ro)


    assert 0==0, "Error found?"
             
    return objtext




def MAINMESHOFMODEL(Data):

    List,TName = [],"\"collision01_m21\""

    FACES,UVS = Data[6],Data[7]

    for i in range ( len(FACES)-1 , -1 , -1 ):
        if Data[2][FACES[i][7]][1] == TName :
            List.append(FACES[i][0])

    for i in range ( len(FACES)-1 , -1 , -1 ):
        if Data[2][FACES[i][7]][1] == TName :
            del FACES[i]

    for i in range ( len(UVS)-1 , -1 , -1 ):
        if UVS[i][0] in List:
            del UVS[i]

    if len(UVS) > 0:
        assert len(FACES)==len(UVS),"UV faces != mesh faces "

    VERTS,NORMS = Data[4],Data[5]

    N0,N1 = -1,-1
    for i in range ( 0 , len(FACES) ):
        N0 = max(N0,FACES[i][1],FACES[i][2],FACES[i][3])
        N1 = max(N1,FACES[i][4],FACES[i][5],FACES[i][6])

    for i in range ( len(VERTS)-1 , -1 , -1 ):
        if VERTS[i][0] > N0 :
            del VERTS[i]

    for i in range ( len(NORMS)-1 , -1 , -1 ):
        if NORMS[i][0] > N1 :
            del NORMS[i]

    return Data


def COLLMESHOFMODEL(Data):

    List,TName = [],"\"collision01_m21\""

    FACES,UVS = Data[6],Data[7]

    for i in range ( len(FACES)-1 , -1 , -1 ):
        if Data[2][FACES[i][7]][1] != TName :
            List.append(FACES[i][0])

    for i in range ( len(FACES)-1 , -1 , -1 ):
        if Data[2][FACES[i][7]][1] != TName :
            del FACES[i]

    for i in range ( len(UVS)-1 , -1 , -1 ):
        if UVS[i][0] in List:
            del UVS[i]

    if len(UVS) > 0:
        assert len(FACES)==len(UVS),"UV faces != mesh faces "

    VERTS,NORMS = Data[4],Data[5]

    N0,N1 = len(VERTS),len(NORMS)
    for i in range ( 0 , len(FACES) ):
        N0 = min(N0,FACES[i][1],FACES[i][2],FACES[i][3])
        N1 = min(N1,FACES[i][4],FACES[i][5],FACES[i][6])

    for i in range ( len(VERTS)-1 , -1 , -1 ):
        if VERTS[i][0] < N0 :
            del VERTS[i]

    for i in range ( len(NORMS)-1 , -1 , -1 ):
        if NORMS[i][0] < N1 :
            del NORMS[i]

    assert N0 < 99999 ,"Mesh contains too much vertices "
    
    for i in range ( 0 , len(VERTS) ):
        VERTS[i][0] = VERTS[i][0]-N0
    
    for i in range ( 0 , len(NORMS) ):
        NORMS[i][0] = NORMS[i][0]-N1
    
    for i in range ( 0 , len(FACES) ):
        assert FACES[i][0] == UVS[i][0], "Indices mismatch"
        FACES[i][0],UVS[i][0] = i,i

        FACES[i][1],FACES[i][2] = FACES[i][1]-N0,FACES[i][2]-N0
        FACES[i][3],FACES[i][4] = FACES[i][3]-N0,FACES[i][4]-N1
        FACES[i][5],FACES[i][6] = FACES[i][5]-N1,FACES[i][6]-N1

    return Data
