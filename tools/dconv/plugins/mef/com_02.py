import os 
import numpy as np
from .import reader_ilff
from .import mef_struct
from .mef_struct import *
from .reader_ilff import *

def fromM0(srcpth1,srcpth2,M):

    E,Et,disc = 0,"",""
    
    reader1 = reader_ilff.open(srcpth1)
    reader2 = reader_ilff.open(srcpth2)
    
    hsem1 = parse_hsem(reader1.read(b'HSEM'))
    hsem2 = parse_hsem(reader2.read(b'HSEM'))
    
    atta1 = parse_atta(reader1.read(b'ATTA'))
    atta2 = parse_atta(reader2.read(b'ATTA'))
    
    xtvm1 = parse_xtvm(reader1.read(b'XTVM'))
    xtvm2 = parse_xtvm(reader2.read(b'XTVM'))
    
    trop1 = parse_trop(reader1.read(b'TROP'))
    trop2 = parse_trop(reader2.read(b'TROP'))
    
    xvtp1 = parse_xvtp(reader1.read(b'XVTP'))
    xvtp2 = parse_xvtp(reader2.read(b'XVTP'))
    
    cftp1 = parse_cftp(reader1.read(b'CFTP'))
    cftp2 = parse_cftp(reader2.read(b'CFTP'))

    ecaf1 = parse_ecaf(reader1.read(b'ECAF'))
    ecaf2 = parse_ecaf(reader2.read(b'ECAF'))

    if ( not reader1.find(b'PMTL') ):
    
        d3dr1 = parse_d3dr(reader1.read(b'D3DR'),0)
        d3dr2 = parse_d3dr(reader2.read(b'D3DR'),0)
        
        dner1 = parse_dner(reader1.read(b'DNER'),0)
        dner2 = parse_dner(reader2.read(b'DNER'),0)
        
        xtrv1 = parse_xtrv(reader1.read(b'XTRV'),0)
        xtrv2 = parse_xtrv(reader2.read(b'XTRV'),0)

    if reader1.find(b'PMTL'):
    
        d3dr1 = parse_d3dr(reader1.read(b'D3DR'),3)
        d3dr2 = parse_d3dr(reader2.read(b'D3DR'),3)
        
        dner1 = parse_dner(reader1.read(b'DNER'),3)
        dner2 = parse_dner(reader2.read(b'DNER'),3)
        
        xtrv1 = parse_xtrv(reader1.read(b'XTRV'),3)
        xtrv2 = parse_xtrv(reader2.read(b'XTRV'),3)
    
    if reader1.find(b'WOLG'):
        
        wolg1 = parse_wolg(reader1.read(b'WOLG'))
        wolg2 = parse_wolg(reader2.read(b'WOLG'))

    if reader1.find(b'HPRM'):
        
        hprm1 = parse_hprm(reader1.read(b'HPRM'))[1]
        hprm2 = parse_hprm(reader2.read(b'HPRM'))[1]
    
    if reader1.find(b'HSMC'):
    
        xtvc1 = parse_xtvc(reader1.read(b'XTVC'),0)
        xtvc2 = parse_xtvc(reader2.read(b'XTVC'),0)
    
        ecfc1 = parse_ecfc(reader1.read(b'ECFC',0))
        ecfc2 = parse_ecfc(reader2.read(b'ECFC',0))
    
        tamc1 = parse_tamc(reader1.read(b'TAMC',0))
        tamc2 = parse_tamc(reader2.read(b'TAMC',0))
    
        hpsc1 = parse_hpsc(reader1.read(b'HPSC',0))
        hpsc2 = parse_hpsc(reader2.read(b'HPSC',0))

#-------------------------------------------

    IDT = [ "ECAF" ]

    IDT0 = [ "HSEM" , "ATTA" , "XTVM" , "TROP" , "XTVP" , "CFTP" , "D3DR" , "ECAF" , "DNER" , "XTRV" , "WOLG" , "XTVC" , "ECFC" , "TAMC" , "HPSC" ]

#-------------------------------------------

    if ( len(hsem1) != len(hsem2) ):

        disc += "\n -> len(HSEM) != len(HSEM) "

    elif "HSEM" not in IDT:

        for i in range ( 0 , len(hsem1) ):

            if hsem1['model_type'][i] != hsem2['model_type'][i] :

                disc += "\n -> hsem['model_type'][" + str(i) + "] != hsem['model_type'][" + str(i) + "]  " + " , " + str(hsem1['model_type'][i]) + " != " + str(hsem2['model_type'][i])

            if abs(hsem1['model_radius'][i] - hsem2['model_radius'][i]) >= 40.96 :

                disc += "\n -> hsem['model_radius'][" + str(i) + "] != hsem['model_radius'][" + str(i) + "]  " + " , " + str(hsem1['model_radius'][i]) + " != " + str(hsem2['model_radius'][i])

#-------------------------------------------

    if ( len(atta1) != len(atta2) ):

        disc += "\n -> len(ATTA) != len(ATTA) "

    elif "ATTA" not in IDT:

        for i in range ( 0 , len(atta1) ):
            
            if atta1['name'][i] != atta2['name'][i] :

                disc += "\n -> atta['name'][" + str(i) + "] != atta['name'][" + str(i) + "]  " + " , " + str(atta1['name'][i]) + " != " + str(atta2['name'][i])

            if abs(atta1['px'][i] - atta2['px'][i]) >= 1 :

                disc += "\n -> atta['px'][" + str(i) + "] != atta['px'][" + str(i) + "]  " + " , " + str(atta1['px'][i]) + " != " + str(atta2['px'][i])

            if abs(atta1['py'][i] - atta2['py'][i]) >= 1 :

                disc += "\n -> atta['py'][" + str(i) + "] != atta['py'][" + str(i) + "]  " + " , " + str(atta1['py'][i]) + " != " + str(atta2['py'][i])

            if abs(atta1['pz'][i] - atta2['pz'][i]) >= 1 :

                disc += "\n -> atta['pz'][" + str(i) + "] != atta['pz'][" + str(i) + "]  " + " , " + str(atta1['pz'][i]) + " != " + str(atta2['pz'][i])

            if atta1['_00'][i] != atta2['_00'][i] :

                disc += "\n -> atta['_00'][" + str(i) + "] != atta['_00'][" + str(i) + "]  " + " , " + str(atta1['_00'][i]) + " != " + str(atta2['_00'][i])

            if atta1['_01'][i] != atta2['_01'][i] :

                disc += "\n -> atta['_01'][" + str(i) + "] != atta['_01'][" + str(i) + "]  " + " , " + str(atta1['_01'][i]) + " != " + str(atta2['_01'][i])

            if atta1['_02'][i] != atta2['_02'][i] :

                disc += "\n -> atta['_02'][" + str(i) + "] != atta['_02'][" + str(i) + "]  " + " , " + str(atta1['_02'][i]) + " != " + str(atta2['_02'][i])

            if atta1['_09'][i] != atta2['_09'][i] :

                disc += "\n -> atta['_09'][" + str(i) + "] != atta['_09'][" + str(i) + "]  " + " , " + str(atta1['_09'][i]) + " != " + str(atta2['_09'][i])

            if atta1['_an'][i] != atta2['_an'][i] :

                disc += "\n -> atta['_an'][" + str(i) + "] != atta['_an'][" + str(i) + "]  " + " , " + str(atta1['_an'][i]) + " != " + str(atta2['_an'][i])
                
  
#-------------------------------------------

    if ( len(xtvm1) != len(xtvm2) ):

        disc += "\n -> len(XTVM) != len(XTVM) "

    elif "XTVM" not in IDT:

        for i in range ( 0 , len(xtvm1) ):
            
            if abs(xtvm1['px'][i] - xtvm2['px'][i]) >= 1 :

                disc += "\n -> xtvm['px'][" + str(i) + "] != xtvm['px'][" + str(i) + "]  " + " , " + str(xtvm1['px'][i]) + " != " + str(xtvm2['px'][i])

            if abs(xtvm1['py'][i] - xtvm2['py'][i]) >= 1 :

                disc += "\n -> xtvm['py'][" + str(i) + "] != xtvm['py'][" + str(i) + "]  " + " , " + str(xtvm1['py'][i]) + " != " + str(xtvm2['py'][i])

            if abs(xtvm1['pz'][i] - xtvm2['pz'][i]) >= 1 :

                disc += "\n -> xtvm['pz'][" + str(i) + "] != xtvm['pz'][" + str(i) + "]  " + " , " + str(xtvm1['pz'][i]) + " != " + str(xtvm2['pz'][i])

            if xtvm1['_0'][i] != xtvm2['_0'][i] :

                disc += "\n -> xtvm['_0'][" + str(i) + "] != xtvm['_0'][" + str(i) + "]  " + " , " + str(xtvm1['_0'][i]) + " != " + str(xtvm2['_0'][i])
                

