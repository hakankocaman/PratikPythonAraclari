#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HavaTahmin Web Arayüzü (Flask)
HavaTahmin uygulamasını web üzerinden kullanmaya olanak tanır.
"""

import argparse
import json
import sys
from pathlib import Path
from flask import Flask, jsonify, render_template_string, request

# HavaTahmin modülünü import et
sys.path.insert(0, str(Path(__file__).parent))
from HavaTahmin import HavaDurumuApp

app = Flask(__name__)
hava_app = HavaDurumuApp()

# =========================================================
# HTML Template (Bootstrap 5 ile)
# =========================================================
INDEX_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌤️ Hava Durumu Uygulaması</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #74b9ff, #0984e3); min-height: 100vh; }
        .card { border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); }
        .weather-card { background: rgba(255,255,255,0.95); }
        .badge-durum { font-size: 1rem; padding: 8px 16px; border-radius: 20px; }
        .forecast-item { border-left: 4px solid #0984e3; padding: 10px 15px; margin: 5px 0; background: #f8f9fa; border-radius: 8px; }
        .uyari-item { border-radius: 8px; margin: 5px 0; padding: 10px; }
        .gecmis-item { border-bottom: 1px solid #dee2e6; padding: 8px 0; }
        #yukleniyor { display: none; }
    </style>
</head>
<body>
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <!-- Başlık -->
            <div class="text-center mb-4">
                <h1 class="text-white display-4">🌤️ Hava Durumu</h1>
                <p class="text-white-50">OpenWeatherMap ile gerçek zamanlı hava bilgisi</p>
            </div>

            <!-- Arama Formu -->
            <div class="card weather-card mb-4">
                <div class="card-body p-4">
                    <div class="input-group input-group-lg">
                        <span class="input-group-text">🏙️</span>
                        <input type="text" id="sehirInput" class="form-control" placeholder="Şehir adı girin... (ör: Sakarya, Ankara)" onkeypress="enterKontrol(event)">
                        <button class="btn btn-primary" onclick="havaDurumuGetir()">Sorgula</button>
                    </div>
                    <div class="mt-2 d-flex gap-2 flex-wrap">
                        <button class="btn btn-sm btn-outline-secondary" onclick="hizliSehir('Sakarya')">Sakarya</button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="hizliSehir('Ankara')">Ankara</button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="hizliSehir('Istanbul')">İstanbul</button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="hizliSehir('Izmir')">İzmir</button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="hizliSehir('Antalya')">Antalya</button>
                    </div>
                </div>
            </div>

            <!-- Yükleniyor -->
            <div id="yukleniyor" class="text-center text-white mb-3">
                <div class="spinner-border" role="status"></div>
                <p>Hava durumu alınıyor...</p>
            </div>

            <!-- Sonuçlar -->
            <div id="sonuclar"></div>
        </div>
    </div>
</div>

<script>
function enterKontrol(e) { if (e.key === 'Enter') havaDurumuGetir(); }
function hizliSehir(s) { document.getElementById('sehirInput').value = s; havaDurumuGetir(); }

async function havaDurumuGetir() {
    const sehir = document.getElementById('sehirInput').value.trim();
    if (!sehir) { alert('Lütfen bir şehir adı girin!'); return; }

    document.getElementById('yukleniyor').style.display = 'block';
    document.getElementById('sonuclar').innerHTML = '';

    try {
        const [havaRes, tahminRes, uyariRes, gecmisRes] = await Promise.all([
            fetch(`/hava/${encodeURIComponent(sehir)}`),
            fetch(`/tahmin/${encodeURIComponent(sehir)}`),
            fetch(`/uyari/${encodeURIComponent(sehir)}`),
            fetch(`/gecmis/${encodeURIComponent(sehir)}`)
        ]);

        const hava = await havaRes.json();
        const tahmin = await tahminRes.json();
        const uyari = await uyariRes.json();
        const gecmis = await gecmisRes.json();

        document.getElementById('yukleniyor').style.display = 'none';
        document.getElementById('sonuclar').innerHTML = sonuclariOlustur(hava, tahmin, uyari, gecmis);
    } catch(e) {
        document.getElementById('yukleniyor').style.display = 'none';
        document.getElementById('sonuclar').innerHTML = '<div class="alert alert-danger">❌ Hata oluştu: ' + e.message + '</div>';
    }
}

function sonuclariOlustur(hava, tahmin, uyari, gecmis) {
    let html = '';

    if (hava.hata) {
        return `<div class="alert alert-danger">❌ ${hava.hata}</div>`;
    }

    // Mevcut hava durumu kartı
    html += `
    <div class="card weather-card mb-3">
        <div class="card-body">
            <div class="row align-items-center">
                <div class="col-md-6">
                    <h3>🌍 ${hava.sehir}, ${hava.ulke}</h3>
                    <h2 class="display-5 text-primary">${hava.emoji} ${hava.sicaklik}°C</h2>
                    <p class="text-muted">Hissedilen: ${hava.hissedilen}°C</p>
                    <span class="badge bg-info badge-durum">${hava.aciklama}</span>
                </div>
                <div class="col-md-6">
                    <ul class="list-unstyled mt-3">
                        <li>💧 <strong>Nem:</strong> %${hava.nem}</li>
                        <li>🌬️ <strong>Rüzgar:</strong> ${hava.ruzgar} m/s</li>
                        <li>📊 <strong>Basınç:</strong> ${hava.basinc} hPa</li>
                        <li>🌅 <strong>Gün Doğumu:</strong> ${hava.gun_dogus}</li>
                        <li>🌇 <strong>Gün Batımı:</strong> ${hava.gun_batis}</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>`;

    // Uyarılar
    if (uyari.uyarilar && uyari.uyarilar.length > 0) {
        html += '<div class="card weather-card mb-3"><div class="card-body"><h5>🚨 Hava Uyarıları</h5>';
        uyari.uyarilar.forEach(u => {
            const renk = u.seviye.includes('KRİTİK') ? 'danger' : u.seviye.includes('UYARI') ? 'warning' : 'info';
            html += `<div class="alert alert-${renk} uyari-item">${u.seviye}: ${u.mesaj}</div>`;
        });
        html += '</div></div>';
    }

    // 5 günlük tahmin
    if (tahmin.gunler && tahmin.gunler.length > 0) {
        html += '<div class="card weather-card mb-3"><div class="card-body"><h5>📅 5 Günlük Tahmin</h5>';
        tahmin.gunler.forEach(g => {
            html += `
            <div class="forecast-item">
                <div class="d-flex justify-content-between align-items-center">
                    <div><strong>${g.gun}</strong> <small class="text-muted">${g.tarih}</small></div>
                    <div>${g.emoji} ${g.aciklama}</div>
                    <div class="text-end">
                        <span class="text-danger">↑${g.max}°C</span> /
                        <span class="text-primary">↓${g.min}°C</span>
                        <br><small>💧 %${g.nem}</small>
                    </div>
                </div>
            </div>`;
        });
        html += '</div></div>';
    }

    // Geçmiş sorgular
    if (gecmis.gecmis && gecmis.gecmis.length > 0) {
        html += '<div class="card weather-card mb-3"><div class="card-body"><h5>📜 Son Sorgular</h5>';
        gecmis.gecmis.forEach(g => {
            html += `
            <div class="gecmis-item">
                <small class="text-muted">📅 ${g.tarih}</small>
                <span class="ms-2">${g.aciklama} | 🌡️ ${g.sicaklik}°C | 💧 %${g.nem} | 🌬️ ${g.ruzgar} m/s</span>
            </div>`;
        });
        html += '</div></div>';
    }

    return html;
}
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# =========================================================
# Flask Route'ları
# =========================================================

@app.route("/")
def ana_sayfa():
    """Ana sayfa — şehir arama formu."""
    return render_template_string(INDEX_HTML)


@app.route("/hava/<sehir>")
def hava_durumu(sehir):
    """Belirtilen şehir için güncel hava durumu JSON olarak döner."""
    veri = hava_app.hava_durumu_getir(sehir)
    if not veri:
        return jsonify({"hata": f"'{sehir}' için hava durumu alınamadı."}), 404

    from datetime import datetime
    return jsonify({
        "sehir": veri["name"],
        "ulke": veri["sys"]["country"],
        "sicaklik": veri["main"]["temp"],
        "hissedilen": veri["main"]["feels_like"],
        "nem": veri["main"]["humidity"],
        "basinc": veri["main"]["pressure"],
        "ruzgar": veri["wind"]["speed"],
        "aciklama": veri["weather"][0]["description"].capitalize(),
        "emoji": hava_app.hava_emoji(veri["weather"][0]["description"]),
        "gun_dogus": datetime.fromtimestamp(veri["sys"]["sunrise"]).strftime("%H:%M"),
        "gun_batis": datetime.fromtimestamp(veri["sys"]["sunset"]).strftime("%H:%M"),
    })


@app.route("/tahmin/<sehir>")
def tahmin(sehir):
    """Belirtilen şehir için 5 günlük tahmin JSON olarak döner."""
    veri = hava_app.tahmin_getir(sehir)
    if not veri:
        return jsonify({"hata": f"'{sehir}' için tahmin alınamadı."}), 404

    from datetime import datetime
    gunluk_veri = {}
    for kayit in veri["list"]:
        tarih = datetime.fromtimestamp(kayit["dt"]).strftime("%Y-%m-%d")
        gunluk_veri.setdefault(tarih, []).append(kayit)

    gunler = []
    for tarih, kayitlar in list(gunluk_veri.items())[:5]:
        sicakliklar = [k["main"]["temp"] for k in kayitlar]
        secilen = min(kayitlar, key=lambda x: abs(datetime.fromtimestamp(x["dt"]).hour - 12))
        tarih_obj = datetime.strptime(tarih, "%Y-%m-%d")
        gun_adi_tr = hava_app.gunler_tr.get(tarih_obj.strftime("%A"), tarih_obj.strftime("%A"))
        aciklama = secilen["weather"][0]["description"].capitalize()
        gunler.append({
            "gun": gun_adi_tr,
            "tarih": tarih_obj.strftime("%d.%m.%Y"),
            "min": round(min(sicakliklar), 1),
            "max": round(max(sicakliklar), 1),
            "aciklama": aciklama,
            "emoji": hava_app.hava_emoji(aciklama),
            "nem": secilen["main"]["humidity"],
        })

    return jsonify({"sehir": veri["city"]["name"], "gunler": gunler})


@app.route("/uyari/<sehir>")
def uyari(sehir):
    """Belirtilen şehir için hava uyarılarını JSON olarak döner."""
    veri = hava_app.hava_durumu_getir(sehir)
    if not veri:
        return jsonify({"hata": f"'{sehir}' için hava durumu alınamadı."}), 404

    uyarilar_ham = hava_app.hava_uyarisi_kontrol(veri)
    uyarilar = [{"seviye": s, "mesaj": m} for s, m in uyarilar_ham]
    return jsonify({"sehir": veri["name"], "uyarilar": uyarilar})


@app.route("/gecmis/<sehir>")
def gecmis(sehir):
    """Belirtilen şehir için SQLite geçmişini JSON olarak döner."""
    import sqlite3
    try:
        with sqlite3.connect(hava_app.db_dosyasi) as conn:
            cursor = conn.execute("""
                SELECT tarih, sicaklik, hissedilen, nem, ruzgar, aciklama
                FROM hava_gecmisi
                WHERE LOWER(sehir) = LOWER(?)
                ORDER BY id DESC
                LIMIT 10
            """, (sehir,))
            satirlar = cursor.fetchall()

        gecmis_liste = [{
            "tarih": r[0],
            "sicaklik": r[1],
            "hissedilen": r[2],
            "nem": r[3],
            "ruzgar": r[4],
            "aciklama": r[5].capitalize() if r[5] else "",
        } for r in satirlar]

        return jsonify({"sehir": sehir, "gecmis": gecmis_liste})
    except Exception as e:
        return jsonify({"hata": str(e)}), 500


# =========================================================
# Ana Giriş Noktası
# =========================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HavaTahmin Web Sunucusu")
    parser.add_argument("--port", type=int, default=5000, help="Dinlenecek port (varsayılan: 5000)")
    parser.add_argument("--host", default="0.0.0.0", help="Dinlenecek host (varsayılan: 0.0.0.0)")
    args = parser.parse_args()

    print(f"🌐 HavaTahmin web sunucusu başlatılıyor...")
    print(f"   Adres: http://localhost:{args.port}")
    print(f"   Durdurmak için Ctrl+C\n")
    app.run(host=args.host, port=args.port, debug=False)
