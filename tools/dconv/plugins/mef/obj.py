import os
from utils import fs
from format.mef import MEF
from . import objS
def func(args):
    count = 0

    for srcpath in fs.walkdir(args.src, '*.MEF'):
        meffile = MEF()
        objS.Arg0 = args.dst
        objS.Arg1 = args.src
        objtext = objS.fromtree(srcpath,-1,[],[],[])

        dstfile = srcpath.replace(args.src, args.dst, 1).replace('.MEF', '.obj') # Model file
        os.makedirs(os.path.dirname(dstfile), exist_ok=True)
        
        with open(dstfile, 'w') as o:
            o.write(objtext)        

        count += 1

    print('\n Created: {0}'.format(count))
