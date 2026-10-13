import os
from utils import fs
from format.mef import MEF
from . import Version0_0
def func(args):
    count = 0

    for srcpath in fs.walkdir(args.src, '*.mef'):
        meffile = MEF()
        meffilename = (srcpath.replace(args.src, args.dst, 1).replace('.mef', '.mef'))
        Bytes = Version0_0.fromtree(srcpath)

        dstfile = srcpath.replace(args.src, args.dst, 1).replace('.mef', '.mef')    
        os.makedirs(os.path.dirname(dstfile), exist_ok=True)
        
        with open(dstfile, 'wb') as o:
            o.write(Bytes)       

        count += 1

    print('\n\n Version Converted: {0}'.format(count))