#-------------------------------------------

    if ( len(trop1) != len(trop2) ):

        disc += "\n -> len(TROP) != len(TROP) "

    elif "TROP" not in IDT:

        for i in range ( 0 , len(trop1) ):

            if trop1['o_vertex'][i] != trop2['o_vertex'][i] :

                disc += "\n -> trop['o_vertex'][" + str(i) + "] != trop['o_vertex'][" + str(i) + "]  " + " , " + str(trop1['o_vertex'][i]) + " != " + str(trop2['o_vertex'][i])

            if trop1['n_vertex'][i] != trop2['n_vertex'][i] :

                disc += "\n -> trop['n_vertex'][" + str(i) + "] != trop['n_vertex'][" + str(i) + "]  " + " , " + str(trop1['n_vertex'][i]) + " != " + str(trop2['n_vertex'][i])

            if trop1['o_face'][i] != trop2['o_face'][i] :

                disc += "\n -> trop['o_face'][" + str(i) + "] != trop['o_face'][" + str(i) + "]  " + " , " + str(trop1['o_face'][i]) + " != " + str(trop2['o_face'][i])

            if trop1['n_face'][i] != trop2['n_face'][i] :

                disc += "\n -> trop['n_face'][" + str(i) + "] != trop['n_face'][" + str(i) + "]  " + " , " + str(trop1['n_face'][i]) + " != " + str(trop2['n_face'][i])

            if trop1['id'][i] != trop2['id'][i] :

                disc += "\n -> trop['id'][" + str(i) + "] != trop['id'][" + str(i) + "]  " + " , " + str(trop1['id'][i]) + " != " + str(trop2['id'][i])
                
                                                                                                                                              
#-------------------------------------------

    if ( len(xvtp1) != len(xvtp2) ):

        disc += "\n -> len(XVTP) != len(XVTP) "

    elif "XTVP" not in IDT:

        for i in range ( 0 , len(xvtp1) ):

            if abs(xvtp1['px'][i] - xvtp2['px'][i]) >= 1 :

                disc += "\n -> xvtp['px'][" + str(i) + "] != xvtp['px'][" + str(i) + "]  " + " , " + str(xvtp1['px'][i]) + " != " + str(xvtp2['px'][i])

            if abs(xvtp1['py'][i] - xvtp2['py'][i]) >= 1 :

                disc += "\n -> xvtp['py'][" + str(i) + "] != xvtp['py'][" + str(i) + "]  " + " , " + str(xvtp1['py'][i]) + " != " + str(xvtp2['py'][i])

            if abs(xvtp1['pz'][i] - xvtp2['pz'][i]) >= 1 :

                disc += "\n -> xvtp['pz'][" + str(i) + "] != xvtp['pz'][" + str(i) + "]  " + " , " + str(xvtp1['pz'][i]) + " != " + str(xvtp2['pz'][i])

                                                                                                                                              
#-------------------------------------------

    if ( len(cftp1) != len(cftp2) ):

        disc += "\n -> len(CFTP) != len(CFTP) "

    elif "CFTP" not in IDT:

        for i in range ( 0 , len(cftp1) ):

            if cftp1['a'][i] != cftp2['a'][i] :

                disc += "\n -> cftp['a'][" + str(i) + "] != cftp['a'][" + str(i) + "]  " + " , " + str(cftp1['a'][i]) + " != " + str(cftp2['a'][i])

            if cftp1['b'][i] != cftp2['b'][i] :

                disc += "\n -> cftp['b'][" + str(i) + "] != cftp['b'][" + str(i) + "]  " + " , " + str(cftp1['b'][i]) + " != " + str(cftp2['b'][i])

            if cftp1['c'][i] != cftp2['c'][i] :

                disc += "\n -> cftp['c'][" + str(i) + "] != cftp['c'][" + str(i) + "]  " + " , " + str(cftp1['c'][i]) + " != " + str(cftp2['c'][i])


#-------------------------------------------

    if not reader1.find(b'PMTL'):

     if ( len(dner1) != len(dner2) ):

        disc += "\n -> len(DNER) != len(DNER) "

     elif "DNER" not in IDT:

        for i in range ( 0 , len(dner1) ):

            if dner1['_opacity'][i] != dner2['_opacity'][i] :

                disc += "\n -> dner['_opacity'][" + str(i) + "] != dner['_opacity'][" + str(i) + "]  " + " , " + str(dner1['_opacity'][i]) + " != " + str(dner2['_opacity'][i])

            if dner1['_mshine'][i] != dner2['_mshine'][i] :

                disc += "\n -> dner['_mshine'][" + str(i) + "] != dner['_mshine'][" + str(i) + "]  " + " , " + str(dner1['_mshine'][i]) + " != " + str(dner2['_mshine'][i])

            if dner1['_Scolor'][i] != dner2['_Scolor'][i] :

                disc += "\n -> dner['_Scolor'][" + str(i) + "] != dner['_Scolor'][" + str(i) + "]  " + " , " + str(dner1['_Scolor'][i]) + " != " + str(dner2['_Scolor'][i])

            if dner1['_Opacitd'][i] != dner2['_Opacitd'][i] :

                disc += "\n -> dner['_Opacitd'][" + str(i) + "] != dner['_Opacitd'][" + str(i) + "]  " + " , " + str(dner1['_Opacitd'][i]) + " != " + str(dner2['_Opacitd'][i])

            if dner1['num_face'][i] != dner2['num_face'][i] :

                disc += "\n -> dner['num_face'][" + str(i) + "] != dner['num_face'][" + str(i) + "]  " + " , " + str(dner1['num_face'][i]) + " != " + str(dner2['num_face'][i])

            if dner1['_td'][i] != dner2['_td'][i] :

                disc += "\n -> dner['_td'][" + str(i) + "] != dner['_td'][" + str(i) + "]  " + " , " + str(dner1['_td'][i]) + " != " + str(dner2['_td'][i])

            if dner1['_tb'][i] != dner2['_tb'][i] :

                disc += "\n -> dner['_tb'][" + str(i) + "] != dner['_tb'][" + str(i) + "]  " + " , " + str(dner1['_tb'][i]) + " != " + str(dner2['_tb'][i])

            if dner1['_tr'][i] != dner2['_tr'][i] :

                disc += "\n -> dner['_tr'][" + str(i) + "] != dner['_tr'][" + str(i) + "]  " + " , " + str(dner1['_tr'][i]) + " != " + str(dner2['_tr'][i])

            if dner1['_trd'][i] != dner2['_trd'][i] :

                disc += "\n -> dner['_trd'][" + str(i) + "] != dner['_trd'][" + str(i) + "]  " + " , " + str(dner1['_trd'][i]) + " != " + str(dner2['_trd'][i])

            if dner1['_tbd'][i] != dner2['_tbd'][i] :

                disc += "\n -> dner['_tbd'][" + str(i) + "] != dner['_tbd'][" + str(i) + "]  " + " , " + str(dner1['_tbd'][i]) + " != " + str(dner2['_tbd'][i])

#---

    else:

     Mt1,Mt2 = [],[]

     if ( True ): 

         for R in range ( 0 , len(dner1) ):
             if ([ dner1['_opacity'][R] , dner1['_mshine'][R] , dner1['_mcolor'][R] , dner1['_Opacitd'][R] , dner1['_td'][R] ]) not in Mt1:
                 Mt1.append([ dner1['_opacity'][R] , dner1['_mshine'][R] , dner1['_mcolor'][R] , dner1['_Opacitd'][R] , dner1['_td'][R] ])
         for R in range ( 0 , len(dner2) ):
             if ([ dner2['_opacity'][R] , dner2['_mshine'][R] , dner2['_mcolor'][R] , dner2['_Opacitd'][R] , dner2['_td'][R] ]) not in Mt2:
                 Mt2.append([ dner2['_opacity'][R] , dner2['_mshine'][R] , dner2['_mcolor'][R] , dner2['_Opacitd'][R] , dner2['_td'][R] ])

     if ( len(Mt1) != len(Mt2) ):

        disc += "\n -> len(DNER) != len(DNER) "

     elif "DNER" not in IDT:

        for i in range ( 0 , len(Mt1) ):
            
            if Mt1[i][0] != Mt2[i][0] :

                disc += "\n -> dner['_opacity'][" + str(i) + "] != dner['_opacity'][" + str(i) + "]  " + " , " + str(Mt1[i][0]) + " != " + str(Mt2[i][0])

            if Mt1[i][1] != Mt2[i][1] :

                disc += "\n -> dner['_mshine'][" + str(i) + "] != dner['_mshine'][" + str(i) + "]  " + " , " + str(Mt1[i][1]) + " != " + str(Mt2[i][1])

            if Mt1[i][2] != Mt2[i][2] :

                disc += "\n -> dner['_mcolor'][" + str(i) + "] != dner['_mcolor'][" + str(i) + "]  " + " , " + str(Mt1[i][2]) + " != " + str(Mt2[i][2])

            if Mt1[i][3] != Mt2[i][3] :

                disc += "\n -> dner['_Opacitd'][" + str(i) + "] != dner['_Opacitd'][" + str(i) + "]  " + " , " + str(Mt1[i][3]) + " != " + str(Mt2[i][3])

            if Mt1[i][4] != Mt2[i][4] :

                disc += "\n -> dner['_td'][" + str(i) + "] != dner['_td'][" + str(i) + "]  " + " , " + str(Mt1[i][4]) + " != " + str(Mt2[i][4])
                

