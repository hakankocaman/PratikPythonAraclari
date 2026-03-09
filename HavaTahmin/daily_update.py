#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Günlük Hava Durumu Uygulaması Geliştirme Scripti
Her gün otomatik olarak yeni özellikler ekler
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Proje kök dizini
PROJECT_ROOT = Path(__file__).resolve().parent.parent
HAVA_TAHMIN_DIR = PROJECT_ROOT / "HavaTahmin"
PLAN_FILE = HAVA_TAHMIN_DIR / "development_plan.json"
COMMIT_MSG_FILE = HAVA_TAHMIN_DIR / "commit_message.txt"
HAVA_TAHMIN_FILE = HAVA_TAHMIN_DIR / "HavaTahmin.py"

def load_plan():
    """Geliştirme planını yükler"""
    if PLAN_FILE.exists():
        with open(PLAN_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_plan(plan):
    """Geliştirme planını kaydeder"""
    with open(PLAN_FILE, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

def get_current_day(plan):
    """Mevcut geliştirme gününü döndürür"""
    if not plan:
        return 1
    return plan.get('current_day', 1)

def apply_day_2_changes():
    """Gün 2: 5 Günlük Hava Tahmini Ekle"""
    code = HAVA_TAHMIN_FILE.read_text(encoding='utf-8')
    
    # Yeni import ekle
    if 'from datetime import datetime, timedelta' not in code:
        code = code.replace(
            'from datetime import datetime',
            'from datetime import datetime, timedelta'
        )
    
    # Yeni metod ekle (calistir metodundan önce)
    new_method = '''
    def tahmin_getir(self, sehir):
        """Belirtilen şehir için 5 günlük hava tahmini getirir."""
        try:
            forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {
                'q': sehir,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'tr'
            }
            
            response = requests.get(forecast_url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Tahmin verisi alınamadı (Kod: {response.status_code})")
                return None
                
        except Exception as e:
            print(f"❌ Tahmin hatası: {e}")
            return None
    
    def tahmin_goster(self, veri):
        """5 günlük hava tahminini gösterir."""
        if not veri:
            return
        
        print("\\n" + "="*70)
        print(f"📅 5 GÜNLÜK HAVA TAHMİNİ - {veri['city']['name']}, {veri['city']['country']}")
        print("="*70)
        
        # Günlük verileri grupla
        daily_data = {}
        for item in veri['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(item)
        
        # İlk 5 günü göster
        for i, (date, items) in enumerate(list(daily_data.items())[:5]):
            temps = [item['main']['temp'] for item in items]
            min_temp = min(temps)
            max_temp = max(temps)
            desc = items[0]['weather'][0]['description'].capitalize()
            
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            day_name = date_obj.strftime('%A')
            
            print(f"\\n{day_name}, {date_obj.strftime('%d.%m.%Y')}")
            print(f"  🌡️  Min: {min_temp:.1f}°C | Max: {max_temp:.1f}°C")
            print(f"  ☁️  {desc}")
        
        print("\\n" + "="*70 + "\\n")
'''
    
    if 'def tahmin_getir' not in code:
        # calistir metodundan önce ekle
        code = code.replace(
            '    def calistir(self):',
            new_method + '    def calistir(self):'
        )
    
    # calistir metoduna tahmin seçeneği ekle
    if '5 günlük tahmin' not in code:
        menu_addition = '''
            print("Seçenekler:")
            print("  1. Mevcut hava durumu")
            print("  2. 5 günlük tahmin")
            print("  q. Çıkış")
            print()
            
            secim = input("🏙️  Şehir adı girin veya seçenek (1/2/q): ").strip()
            
            if secim.lower() in ['q', 'quit', 'exit', 'çık']:
                print("\\n👋 Görüşmek üzere!\\n")
                break
            
            if secim == '2':
                sehir = input("🏙️  Tahmin için şehir adı: ").strip()
                if sehir:
                    veri = self.tahmin_getir(sehir)
                    self.tahmin_goster(veri)
                continue
            
            # Seçim 1 veya direkt şehir adı
            sehir = secim if secim != '1' else input("🏙️  Şehir adı: ").strip()
'''
        
        code = code.replace(
            '        while True:\n            # Kullanıcıdan şehir adı al\n            sehir = input("🏙️  Şehir adı girin (çıkmak için \'q\'): ").strip()',
            '        while True:\n' + menu_addition
        )
    
    HAVA_TAHMIN_FILE.write_text(code, encoding='utf-8')
    return "🌤️ Gün 2: 5 günlük hava tahmini özelliği eklendi"

def apply_day_3_changes():
    """Gün 3: Favori Şehirler Sistemi"""
    code = HAVA_TAHMIN_FILE.read_text(encoding='utf-8')
    
    # JSON import ekle
    if 'import json' not in code:
        code = code.replace('import sys', 'import sys\nimport json')
    
    # Favori şehirler metodları ekle
    new_methods = '''
    def favori_yukle(self):
        """Favori şehirleri yükler."""
        try:
            if os.path.exists('favoriler.json'):
                with open('favoriler.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def favori_kaydet(self, favoriler):
        """Favori şehirleri kaydeder."""
        with open('favoriler.json', 'w', encoding='utf-8') as f:
            json.dump(favoriler, f, ensure_ascii=False, indent=2)
    
    def favori_ekle(self, sehir):
        """Şehri favorilere ekler."""
        favoriler = self.favori_yukle()
        if sehir not in favoriler:
            favoriler.append(sehir)
            self.favori_kaydet(favoriler)
            print(f"✅ {sehir} favorilere eklendi!")
        else:
            print(f"⚠️  {sehir} zaten favorilerde!")
    
    def favori_listele(self):
        """Favori şehirleri listeler."""
        favoriler = self.favori_yukle()
        if not favoriler:
            print("📝 Henüz favori şehir yok!")
            return
        
        print("\\n⭐ FAVORİ ŞEHİRLER:")
        for i, sehir in enumerate(favoriler, 1):
            print(f"  {i}. {sehir}")
        print()
'''
    
    if 'def favori_yukle' not in code:
        code = code.replace(
            '    def tahmin_getir',
            new_methods + '    def tahmin_getir'
        )
    
    # os import ekle
    if 'import os' not in code:
        code = code.replace('import json', 'import json\nimport os')
    
    HAVA_TAHMIN_FILE.write_text(code, encoding='utf-8')
    return "💾 Gün 3: Favori şehirler sistemi eklendi"

def apply_day_4_changes():
    """Gün 4: Görsel İyileştirmeler ve Emoji Desteği"""
    code = HAVA_TAHMIN_FILE.read_text(encoding='utf-8')
    
    # Hava durumu emoji fonksiyonu ekle
    new_method = '''
    def hava_emoji(self, aciklama):
        """Hava durumuna göre emoji döndürür."""
        aciklama = aciklama.lower()
        if 'güneş' in aciklama or 'açık' in aciklama:
            return '☀️'
        elif 'bulut' in aciklama:
            return '☁️'
        elif 'yağmur' in aciklama:
            return '🌧️'
        elif 'kar' in aciklama:
            return '❄️'
        elif 'fırtına' in aciklama:
            return '⛈️'
        elif 'sis' in aciklama:
            return '🌫️'
        else:
            return '🌤️'
'''
    
    if 'def hava_emoji' not in code:
        code = code.replace(
            '    def bilgileri_goster',
            new_method + '    def bilgileri_goster'
        )
    
    HAVA_TAHMIN_FILE.write_text(code, encoding='utf-8')
    return "🎨 Gün 4: Görsel iyileştirmeler ve emoji desteği eklendi"

def apply_day_5_changes():
    """Gün 5: Şehir Karşılaştırma"""
    code = HAVA_TAHMIN_FILE.read_text(encoding='utf-8')
    
    new_method = '''
    def sehir_karsilastir(self, sehirler):
        """Birden fazla şehrin hava durumunu karşılaştırır."""
        print("\\n" + "="*80)
        print("📊 ŞEHİR KARŞILAŞTIRMA")
        print("="*80)
        
        veriler = []
        for sehir in sehirler:
            veri = self.hava_durumu_getir(sehir)
            if veri:
                veriler.append(veri)
        
        if not veriler:
            print("❌ Karşılaştırma için veri alınamadı!")
            return
        
        # Başlık
        print(f"\\n{'Şehir':<20} {'Sıcaklık':<15} {'Durum':<20} {'Nem':<10}")
        print("-" * 80)
        
        for veri in veriler:
            sehir = veri['name']
            sicaklik = f"{veri['main']['temp']:.1f}°C"
            durum = veri['weather'][0]['description'].capitalize()
            nem = f"{veri['main']['humidity']}%"
            
            print(f"{sehir:<20} {sicaklik:<15} {durum:<20} {nem:<10}")
        
        print("="*80 + "\\n")
'''
    
    if 'def sehir_karsilastir' not in code:
        code = code.replace(
            '    def calistir',
            new_method + '    def calistir'
        )
    
    HAVA_TAHMIN_FILE.write_text(code, encoding='utf-8')
    return "📊 Gün 5: Şehir karşılaştırma özelliği eklendi"

def apply_day_6_changes():
    """Gün 6: Grafik Desteği (requirements.txt güncelleme)"""
    req_file = HAVA_TAHMIN_DIR / "requirements.txt"
    content = req_file.read_text()
    
    if 'matplotlib' not in content:
        content += "matplotlib>=3.7.0\n"
        req_file.write_text(content)
    
    return "📈 Gün 6: Grafik desteği için matplotlib eklendi (requirements.txt güncellendi)"

def apply_day_7_changes():
    """Gün 7: Hava Durumu Uyarıları"""
    code = HAVA_TAHMIN_FILE.read_text(encoding='utf-8')
    
    new_method = '''
    def uyari_kontrol(self, veri):
        """Hava durumu uyarılarını kontrol eder."""
        if not veri:
            return
        
        uyarilar = []
        sicaklik = veri['main']['temp']
        ruzgar = veri['wind']['speed']
        
        if sicaklik > 35:
            uyarilar.append("🔥 UYARI: Aşırı sıcak! Güneşten korunun.")
        elif sicaklik < 0:
            uyarilar.append("❄️ UYARI: Donma noktasının altında! Dikkatli olun.")
        
        if ruzgar > 15:
            uyarilar.append("💨 UYARI: Kuvvetli rüzgar! Dışarıda dikkatli olun.")
        
        if uyarilar:
            print("\\n⚠️  HAVA DURUMU UYARILARI:")
            for uyari in uyarilar:
                print(f"  {uyari}")
            print()
'''
    
    if 'def uyari_kontrol' not in code:
        code = code.replace(
            '    def calistir',
            new_method + '    def calistir'
        )
    
    HAVA_TAHMIN_FILE.write_text(code, encoding='utf-8')
    return "⚠️ Gün 7: Hava durumu uyarı sistemi eklendi"

def main():
    """Ana fonksiyon"""
    print("🚀 Günlük Geliştirme Scripti Başlatıldı...")
    
    # Plan dosyasını yükle veya oluştur
    plan = load_plan()
    if not plan:
        plan = {
            'current_day': 2,  # Gün 1 zaten tamamlandı
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'completed_days': [1]
        }
    
    current_day = plan['current_day']
    
    # Eğer tüm günler tamamlandıysa
    if current_day > 7:
        print("✅ Tüm geliştirmeler tamamlandı!")
        commit_msg = "🎉 Hava Durumu Uygulaması - Tüm özellikler tamamlandı!"
        COMMIT_MSG_FILE.write_text(commit_msg, encoding='utf-8')
        return
    
    # Günlük geliştirmeyi uygula
    commit_msg = ""
    
    if current_day == 2:
        commit_msg = apply_day_2_changes()
    elif current_day == 3:
        commit_msg = apply_day_3_changes()
    elif current_day == 4:
        commit_msg = apply_day_4_changes()
    elif current_day == 5:
        commit_msg = apply_day_5_changes()
    elif current_day == 6:
        commit_msg = apply_day_6_changes()
    elif current_day == 7:
        commit_msg = apply_day_7_changes()
    
    # Planı güncelle
    plan['current_day'] = current_day + 1
    plan['completed_days'].append(current_day)
    plan['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_plan(plan)
    
    # Commit mesajını kaydet
    COMMIT_MSG_FILE.write_text(commit_msg, encoding='utf-8')
    
    print(f"✅ {commit_msg}")
    print(f"📅 Sonraki gün: {plan['current_day']}")

if __name__ == "__main__":
    main()
