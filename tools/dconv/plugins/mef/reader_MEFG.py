import os
import io
import struct
import builtins


def read(File):

    MainIdentifier = ["(",");",","]

    ListIdentifier = [ "NewObject(",#0
                       "",
                       "Material(",#2
                       "MaterialShininess(",#3
                       "MaterialTransparencyType(",#4
                       "Bone(",#5
                       "BuildHierarchy(",#6
                       "BreakScript(",#7
                       "",
                       "DiffuseTMap(",#9
                       "OpacityTMap(",#10
                       "ReflectionTMap(",#11
                       "BumpTMap(",#12
                       "",
                       "Vertex(",#14
                       "Normal(",#15
                       "Face(",#16
                       "UV(",#17
                       "VertexInfluenceRigid(",#18
                       "MagicVertex(",#19
                       "Glow(",#20
                       "AttachObject(",#21
                       "AttachObjectBoneID(" ]

    LINES = []

    with open(File, 'r') as FILE:

        for line in FILE:

            LINES.append(str(line[:-1]))

    LINES.append(str(""))


## -------------------- CHECKS ----------------------

    for i in range ( 0 , len(LINES) ):

      if len(LINES[i]) > 1 :  

        E = False

        assert MainIdentifier[0] in LINES[i] , "Check Line Number "+str(i)

        assert MainIdentifier[1] in LINES[i] , "Check Line Number "+str(i)

        for j in range ( 0 , len(ListIdentifier) ):
                        if ListIdentifier[j] in LINES[i]:
                                                         E = True
        assert E == True , "Check Line Number "+str(i)


## -------------------- COMPILING ----------------------


    DATA = []

    Mod_type = 0

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[6] in LINES[i] ):

        Mod_type = 1

        break

    DATA.append(Mod_type) # Defines the type ( Simple / Bone Model )

    Mod_name = "noname"

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[0] in LINES[i] ):

        Mod_name = ReadData(LINES[i][9:-1],1,i)[0]

        break

    DATA.append(Mod_name) # Defines the mesh name ( e.g:- "515_01_1" )

    Mod_Mats = []

    for i in range ( 0 , len(LINES) ):  

      if ( ListIdentifier[2] in LINES[i] ):
          
           Mod_Mats.append(ReadData(LINES[i][8:-1],14,i))

           if ( ListIdentifier[3] in LINES[i+1] ):

            Mod_Mats[-1] += (ReadData(LINES[i+1][17:-1],2,i))

           if ( ListIdentifier[3]  not in LINES[i+1] ):

             Mod_Mats[-1] += [0,0.1]  

           continue

    Mod_Texs = []

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[9] in LINES[i] ):

           Mod_Texs.append(["DIFFUSE",ReadData(LINES[i][11:-1],4,i)])

           FILE = os.path.dirname(File)+"\\"+(Mod_Texs[-1][1][1][1:-1]).replace("/","\\")

           if (os.path.exists(FILE)) == False :

            print("\n- ERROR - Texture File Not Found ?? "+str(FILE))

      if ( ListIdentifier[10] in LINES[i] ):

           Mod_Texs.append(["OPACITY",ReadData(LINES[i][11:-1],4,i)])

           FILE = os.path.dirname(File)+"\\"+(Mod_Texs[-1][1][1][1:-1]).replace("/","\\")

           if (os.path.exists(FILE)) == False :

            print("\n- ERROR - Texture File Not Found ?? "+str(FILE))

      if ( ListIdentifier[11] in LINES[i] ):

           Mod_Texs.append(["REFLECT",ReadData(LINES[i][14:-1],4,i)])

           FILE = os.path.dirname(File)+"\\"+(Mod_Texs[-1][1][1][1:-1]).replace("/","\\")

           if (os.path.exists(FILE)) == False :

            print("\n- ERROR - Texture File Not Found ?? "+str(FILE))

      if ( ListIdentifier[12] in LINES[i] ):

           Mod_Texs.append(["BUMP",ReadData(LINES[i][8:-1],4,i)])

           FILE = os.path.dirname(File)+"\\"+(Mod_Texs[-1][1][1][1:-1]).replace("/","\\")

           if (os.path.exists(FILE)) == False :

            print("\n- ERROR - Texture File Not Found ?? "+str(FILE))

           continue

    DATA.append(Mod_Mats) # Defines the mesh materials ( wood,metal etc )

    DATA.append(Mod_Texs) # Defines the mesh textures ( tex2,wall.tga etc )

    Mod_Verts = []

    Mod_Norms = []

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[14] in LINES[i] ):

        for j in range ( i , len(LINES) ):

           if ( ListIdentifier[14] not in LINES[j] ):

            break

           Mod_Verts.append(ReadData(LINES[j][6:-1],4,j))

        break

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[15] in LINES[i] ):

        for j in range ( i , len(LINES) ):

           if ( ListIdentifier[15] not in LINES[j] ):

            break

           Mod_Norms.append(ReadData(LINES[j][6:-1],4,j))

        break

    DATA.append(Mod_Verts) # Defines the mesh points ( 0,1,2 ... )

    DATA.append(Mod_Norms) # Defines the mesh points ( 0,1,2 ... )
    
    Mod_Faces = []

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[16] in LINES[i] ):

        for j in range ( i , len(LINES) ):

           if ( ListIdentifier[16] not in LINES[j] ):

            break

           Mod_Faces.append(ReadData(LINES[j][4:-1],8,j))

        break

    DATA.append(Mod_Faces) # Defines the mesh face indexing ( A,B,C ... )

    Mod_Texcrd = []

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[17] in LINES[i] ):

        for j in range ( i , len(LINES) ):

           if ( ListIdentifier[17] not in LINES[j] ):

            break

           Mod_Texcrd.append(ReadData(LINES[j][2:-1],7,j))

        break

    DATA.append(Mod_Texcrd) # Defines the UV mapping Coordinates ( 0,1,0 ... )

    Mod_MVerts = []

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[19] in LINES[i] ):

        for j in range ( i , len(LINES) ):

           if ( ListIdentifier[19] not in LINES[j] ):

            break

           Mod_MVerts.append(ReadData(LINES[j][11:-1],6,j))

        break

    DATA.append(Mod_MVerts) # Defines the Magic occurence points ( X,Y,Z ... )

    Mod_Glows = []

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[20] in LINES[i] ):

        for j in range ( i , len(LINES) ):

           if ( ListIdentifier[20] not in LINES[j] ):

            break

           Mod_Glows.append(ReadData(LINES[j][4:-1],7,j))

        break

    DATA.append(Mod_Glows) # Defines the Light glowing sphere ( X,Y,Z ... )

    Mod_attas = []

    for i in range ( 0 , len(LINES) ):

      if ( ListIdentifier[21] in LINES[i] ):

         Mod_attas.append(ReadData(LINES[i][12:-1],14,i))

         continue

    DATA.append(Mod_attas) # Defines the attachment Position ( X,Y,Z ... )

    Mod_bones = []

    if Mod_type == 1 :

        for i in range ( 0 , len(LINES) ):

          if ( ListIdentifier[5] in LINES[i] ):

             Mod_bones.append(ReadData(LINES[i][4:-1],6,i))

    DATA.append(Mod_bones) # Defines the attachment Position ( str,X,Y,Z )

    Mod_Vfts = []

    if Mod_type == 1 :

        for i in range ( 0 , len(LINES) ):

          if ( ListIdentifier[18] in LINES[i] ):

             #Mod_Vfts.append(ReadData(LINES[i][20:-1],6,i))???????????

             continue

    DATA.append(Mod_Vfts) # Defines the attachment Position ( X,Y,Z,W,B. )

    return DATA