#-------------------------------------------

    if True :

     ecaf3 = [] 

     if ( len(ecaf1) != len(ecaf2) ):

        disc += "\n -> len(ECAF) != len(ECAF) "

     elif False:#"ECAF" not in IDT:

        for i in range ( 0 , len(ecaf1) ):

          for j in range ( 0 , len(ecaf2) ):

            Pa,Pb,Pc,PA,PB,PC = xtrv1[ecaf1['a'][i]],xtrv1[ecaf1['b'][i]],xtrv1[ecaf1['c'][i]],xtrv2[ecaf2['a'][j]],xtrv2[ecaf2['b'][j]],xtrv2[ecaf2['c'][j]]
            
            if abs(Pa[0]-PA[0]) < 1 and abs(Pa[1]-PA[1]) < 1 and abs(Pa[2]-PA[2]) < 1 and abs(Pa[3]-PA[3]) < 0.1 and abs(Pa[4]-PA[4]) < 0.1 :
            
             if abs(Pb[0]-PB[0]) < 1 and abs(Pb[1]-PB[1]) < 1 and abs(Pb[2]-PB[2]) < 1 and abs(Pb[3]-PB[3]) < 0.1 and abs(Pb[4]-PB[4]) < 0.1 :
            
              if abs(Pc[0]-PC[0]) < 1 and abs(Pc[1]-PC[1]) < 1 and abs(Pc[2]-PC[2]) < 1 and abs(Pc[3]-PC[3]) < 0.1 and abs(Pc[4]-PC[4]) < 0.1 :

               ecaf3.append(ecaf1[i])

               break

        if len(ecaf3) != len(ecaf1) :
                                        disc += "\n -> data(ECAF) != data(ECAF) "
                
     elif "ECAF" not in IDT:

        for i in range ( 0 , len(ecaf1) ):
                
            if abs(xtrv1['px'][ecaf1['a'][i]] - xtrv2['px'][ecaf2['a'][i]]) >= 1 or abs(xtrv1['py'][ecaf1['a'][i]] - xtrv2['py'][ecaf2['a'][i]]) >= 1 or abs(xtrv1['pz'][ecaf1['a'][i]] - xtrv2['pz'][ecaf2['a'][i]]) >= 1 or abs(xtrv1['u'][ecaf1['a'][i]] - xtrv2['u'][ecaf2['a'][i]]) >= 0.1 or abs(xtrv1['v'][ecaf1['a'][i]] - xtrv2['v'][ecaf2['a'][i]]) >= 0.1 or abs(xtrv1['px'][ecaf1['b'][i]] - xtrv2['px'][ecaf2['b'][i]]) >= 1 or abs(xtrv1['py'][ecaf1['b'][i]] - xtrv2['py'][ecaf2['b'][i]]) >= 1 or abs(xtrv1['pz'][ecaf1['b'][i]] - xtrv2['pz'][ecaf2['b'][i]]) >= 1 or abs(xtrv1['u'][ecaf1['b'][i]] - xtrv2['u'][ecaf2['b'][i]]) >= 0.1 or abs(xtrv1['v'][ecaf1['b'][i]] - xtrv2['v'][ecaf2['b'][i]]) >= 0.1 or abs(xtrv1['px'][ecaf1['c'][i]] - xtrv2['px'][ecaf2['c'][i]]) >= 1 or abs(xtrv1['py'][ecaf1['c'][i]] - xtrv2['py'][ecaf2['c'][i]]) >= 1 or abs(xtrv1['pz'][ecaf1['c'][i]] - xtrv2['pz'][ecaf2['c'][i]]) >= 1 or abs(xtrv1['u'][ecaf1['c'][i]] - xtrv2['u'][ecaf2['c'][i]]) >= 0.1 or abs(xtrv1['v'][ecaf1['c'][i]] - xtrv2['v'][ecaf2['c'][i]]) >= 0.1 :

                disc += "\n -> ecaf[" + str(i) + "] != ecaf[" + str(i) + "]  " + " , " + str(ecaf1[i]) + " != " + str(ecaf2[i])



#-------------------------------------------
                
    if not reader1.find(b'PMTL'):

     if ( len(xtrv1) != len(xtrv2) ):

        disc += "\n -> len(XTRV) != len(XTRV) "

     elif "XTRV" not in IDT:

        for i in range ( 0 , len(xtrv1) ):

            if abs(xtrv1['px'][i] - xtrv2['px'][i]) >= 1 :

                disc += "\n -> xtrv['px'][" + str(i) + "] != xtrv['px'][" + str(i) + "]  " + " , " + str(xtrv1['px'][i]) + " != " + str(xtrv2['px'][i])

            if abs(xtrv1['py'][i] - xtrv2['py'][i]) >= 1 :

                disc += "\n -> xtrv['py'][" + str(i) + "] != xtrv['py'][" + str(i) + "]  " + " , " + str(xtrv1['py'][i]) + " != " + str(xtrv2['py'][i])

            if abs(xtrv1['pz'][i] - xtrv2['pz'][i]) >= 1 :

                disc += "\n -> xtrv['pz'][" + str(i) + "] != xtrv['pz'][" + str(i) + "]  " + " , " + str(xtrv1['pz'][i]) + " != " + str(xtrv2['pz'][i])

            if abs(xtrv1['nx'][i] - xtrv2['nx'][i]) >= 0.1 :

                disc += "\n -> xtrv['nx'][" + str(i) + "] != xtrv['nx'][" + str(i) + "]  " + " , " + str(xtrv1['nx'][i]) + " != " + str(xtrv2['nx'][i])

            if abs(xtrv1['ny'][i] - xtrv2['ny'][i]) >= 0.1 :

                disc += "\n -> xtrv['ny'][" + str(i) + "] != xtrv['ny'][" + str(i) + "]  " + " , " + str(xtrv1['ny'][i]) + " != " + str(xtrv2['ny'][i])

            if abs(xtrv1['nz'][i] - xtrv2['nz'][i]) >= 0.1 :

                disc += "\n -> xtrv['nz'][" + str(i) + "] != xtrv['nz'][" + str(i) + "]  " + " , " + str(xtrv1['nz'][i]) + " != " + str(xtrv2['nz'][i])

            if xtrv1['u'][i] != xtrv2['u'][i] :

                disc += "\n -> xtrv['u'][" + str(i) + "] != xtrv['u'][" + str(i) + "]  " + " , " + str(xtrv1['u'][i]) + " != " + str(xtrv2['u'][i])

            if xtrv1['v'][i] != xtrv2['v'][i] :

                disc += "\n -> xtrv['v'][" + str(i) + "] != xtrv['v'][" + str(i) + "]  " + " , " + str(xtrv1['v'][i]) + " != " + str(xtrv2['v'][i])

    else:

     V1,V2 = [],[]

     if ( True) :

             for i in range ( 0 , len(xtrv1) ):
              if ([ xtrv1['px'][i] , xtrv1['py'][i] , xtrv1['pz'][i] , xtrv1['u'][i] , xtrv1['u'][i] ]) not in V1:
                   V1.append([ xtrv1['px'][i] , xtrv1['py'][i] , xtrv1['pz'][i] , xtrv1['u'][i] , xtrv1['u'][i] ])
             for i in range ( 0 , len(xtrv2) ):
              if ([ xtrv2['px'][i] , xtrv2['py'][i] , xtrv2['pz'][i] , xtrv2['u'][i] , xtrv2['u'][i] ]) not in V2:
                   V2.append([ xtrv2['px'][i] , xtrv2['py'][i] , xtrv2['pz'][i] , xtrv2['u'][i] , xtrv2['u'][i] ])
                
     if ( len(V1) != len(V2) ):

        disc += "\n -> len(XTRV) != len(XTRV) , " + str(len(V1)) + " != " + str(len(V2))

     elif "XTRV" not in IDT:

        for i in range ( 0 , len(V1) ):

            if abs(V1[i][0] - V2[i][0]) >= 1 :

                disc += "\n -> xtrv['px'][" + str(i) + "] != xtrv['px'][" + str(i) + "]  " + " , " + str(V1[i][0]) + " != " + str(V2[i][0])

            if abs(V1[i][1] - V2[i][1]) >= 1 :

                disc += "\n -> xtrv['py'][" + str(i) + "] != xtrv['py'][" + str(i) + "]  " + " , " + str(V1[i][1]) + " != " + str(V2[i][1])

            if abs(V1[i][2] - V2[i][2]) >= 1 :

                disc += "\n -> xtrv['pz'][" + str(i) + "] != xtrv['pz'][" + str(i) + "]  " + " , " + str(V1[i][2]) + " != " + str(V2[i][2])

            if V1[i][3] != V2[i][3] :

                disc += "\n -> xtrv['u'][" + str(i) + "] != xtrv['u'][" + str(i) + "]  " + " , " + str(V1[i][3]) + " != " + str(V2[i][3])

            if V1[i][4] != V2[i][4] :

                disc += "\n -> xtrv['v'][" + str(i) + "] != xtrv['v'][" + str(i) + "]  " + " , " + str(V1[i][4]) + " != " + str(V2[i][4])

     
