#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hava Durumu Tahmin Uygulaması
OpenWeatherMap API kullanarak gerçek zamanlı hava durumu bilgisi sağlar.
"""

import json
import requests
import sys
from datetime import datetime
from pathlib import Path

class HavaDurumuApp:
    def __init__(self):
        # OpenWeatherMap API anahtarı (Ücretsiz: https://openweathermap.org/api)
        self.api_key = "a693375440701d0d3bff0a4d640c3eb2"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.favoriler_dosyasi = Path(__file__).with_name("favoriler.json")
        self.gunler_tr = {
            "Monday": "Pazartesi",
            "Tuesday": "Salı",
            "Wednesday": "Çarşamba",
            "Thursday": "Perşembe",
            "Friday": "Cuma",
            "Saturday": "Cumartesi",
            "Sunday": "Pazar",
        }

    def hava_emoji(self, aciklama):
        """Hava durumu açıklamasına göre uygun emoji döndürür."""
        aciklama = aciklama.lower()

        if any(kelime in aciklama for kelime in ["gök gürültülü", "fırtına", "storm", "thunder"]):
            return "⛈️"
        if any(kelime in aciklama for kelime in ["kar", "snow"]):
            return "❄️"
        if any(kelime in aciklama for kelime in ["yağmur", "rain", "sağanak"]):
            return "🌧️"
        if any(kelime in aciklama for kelime in ["sis", "mist", "fog", "pus"]):
            return "🌫️"
        if any(kelime in aciklama for kelime in ["kapalı", "bulut", "cloud"]):
            return "☁️"
        if any(kelime in aciklama for kelime in ["parçalı", "az bulutlu"]):
            return "⛅"
        if any(kelime in aciklama for kelime in ["açık", "güneş", "clear"]):
            return "☀️"
        return "🌤️"

    def sicaklik_emoji(self, sicaklik):
        """Sıcaklığa göre küçük bir durum emojisi döndürür."""
        if sicaklik <= 0:
            return "🥶"
        if sicaklik >= 30:
            return "🥵"
        return "🙂"

    def sehir_girdisini_duzenle(self, sehir):
        """Kullanıcıdan gelen şehir girdisini temizler."""
        return sehir.strip().strip('"').strip("'").strip()

    def sehir_listesini_ayikla(self, girdi):
        """Virgülle ayrılmış şehir listesini temizleyip döndürür."""
        return [
            sehir for sehir in
            (self.sehir_girdisini_duzenle(parca) for parca in girdi.split(","))
            if sehir
        ]

    def sehir_karsilastir(self, sehirler):
        """Birden fazla şehrin mevcut hava durumunu karşılaştırır."""
        if len(sehirler) < 2:
            print("⚠️  Karşılaştırma için en az iki şehir girin!\n")
            return

        veriler = []
        for sehir in sehirler:
            veri = self.hava_durumu_getir(sehir)
            if veri:
                veriler.append(veri)

        if len(veriler) < 2:
            print("⚠️  Karşılaştırma için yeterli şehir verisi alınamadı!\n")
            return

        print("\n" + "=" * 96)
        print("📊 ŞEHİR KARŞILAŞTIRMA")
        print("=" * 96)
        print(
            f"{'Şehir':<18} {'Sıcaklık':<12} {'Hissedilen':<14} "
            f"{'Durum':<28} {'Nem':<8} {'Rüzgar':<10}"
        )
        print("-" * 96)

        for veri in veriler:
            sehir_adi = veri['name'][:18]
            sicaklik = f"{veri['main']['temp']:.1f}°C"
            hissedilen = f"{veri['main']['feels_like']:.1f}°C"
            durum = veri['weather'][0]['description'].capitalize()
            hava_ikonu = self.hava_emoji(durum)
            durum_metin = f"{hava_ikonu} {durum}"
            if len(durum_metin) > 27:
                durum_metin = durum_metin[:24] + "..."
            nem = f"{veri['main']['humidity']}%"
            ruzgar = f"{veri['wind']['speed']:.1f} m/s"

            print(
                f"{sehir_adi:<18} {sicaklik:<12} {hissedilen:<14} "
                f"{durum_metin:<28} {nem:<8} {ruzgar:<10}"
            )

        print("=" * 96 + "\n")
        
    def hava_durumu_getir(self, sehir):
        """Belirtilen şehir için hava durumu bilgisi getirir."""
        sehir = self.sehir_girdisini_duzenle(sehir)

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
        hava_ikonu = self.hava_emoji(aciklama)
        sicaklik_ikonu = self.sicaklik_emoji(sicaklik)
        ruzgar = veri['wind']['speed']
        
        # Güneş doğuş/batış zamanları
        gun_dogus = datetime.fromtimestamp(veri['sys']['sunrise']).strftime('%H:%M')
        gun_batis = datetime.fromtimestamp(veri['sys']['sunset']).strftime('%H:%M')
        
        # Ekrana yazdırma
        print("\n" + "="*50)
        print(f"🌍 Şehir: {sehir}, {ulke}")
        print("="*50)
        print(f"🌡️  Sıcaklık: {sicaklik}°C (Hissedilen: {hissedilen}°C) {sicaklik_ikonu}")
        print(f"{hava_ikonu}  Durum: {aciklama}")
        print(f"💧 Nem: {nem}%")
        print(f"🌬️  Rüzgar: {ruzgar} m/s")
        print(f"📊 Basınç: {basinc} hPa")
        print(f"🌅 Gün Doğumu: {gun_dogus}")
        print(f"🌇 Gün Batımı: {gun_batis}")
        print("="*50 + "\n")

    def tahmin_getir(self, sehir):
        """Belirtilen şehir için 5 günlük hava tahmini getirir."""
        sehir = self.sehir_girdisini_duzenle(sehir)

        try:
            params = {
                "q": sehir,
                "appid": self.api_key,
                "units": "metric",
                "lang": "tr"
            }

            response = requests.get(self.forecast_url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("❌ HATA: Geçersiz API anahtarı!")
                return None
            elif response.status_code == 404:
                print(f"❌ HATA: '{sehir}' şehri için tahmin verisi bulunamadı!")
                return None
            else:
                print(f"❌ HATA: Tahmin API hatası (Kod: {response.status_code})")
                return None

        except requests.exceptions.ConnectionError:
            print("❌ HATA: İnternet bağlantısı yok!")
            return None
        except requests.exceptions.Timeout:
            print("❌ HATA: Tahmin isteği zaman aşımına uğradı!")
            return None
        except Exception as e:
            print(f"❌ Beklenmeyen tahmin hatası: {e}")
            return None

    def tahmin_goster(self, veri):
        """5 günlük hava tahminini ekranda gösterir."""
        if not veri:
            return

        print("\n" + "="*70)
        print(f"📅 5 GÜNLÜK HAVA TAHMİNİ: {veri['city']['name']}, {veri['city']['country']}")
        print("="*70)

        gunluk_veri = {}
        for kayit in veri["list"]:
            tarih = datetime.fromtimestamp(kayit["dt"]).strftime("%Y-%m-%d")
            gunluk_veri.setdefault(tarih, []).append(kayit)

        for tarih, kayitlar in list(gunluk_veri.items())[:5]:
            sicakliklar = [kayit["main"]["temp"] for kayit in kayitlar]
            secilen_kayit = min(
                kayitlar,
                key=lambda item: abs(datetime.fromtimestamp(item["dt"]).hour - 12)
            )

            tarih_obj = datetime.strptime(tarih, "%Y-%m-%d")
            gun_adi_en = tarih_obj.strftime("%A")
            gun_adi_tr = self.gunler_tr.get(gun_adi_en, gun_adi_en)
            aciklama = secilen_kayit["weather"][0]["description"].capitalize()
            hava_ikonu = self.hava_emoji(aciklama)
            nem = secilen_kayit["main"]["humidity"]

            print(f"\n🗓️  {gun_adi_tr} - {tarih_obj.strftime('%d.%m.%Y')}")
            print(f"   🌡️  Min: {min(sicakliklar):.1f}°C | Max: {max(sicakliklar):.1f}°C")
            print(f"   {hava_ikonu}  Durum: {aciklama}")
            print(f"   💧 Nem: {nem}%")

        print("="*70 + "\n")

    def favorileri_yukle(self):
        """Favori şehir listesini JSON dosyasından yükler."""
        if not self.favoriler_dosyasi.exists():
            return []

        try:
            with open(self.favoriler_dosyasi, "r", encoding="utf-8") as dosya:
                veriler = json.load(dosya)
                return veriler if isinstance(veriler, list) else []
        except (json.JSONDecodeError, OSError):
            print("⚠️  Favori şehir dosyası okunamadı. Boş liste ile devam ediliyor.")
            return []

    def favorileri_kaydet(self, favoriler):
        """Favori şehir listesini JSON dosyasına kaydeder."""
        with open(self.favoriler_dosyasi, "w", encoding="utf-8") as dosya:
            json.dump(favoriler, dosya, ensure_ascii=False, indent=2)

    def favorileri_listele(self):
        """Favori şehirleri ekrana yazdırır."""
        favoriler = self.favorileri_yukle()

        if not favoriler:
            print("\n⭐ Henüz kayıtlı favori şehir bulunmuyor.\n")
            return []

        print("\n⭐ FAVORİ ŞEHİRLER")
        print("-" * 30)
        for index, sehir in enumerate(favoriler, start=1):
            print(f"{index}. {sehir}")
        print()
        return favoriler

    def favori_ekle(self, sehir):
        """Yeni bir şehri favorilere ekler."""
        sehir = self.sehir_girdisini_duzenle(sehir)
        if not sehir:
            print("⚠️  Lütfen geçerli bir şehir adı girin!\n")
            return

        favoriler = self.favorileri_yukle()
        if any(kayit.lower() == sehir.lower() for kayit in favoriler):
            print(f"⚠️  '{sehir}' zaten favoriler arasında kayıtlı.\n")
            return

        favoriler.append(sehir)
        self.favorileri_kaydet(favoriler)
        print(f"✅ '{sehir}' favorilere eklendi.\n")

    def favori_sec(self):
        """Favoriler içinden şehir seçtirir."""
        favoriler = self.favorileri_listele()
        if not favoriler:
            return None

        secim = self.sehir_girdisini_duzenle(
            input("⭐ Seçmek istediğiniz favori şehir numarası veya adı: ")
        )

        if not secim:
            print("⚠️  Lütfen geçerli bir seçim yapın!\n")
            return None

        if not secim.isdigit():
            for sehir in favoriler:
                if sehir.lower() == secim.lower():
                    return sehir
            print("⚠️  Bu isimde favori şehir bulunamadı!\n")
            return None

        index = int(secim) - 1
        if 0 <= index < len(favoriler):
            return favoriler[index]

        print("⚠️  Geçersiz seçim yaptınız!\n")
        return None

    def favori_sil(self):
        """Favori şehir listesinden seçimle silme işlemi yapar."""
        favoriler = self.favorileri_listele()
        if not favoriler:
            return

        secim = input("🗑️  Silmek istediğiniz favori şehir numarası: ").strip()
        if not secim.isdigit():
            print("⚠️  Lütfen geçerli bir numara girin!\n")
            return

        index = int(secim) - 1
        if 0 <= index < len(favoriler):
            silinen = favoriler.pop(index)
            self.favorileri_kaydet(favoriler)
            print(f"✅ '{silinen}' favorilerden silindi.\n")
            return

        print("⚠️  Geçersiz seçim yaptınız!\n")
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
            print("Seçenekler:")
            print("  1. 🌡️  Mevcut hava durumu")
            print("  2. 📅 5 günlük hava tahmini")
            print("  3. ⭐ Favori şehre ekle")
            print("  4. 📋 Favori şehirleri listele")
            print("  5. 🌍 Favori şehirden hava durumu göster")
            print("  6. 🗑️  Favori şehir sil")
            print("  7. 📊 Birden fazla şehri karşılaştır")
            print("  q. Çıkış")
            print("  İpucu: Doğrudan şehir adı da yazabilirsiniz. Örnek: Sakarya")

            secim = self.sehir_girdisini_duzenle(
                input("🔹 Seçim yapın veya direkt şehir adı girin: ")
            )

            if secim.lower() in ['q', 'quit', 'exit', 'çık']:
                print("\n👋 Görüşmek üzere!\n")
                break

            if secim == '2':
                sehir = self.sehir_girdisini_duzenle(input("🏙️  Tahmin alınacak şehir: "))
                if not sehir:
                    print("⚠️  Lütfen geçerli bir şehir adı girin!\n")
                    continue

                veri = self.tahmin_getir(sehir)
                self.tahmin_goster(veri)
                continue

            if secim == '3':
                sehir = self.sehir_girdisini_duzenle(input("⭐ Favorilere eklenecek şehir: "))
                self.favori_ekle(sehir)
                continue

            if secim == '4':
                self.favorileri_listele()
                continue

            if secim == '5':
                sehir = self.favori_sec()
                if sehir:
                    veri = self.hava_durumu_getir(sehir)
                    self.bilgileri_goster(veri)
                continue

            if secim == '6':
                self.favori_sil()
                continue

            if secim == '7':
                girdi = input(
                    "📊 Karşılaştırılacak şehirleri virgülle girin (örn: Sakarya, Ankara, İzmir): "
                )
                sehirler = self.sehir_listesini_ayikla(girdi)
                self.sehir_karsilastir(sehirler)
                continue

            if secim == '1':
                sehir = self.sehir_girdisini_duzenle(input("🏙️  Şehir adı girin: "))
            else:
                sehir = self.sehir_girdisini_duzenle(secim)

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
