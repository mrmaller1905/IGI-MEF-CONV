from . import ase
from . import asec
from . import obj
from . import convert
from . import decompile
from . import compare
from . import create_qsc
from . import create_mtp
from . import extrct_mtp
from . import Version

def register_parser(cli):
	cmd = cli.add_parser('mef')
	sub = cmd.add_subparsers()
	sub.require = True	

	sub_ase = sub.add_parser('ase')
	sub_ase.add_argument('src', help="Source folder")
	sub_ase.add_argument('dst', help="Destination folder")
	sub_ase.set_defaults(func=ase.func)

	sub_asec = sub.add_parser('asec')
	sub_asec.add_argument('src', help="Source folder")
	sub_asec.add_argument('dst', help="Destination folder")
	sub_asec.set_defaults(func=asec.func)

	sub_obj = sub.add_parser('obj')
	sub_obj.add_argument('src', help="Source folder")
	sub_obj.add_argument('dst', help="Destination folder")
	sub_obj.set_defaults(func=obj.func)	
	
	sub_convert = sub.add_parser('convert')
	sub_convert.add_argument('src', help="Source folder")
	sub_convert.add_argument('dst', help="Destination folder")
	sub_convert.set_defaults(func=convert.func)	

	sub_decompile = sub.add_parser('decompile')
	sub_decompile.add_argument('src', help="Source folder")
	sub_decompile.add_argument('dst', help="Destination folder")
	sub_decompile.set_defaults(func=decompile.func)	
	sub_obj.set_defaults(func=obj.func)	

	sub_compare = sub.add_parser('compare')
	sub_compare.add_argument('src', help="Source folder")
	sub_compare.add_argument('dst', help="Destination folder")
	sub_compare.set_defaults(func=compare.func)	

	sub_create_qsc = sub.add_parser('create_qsc')
	sub_create_qsc.add_argument('src', help="Source folder")
	sub_create_qsc.add_argument('dst', help="Destination folder")
	sub_create_qsc.set_defaults(func=create_qsc.func)		

	sub_create_mtp = sub.add_parser('create_mtp')
	sub_create_mtp.add_argument('src', help="Source folder")
	sub_create_mtp.add_argument('dst', help="Destination folder")
	sub_create_mtp.set_defaults(func=create_mtp.func)	

	sub_extrct_mtp = sub.add_parser('extrct_mtp')
	sub_extrct_mtp.add_argument('src', help="Source folder")
	sub_extrct_mtp.add_argument('dst', help="Destination folder")
	sub_extrct_mtp.set_defaults(func=extrct_mtp.func)

	sub_Version = sub.add_parser('Version')
	sub_Version.add_argument('src', help="Source folder")
	sub_Version.add_argument('dst', help="Destination folder")
	sub_Version.set_defaults(func=Version.func)