#-------------------------------------------

    if reader1.find(b'WOLG'):

     if ( len(wolg1) != len(wolg2) ):

        disc += "\n -> len(WOLG) != len(WOLG) "

        E += 1

     elif "WOLG" not in IDT:

        for i in range ( 0 , len(wolg1) ):
            
            if abs(wolg1['px'][i] - wolg2['px'][i]) >= 1 :

                disc += "\n -> wolg['px'][" + str(i) + "] != wolg['px'][" + str(i) + "]  " + " , " + str(wolg1['px'][i]) + " != " + str(wolg2['px'][i])

            if abs(wolg1['py'][i] - wolg2['py'][i]) >= 1 :

                disc += "\n -> wolg['py'][" + str(i) + "] != wolg['py'][" + str(i) + "]  " + " , " + str(wolg1['py'][i]) + " != " + str(wolg2['py'][i])

            if abs(wolg1['pz'][i] - wolg2['pz'][i]) >= 1 :

                disc += "\n -> wolg['pz'][" + str(i) + "] != wolg['pz'][" + str(i) + "]  " + " , " + str(wolg1['pz'][i]) + " != " + str(wolg2['pz'][i])

            if wolg1['R'][i] != wolg2['R'][i] :

                disc += "\n -> wolg['R'][" + str(i) + "] != wolg['R'][" + str(i) + "]  " + " , " + str(wolg1['R'][i]) + " != " + str(wolg2['R'][i])

            if wolg1['G'][i] != wolg2['G'][i] :

                disc += "\n -> wolg['G'][" + str(i) + "] != wolg['G'][" + str(i) + "]  " + " , " + str(wolg1['G'][i]) + " != " + str(wolg2['G'][i])

            if wolg1['B'][i] != wolg2['B'][i] :

                disc += "\n -> wolg['B'][" + str(i) + "] != wolg['B'][" + str(i) + "]  " + " , " + str(wolg1['B'][i]) + " != " + str(wolg2['B'][i])

            if wolg1['_r0'][i] != wolg2['_r0'][i] :

                disc += "\n -> wolg['_r0'][" + str(i) + "] != wolg['_r0'][" + str(i) + "]  " + " , " + str(wolg1['_r0'][i]) + " != " + str(wolg2['_r0'][i])

            if abs(wolg1['size'][i] - wolg2['size'][i]) >= 0.1 :

                disc += "\n -> wolg['size'][" + str(i) + "] != wolg['size'][" + str(i) + "]  " + " , " + str(wolg1['size'][i]) + " != " + str(wolg2['size'][i])


#-------------------------------------------

    if reader1.find(b'HSMC'):

     V1,V2 = [],[]

     if ( True ) :

             for i in range ( 0 , len(xtvc1) ):
              if ([ xtvc1['px'][i] , xtvc1['py'][i] , xtvc1['pz'][i] ]) not in V1:
                   V1.append([ xtvc1['px'][i] , xtvc1['py'][i] , xtvc1['pz'][i] ])
             for i in range ( 0 , len(xtvc2) ):
              if ([ xtvc2['px'][i] , xtvc2['py'][i] , xtvc2['pz'][i] ]) not in V2:
                   V2.append([ xtvc2['px'][i] , xtvc2['py'][i] , xtvc2['pz'][i] ])
                
     if ( len(V1) != len(V2) ):

        disc += "\n -> len(XTVC) != len(XTVC) , " + str(len(V1)) + " != " + str(len(V2))

     elif "XTVC" not in IDT:

        for i in range ( 0 , len(V1) ):

            if abs(V1[i][0] - V2[i][0]) >= 1 :

                disc += "\n -> xtvc['px'][" + str(i) + "] != xtvc['px'][" + str(i) + "]  " + " , " + str(V1[i][0]) + " != " + str(V2[i][0])

            if abs(V1[i][1] - V2[i][1]) >= 1 :

                disc += "\n -> xtvc['py'][" + str(i) + "] != xtvc['py'][" + str(i) + "]  " + " , " + str(V1[i][1]) + " != " + str(V2[i][1])

            if abs(V1[i][2] - V2[i][2]) >= 1 :

                disc += "\n -> xtvc['pz'][" + str(i) + "] != xtvc['pz'][" + str(i) + "]  " + " , " + str(V1[i][2]) + " != " + str(V2[i][2])


#-------------------------------------------

     if ( len(ecfc1) != len(ecfc2) ):

        disc += "\n -> len(ECFC) != len(ECFC) "

        E += 1

     elif "ECFC" not in IDT:

        for i in range ( 0 , len(ecfc1) ):

            if abs(xtvc1['px'][ecfc1['a'][i]] - xtvc2['px'][ecfc2['a'][i]]) >= 1 and abs(xtvc1['py'][ecfc1['a'][i]] - xtvc2['py'][ecfc2['a'][i]]) >= 1 and abs(xtvc1['pz'][ecfc1['a'][i]] - xtvc2['pz'][ecfc2['a'][i]]) >= 1 :

                disc += "\n -> ecfc['a'][" + str(i) + "] != ecfc['a'][" + str(i) + "]  " + " , " + str(ecfc1['a'][i]) + " != " + str(ecfc2['a'][i])

            if abs(xtvc1['px'][ecfc1['b'][i]] - xtvc2['px'][ecfc2['b'][i]]) >= 1 and abs(xtvc1['py'][ecfc1['b'][i]] - xtvc2['py'][ecfc2['b'][i]]) >= 1 and abs(xtvc1['pz'][ecfc1['b'][i]] - xtvc2['pz'][ecfc2['b'][i]]) >= 1 :

                disc += "\n -> ecfc['b'][" + str(i) + "] != ecfc['b'][" + str(i) + "]  " + " , " + str(ecfc1['b'][i]) + " != " + str(ecfc2['b'][i])

            if abs(xtvc1['px'][ecfc1['c'][i]] - xtvc2['px'][ecfc2['c'][i]]) >= 1 and abs(xtvc1['py'][ecfc1['c'][i]] - xtvc2['py'][ecfc2['c'][i]]) >= 1 and abs(xtvc1['pz'][ecfc1['c'][i]] - xtvc2['pz'][ecfc2['c'][i]]) >= 1 :

                disc += "\n -> ecfc['c'][" + str(i) + "] != ecfc['c'][" + str(i) + "]  " + " , " + str(ecfc1['c'][i]) + " != " + str(ecfc2['c'][i])

            if ecfc1['_mat'][i] != ecfc2['_mat'][i] :
                                                    disc += "\n -> ecfc['_mat'][" + str(i) + "] != ecfc['_mat'][" + str(i) + "]  " + " , " + str(ecfc1['_mat'][i]) + " != " + str(ecfc2['_mat'][i])
            if ecfc1['_lmp'][i] != ecfc2['_lmp'][i] :
                                                    disc += "\n -> ecfc['_lmp'][" + str(i) + "] != ecfc['_lmp'][" + str(i) + "]  " + " , " + str(ecfc1['_lmp'][i]) + " != " + str(ecfc2['_lmp'][i])

#-------------------------------------------

     if ( len(tamc1) != len(tamc2) ):

        disc += "\n -> len(TAMC) != len(TAMC) "

        E += 1

     elif "TAMC" not in IDT:

        for i in range ( 0 , len(tamc1) ):

            if tamc1['opacity'][i] != tamc2['opacity'][i] :

                disc += "\n -> tamc['opacity'][" + str(i) + "] != tamc['opacity'][" + str(i) + "]  " + " , "+str(tamc1['opacity'][i])+" != " + str(tamc2['opacity'][i])

            if tamc1['portal'][i] != tamc2['portal'][i] :

                disc += "\n -> tamc['portal'][" + str(i) + "] != tamc['portal'][" + str(i) + "]  " + " , " + str(tamc1['portal'][i]) + " != " + str(tamc2['portal'][i])

            if tamc1['diffuse'][i] != tamc2['diffuse'][i] :

                disc += "\n -> tamc['diffuse'][" + str(i) + "] != tamc['diffuse'][" + str(i) + "]  " + " , "+str(tamc1['diffuse'][i])+" != " + str(tamc2['diffuse'][i])

            if tamc1['mat_id'][i] != tamc2['mat_id'][i] :

                disc += "\n -> tamc['mat_id'][" + str(i) + "] != tamc['mat_id'][" + str(i) + "]  " + " , " + str(tamc1['mat_id'][i]) + " != " + str(tamc2['mat_id'][i])
                

#-------------------------------------------

     if ( len(hpsc1) != len(hpsc2) ):

        disc += "\n -> len(HPSC) != len(HPSC) "

     elif "HPSC" not in IDT:

        hpsc3 = [] 

        for i in range ( 0 , len(hpsc1) ):

         for j in range ( 0 , len(hpsc2) ):

          if hpsc1['_0'][i] == hpsc2['_0'][j] and hpsc1['_1'][i] == hpsc2['_1'][j] :

           if abs(hpsc1['px'][i] - hpsc2['px'][j]) < 1 and abs(hpsc1['py'][i] - hpsc2['py'][j]) < 1 :

             if abs(hpsc1['pz'][i] - hpsc2['pz'][j]) < 1 and abs(hpsc1['size'][i] - hpsc2['size'][j]) < 1 :

               hpsc3.append(hpsc1[i])

               break

        if ( len(hpsc3) != len(hpsc1) ):

            disc += ""#"\n -> data(HPSC) != data(HPSC) "
                

#-------------------------------------------

    if reader1.find(b'HPRM'):                                                                             

     if ( len(hprm1) != len(hprm2) ):

        disc += "\n -> len(HPRM) != len(HPRM) "

     elif "HPRM" not in IDT:

        hprm3 = [] 

        for i in range ( 0 , len(hprm1) ):

         for j in range ( 0 , len(hprm2) ):

          if ( hprm1['_Vn'][i] == hprm2['_Vn'][j] ):

           if (  abs(hprm1['_px'][i] - hprm2['_px'][j]) < 1 and abs(hprm1['_py'][i] - hprm2['_py'][j]) < 1 and abs(hprm1['_pz'][i] - hprm2['_pz'][j]) < 1 ):

            hprm3.append(hprm1[i])

        if ( len(hprm1) != len(hprm3) ):

            disc += "\n -> data(HPRM) != data(HPRM) "



# --------------------------------------------


    return disc




# ___________________________________________


