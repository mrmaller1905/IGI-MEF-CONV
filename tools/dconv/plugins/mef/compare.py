import os
from utils import fs
from .import com_00
def func(args):
    
    count = 0

    text = "\n"

    text += " * ModelFileNames :- " + "\n\n"

    disc = "\n"

    Efile1 = 'IGI 2\MefErrorList.qsc'

    Efile2 = 'IGI 2\MefErrorDisc.qsc'

    for srcpath in fs.walkdir(args.src, '*.mef'):

        srcpth1 = srcpath

        E = 0

        meffile1 = os.path.basename(srcpth1)

        for srcpath in fs.walkdir(args.dst, meffile1):

            E = 1

            srcpth2 = srcpath

            print ("\n * Model MEF ---- " + os.path.basename(meffile1))

            disc += "\n * Model MEF ---- " + os.path.basename(meffile1)

        if E == 1 :

            com00 = com_00.fromtree(srcpth1,srcpth2)
            
            text += com00[0]

            disc += com00[1]

            count += 1

            print("\n --------------------------------------")

            disc += "\n ------------------------------------"

        if E == 0 :
            
            E = -1

            #print("\n - !Model " + str(meffile1) + " Not Found. ????????????????????????? ")

            #disc += "\n - !Model " + str(meffile1) + " Not Found. ??????????????????????? "

    with open(Efile1, 'w') as o:
        
        o.write(text)

    with open(Efile2, 'w') as o:
        
        o.write(disc)            

    print('\n Compared: {0}'.format(count))
