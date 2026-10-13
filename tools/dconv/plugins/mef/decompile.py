import os
from utils import fs
from format.mef import MEF
from . import mef
def func(args):
    count = 0

    for srcpath in fs.walkdir(args.src, '*.mef'):
        meffile = MEF()
        mef.srcpth = srcpath
        meffilename = (srcpath.replace(args.src, args.dst, 1).replace('.mef', '.MEX'))
        meftext = mef.fromtree(meffilename)

        dstfile = srcpath.replace(args.src, args.dst, 1).replace('.mef', '.MEX')
        os.makedirs(os.path.dirname(dstfile), exist_ok=True)

        if meftext != "" :
          with open(dstfile, 'w') as o:
            o.write(meftext)

          count += 1


    print('\n Decompiled: {0}'.format(count))
