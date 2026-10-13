import os
import io
import struct
import builtins


def read(File):

    MainIdentifier = ["*","{","\"","\'","}"]

    PriIdentifiers = [ "3DSMAX_ASCIIEXPORT",
                       "COMMENT",
                       "SCENE",
                       "MATERIAL_LIST",
                       "GEOMOBJECT",
                       "HELPEROBJECT" ]
    SecIdentifiers = [ "NODE_NAME",
                       "NODE_TM",
                       "MESH",
                       "MATERIAL_REF",
                       "NUMSUBMTLS",
                       "MATERIAL_CLASS",
                       "MAP_CLASS",
                       "MAP_TYPE" ]

    LINES = []

    with open(File, 'r') as FILE:

        for line in FILE:

            LINES.append(str(line[:-1]))

    LINES.append(str(""))


## -------------------- CHECKS ----------------------
    
        
    assert 200 == ReadData(LINES[0])[1][0] , "Check Line Number "+str(i)
        
    assert PriIdentifiers[0] == ReadData(LINES[0])[0] , "Check Line Number "+str(i)
    
    assert PriIdentifiers[1] == ReadData(LINES[1])[0] , "Check Line Number "+str(i)
    
        


## -------------------- COMPILING ----------------------


    DATA = []

    Mod_type = 0

    Mod_Meshes = []

    DATA.append(Mod_type) # Defines the type ( Simple / Bone Model )

    Mod_Scene = [""]

    for i in range ( 0 , len(LINES) ):

      if ( PriIdentifiers[2] in LINES[i] ):
                                            Mod_Scene = ReadData_Sc(LINES,i)

                                            break

    DATA.append(Mod_Scene) # Defines the 3dsmax scene ( )

    Mod_Mats = []

    for i in range ( 0 , len(LINES) ): 

      if ( PriIdentifiers[3] in LINES[i] ):
                                            Mod_Mats = ReadData_Mt(LINES,i)

                                            break

    DATA.append(Mod_Mats) # Defines the mesh materials ( )

    DATA.append([])

    for i in range ( 0 , len(LINES) ):

      if ( PriIdentifiers[4] in LINES[i] ):
                                            Mod_Meshes = ReadData_Msh(LINES,i)

                                            break
          
    DATA.append(Mod_Meshes) # Defines the mesh objects ( 0,1,2 ... )

    Mod_Hobjs = []

    return DATA





#---------------------------------------------------------------------



def ReadData(Str):

    St,Sps,Data = "",[" ","\t"],[]

    Num = ["0","1","2","3","4","5","6","7","8","9","-","+","."]

    for i in range ( 0 , len(Str) ):

        if (Str[i]) == "*":

            for j in range ( i , len(Str) ):
            
              if (Str[j]) in Sps:

                St = Str[i+1:j]
                            
                break

            break

    Str,i = Str+" ",-1
    
    Nums = ["0","1","2","3","4","5","6","7","8","9","-","+",".","e"]

    if St == "MESH_FACE":
        
     Str = Str.replace("AB:","").replace("BC:","").replace("CA:","")
        
     Str = Str.replace("A:","").replace("B:","").replace("C:","").replace(":","")

    while ( i < len(Str)-1 ):

        i += 1

        if Str[i] != " " and Str[i] == "*" :

            for j in range ( i+1 , len(Str) ):

                if ( Str[j] == " " or Str[j] == "\t" ):

                    i = j+0

                    break

        elif Str[i] != " " and Str[i] == "\"" :

            for j in range ( i+1 , len(Str) ):

                if ( Str[j] == "\"" and Str[j-1] != "\\" ):

                    Data.append(Str[i:j+1])

                    i = j+0

                    break

        elif Str[i] != " " and Str[i] in Num :

            for j in range ( i+1 , len(Str) ):

                if ( Str[j] not in Nums and Str[j] in Sps ):

                    Data.append(Str[i:j+0])

                    i = j+0

                    break
        
    for i in range ( 0 , len(Data) ):

        if  Data[i].find("\"") != -1:
                                     Data[i] = Data[i][1:-1]
        elif Data[i].find("e") != -1:
                                     Data[i] = float(Data[i])
        elif Data[i].find(".") != -1:
                                     Data[i] = float(Data[i])
        elif Data[i].find(".") == -1:
                                     Data[i] = int((Data[i]))
    return St,Data



