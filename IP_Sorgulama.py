""" Bu uygulama Hakan KOCAMAN tarafından ip adreslerinin konum bilgilerinin
https://ipstack.com/ 'un sağlamış olduğu web serviler üzerinden liste halinde
hızlı bir şekilde temin edilmesi için kodlanmıştır. Daha fazla bilgi ve iletişim
için www.hakankocaman.com adresini ziyeret edebilir iletisim@hakankocaman.com
adresine e-posta atabilirsiniz."""

#!/usr/bin/env python
#-*-coding:utf-8-*-

#Sorgu işleminde kullanılacak modüller:
#(eğer modüller yüklü değil ise komut sistemine "pip install requests" komutunu kullanara yükleyebilirsiniz)
import requests, json

#Sorgu sonucu listelenecek başlıklar:
print ("IP","Ülke","İl","İlçe","Enlem","Boylam")

#Sorgulanacak ip lere ait liste:
ip = ["176.55.55.252","176.55.55.252","88.230.177.68","88.230.177.68"]

#ip listesinin teker teker web servis üzerinden sorgulanması:
for x in ip:
  #Bu kısımda yer alan API_KEY'i https://ipstack.com/ adresine üye olarak temin edebilirsiniz.
  serviceURL = "http://api.ipapi.com/"+x+"?access_key=API_KEY&output=json"  
  r = requests.get(serviceURL)
  y = json.loads(r.text)
  print(y["ip"],y["country_name"],y["region_name"],y["city"],y["latitude"],y["longitude"])  
