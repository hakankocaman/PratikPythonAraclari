#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hava Durumu Tahmin Uygulaması
OpenWeatherMap API kullanarak gerçek zamanlı hava durumu bilgisi sağlar.
"""

import requests
import sys
from datetime import datetime

class HavaDurumuApp:
    def __init__(self):
        # OpenWeatherMap API anahtarı (Ücretsiz: https://openweathermap.org/api)
        self.api_key = "a693375440701d0d3bff0a4d640c3eb2"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def hava_durumu_getir(self, sehir):
        """Belirtilen şehir için hava durumu bilgisi getirir."""
        try:
            # API parametreleri
            params = {
                'q': sehir,
                'appid': self.api_key,
                'units': 'metric',  # Celsius için
                'lang': 'tr'  # Türkçe açıklamalar
            }
            
            # API isteği
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("❌ HATA: Geçersiz API anahtarı!")
                print("🔑 Lütfen OpenWeatherMap'ten ücretsiz API anahtarı alın:")
                print("   https://openweathermap.org/api")
                return None
            elif response.status_code == 404:
                print(f"❌ HATA: '{sehir}' şehri bulunamadı!")
                return None
            else:
                print(f"❌ HATA: API hatası (Kod: {response.status_code})")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ HATA: İnternet bağlantısı yok!")
            return None
        except requests.exceptions.Timeout:
            print("❌ HATA: İstek zaman aşımına uğradı!")
            return None
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return None
    
    def bilgileri_goster(self, veri):
        """Hava durumu bilgilerini formatlanmış şekilde gösterir."""
        if not veri:
            return
        
        # Veri çıkarma
        sehir = veri['name']
        ulke = veri['sys']['country']
        sicaklik = veri['main']['temp']
        hissedilen = veri['main']['feels_like']
        nem = veri['main']['humidity']
        basinc = veri['main']['pressure']
        aciklama = veri['weather'][0]['description'].capitalize()
        ruzgar = veri['wind']['speed']
        
        # Güneş doğuş/batış zamanları
        gun_dogus = datetime.fromtimestamp(veri['sys']['sunrise']).strftime('%H:%M')
        gun_batis = datetime.fromtimestamp(veri['sys']['sunset']).strftime('%H:%M')
        
        # Ekrana yazdırma
        print("\n" + "="*50)
        print(f"🌍 Şehir: {sehir}, {ulke}")
        print("="*50)
        print(f"🌡️  Sıcaklık: {sicaklik}°C (Hissedilen: {hissedilen}°C)")
        print(f"☁️  Durum: {aciklama}")
        print(f"💧 Nem: {nem}%")
        print(f"🌬️  Rüzgar: {ruzgar} m/s")
        print(f"📊 Basınç: {basinc} hPa")
        print(f"🌅 Gün Doğumu: {gun_dogus}")
        print(f"🌇 Gün Batımı: {gun_batis}")
        print("="*50 + "\n")
    
    def calistir(self):
        """Uygulamayı çalıştırır."""
        print("\n" + "🌤️  " * 10)
        print("     HAVA DURUMU TAHMİN UYGULAMASI")
        print("🌤️  " * 10 + "\n")
        
        # API anahtarı kontrolü
        if self.api_key == "BURAYA_API_ANAHTARINIZI_GIRIN":
            print("⚠️  API anahtarı ayarlanmamış!")
            print("🔑 OpenWeatherMap'ten ücretsiz API anahtarı alın:")
            print("   1. https://openweathermap.org/api adresine gidin")
            print("   2. Ücretsiz hesap oluşturun")
            print("   3. API anahtarınızı kopyalayın")
            print("   4. HavaTahmin.py dosyasındaki 'BURAYA_API_ANAHTARINIZI_GIRIN' kısmına yapıştırın\n")
            
            # Demo modu
            demo = input("Demo modu için 'demo' yazın veya çıkmak için Enter'a basın: ").strip().lower()
            if demo == 'demo':
                print("\n📝 Demo Modu: İstanbul için örnek çıktı gösteriliyor...\n")
                print("="*50)
                print("🌍 Şehir: İstanbul, TR")
                print("="*50)
                print("🌡️  Sıcaklık: 15°C (Hissedilen: 13°C)")
                print("☁️  Durum: Az bulutlu")
                print("💧 Nem: 65%")
                print("🌬️  Rüzgar: 3.5 m/s")
                print("📊 Basınç: 1013 hPa")
                print("🌅 Gün Doğumu: 06:45")
                print("🌇 Gün Batımı: 18:30")
                print("="*50 + "\n")
            return
        
        while True:
            # Kullanıcıdan şehir adı al
            sehir = input("🏙️  Şehir adı girin (çıkmak için 'q'): ").strip()
            
            if sehir.lower() in ['q', 'quit', 'exit', 'çık']:
                print("\n👋 Görüşmek üzere!\n")
                break
            
            if not sehir:
                print("⚠️  Lütfen geçerli bir şehir adı girin!\n")
                continue
            
            # Hava durumu bilgisi getir ve göster
            veri = self.hava_durumu_getir(sehir)
            self.bilgileri_goster(veri)


def main():
    """Ana fonksiyon"""
    try:
        app = HavaDurumuApp()
        app.calistir()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