def fromM1(srcpth1,srcpth2,M):

    E,Et,disc,IDT = 0,"","",[]
    
    reader1 = reader_ilff.open(srcpth1)
    reader2 = reader_ilff.open(srcpth2)
    
    hsem1 = parse_hsem(reader1.read(b'HSEM'))
    hsem2 = parse_hsem(reader2.read(b'HSEM'))
    
    manb1 = parse_manb(reader1.read(b'MANB'))
    manb2 = parse_manb(reader2.read(b'MANB'))
    
    rech1 = parse_reih(reader1.read(b'REIH'))[0]
    rech2 = parse_reih(reader2.read(b'REIH'))[0]
    
    reih1 = parse_reih(reader1.read(b'REIH'))[1]
    reih2 = parse_reih(reader2.read(b'REIH'))[1]
    
    atta1 = parse_atta(reader1.read(b'ATTA'))
    atta2 = parse_atta(reader2.read(b'ATTA'))
    
    xtvm1 = parse_xtvm(reader1.read(b'XTVM'))
    xtvm2 = parse_xtvm(reader2.read(b'XTVM'))
    
    trop1 = parse_trop(reader1.read(b'TROP'))
    trop2 = parse_trop(reader2.read(b'TROP'))
    
    xvtp1 = parse_xvtp(reader1.read(b'XVTP'))
    xvtp2 = parse_xvtp(reader2.read(b'XVTP'))
    
    cftp1 = parse_cftp(reader1.read(b'CFTP'))
    cftp2 = parse_cftp(reader2.read(b'CFTP'))

    ecaf1 = parse_ecaf(reader1.read(b'ECAF'))
    ecaf2 = parse_ecaf(reader2.read(b'ECAF'))
    
    d3dr1 = parse_d3dr(reader1.read(b'D3DR'),1)
    d3dr2 = parse_d3dr(reader2.read(b'D3DR'),1)
        
    dner1 = parse_dner(reader1.read(b'DNER'),1)
    dner2 = parse_dner(reader2.read(b'DNER'),1)
        
    xtrv1 = parse_xtrv(reader1.read(b'XTRV'),1)
    xtrv2 = parse_xtrv(reader2.read(b'XTRV'),1)

    if reader1.find(b'HPRM'):
        
        hprm1 = parse_hprm(reader1.read(b'HPRM'))[1]
        hprm2 = parse_hprm(reader2.read(b'HPRM'))[1]
    
    if reader1.find(b'HSMC'):
    
        xtvc1 = parse_xtvc(reader1.read(b'XTVC'),0)
        xtvc2 = parse_xtvc(reader2.read(b'XTVC'),0)
    
        ecfc1 = parse_ecfc(reader1.read(b'ECFC',0))
        ecfc2 = parse_ecfc(reader2.read(b'ECFC',0))
    
        tamc1 = parse_tamc(reader1.read(b'TAMC',0))
        tamc2 = parse_tamc(reader2.read(b'TAMC',0))
    
        hpsc1 = parse_hpsc(reader1.read(b'HPSC',0))
        hpsc2 = parse_hpsc(reader2.read(b'HPSC',0))

#-------------------------------------------

    IDT = [ "HSEM" , "HPSC" ]

#-------------------------------------------

    if ( len(hsem1) != len(hsem2) ):

        disc += "\n -> len(HSEM) != len(HSEM) "

        E += 1

    elif "HSEM" not in IDT:

        for i in range ( 0 , len(hsem1) ):

            if hsem1['model_type'][i] != hsem2['model_type'][i] :

                disc += "\n -> hsem['model_type'][" + str(i) + "] != hsem['model_type'][" + str(i) + "]  " + " , " + str(hsem1['model_type'][i]) + " != " + str(hsem2['model_type'][i])

            if abs(hsem1['_0'][i] - hsem2['_0'][i]) >= 1 :

                disc += "\n -> hsem['_0'][" + str(i) + "] != hsem['_0'][" + str(i) + "]  " + " , " + str(hsem1['_0'][i]) + " != " + str(hsem2['_0'][i])

#-------------------------------------------

    if ( len(manb1) != len(manb2) ):

        disc += "\n -> len(REIH) != len(REIH) "

        E += 1

    else:

        for i in range ( 0 , len(reih1) ):
            
            if manb1['bone_name'][i] != manb2['bone_name'][i] :

                disc += "\n -> manb['b_name']["+ str(i) +"] != manb['b_name'][" + str(i) + "]  " + " , " + str(manb1['bone_name'][i]) + " != " + str(manb2['bone_name'][i])
            
            if rech1['num_child'][i] != rech2['num_child'][i] :

                disc += "\n -> reih1['n_ch'][" + str(i) + "] != reih1['n_ch'][" + str(i) + "]  " + " , " + str(rech1['num_child'][i]) + " != " + str(rech2['num_child'][i])
            
            if abs(reih1['px'][i] - reih2['px'][i]) >= 1 :

                disc += "\n -> reih2['px'][" + str(i) + "] != reih2['px'][" + str(i) + "]  " + " , " + str(reih1['px'][i]) + " != " + str(reih2['px'][i])

            if abs(reih1['py'][i] - reih2['py'][i]) >= 1 :

                disc += "\n -> reih2['py'][" + str(i) + "] != reih2['py'][" + str(i) + "]  " + " , " + str(reih1['py'][i]) + " != " + str(reih2['py'][i])

            if abs(reih1['pz'][i] - reih2['pz'][i]) >= 1 :

                disc += "\n -> reih2['pz'][" + str(i) + "] != reih2['pz'][" + str(i) + "]  " + " , " + str(reih1['pz'][i]) + " != " + str(reih2['pz'][i])
                
    
#-------------------------------------------

    if ( len(atta1) != len(atta2) ):

        disc += "\n -> len(ATTA) != len(ATTA) "

        E += 1

    elif "ATTA" not in IDT:

        for i in range ( 0 , len(atta1) ):
            
            if atta1['name'][i] != atta2['name'][i] :

                disc += "\n -> atta['name'][" + str(i) + "] != atta['name'][" + str(i) + "]  " + " , " + str(atta1['name'][i]) + " != " + str(atta2['name'][i])

            if abs(atta1['px'][i] - atta2['px'][i]) >= 1 :

                disc += "\n -> atta['px'][" + str(i) + "] != atta['px'][" + str(i) + "]  " + " , " + str(atta1['px'][i]) + " != " + str(atta2['px'][i])

            if abs(atta1['py'][i] - atta2['py'][i]) >= 1 :

                disc += "\n -> atta['py'][" + str(i) + "] != atta['py'][" + str(i) + "]  " + " , " + str(atta1['py'][i]) + " != " + str(atta2['py'][i])

            if abs(atta1['pz'][i] - atta2['pz'][i]) >= 1 :

                disc += "\n -> atta['pz'][" + str(i) + "] != atta['pz'][" + str(i) + "]  " + " , " + str(atta1['pz'][i]) + " != " + str(atta2['pz'][i])

            if atta1['_00'][i] != atta2['_00'][i] :

                disc += "\n -> atta['_00'][" + str(i) + "] != atta['_00'][" + str(i) + "]  " + " , " + str(atta1['_00'][i]) + " != " + str(atta2['_00'][i])

            if atta1['_01'][i] != atta2['_01'][i] :

                disc += "\n -> atta['_01'][" + str(i) + "] != atta['_01'][" + str(i) + "]  " + " , " + str(atta1['_01'][i]) + " != " + str(atta2['_01'][i])

            if atta1['_02'][i] != atta2['_02'][i] :

                disc += "\n -> atta['_02'][" + str(i) + "] != atta['_02'][" + str(i) + "]  " + " , " + str(atta1['_02'][i]) + " != " + str(atta2['_02'][i])

            if atta1['_09'][i] != atta2['_09'][i] :

                disc += "\n -> atta['_09'][" + str(i) + "] != atta['_09'][" + str(i) + "]  " + " , " + str(atta1['_09'][i]) + " != " + str(atta2['_09'][i])

            if atta1['_an'][i] != atta2['_an'][i] :

                disc += "\n -> atta['_an'][" + str(i) + "] != atta['_an'][" + str(i) + "]  " + " , " + str(atta1['_an'][i]) + " != " + str(atta2['_an'][i])
                
  
#-------------------------------------------

    if ( len(xtvm1) != len(xtvm2) ):

        disc += "\n -> len(XTVM) != len(XTVM) "

        E += 1

    elif "XTVM" not in IDT:

        for i in range ( 0 , len(xtvm1) ):
            

            if abs(xtvm1['px'][i] - xtvm2['px'][i]) >= 1 :

                disc += "\n -> xtvm['px'][" + str(i) + "] != xtvm['px'][" + str(i) + "]  " + " , " + str(xtvm1['px'][i]) + " != " + str(xtvm2['px'][i])

            if abs(xtvm1['py'][i] - xtvm2['py'][i]) >= 1 :

                disc += "\n -> xtvm['py'][" + str(i) + "] != xtvm['py'][" + str(i) + "]  " + " , " + str(xtvm1['py'][i]) + " != " + str(xtvm2['py'][i])

            if abs(xtvm1['pz'][i] - xtvm2['pz'][i]) >= 1 :

                disc += "\n -> xtvm['pz'][" + str(i) + "] != xtvm['pz'][" + str(i) + "]  " + " , " + str(xtvm1['pz'][i]) + " != " + str(xtvm2['pz'][i])

            if xtvm1['_0'][i] != xtvm2['_0'][i] :

                disc += "\n -> xtvm['_0'][" + str(i) + "] != xtvm['_0'][" + str(i) + "]  " + " , " + str(xtvm1['_0'][i]) + " != " + str(xtvm2['_0'][i])
                

