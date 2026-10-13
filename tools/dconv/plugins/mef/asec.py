import os
from utils import fs
from format.mef import MEF
from . import asec_CS
def func(args):
    count = 0

    for srcpath in fs.walkdir(args.src, '*.ASE'):
        meffile = MEF()
        FILE = srcpath
        asec_CS.Arg0 = args.src
        asec_CS.srcpth = srcpath
        TEXT = asec_CS.fromtree(FILE)

        dstfile = srcpath.replace(args.src, args.dst, 1).replace('.ASE', '.MEF')
        os.makedirs(os.path.dirname(dstfile), exist_ok=True)
        
        with open(dstfile, 'w') as o:
            o.write(TEXT)         

        count += 1

    print('\n Converted: {0}'.format(count))
