#!/usr/bin/env python
"""This application is coded by Hakan KOCAMAN in order to make coordinate conversions
quickly via web services provided by https://epsg.io. For more information and contact,
you can visit www.hakankocaman.com and send an e-mail to İletişim@hakankocaman.com."""

#-*-coding:utf-8-*-

"""
#example coordinate.txt file format:
longitude latitude

32.850814 39.910991
32.836825 39.924765
32.853683 39.941803
32.852578 39.940583

"""

import requests, json

try:
  file=open("coordinate.txt","r+",encoding="utf-8")
  coordinate=file.readlines() 

except FileNotFoundError:
  print("coordinate.txt not found!")
  exit()


#s_srs = input("Please enter the EPSG code of the source coordinate system: ")
#t_srs = input("Please enter the EPSG code of the target coordinate system: ")

s_srs = 4326
t_srs = 5255

file.seek(0) #The top row operation in the coordinate.txt file.
for coor in coordinate:

  index=coor.find(" ")
  l=len(coor)
  s_xcoor=coor[0:index]
  s_ycoor=coor[(index+1):l]

  serviceURL = "https://epsg.io/trans?x="+str(s_xcoor)+"&y="+str(s_ycoor)+"&s_srs="+str(s_srs)+"&t_srs="+str(t_srs)
  #print (serviceURL)
  r = requests.get(serviceURL)
  #print(r.text)
  y = json.loads(r.text)

  xcoor=y["x"]
  ycoor=y["y"]
  zcoor=y["z"]
  file.write(str(xcoor)+" "+str(ycoor)+" "+str(zcoor)+"\n")
    
print ("The query is completed, new coordinate values are written to the existing file.")
file.close()
