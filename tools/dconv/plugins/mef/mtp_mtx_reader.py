import os
import io
import struct
import builtins


def read(File):

# ------------------Reading Lines From File
    
    FLINES = []

    with open(File, 'r') as FILE:

        for line in FILE:

         FLINES.append(line[:-1])

        FILE.close()


# ------------------ Reading Data From Lines


    if ( True ): 
        
        Size = []

        POS = []
    
        Header = [ "Animations (.iff)",
                   "Sounds (.wav)",
                   "Shadows (.mef)",
                   "Models (.mef)",
                   "Virtual Names",
                   "Model-Texture Info",
                   "Textures (.tex)",
                   "Palletes (.pal)",
                   "GameTypeTexture (GTT)" ]

        for i in  range ( 0 , len(FLINES) ):

          if ( FLINES[i][:2] == "\\\\" ):

            assert Header[0] == FLINES[i][3:-1], "Header -> \""+str(Header[0])+"\" Not Found in MTP File"

            for j in range ( i+1 , len(FLINES) ):

              if ( FLINES[j].find("[") != -1 and FLINES[j].find("]") != -1 ):

                  Size.append([int(i) for i in FLINES[j][1:-1].split()])

                  POS.append(j+1)

                  break

            del Header[0]


 # CHECK FOR REQUIRED FORMAT ---->
 
 
        if ( len(Size) == 8  ):
                               assert 0 != 0 , "Wrong Format in MTX File" 
 
        if ( len(POS) == 8  ):
                               assert 0 != 0 , "Wrong Format in MTX File" 





# -------------------------> Reading Animation Frame Data!


        Data = []

        for i in  range ( 0 , len(POS) ):

            if ( i in ( 0, 1, 2, 3, 4, 6, 7 ) ):

             for j in range ( POS[i] , len(FLINES) ):

              if ( FLINES[j].find("[") != -1 ):

                for k in range ( j , len(FLINES) ):

                 if ( FLINES[k].find("]") != -1 ):

                  Data.append(FLINES[j:k+1])

                  break

                break

            if ( i in ( 5, 8 ) ):

             for j in range ( POS[i] , len(FLINES) ):

              if ( FLINES[j].find("[") != -1 and FLINES[j].find("]") != -1 ):

                for k in range ( j , len(FLINES) ):

                  if ( FLINES[k][:-1] == "" ):

                    Data.append(str(FLINES[j:k]).replace("'"," "))

                    break

                break
            

# ------------------->  Converting!
 
        
        Num = [ "0","1","2","3","4","5","6","7","8","9" ]

        Float = [ "0","1","2","3","4","5","6","7","8","9",".","e","-","+" ]

        Str = [ "\'" ]

        End = [ " ",",","[","]","(",")" ]

        DATA = []

        for i in range ( 0 , len(Data) ):

            Par = []

            P = -1

            STR = str(Data[i])

            while ( P < len(STR)-1 ):

                P += 1

                if ( STR[P] in End ):

                    continue

                if ( STR[P] in Str ):

                   p = 0

                   while ( P+p < len(STR)-1 ):

                    p += 1   

                    if ( STR[P+p] in Str ):

                     Par.append(STR[P+1:P+p])

                     break
                
                   P += p
                                   
                if STR[P] in Float:

                   p = 0   

                   while ( P+p < len(STR)-1 ):

                    p += 1 

                    if ( STR[P+p] in End ):

                      if ( "." in STR[P:P+p] ):  

                        Par.append(float(STR[P:P+p]))

                      if ( "." not in STR[P:P+p] ):  

                        Par.append(int(STR[P:P+p]))

                      break
                
                   P += p

            if ( Par == ['[]'] ):
                
                DATA.append([])

            else:
                
                DATA.append(Par)


# -----------------------------------------------
                

    return [Size[0],DATA[0]],[Size[1],DATA[1]],[Size[2],DATA[2]],[Size[3],DATA[3]],[Size[4],DATA[4]],[Size[5],DATA[5]],[Size[6],DATA[6]],[Size[7],DATA[7]],[Size[8],DATA[8]]
