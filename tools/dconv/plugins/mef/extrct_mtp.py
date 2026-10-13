import os
from utils import fs
from . import mtp_decoder
def func(args):
   count = 0

   print()

   for srcpath in fs.walkdir(args.src, '*.mtp'):

    print(" \n -> MTP = " + str((os.path.basename(srcpath))) + " !")
    
    qsctext = mtp_decoder.fromFile(args.src,srcpath)
    
    dstfile = srcpath.replace(args.src, args.dst, 1).replace('.mtp', '.mtx')

    os.makedirs(os.path.dirname(dstfile), exist_ok=True)
    
    count += 1
    
    with open(dstfile, 'w') as o:
        o.write(qsctext)

   print("\n\n\n Decompiled! " + str(count))