#--------------------------------------------------------------------->
#------------------------------ SCENE -------------------------------->
#--------------------------------------------------------------------->




def ReadData_Sc(Lines,O):

    Data = []

    Id_N,C = [ 1,1,1,1,1,3,3 ],0

    Id_Defs = [ "SCENE_FILENAME","SCENE_FIRSTFRAME","SCENE_LASTFRAME","SCENE_FRAMESPEED","SCENE_TICKSPERFRAME","SCENE_BACKGROUND_STATIC","SCENE_AMBIENT_STATIC" ]

    for i in range ( O , len(Lines) ):

        if Lines[i].find('{') != -1:
                                    C += 1
        if Lines[i].find('}') != -1:
                                    C -= 1
        if ( C == 0 ) or ( C == 0 ):
                                    I=i-1
                                    break  
        assert C == 0 or i+1 != len(Lines), "\n\n -> Syntax Error ({})."
        
    for i in range ( O+1 , I+1 ):

      D = (ReadData(Lines[i]))

      for x in range ( 0, len(Id_Defs) ):

        if D[0] == Id_Defs[x]:
          
          Data.append(D[1])

          assert Id_N[x] == len(D[1]),"\n\n -> Required No. of Inputs Not found "+str(D[0])
        
    return Data



#--------------------------------------------------------------------->
#------------------------------- MATERIAL ---------------------------->
#--------------------------------------------------------------------->



