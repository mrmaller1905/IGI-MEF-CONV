import os
import io
import struct
import builtins


def fromtex(meffilename,Tm):

    with open("IGI 1\Models.dat", 'r') as read_obj:

        ModelName = str(os.path.splitext(os.path.basename(meffilename))[0])

        NumTex = 0

        NumExe = 0

        headerM = "<Object>"

        headerTn = "<Textures>"

        headerT = "<TextureName>"

        while  NumTex != Tm :

            n = 0

            NumExe += 1

            Mn = 0

            Tr = 0

            Er = 0

            for line in read_obj:

                n += 1

                if ( ModelName in line and Tr == 1 ):

                    Mn = n

                    break            

                if headerM in line:

                    Tr = 1

                else:

                    Tr = 0

                
            if ( Mn == 0 and NumExe == 1 ):

                assert Er != 0, "Error! Model Not Found"

            if ( Mn == 0 and NumExe > 1 ):

                assert Er != 0, "Error! Model Relevant Textures Not Found"                

            Tr = 0

            for line in read_obj:

                n += 1

                if ( n == Mn + 2 ):

                    if headerTn in line:

                        Tr = 1

                        break

                    else:

                        assert Er != 0, "Error! HeaderTn Not Found"

            Tr = 0

            for line in read_obj:

                n += 1

                if ( n == Mn + 3 ):
            
                        Nt = [int(i) for i in line.split()]

                        Ntex = Nt [0]

                        Tr = 1

                        break 

                else:

                        assert Er != 0, "Error! Header Tn Not Supported"

            Tr = 0

            for line in read_obj:

                n += 1

                if ( n == Mn + 5 ):

                    if headerT in line:

                        Tr = 1

                        break

                    else:

                        assert Er != 0, "Error! HeaderT Not Found"

            Textures = []

            NumTex = Ntex

            for Ntex in range(0,Ntex):

                for line in read_obj:

                    Temp = line[:-1]

                    Textures.append(Temp)

                    break
                

    return Textures
