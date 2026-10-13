import os
import io
import struct
from .import reader_ilff
from .import mef_struct
from .mef_struct import *
from .reader_ilff import *
import numpy as np

def fromfile(File):


# Reading Data !!!!!

  if (True):
    
    reader = reader_ilff.open(File)

    Signs = [ b'HSEM' , b'ATTA' , b'XTVM' , b'TROP' , b'XVTP' , b'CFTP' , b'D3DR' , b'DNER' , b'XTRV' , b'HSMC' , b'XTVC' , b'ECFC' , b'TAMC' , b'HPSC' ]


# -------------------------------------------------
# -------------------------------------------------
#  FORMAT CONVERSION
#--------------------------------------------------
#--------------------------------------------------


  CHUNKS = []


# FORM HEADER--------------------------->


  if ( b'HSEM' in Signs ):

   DATA = b''

   SIZE = 4 + 16
  

# HSEM ----------------------->


  if ( b'HSEM' in Signs ):

   DATA += struct.pack('=1f',0.10)
   DATA += struct.pack('=7I',2002,10,5,20,15,25,300)
   DATA += struct.pack('=4I',0,0,0,0)
   DATA += struct.pack('=12f', 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0 )
   DATA += struct.pack('=6I',0,0,48,0,0,64)#
   DATA += struct.pack('=1f',0.0)
   DATA += struct.pack('=5H',1,0,0,0,0)
   DATA += struct.pack('=22B',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

   CHUNKS.append([ b'HSEM' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


# ATTA ----------------------->


  if ( b'ATTA' in Signs ):

   DATA = b''

   CHUNKS.append([ b'ATTA' , len(DATA) , 4 , len(DATA) + 16 , DATA ])   

   SIZE += len(DATA) + 16


  if ( b'XTVM' in Signs ):

   DATA = struct.pack('=3f1i',0.0,0.0,0.0,-1)

   CHUNKS.append([ b'XTVM' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16
                


# PORTLAS -------------------->


  if ( b'TROP' in Signs ):

   DATA = b''

   CHUNKS.append([ b'TROP' , len(DATA) , 4 , len(DATA) + 16 , DATA ])  

   SIZE += len(DATA) + 16  


  if ( b'XVTP' in Signs ):

   DATA = b''

   CHUNKS.append([ b'XVTP' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


  if ( b'CFTP' in Signs ):

   DATA = b''

   CHUNKS.append([ b'CFTP' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# REND. MESH DEF -------------------->


  if ( b'D3DR' in Signs ):

   DATA = struct.pack('=12I',4,0,0,0,0,0,0,0,0,0,0,0)

   CHUNKS.append([ b'D3DR' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


  if ( b'DNER' in Signs ):

   DATA = b''

   CHUNKS.append([ b'DNER' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16


  if ( b'XTRV' in Signs ):

   DATA = b''

   CHUNKS.append([ b'XTRV' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# COL MESH DEFS ----------------------->


  if ( b'HSMC' in Signs ):

   DATA = b''

   for i in range ( 0 , 1 ):

    DATA += struct.pack('=8I',0,0,0,0,0,0,0,0)

    DATA += struct.pack('=8I',0,0,0,0,0,0,0,0)

   CHUNKS.append([ b'HSMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



#  COL MESH 00 ----------------------->



  if ( b'XTVC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

  if ( b'ECFC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

  if ( b'TAMC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'TAMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

  if ( b'HPSC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'HPSC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16



# COL MESH 01 ----------------------->



  if ( b'XTVC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'XTVC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

  if ( b'ECFC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'ECFC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

  if ( b'TAMC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'TAMC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16

  if ( b'HPSC' in Signs ):

   DATA = b''

   CHUNKS.append([ b'HPSC' , len(DATA) , 4 , len(DATA) + 16 , DATA ])

   SIZE += len(DATA) + 16
   


# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------


# Data Writing !!


  Bytes = b''

  Bytes += struct.pack('=4s',b'ILFF')

  Bytes += struct.pack('=1I',SIZE)

  Bytes += struct.pack('=1I',4)

  Bytes += struct.pack('=1I',0)

  Bytes += struct.pack('=4s',b'OCEM')

  for i in range ( 0 , len(CHUNKS) ):

    Bytes += struct.pack('=4s',CHUNKS[i][0])

    Bytes += struct.pack('=1I',CHUNKS[i][1])

    Bytes += struct.pack('=1I',CHUNKS[i][2])

    if ( i != len(CHUNKS)-1 ):

     Bytes += struct.pack('=1I',CHUNKS[i][3])

    if ( i == len(CHUNKS)-1 ):

     Bytes += struct.pack('=1I',0)

    Bytes += CHUNKS[i][4]


      
# -------------------------------------------------
        
  return Bytes
