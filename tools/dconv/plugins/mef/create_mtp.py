import os
from utils import fs
from . import mtp_BytesWriter
def func(args):
   count = 0

   for srcpath in fs.walkdir(args.src, '*.mtx'):

    print(" \n -> MTX = " + str((os.path.basename(srcpath))) + " !")
    
    Data = mtp_BytesWriter.fromFile(args.src,srcpath)
    
    dstfile = srcpath.replace(args.src, args.dst, 1).replace('.mtx', '.mtp')

    os.makedirs(os.path.dirname(dstfile), exist_ok=True)
    
    count += 1
    
    with open(dstfile, 'wb') as o:
        o.write(Data)

   print("\n\n Compiled! " + str(count))