def ReadData_Mt(Lines,O):

    Data = []

    Id_N,C = [ 1,1,1,3,3,3,1,1,1,1,1,1,0,0,0,0,1,1,1,1 ],0

    Id_Defs = [ "MATERIAL","MATERIAL_NAME","MATERIAL_CLASS","MATERIAL_AMBIENT","MATERIAL_DIFFUSE","MATERIAL_SPECULAR","MATERIAL_SHINESTRENGTH","MATERIAL_SELFILLUM","MATERIAL_TRANSPARENCY","MATERIAL_SHINE","NUMSUBMTLS","SUBMATERIAL","MAP_DIFFUSE","MAP_OPACITY","MAP_BUMP","MAP_REFLECT","MAP_NAME","MAP_CLASS","MAP_AMOUNT","BITMAP" ]
    
    for i in range ( O , len(Lines) ):

        if Lines[i].find('{') != -1:
                                    C += 1
        if Lines[i].find('}') != -1:
                                    C -= 1
        if ( C == 0 ) or ( C == 0 ):
                                    I=i-1
                                    break
                                
        assert C == 0 or i+1 != len(Lines), "\n\n -> Syntax Error ({})."

    assert ReadData(Lines[O+1])[0] == 'MATERIAL_COUNT',"\n\n Required Data Command Not Found"

        
    O,N = O+1,ReadData(Lines[O+1])[1][0]
        
    for i in range ( O+1 , I+1 ):

      D = ReadData(Lines[i])

      for x in range ( 0, len(Id_Defs) ):

        if D[0] == Id_Defs[x]:
          
          Data.append(D)

          assert Id_N[x] == len(D[1]),"\n\n -> Required No. of Inputs Not found "+str(D[0])

    Id_Def01 = [ "MATERIAL","SUBMATERIAL" ]

    Id_Def02 = [ "MAP_DIFFUSE","MAP_OPACITY","MAP_BUMP","MAP_REFLECT" ]

    Id_Def11 = [ "MATERIAL_NAME","MATERIAL_CLASS","MATERIAL_AMBIENT","MATERIAL_DIFFUSE","MATERIAL_SPECULAR","MATERIAL_SHINESTRENGTH","MATERIAL_SELFILLUM","MATERIAL_TRANSPARENCY","MATERIAL_SHINE","NUMSUBMTLS" ]

    Id_Def12 = [ "MAP_NAME","MAP_CLASS","MAP_AMOUNT","BITMAP" ]

    i,Mts = -1,[]

    while ( i < len(Data)-1 ):

        i += 1

        if Data[i][0] in Id_Def01:

            Mts.append([ Data[i][0],Data[i][1][0],"9-Default","Standard", 0.5,0.5,0.5,0.1,0.1,0.1,0.9,0.9,0.9, 0,0,0,0.1,0 ])
            while ( i+1 < len(Data) ):

                if ( Data[i+1][0] not in Id_Def11 ):
                                                      break
                elif ( Data[i+1][0] == Id_Def11[0] ):
                                                      Mts[-1][2] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def11[1] ):
                                                      Mts[-1][3] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def11[2] ):
                                                      Mts[-1][4],Mts[-1][5],Mts[-1][6] = Data[i+1][1][0],Data[i+1][1][1],Data[i+1][1][2]
                elif ( Data[i+1][0] == Id_Def11[3] ):
                                                      Mts[-1][7],Mts[-1][8],Mts[-1][9] = Data[i+1][1][0],Data[i+1][1][1],Data[i+1][1][2]
                elif ( Data[i+1][0] == Id_Def11[4] ):
                                                      Mts[-1][10],Mts[-1][11],Mts[-1][12] = Data[i+1][1][0],Data[i+1][1][1],Data[i+1][1][2]
                elif ( Data[i+1][0] == Id_Def11[5] ):
                                                      Mts[-1][13] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def11[6] ):
                                                      Mts[-1][14] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def11[7] ):
                                                      Mts[-1][15] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def11[8] ):
                                                      Mts[-1][16] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def11[9] ):
                                                      Mts[-1][17] = Data[i+1][1][0]
                i += 1

        elif ( Data[i][0] in Id_Def02 ):

            Mts.append([ Data[i][0], "Map00", "Bitmap", 1.00, "<Path>" ])
            while ( i+1 < len(Data) ):
                
                if  ( Data[i+1][0] not in Id_Def12 ):
                                                      break
                elif ( Data[i+1][0] == Id_Def12[0] ):
                                                      Mts[-1][1] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def12[1] ):
                                                      Mts[-1][2] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def12[2] ):
                                                      Mts[-1][3] = Data[i+1][1][0]
                elif ( Data[i+1][0] == Id_Def12[3] ):
                                                      Mts[-1][4] = Data[i+1][1][0]
                i += 1

            
    Mats,i = [],0

    for I in range ( len(Mts)-1,-0,-1 ):

        if ( Mts[I][0] in Id_Def02 ):

         Mts[I-1] += (Mts[I])

         del Mts[I]

    while ( i < len(Mts)):

        if ( Mts[i][0] == Id_Def01[0] ):
                                          Mats.append(Mts[i])
        elif ( Mts[i][0] == Id_Def01[1] ):
                                          Mats[-1].append(Mts[i])
        i += 1
        
    
    return Mats





#--------------------------------------------------------------------->
#------------------------------- MESHOBJECT -------------------------->
#--------------------------------------------------------------------->




