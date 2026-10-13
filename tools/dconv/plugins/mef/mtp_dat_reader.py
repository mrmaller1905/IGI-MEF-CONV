import os
from utils import fs

def fromdat(srcpath,srcpth):

    with open(srcpath, 'r') as read_obj:

        ModelNames = []

        TextureNames = []

        n = 0

        Mn = 0

        Tn = 0

        for line in read_obj:

            n += 1

            if ( n == 1 and str(line) != "*** This file is machine generated\n" ):

                assert 0!=0, "Error! Something Wrong with the File"

            if ( n == 2 and str(line) != "*** DO NOT EDIT!\n" ):

                assert 0!=0, "Error! Something Wrong with the File"

            if ( n == 3 and str(line) != "\n" ):

                assert 0!=0, "Error! Something Wrong with the File"

            if ( n > 3 ):

                Mn = [int(i) for i in line.split()][0]

                break

        for i in range ( 0 , Mn ):

            for line in read_obj:

                MEF = (str(line)[:-1])

                Er = len(ModelNames)

                for spath in fs.walkdir(srcpth, MEF+".mef"):

                  ModelNames.append(MEF+".mef")

                if Er == len(ModelNames) :

                  assert 0!=0, "Error! Model Not Found in folder, "+str(srcpth)+str(MEF)

                break

            for line in read_obj:

                Skip = [int(i) for i in line.split()]

                break

            for j in range ( 0 , Skip[0] ):

              for line in read_obj:

                break

        for i in range ( 0 , 1 ):

            for line in read_obj:

                Tn = [int(i) for i in line.split()][0]

                break

        for i in range ( 0 , Tn ):

            for line in read_obj:

                TextureNames.append(str(line)[:-1])

                break
            

    return ModelNames,TextureNames
