#!/usr/bin/env python
"""This application was coded by Hakan KOCAMAN to convert the coordinates of the
Military Grid Reference System (MGRS) into WGS84 geographical coordinates using
the mgrs module at https://pypi.org/project/mgrs/. For more information and contact,
you can visit www.hakankocaman.com and send an e-mail to İletişim@hakankocaman.com."""

#-*-coding:utf-8-*-
"""
#example coordinate.txt file format for for geographic coordinates:
longitude latitude

32.850814 39.910991
32.836825 39.924765
32.853683 39.941803
32.852578 39.940583

#example coordinate.txt file format for for MGRS coordinates:
MGRS

36SVK8724917888
36SVK8605619419
36SVK8749921308
36SVK8740521172

"""


import mgrs

try:
  file=open("coordinate.txt","r+",encoding="utf-8")
  coordinate=file.readlines() 

except FileNotFoundError:
  print("coordinate.txt not found!")
  exit()

file.seek(0) #The top row operation in the coordinate.txt file

#Determining whether the coordinates are MGRS or Geographic.
firstline=file.readline()
spaceindex=firstline.find(" ")
control=firstline[spaceindex]

if control == " ":
  print ("Geographic > MGRS conversion type is selected.")
  for coor in coordinate:
      index=coor.find(" ")
      l=len(coor)
      longitude=coor[0:index]
      latitude=coor[(index+1):l]
      m = mgrs.MGRS()
      c = m.toMGRS(latitude, longitude)
      c = c.decode() #Converting byte data type to string  variable
      c=str(c)
      file2=open("coordinate_MGRS.txt","a+",encoding="utf-8")
      file2.write(c+"\n")
  file2.close()
  print("The conversion is complete. A file named coordinate_MGRS.txt was created in the same directory.")
else:
    print ("MGRS > Geographic conversion type is selected.")
    for c in coordinate:
      m = mgrs.MGRS()
      c=c.encode() #Converting string variable to byte data type
      d = m.toLatLon(c)
      d=str(d)
      index=d.find(",")
      l=len(d)
      latitude=d[1:index]
      longitude=d[(index+2):(l-1)]
      file2=open("coordinate_Geographic.txt","a+",encoding="utf-8")
      file2.write(longitude+" "+latitude+"\n")
    file2.close()
    print("The conversion is complete. A file named coordinate_Geographic.txt was created in the same directory.")
    
file.close()