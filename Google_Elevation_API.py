""" This application was written by Hakan KOCAMAN using Google Elevation API
to provide altitude information of latitude and longitude coordinates in
WGS84 datum. For more information and communication,
you can visit www.hakankocaman.com and
send an e-mail to iletisim@hakankocaman.com."""

#!/usr/bin/env python
#-*-coding:utf-8-*-

"""
#example coordinate.txt file format for WGS84 geographic coordinates:
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
  print("File coordinate.txt not found!")

apikey="Google Elevation Api Key"

if apikey=="Google Elevation Api Key":
        apikey= input ("Please enter your Google Elevation API key, otherwise, the program will not work:")
        
file.seek(0) #The process of getting to the top line in the txt file
for latlng in coordinate:
  serviceURL = "https://maps.googleapis.com/maps/api/elevation/json?locations="+latlng+"&key="+apikey
  #print(serviceURL)
  r = requests.get(serviceURL)
  #print(r.text)
  y = json.loads(r.text)
  for result in y["results"]:
    elev=result["elevation"]
    file.write((str(latlng.rstrip())+" "+str(elev))+"\n")

print ("Query completed")
file.close()