def ReadData_Msh(Lines,O):

    Data,C = [],0

    Id_N = [ 1,1,3,3,3,3,1,1,4,4,1,1,4,4,0,4,1,3,0,0,0,0,0 ]

    Id_Defs = [ "NODE_NAME","NODE_PARENT","TM_ROW0","TM_ROW1","TM_ROW2","TM_ROW3","MESH_NUMVERTEX","MESH_NUMFACES","MESH_VERTEX","MESH_FACE","MESH_NUMTVERTEX","MESH_NUMTVFACES","MESH_TVERT","MESH_TFACE","MESH_NORMALS","MESH_VERTEXNORMAL","MATERIAL_REF","WIREFRAME_COLOR","GEOMOBJECT","HELPEROBJECT","SHAPEOBJECT","LIGHTOBJECT","CAMERAOBJECT" ]
        
    for i in range ( O , len(Lines) ):

      D = (ReadData(Lines[i]))

      for x in range ( 0, len(Id_Defs) ):

        if D[0] == Id_Defs[x]:
          
          Data.append(D)

          if D[0] != "MESH_FACE":

           assert Id_N[x] == len(D[1]),"\n\n -> Required No. of Inputs Not found "+str(D[0])

    Id_Def11 = [ "NODE_NAME","NODE_PARENT","TM_ROW0","TM_ROW1","TM_ROW2","TM_ROW3","MESH_NUMVERTEX","MESH_NUMFACES","MESH_VERTEX","MESH_FACE","MESH_NUMTVERTEX","MESH_NUMTVFACES","MESH_TVERT","MESH_TFACE","MESH_NORMALS","MESH_VERTEXNORMAL","MATERIAL_REF","WIREFRAME_COLOR" ]
    
    i,Msh = -1,[]

    while ( i < len(Data)-1 ):

      i += 1

      if Data[i][0] == Id_Defs[18] or Data[i][0] == Id_Defs[19] :
        Msh.append([ "", "", [], [], [], [], 0, 0, [], [], 0, 0, [], [], 0, [], -1, [ 0.5, 0.5, 0.5 ] ])
        
        while ( i+1 < len(Data) ):

          if Data[i+1][0] not in Id_Def11:
                                            break  
          elif Data[i+1][0] == Id_Defs[0]:
                                            Msh[-1][0] = Data[i+1][1][0]
          elif Data[i+1][0] == Id_Defs[1]:
                                            Msh[-1][1] = Data[i+1][1][0]
          elif Data[i+1][0] == Id_Defs[2]:
                                            Msh[-1][2] = Data[i+1][1]
          elif Data[i+1][0] == Id_Defs[3]:
                                            Msh[-1][3] = Data[i+1][1]
          elif Data[i+1][0] == Id_Defs[4]:
                                            Msh[-1][4] = Data[i+1][1]
          elif Data[i+1][0] == Id_Defs[5]:
                                            Msh[-1][5] = Data[i+1][1]
          elif Data[i+1][0] == Id_Defs[6]:
                                            Msh[-1][6] = Data[i+1][1][0]
          elif Data[i+1][0] == Id_Defs[7]:
                                            Msh[-1][7] = Data[i+1][1][0]
          elif Data[i+1][0] == Id_Defs[8]:
                                            Msh[-1][8].append(Data[i+1][1])
          elif Data[i+1][0] == Id_Defs[9]:
                                            Msh[-1][9].append(Data[i+1][1])
          elif Data[i+1][0] == Id_Defs[10]:
                                            Msh[-1][10] = Data[i+1][1][0]
          elif Data[i+1][0] == Id_Defs[11]:
                                            Msh[-1][11] = Data[i+1][1][0]
          elif Data[i+1][0] == Id_Defs[12]:
                                            Msh[-1][12].append(Data[i+1][1])
          elif Data[i+1][0] == Id_Defs[13]:
                                            Msh[-1][13].append(Data[i+1][1])
          elif Data[i+1][0] == Id_Defs[15]:
                                            Msh[-1][15].append(Data[i+1][1])
          elif Data[i+1][0] == Id_Defs[16]:
                                            Msh[-1][16] = Data[i+1][1][0] 
          elif Data[i+1][0] == Id_Defs[17]:
                                            Msh[-1][17] = Data[i+1][1] 
          i += 1
            
    
    return Msh


#--------------------------------------------------------------------->
#------------------------------- ????????  --------------------------->
#--------------------------------------------------------------------->
