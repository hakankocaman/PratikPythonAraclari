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

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_MEVCUT = True
except ImportError:
    MATPLOTLIB_MEVCUT = False

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

    def grafik_goster(self, sehir):
        """Belirtilen şehir için 5 günlük sıcaklık grafiği çizer."""
        if not MATPLOTLIB_MEVCUT:
            print("❌ Grafik özelliği için matplotlib kurulu olmalı: pip install matplotlib\n")
            return

        veri = self.tahmin_getir(sehir)
        if not veri:
            return

        tarihler = []
        min_sicakliklar = []
        max_sicakliklar = []
        ortalama_sicakliklar = []
        nem_degerleri = []

        gunluk_veri = {}
        for kayit in veri["list"]:
            tarih = datetime.fromtimestamp(kayit["dt"]).strftime("%Y-%m-%d")
            gunluk_veri.setdefault(tarih, []).append(kayit)

        for tarih, kayitlar in list(gunluk_veri.items())[:5]:
            sicakliklar = [k["main"]["temp"] for k in kayitlar]
            nem = [k["main"]["humidity"] for k in kayitlar]
            tarihler.append(datetime.strptime(tarih, "%Y-%m-%d"))
            min_sicakliklar.append(min(sicakliklar))
            max_sicakliklar.append(max(sicakliklar))
            ortalama_sicakliklar.append(sum(sicakliklar) / len(sicakliklar))
            nem_degerleri.append(sum(nem) / len(nem))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        fig.suptitle(
            f"5 Günlük Hava Durumu Grafiği — {veri['city']['name']}, {veri['city']['country']}",
            fontsize=14, fontweight="bold"
        )

        # Sıcaklık grafiği
        ax1.fill_between(tarihler, min_sicakliklar, max_sicakliklar, alpha=0.3, color="orange", label="Min-Max aralığı")
        ax1.plot(tarihler, ortalama_sicakliklar, "o-", color="red", linewidth=2, markersize=8, label="Ortalama sıcaklık")
        ax1.plot(tarihler, min_sicakliklar, "v--", color="blue", linewidth=1.5, markersize=6, label="Min sıcaklık")
        ax1.plot(tarihler, max_sicakliklar, "^--", color="darkred", linewidth=1.5, markersize=6, label="Max sıcaklık")

        for i, (tarih, ort) in enumerate(zip(tarihler, ortalama_sicakliklar)):
            ax1.annotate(f"{ort:.1f}°C", (tarih, ort), textcoords="offset points",
                         xytext=(0, 10), ha="center", fontsize=9, color="red")

        ax1.set_ylabel("Sıcaklık (°C)", fontsize=11)
        ax1.legend(loc="upper right", fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor("#f9f9f9")

        # Nem grafiği
        ax2.bar(tarihler, nem_degerleri, color="steelblue", alpha=0.7, width=0.6, label="Ortalama nem")
        for i, (tarih, nem) in enumerate(zip(tarihler, nem_degerleri)):
            ax2.text(tarih, nem + 1, f"{nem:.0f}%", ha="center", fontsize=9, color="steelblue")

        ax2.set_ylabel("Nem (%)", fontsize=11)
        ax2.set_ylim(0, 110)
        ax2.legend(loc="upper right", fontsize=9)
        ax2.grid(True, alpha=0.3, axis="y")
        ax2.set_facecolor("#f9f9f9")

        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%A"))
        plt.xticks(tarihler)
        plt.tight_layout()
        plt.savefig(f"{sehir.replace(' ', '_')}_hava_grafik.png", dpi=150, bbox_inches="tight")
        print(f"✅ Grafik kaydedildi: {sehir.replace(' ', '_')}_hava_grafik.png\n")
        plt.show()

    def sicaklik_karsilastirma_grafigi(self, sehirler):
        """Birden fazla şehrin sıcaklık karşılaştırma grafiğini çizer."""
        if not MATPLOTLIB_MEVCUT:
            print("❌ Grafik özelliği için matplotlib kurulu olmalı.\n")
            return

        if len(sehirler) < 2:
            print("⚠️  Karşılaştırma için en az iki şehir gerekli!\n")
            return

        fig, ax = plt.subplots(figsize=(11, 6))
        renkler = ["red", "blue", "green", "purple", "orange"]

        for i, sehir in enumerate(sehirler[:5]):
            veri = self.tahmin_getir(sehir)
            if not veri:
                continue

            gunluk_veri = {}
            for kayit in veri["list"]:
                tarih = datetime.fromtimestamp(kayit["dt"]).strftime("%Y-%m-%d")
                gunluk_veri.setdefault(tarih, []).append(kayit)

            tarihler = []
            ortalamalar = []
            for tarih, kayitlar in list(gunluk_veri.items())[:5]:
                sicakliklar = [k["main"]["temp"] for k in kayitlar]
                tarihler.append(datetime.strptime(tarih, "%Y-%m-%d"))
                ortalamalar.append(sum(sicakliklar) / len(sicakliklar))

            renk = renkler[i % len(renkler)]
            ax.plot(tarihler, ortalamalar, "o-", color=renk, linewidth=2,
                    markersize=8, label=f"{veri['city']['name']}")

        ax.set_title("Şehir Karşılaştırma — 5 Günlük Ortalama Sıcaklık", fontsize=14, fontweight="bold")
        ax.set_ylabel("Sıcaklık (°C)", fontsize=11)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor("#f9f9f9")
        plt.tight_layout()
        dosya_adi = "karsilastirma_grafik.png"
        plt.savefig(dosya_adi, dpi=150, bbox_inches="tight")
        print(f"✅ Karşılaştırma grafiği kaydedildi: {dosya_adi}\n")
        plt.show()

    def hava_uyarisi_kontrol(self, veri):
        """Hava durumu verisini analiz ederek aşırı koşullar için uyarı üretir."""
        if not veri:
            return []

        uyarilar = []
        sicaklik = veri["main"]["temp"]
        hissedilen = veri["main"]["feels_like"]
        nem = veri["main"]["humidity"]
        ruzgar = veri["wind"]["speed"]
        aciklama = veri["weather"][0]["description"].lower()
        gorunurluk = veri.get("visibility", 10000)

        if sicaklik >= 38:
            uyarilar.append(("🔴 KRİTİK", f"Çok yüksek sıcaklık: {sicaklik:.1f}°C — Dışarı çıkmayın!"))
        elif sicaklik >= 33:
            uyarilar.append(("🟠 UYARI", f"Yüksek sıcaklık: {sicaklik:.1f}°C — Bol su için."))

        if sicaklik <= -10:
            uyarilar.append(("🔴 KRİTİK", f"Aşırı soğuk: {sicaklik:.1f}°C — Don tehlikesi!"))
        elif sicaklik <= 0:
            uyarilar.append(("🟠 UYARI", f"Donma noktası: {sicaklik:.1f}°C — Buzlanma riski."))

        if hissedilen <= -15:
            uyarilar.append(("🔴 KRİTİK", f"Hissedilen sıcaklık: {hissedilen:.1f}°C — Hipotermi riski!"))

        if ruzgar >= 20:
            uyarilar.append(("🔴 KRİTİK", f"Fırtına şiddeti rüzgar: {ruzgar:.1f} m/s — Dışarı çıkmayın!"))
        elif ruzgar >= 13:
            uyarilar.append(("🟠 UYARI", f"Kuvvetli rüzgar: {ruzgar:.1f} m/s — Dikkatli olun."))

        if nem >= 90:
            uyarilar.append(("🟡 BİLGİ", f"Çok yüksek nem: %{nem} — Bunaltıcı hava."))

        if any(k in aciklama for k in ["fırtına", "storm", "thunder", "gök gürültü"]):
            uyarilar.append(("🔴 KRİTİK", "Fırtına uyarısı! Açık alanda bulunmayın."))

        if any(k in aciklama for k in ["yoğun kar", "heavy snow", "blizzard"]):
            uyarilar.append(("🔴 KRİTİK", "Yoğun kar yağışı! Seyahat etmekten kaçının."))
        elif any(k in aciklama for k in ["kar", "snow"]):
            uyarilar.append(("🟠 UYARI", "Kar yağışı bekleniyor — Yollar kaygan olabilir."))

        if gorunurluk < 200:
            uyarilar.append(("🔴 KRİTİK", f"Görüş mesafesi çok düşük: {gorunurluk}m — Araç kullanmayın!"))
        elif gorunurluk < 1000:
            uyarilar.append(("🟠 UYARI", f"Düşük görüş mesafesi: {gorunurluk}m — Yavaş sürün."))

        return uyarilar

    def uyarilari_goster(self, sehir):
        """Şehir için hava durumu uyarılarını getirir ve gösterir."""
        veri = self.hava_durumu_getir(sehir)
        if not veri:
            return

        uyarilar = self.hava_uyarisi_kontrol(veri)

        print(f"\n{'='*55}")
        print(f"🚨 HAVA DURUMU UYARI RAPORU — {veri['name']}, {veri['sys']['country']}")
        print(f"{'='*55}")

        if not uyarilar:
            print("✅ Herhangi bir aşırı hava koşulu tespit edilmedi.")
            print(f"   Sıcaklık: {veri['main']['temp']:.1f}°C | Rüzgar: {veri['wind']['speed']:.1f} m/s | Nem: %{veri['main']['humidity']}")
        else:
            for seviye, mesaj in uyarilar:
                print(f"\n  {seviye}: {mesaj}")

        print(f"{'='*55}\n")

    def tahmin_uyari_taramasi(self, sehir):
        """5 günlük tahmin içinde aşırı koşulları tarayarak uyarı verir."""
        veri = self.tahmin_getir(sehir)
        if not veri:
            return

        print(f"\n{'='*60}")
        print(f"🔍 5 GÜNLÜK UYARI TARAMASI — {veri['city']['name']}, {veri['city']['country']}")
        print(f"{'='*60}")

        uyari_bulundu = False
        gunluk_veri = {}
        for kayit in veri["list"]:
            tarih = datetime.fromtimestamp(kayit["dt"]).strftime("%Y-%m-%d")
            gunluk_veri.setdefault(tarih, []).append(kayit)

        for tarih, kayitlar in list(gunluk_veri.items())[:5]:
            gun_uyarilari = []
            for kayit in kayitlar:
                uyarilar = self.hava_uyarisi_kontrol(kayit)
                gun_uyarilari.extend(uyarilar)

            if gun_uyarilari:
                uyari_bulundu = True
                tarih_obj = datetime.strptime(tarih, "%Y-%m-%d")
                gun_adi = self.gunler_tr.get(tarih_obj.strftime("%A"), tarih_obj.strftime("%A"))
                print(f"\n📅 {gun_adi} {tarih_obj.strftime('%d.%m.%Y')}:")
                tekrar = set()
                for seviye, mesaj in gun_uyarilari:
                    if mesaj not in tekrar:
                        print(f"   {seviye}: {mesaj}")
                        tekrar.add(mesaj)

        if not uyari_bulundu:
            print("\n✅ Önümüzdeki 5 gün için aşırı hava koşulu öngörülmüyor.")

        print(f"\n{'='*60}\n")

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
            print("  8. 📈 Sıcaklık grafiği göster")
            print("  9. 📉 Şehirleri grafikle karşılaştır")
            print(" 10. 🚨 Anlık hava durumu uyarıları")
            print(" 11. 🔍 5 günlük uyarı taraması")
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

            if secim == '10':
                sehir = self.sehir_girdisini_duzenle(input("🚨 Uyarı kontrolü için şehir adı: "))
                if sehir:
                    self.uyarilari_goster(sehir)
                continue

            if secim == '11':
                sehir = self.sehir_girdisini_duzenle(input("🔍 5 günlük uyarı taraması için şehir adı: "))
                if sehir:
                    self.tahmin_uyari_taramasi(sehir)
                continue

            if secim == '8':
                sehir = self.sehir_girdisini_duzenle(input("📈 Grafik için şehir adı: "))
                if sehir:
                    self.grafik_goster(sehir)
                continue

            if secim == '9':
                girdi = input("📉 Karşılaştırılacak şehirleri virgülle girin (örn: Sakarya, Ankara, İzmir): ")
                sehirler = self.sehir_listesini_ayikla(girdi)
                self.sicaklik_karsilastirma_grafigi(sehirler)
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
