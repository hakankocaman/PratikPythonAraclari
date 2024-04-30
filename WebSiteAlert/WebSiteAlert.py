#pip install python-telegram-bot
#pip install requests
#pip install colorama

import colorama
from colorama import Fore, Style

import requests, time
print(time.strftime("%d-%m-%Y %H:%M:%S"))

telegramapi=""

try:
    with open('TelegramApi.txt', 'r') as file:
        for line in file:
            telegramapi += line.strip()

except FileNotFoundError:
  print("TelegramApi.txt not found!")
  exit()


try:
    file=open("SiteList.txt","r+",encoding="utf-8")
    sitelist=file.readlines()
  
except FileNotFoundError:
    print("SiteList.txt not found!")
    exit()

i=0
file.seek(0) 
print("The query will begin shortly...")
while True:
    if i>0:
        time.sleep(56) # 56 secons wait
    i +=1
    print(str(i)+"st query "+time.strftime("%d-%m-%Y %H:%M:%S"))
    for list in sitelist:
        index=list.find(" ")
        url=list[0:index]
        try:
            response=requests.get(url)
            response.raise_for_status()  # Throws an exception in case of error
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Something went wrong:",err)
        
        if response.status_code==200:
            print(f'{url} site is working.')
            mesaj=f'{url} site is working.'
            
        else:
            print(f'{Fore.RED}{url} site is not working.{Style.RESET_ALL}')
            mesaj=f'{url} site is not working.'

        try:
            response = requests.post(url="https://api.telegram.org/bot"+telegramapi+"/sendMessage",data={"chat_id":"443045867","text":mesaj})
            response.raise_for_status()  # Throws an exception in case of error
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Connection Error:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Something went wrong:",err)