#---------------------------------------------------------------------




def ReadData(Str,N,I):

    Identifiers = ["(",")",","]

    if Str.find("\"") == -1:

        Str = Str.replace(" ","")

    else:

        I = 0

        for i in range ( 0, len(Str) ):

         if ( I == 0 and Str[i][0] == " " ):
                                                Str = Str[:i]+"|"+Str[i+1:]
         elif I == 0 and Str[i][0] == "\"" :
                                                I=1
         elif I == 1 and Str[i][0] == "\"" :
                                                I=0
        Str = Str.replace("|","")
              

    assert Str[+0] == Identifiers[0] , "START Bracket not found, Line Number "+str(I)

    assert Str[-1] == Identifiers[1] , "END Bracket not found, Line Number "+str(I)

    Str = "|"+Str[1:-1]+"|"

    if Str.find("\"") == -1:

        Str = Str.replace(",","|")

    else:

        I = 0

        for i in range ( 0, len(Str) ):

         if ( I == 0 and Str[i][0] == "," ):
                                                Str = Str[:i]+"|"+Str[i+1:]
         elif I == 0 and Str[i][0] == "\"" :
                                                I=1
         elif I == 1 and Str[i][0] == "\"" :
                                                I=0
        Str = Str.replace("|","|")
        



    if True: # ----\\\\\\\\\\\\\\

        Ind = []

        STR = []

        for j in range ( 0 , len(Str) ):

          if ( "|" == Str[j] ):

            Ind.append(j+1)

        for j in range ( 0 , len(Ind)-1 ):

            x,y = Ind[j],Ind[j+1]-1

            STR.append(Str[x:y])

            continue


    if True:

        Data = []

        for j in range ( 0 , len(STR) ):

            if ( STR[j][-1] == "\""  and  STR[j][0] == "\"" ):

                Data.append(str(STR[j]))

            elif ( "\"" in STR[j] or "\'" in STR[j] ):

                assert 0!=0,"Error in Line "+str(j)

            elif ( "e" in STR[j] or "." in STR[j] ):

                Data.append(float(STR[j]))

            elif ( "e" not in STR[j] and "." not in STR[j] ):

                Data.append(int(STR[j]))
                

    assert N == len(Data),"Required No. of Parameters not found!"

    return Data