#-------------------------------------------

    if ( len(trop1) != len(trop2) ):

        disc += "\n -> len(TROP) != len(TROP) "

        E += 1

    elif "TROP" not in IDT:

        for i in range ( 0 , len(trop1) ):

            if trop1['o_vertex'][i] != trop2['o_vertex'][i] :

                disc += "\n -> trop['o_vertex'][" + str(i) + "] != trop['o_vertex'][" + str(i) + "]  " + " , " + str(trop1['o_vertex'][i]) + " != " + str(trop2['o_vertex'][i])

            if trop1['n_vertex'][i] != trop2['n_vertex'][i] :

                disc += "\n -> trop['n_vertex'][" + str(i) + "] != trop['n_vertex'][" + str(i) + "]  " + " , " + str(trop1['n_vertex'][i]) + " != " + str(trop2['n_vertex'][i])

            if trop1['o_face'][i] != trop2['o_face'][i] :

                disc += "\n -> trop['o_face'][" + str(i) + "] != trop['o_face'][" + str(i) + "]  " + " , " + str(trop1['o_face'][i]) + " != " + str(trop2['o_face'][i])

            if trop1['n_face'][i] != trop2['n_face'][i] :

                disc += "\n -> trop['n_face'][" + str(i) + "] != trop['n_face'][" + str(i) + "]  " + " , " + str(trop1['n_face'][i]) + " != " + str(trop2['n_face'][i])

            if trop1['id'][i] != trop2['id'][i] :

                disc += "\n -> trop['id'][" + str(i) + "] != trop['id'][" + str(i) + "]  " + " , " + str(trop1['id'][i]) + " != " + str(trop2['id'][i])
                
                                                                                                                                              
#-------------------------------------------

    if ( len(xvtp1) != len(xvtp2) ):

        disc += "\n -> len(XVTP) != len(XVTP) "

        E += 1

    elif "XTVP" not in IDT:

        for i in range ( 0 , len(xvtp1) ):

            if abs(xvtp1['px'][i] - xvtp2['px'][i]) >= 1 :

                disc += "\n -> xvtp['px'][" + str(i) + "] != xvtp['px'][" + str(i) + "]  " + " , " + str(xvtp1['px'][i]) + " != " + str(xvtp2['px'][i])

            if abs(xvtp1['py'][i] - xvtp2['py'][i]) >= 1 :

                disc += "\n -> xvtp['py'][" + str(i) + "] != xvtp['py'][" + str(i) + "]  " + " , " + str(xvtp1['py'][i]) + " != " + str(xvtp2['py'][i])

            if abs(xvtp1['pz'][i] - xvtp2['pz'][i]) >= 1 :

                disc += "\n -> xvtp['pz'][" + str(i) + "] != xvtp['pz'][" + str(i) + "]  " + " , " + str(xvtp1['pz'][i]) + " != " + str(xvtp2['pz'][i])

                                                                                                                                              
#-------------------------------------------

    if ( len(cftp1) != len(cftp2) ):

        disc += "\n -> len(CFTP) != len(CFTP) "

        E += 1

    elif "CFTP" not in IDT:

        for i in range ( 0 , len(cftp1) ):

            if cftp1['a'][i] != cftp2['a'][i] :

                disc += "\n -> cftp['a'][" + str(i) + "] != cftp['a'][" + str(i) + "]  " + " , " + str(cftp1['a'][i]) + " != " + str(cftp2['a'][i])

            if cftp1['b'][i] != cftp2['b'][i] :

                disc += "\n -> cftp['b'][" + str(i) + "] != cftp['b'][" + str(i) + "]  " + " , " + str(cftp1['b'][i]) + " != " + str(cftp2['b'][i])

            if cftp1['c'][i] != cftp2['c'][i] :

                disc += "\n -> cftp['c'][" + str(i) + "] != cftp['c'][" + str(i) + "]  " + " , " + str(cftp1['c'][i]) + " != " + str(cftp2['c'][i])
                
                             
#-------------------------------------------

    if ( len(d3dr1) != len(d3dr2) ):

        disc += "\n -> len(D3DR) != len(D3DR) "

        E += 1

    else:

        for i in range ( 0 , len(d3dr1) ):
            
            if d3dr1['num_face'][i] != d3dr2['num_face'][i] :

                disc += "\n -> d3dr['num_face'][" + str(i) + "] != d3dr['num_face'][" + str(i) + "]  " + " , " + str(d3dr1['num_face'][i]) + " != " + str(d3dr2['num_face'][i])

            if d3dr1['num_mesh'][i] != d3dr2['num_mesh'][i] :

                disc += "\n -> d3dr['num_mesh'][" + str(i) + "] != d3dr['num_mesh'][" + str(i) + "]  " + " , " + str(d3dr1['num_mesh'][i]) + " != " + str(d3dr2['num_mesh'][i])

            if d3dr1['verts_0'][i] != d3dr2['verts_0'][i] :

                disc += "\n -> d3dr['verts_0'][" + str(i) + "] != d3dr['verts_0'][" + str(i) + "]  " + " , " + str(d3dr1['verts_0'][i]) + " != " + str(d3dr2['verts_0'][i])

            if d3dr1['verts_1'][i] != d3dr2['verts_1'][i] :

                disc += "\n -> d3dr['verts_1'][" + str(i) + "] != d3dr['verts_1'][" + str(i) + "]  " + " , " + str(d3dr1['verts_1'][i]) + " != " + str(d3dr2['verts_1'][i])

            if d3dr1['num_verts'][i] != d3dr2['num_verts'][i] :

                disc += "\n -> d3dr['num_verts'][" + str(i) + "] != d3dr['num_verts'][" + str(i) + "]  " + " , " + str(d3dr1['num_verts'][i]) + " != " + str(d3dr2['num_verts'][i])
                

#-------------------------------------------

    if True :

     if ( len(ecaf1) != len(ecaf2) ):

        disc += "\n -> len(ECAF) != len(ECAF) "

        E += 1

     elif "ECAF" not in IDT:

        for i in range ( 0 , len(ecaf1) ):
            
            if abs(xtrv1['px'][ecaf1['a'][i]] - xtrv2['px'][ecaf2['a'][i]]) >= 1 and abs(xtrv1['py'][ecaf1['a'][i]] - xtrv2['py'][ecaf2['a'][i]]) >= 1 and abs(xtrv1['pz'][ecaf1['a'][i]] - xtrv2['pz'][ecaf2['a'][i]]) >= 1 and abs(xtrv1['u'][ecaf1['a'][i]] - xtrv2['u'][ecaf2['a'][i]]) >= 0.0 and abs(xtrv1['v'][ecaf1['a'][i]] - xtrv2['v'][ecaf2['a'][i]]) >= 0.0 :

                disc += "\n -> ecaf['a'][" + str(i) + "] != ecaf['a'][" + str(i) + "]  " + " , " + str(ecaf1['a'][i]) + " != " + str(ecaf2['a'][i])

            if abs(xtrv1['px'][ecaf1['b'][i]] - xtrv2['px'][ecaf2['b'][i]]) >= 1 and abs(xtrv1['py'][ecaf1['b'][i]] - xtrv2['py'][ecaf2['b'][i]]) >= 1 and abs(xtrv1['pz'][ecaf1['b'][i]] - xtrv2['pz'][ecaf2['b'][i]]) >= 1 and abs(xtrv1['u'][ecaf1['b'][i]] - xtrv2['u'][ecaf2['b'][i]]) >= 0.0 and abs(xtrv1['v'][ecaf1['b'][i]] - xtrv2['v'][ecaf2['b'][i]]) >= 0.0 :

                disc += "\n -> ecaf['b'][" + str(i) + "] != ecaf['b'][" + str(i) + "]  " + " , " + str(ecaf1['b'][i]) + " != " + str(ecaf2['b'][i])

            if abs(xtrv1['px'][ecaf1['c'][i]] - xtrv2['px'][ecaf2['c'][i]]) >= 1 and abs(xtrv1['py'][ecaf1['c'][i]] - xtrv2['py'][ecaf2['c'][i]]) >= 1 and abs(xtrv1['pz'][ecaf1['c'][i]] - xtrv2['pz'][ecaf2['c'][i]]) >= 1 and abs(xtrv1['u'][ecaf1['c'][i]] - xtrv2['u'][ecaf2['c'][i]]) >= 0.0 and abs(xtrv1['v'][ecaf1['c'][i]] - xtrv2['v'][ecaf2['c'][i]]) >= 0.0 :

                disc += "\n -> ecaf['c'][" + str(i) + "] != ecaf['c'][" + str(i) + "]  " + " , " + str(ecaf1['c'][i]) + " != " + str(ecaf2['c'][i])

