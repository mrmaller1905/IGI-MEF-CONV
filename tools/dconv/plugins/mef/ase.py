import os
from utils import fs
from format.mef import MEF
from . import ase_CS
def func(args):
    count = 0

    for srcpath in fs.walkdir(args.src, '*.MEF'):
        meffile = MEF()
        FILE = srcpath
        ase_CS.Arg0 = args.src
        ase_CS.srcpth = srcpath
        TEXT = ase_CS.fromtree(FILE,-1,[],[],[])

        dstfile = srcpath.replace(args.src, args.dst, 1).replace('.MEF', '.ASE')
        os.makedirs(os.path.dirname(dstfile), exist_ok=True)
        
        with open(dstfile, 'w') as o:
            o.write(TEXT)         

        count += 1

    print('\n Converted: {0}'.format(count))
