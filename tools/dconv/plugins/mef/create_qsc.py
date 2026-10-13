import os
from utils import fs
from . import mtp
def func(args):
   count = 0

   for srcpath in fs.walkdir(args.src, '*.dat'):
      
    qsctext = ""
    qsctext += "// Script for converting common models //////////////////////////////////////" + '\n'
    qsctext += "" + '\n'
    qsctext += "// Script directories ///////////////////////////////////////////////////////" + '\n'
    qsctext += "" + '\n'
    qsctext += "SetAnimDirectory(\"anims\");" + '\n'
    qsctext += "SetModelDirectory(\"models\");" + '\n'
    qsctext += "SetTextureDirectory(\"textures\");" + '\n'
    qsctext += "SetPaletteDirectory(\"palettes\");" + '\n'
    qsctext += "SetTempDirectory(\"temp\");" + '\n'
    qsctext += "" + '\n'
    qsctext += "// Model settings /////////////////////////////////////////////////////////" + '\n'
    qsctext += "" + '\n'
    qsctext += "SetScale(40.96);" + '\n'
    qsctext += "SetTargetPlatform(\"PC\");" + '\n'
    qsctext += "" + '\n'
    qsctext += "// Texture settings /////////////////////////////////////////////////////////" + '\n'
    qsctext += "" + '\n'
    qsctext += "StartTexScript(\"commontex\");" + '\n'
    qsctext += "" + '\n'
    qsctext += "SetLightmapResolution(1);" + '\n'
    qsctext += "" + '\n'

    print(" \n -> Dat = " + str((os.path.basename(srcpath))) + " !")

    qsctext += mtp.fromFile(args.src,srcpath)
    dstfile = srcpath.replace(args.src, args.dst, 1).replace('.dat', '.qsc')
    os.makedirs(os.path.dirname(dstfile), exist_ok=True)

    qsctext += "" + '\n'
    qsctext += "// End script ///////////////////////////////////////////////////////////////"
    qsctext += "" + '\n'
    qsctext += "EndTexScript();" + '\n'
    qsctext += "" + '\n'
    qsctext += "BuildStatic(\"" + str(str(os.path.splitext(os.path.basename(srcpath))[0])) +"\");" + '\n'
    qsctext += ""
    
    count += 1
    
    with open(dstfile, 'w') as o:
        o.write(qsctext)

   print("\n\n Converted! " + str(count))