#-------------------------------------------

    if not reader1.find(b'PMTL'):

     if ( len(dner1) != len(dner2) ):

        disc += "\n -> len(DNER) != len(DNER) "

        E += 1

     elif "DNER" not in IDT:

        for i in range ( 0 , len(dner1) ):

            if dner1['_opacity'][i] != dner2['_opacity'][i] :

                disc += "\n -> dner['_opacity'][" + str(i) + "] != dner['_opacity'][" + str(i) + "]  " + " , " + str(dner1['_opacity'][i]) + " != " + str(dner2['_opacity'][i])

            if dner1['_mshine'][i] != dner2['_mshine'][i] :

                disc += "\n -> dner['_mshine'][" + str(i) + "] != dner['_mshine'][" + str(i) + "]  " + " , " + str(dner1['_mshine'][i]) + " != " + str(dner2['_mshine'][i])

            if dner1['_Scolor'][i] != dner2['_Scolor'][i] :

                disc += "\n -> dner['_Scolor'][" + str(i) + "] != dner['_Scolor'][" + str(i) + "]  " + " , " + str(dner1['_Scolor'][i]) + " != " + str(dner2['_Scolor'][i])

            if dner1['_Opacitd'][i] != dner2['_Opacitd'][i] :

                disc += "\n -> dner['_Opacitd'][" + str(i) + "] != dner['_Opacitd'][" + str(i) + "]  " + " , " + str(dner1['_Opacitd'][i]) + " != " + str(dner2['_Opacitd'][i])

            if dner1['num_face'][i] != dner2['num_face'][i] :

                disc += "\n -> dner['num_face'][" + str(i) + "] != dner['num_face'][" + str(i) + "]  " + " , " + str(dner1['num_face'][i]) + " != " + str(dner2['num_face'][i])

            if dner1['_td'][i] != dner2['_td'][i] :

                disc += "\n -> dner['_td'][" + str(i) + "] != dner['_td'][" + str(i) + "]  " + " , " + str(dner1['_td'][i]) + " != " + str(dner2['_td'][i])

            if dner1['_tb'][i] != dner2['_tb'][i] :

                disc += "\n -> dner['_tb'][" + str(i) + "] != dner['_tb'][" + str(i) + "]  " + " , " + str(dner1['_tb'][i]) + " != " + str(dner2['_tb'][i])

            if dner1['_tr'][i] != dner2['_tr'][i] :

                disc += "\n -> dner['_tr'][" + str(i) + "] != dner['_tr'][" + str(i) + "]  " + " , " + str(dner1['_tr'][i]) + " != " + str(dner2['_tr'][i])

            if dner1['_trd'][i] != dner2['_trd'][i] :

                disc += "\n -> dner['_trd'][" + str(i) + "] != dner['_trd'][" + str(i) + "]  " + " , " + str(dner1['_trd'][i]) + " != " + str(dner2['_trd'][i])

            if dner1['_tbd'][i] != dner2['_tbd'][i] :

                disc += "\n -> dner['_tbd'][" + str(i) + "] != dner['_tbd'][" + str(i) + "]  " + " , " + str(dner1['_tbd'][i]) + " != " + str(dner2['_tbd'][i])
                

#-------------------------------------------

    if ( len(xtrv1) != len(xtrv2) ):

        disc += "\n -> len(XTRV) != len(XTRV) "

        E += 1

    else:

        for i in range ( 0 , len(xtrv1) ):

            if abs(xtrv1['px'][i] - xtrv2['px'][i]) >= 1 :

                disc += "\n -> xtrv['px'][" + str(i) + "] != xtrv['px'][" + str(i) + "]  " + " , " + str(xtrv1['px'][i]) + " != " + str(xtrv2['px'][i])

            if abs(xtrv1['py'][i] - xtrv2['py'][i]) >= 1 :

                disc += "\n -> xtrv['py'][" + str(i) + "] != xtrv['py'][" + str(i) + "]  " + " , " + str(xtrv1['py'][i]) + " != " + str(xtrv2['py'][i])

            if abs(xtrv1['pz'][i] - xtrv2['pz'][i]) >= 1 :

                disc += "\n -> xtrv['pz'][" + str(i) + "] != xtrv['pz'][" + str(i) + "]  " + " , " + str(xtrv1['pz'][i]) + " != " + str(xtrv2['pz'][i])

            if abs(xtrv1['nx'][i] - xtrv2['nx'][i]) >= 0.1 :

                disc += "\n -> xtrv['nx'][" + str(i) + "] != xtrv['nx'][" + str(i) + "]  " + " , " + str(xtrv1['nx'][i]) + " != " + str(xtrv2['nx'][i])

            if abs(xtrv1['ny'][i] - xtrv2['ny'][i]) >= 0.1 :

                disc += "\n -> xtrv['ny'][" + str(i) + "] != xtrv['ny'][" + str(i) + "]  " + " , " + str(xtrv1['ny'][i]) + " != " + str(xtrv2['ny'][i])

            if abs(xtrv1['nz'][i] - xtrv2['nz'][i]) >= 0.1 :

                disc += "\n -> xtrv['nz'][" + str(i) + "] != xtrv['nz'][" + str(i) + "]  " + " , " + str(xtrv1['nz'][i]) + " != " + str(xtrv2['nz'][i])

            if xtrv1['u'][i] != xtrv2['u'][i] :

                disc += "\n -> xtrv['u'][" + str(i) + "] != xtrv['u'][" + str(i) + "]  " + " , " + str(xtrv1['u'][i]) + " != " + str(xtrv2['u'][i])

            if xtrv1['v'][i] != xtrv2['v'][i] :

                disc += "\n -> xtrv['v'][" + str(i) + "] != xtrv['v'][" + str(i) + "]  " + " , " + str(xtrv1['v'][i]) + " != " + str(xtrv2['v'][i])

            if xtrv1['w'][i] != xtrv2['w'][i] :

                disc += "\n -> xtrv['w'][" + str(i) + "] != xtrv['w'][" + str(i) + "]  " + " , " + str(xtrv1['w'][i]) + " != " + str(xtrv2['w'][i]) 

            if xtrv1['vn'][i] != xtrv2['vn'][i] :

                disc += "\n -> xtrv['vn'][" + str(i) + "] != xtrv['vn'][" + str(i) + "]  " + " , " + str(xtrv1['vn'][i]) + " != " + str(xtrv2['vn'][i]) 

            if xtrv1['bn'][i] != xtrv2['bn'][i] :

                disc += "\n -> xtrv['bn'][" + str(i) + "] != xtrv['bn'][" + str(i) + "]  " + " , " + str(xtrv1['bn'][i]) + " != " + str(xtrv2['bn'][i])

     
#-------------------------------------------

    if reader1.find(b'HSMC'):

     if ( len(xtvc1) != len(xtvc2) ):

        disc += "\n -> len(XTVC) != len(XTVC) , " + str(len(xtvc1)) + " != " + str(len(xtvc2))

        E += 1

     elif "XTVC" not in IDT:

        for i in range ( 0 , len(xtvc1) ):

            if abs(xtvc1['px'][i] - xtvc2['px'][i]) >= 1 :

                disc += "\n -> xtvc['px'][" + str(i) + "] != xtvc['px'][" + str(i) + "]  " + " , " + str(xtvc1['px'][i]) + " != " + str(xtvc2['px'][i])

            if abs(xtvc1['py'][i] - xtvc2['py'][i]) >= 1 :

                disc += "\n -> xtvc['py'][" + str(i) + "] != xtvc['py'][" + str(i) + "]  " + " , " + str(xtvc1['py'][i]) + " != " + str(xtvc2['py'][i])

            if abs(xtvc1['pz'][i] - xtvc2['pz'][i]) >= 1 :

                disc += "\n -> xtvc['pz'][" + str(i) + "] != xtvc['pz'][" + str(i) + "]  " + " , " + str(xtvc1['pz'][i]) + " != " + str(xtvc2['pz'][i])


#-------------------------------------------

     if ( len(ecfc1) != len(ecfc2) ):

        disc += "\n -> len(ECFC) != len(ECFC) "

        E += 1

     elif "ECFC" not in IDT:

        for i in range ( 0 , len(ecfc1) ):

            if abs(xtvc1['px'][ecfc1['a'][i]] - xtvc2['px'][ecfc2['a'][i]]) >= 1 and abs(xtvc1['py'][ecfc1['a'][i]] - xtvc2['py'][ecfc2['a'][i]]) >= 1 and abs(xtvc1['pz'][ecfc1['a'][i]] - xtvc2['pz'][ecfc2['a'][i]]) >= 1 :

                disc += "\n -> ecfc['a'][" + str(i) + "] != ecfc['a'][" + str(i) + "]  " + " , " + str(ecfc1['a'][i]) + " != " + str(ecfc2['a'][i])

            if abs(xtvc1['px'][ecfc1['b'][i]] - xtvc2['px'][ecfc2['b'][i]]) >= 1 and abs(xtvc1['py'][ecfc1['b'][i]] - xtvc2['py'][ecfc2['b'][i]]) >= 1 and abs(xtvc1['pz'][ecfc1['b'][i]] - xtvc2['pz'][ecfc2['b'][i]]) >= 1 :

                disc += "\n -> ecfc['b'][" + str(i) + "] != ecfc['b'][" + str(i) + "]  " + " , " + str(ecfc1['b'][i]) + " != " + str(ecfc2['b'][i])

            if abs(xtvc1['px'][ecfc1['c'][i]] - xtvc2['px'][ecfc2['c'][i]]) >= 1 and abs(xtvc1['py'][ecfc1['c'][i]] - xtvc2['py'][ecfc2['c'][i]]) >= 1 and abs(xtvc1['pz'][ecfc1['c'][i]] - xtvc2['pz'][ecfc2['c'][i]]) >= 1 :

                disc += "\n -> ecfc['c'][" + str(i) + "] != ecfc['c'][" + str(i) + "]  " + " , " + str(ecfc1['c'][i]) + " != " + str(ecfc2['c'][i])

            if ecfc1['_mat'][i] != ecfc2['_mat'][i] :
                                                    disc += "\n -> ecfc['_mat'][" + str(i) + "] != ecfc['_mat'][" + str(i) + "]  " + " , " + str(ecfc1['_mat'][i]) + " != " + str(ecfc2['_mat'][i])
                                                    
            if ecfc1['_lmp'][i] != ecfc2['_lmp'][i] :
                                                    disc += "\n -> ecfc['_lmp'][" + str(i) + "] != ecfc['_lmp'][" + str(i) + "]  " + " , " + str(ecfc1['_lmp'][i]) + " != " + str(ecfc2['_lmp'][i])

#-------------------------------------------

     if ( len(tamc1) != len(tamc2) ):

        disc += "\n -> len(TAMC) != len(TAMC) "

        E += 1

     elif "TAMC" not in IDT:

        for i in range ( 0 , len(tamc1) ):

            if tamc1['opacity'][i] != tamc2['opacity'][i] :

                disc += "\n -> tamc['opacity'][" + str(i) + "] != tamc['opacity'][" + str(i) + "]  " + " , "+str(tamc1['opacity'][i])+" != " + str(tamc2['opacity'][i])

            if tamc1['portal'][i] != tamc2['portal'][i] :

                disc += "\n -> tamc['portal'][" + str(i) + "] != tamc['portal'][" + str(i) + "]  " + " , " + str(tamc1['portal'][i]) + " != " + str(tamc2['portal'][i])

            if tamc1['diffuse'][i] != tamc2['diffuse'][i] :

                disc += "\n -> tamc['diffuse'][" + str(i) + "] != tamc['diffuse'][" + str(i) + "]  " + " , "+str(tamc1['diffuse'][i])+" != " + str(tamc2['diffuse'][i])

            if tamc1['mat_id'][i] != tamc2['mat_id'][i] :

                disc += "\n -> tamc['mat_id'][" + str(i) + "] != tamc['mat_id'][" + str(i) + "]  " + " , " + str(tamc1['mat_id'][i]) + " != " + str(tamc2['mat_id'][i])

            if tamc1['unknown'][i] != tamc2['unknown'][i] :

                disc += "\n -> tamc['unk00'][" + str(i) + "] != tamc['unk00'][" + str(i) + "]  " + " , " + str(tamc1['unknown'][i]) + " != " + str(tamc2['unknown'][i])
                

#-------------------------------------------

     if ( len(hpsc1) != len(hpsc2) ):

        disc += "\n -> len(HPSC) != len(HPSC) "

        E += 1

     elif "HPSC" not in IDT:

        for i in range ( 0 , len(hpsc1) ):

            if abs(hpsc1['px'][i] - hpsc2['px'][i]) >= 1 :

                disc += "\n -> hpsc['px'][" + str(i) + "] != hpsc['px'][" + str(i) + "]  " + " , " + str(hpsc1['px'][i]) + " != " + str(hpsc2['px'][i])

            if abs(hpsc1['py'][i] - hpsc2['py'][i]) >= 1 :

                disc += "\n -> hpsc['py'][" + str(i) + "] != hpsc['py'][" + str(i) + "]  " + " , " + str(hpsc1['py'][i]) + " != " + str(hpsc2['py'][i])

            if abs(hpsc1['pz'][i] - hpsc2['pz'][i]) >= 1 :

                disc += "\n -> hpsc['pz'][" + str(i) + "] != hpsc['pz'][" + str(i) + "]  " + " , " + str(hpsc1['pz'][i]) + " != " + str(hpsc2['pz'][i])

            if abs(hpsc1['size'][i] - hpsc2['size'][i]) >= 1 :

                disc += "\n -> hpsc['size']["+str(i)+"] != hpsc['size'][" + str(i) + "]  " + " , "+str(hpsc1['size'][i])+" != " + str(hpsc2['size'][i])

            if hpsc1['_a'][i] != hpsc2['_a'][i] :

                disc += "\n -> hpsc['_a'][" + str(i) + "] != hpsc['_a'][" + str(i) + "]  " + " , " + str(hpsc1['_a'][i]) + " != " + str(hpsc2['_a'][i])

            if hpsc1['_b'][i] != hpsc2['_b'][i] :

                disc += "\n -> hpsc['_b'][" + str(i) + "] != hpsc['_b'][" + str(i) + "]  " + " , " + str(hpsc1['_b'][i]) + " != " + str(hpsc2['_b'][i])
                

#-------------------------------------------

    if reader1.find(b'HPRM'):                                                                             

     if ( len(hprm1) != len(hprm2) ):

        disc += "\n -> len(HPRM) != len(HPRM) "

        E += 1

     else:

        for i in range ( 0 , len(hprm1) ):

            if hprm1['_Vn'][i] != hprm2['_Vn'][i] :

                disc += "\n -> hprm2['_Vn'][" + str(i) + "] != hprm2['_Vn'][" + str(i) + "]  " + " , " + str(hprm1['_Vn'][i]) + " != " + str(hprm2['_Vn'][i])

            if abs(hprm1['_px'][i] - hprm2['_px'][i]) >= 1 :

                disc += "\n -> hprm2['_px'][" + str(i) + "] != hprm2['_px'][" + str(i) + "]  " + " , " + str(hprm1['_px'][i]) + " != " + str(hprm2['_px'][i])

            if abs(hprm1['_py'][i] - hprm2['_py'][i]) >= 1 :

                disc += "\n -> hprm2['_py'][" + str(i) + "] != hprm2['_py'][" + str(i) + "]  " + " , " + str(hprm1['_py'][i]) + " != " + str(hprm2['_py'][i])

            if abs(hprm1['_pz'][i] - hprm2['_pz'][i]) >= 1 :

                disc += "\n -> hprm2['_pz'][" + str(i) + "] != hprm2['_pz'][" + str(i) + "]  " + " , " + str(hprm1['_pz'][i]) + " != " + str(hprm2['_pz'][i])
                

# --------------------------------------------

    if E != 0:

     print("??????????????????????????")

    return disc




# ___________________________________________


def fromM2(srcpth1,srcpth2,M):

    E,Et,disc = 0,"",""

    reader1 = reader_ilff.open(srcpth1)
    reader2 = reader_ilff.open(srcpth2)

    sems1 = parse_sems(reader1.read(b'SEMS'))
    sems2 = parse_sems(reader2.read(b'SEMS'))
    
    xtvs1 = parse_xtvs(reader1.read(b'XTVS'))
    xtvs2 = parse_xtvs(reader2.read(b'XTVS'))
    
    cafs1 = parse_cafs(reader1.read(b'CAFS'))
    cafs2 = parse_cafs(reader2.read(b'CAFS'))

    egde1 = parse_egde(reader1.read(b'EGDE'))
    egde2 = parse_egde(reader2.read(b'EGDE'))

#-------------------------------------------

    if len(sems1) != len(sems2) :

        disc += "\n -> len(SEMS) != len(SEMS) "

        E += 1

    else:

      for m in range ( 0 , len(sems1) ):

        if sems1['index_num'][m] != sems2['index_num'][m] :

            disc += "\n -> SEMS['index_num'][" + str(m) + "] != SEMS['index_num'][" + str(m) + "]  " + " , " + str(sems1['index_num'][m]) + " != " + str(sems2['index_num'][m])
            

#-------------------------------------------

    if len(xtvs1) != len(xtvs2) :

        disc += "\n -> len(XTVS) != len(XTVS) "

        E += 1

    else:

      for i in range ( 0 , len(xtvs1) ):  

        if abs(xtvs1['px'][i] - xtvs2['px'][i]) >= 1 :

            disc += "\n -> xtvs['px'][" + str(i) + "] != xtvs['px'][" + str(i) + "]  " + " , " + str(xtvs1['px'][i]) + " != " + str(xtvs2['px'][i])

        if abs(xtvs1['py'][i] - xtvs2['py'][i]) >= 1 :

            disc += "\n -> xtvs['py'][" + str(i) + "] != xtvs['py'][" + str(i) + "]  " + " , " + str(xtvs1['py'][i]) + " != " + str(xtvs2['py'][i])

        if abs(xtvs1['pz'][i] - xtvs2['pz'][i]) >= 1 :

            disc += "\n -> xtvs['pz'][" + str(i) + "] != xtvs['pz'][" + str(i) + "]  " + " , " + str(xtvs1['pz'][i]) + " != " + str(xtvs2['pz'][i])

#-------------------------------------------

    if len(cafs1) != len(cafs2) :

        disc += "\n -> len(cafs) != len(cafs) "

        E += 1

    else:

      for m in range ( 0 , len(cafs1) ):  

        if cafs1['a'][m] != cafs2['a'][m] :

            disc += "\n -> cafs['a'][" + str(m) + "] != cafs['a'][" + str(m) + "]  " + " , " + str(cafs1['a'][m]) + " != " + str(cafs2['a'][m])

        if cafs1['b'][m] != cafs2['b'][m] :

            disc += "\n -> cafs['b'][" + str(m) + "] != cafs['b'][" + str(m) + "]  " + " , " + str(cafs1['b'][m]) + " != " + str(cafs2['b'][m])

        if cafs1['c'][m] != cafs2['c'][m] :

            disc += "\n -> cafs['c'][" + str(m) + "] != cafs['c'][" + str(m) + "]  " + " , " + str(cafs1['c'][m]) + " != " + str(cafs2['c'][m])

#-------------------------------------------

    if len(egde1) != len(egde2) :

        disc += "\n -> len(EGDE) != len(EGDE) "

        E += 1

    else:

      for i in range ( 0 , len(egde1) ):  

        if egde1['a'][i] != egde2['a'][i] :

            disc += "\n -> egde['a'][" + str(i) + "] != egde['a'][" + str(i) + "]  " + " , " + str(egde1['a'][i]) + " != " + str(egde2['a'][i])

        if egde1['b'][i] != egde2['b'][i] :

            disc += "\n -> egde['b'][" + str(i) + "] != egde['b'][" + str(i) + "]  " + " , " + str(egde1['b'][i]) + " != " + str(egde2['b'][i])

#-------------------------------------------

    return disc
# ___________________________________________
