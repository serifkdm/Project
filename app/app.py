import requests
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import locale

app = Flask(__name__)


API_KEY = 'Jzk3YzM0ZWYxNzJmNzJmYzA3NGYxYzgyNDE3YzY4NWZjJw=='
DATABASE = 'sehirler.db'


try:
    locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")
except locale.Error:
    pass  


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('CREATE TABLE IF NOT EXISTS sehirler (id INTEGER PRIMARY KEY AUTOINCREMENT, sehir_adı TEXT)')
        db.commit()


@app.route("/")
def index():
    db = get_db()
    
    cursor = db.execute('SELECT sehir_adı FROM sehirler ORDER BY id DESC')
    sehirler = [row['sehir_adı'] for row in cursor.fetchall()]
    return render_template('index.html', sehirler=sehirler)
@app.route("/sil", methods=["POST"])
def sil():
    sehir_adi = request.form.get('sehir')  
    if sehir_adi:
        db = get_db()
        db.execute('DELETE FROM sehirler WHERE sehir_adı = ?', (sehir_adi,))
        db.commit()  
        


@app.route('/arama', methods=['GET'])
def arama():
    arama_kelimesi = request.args.get('q', '').lower()
    if arama_kelimesi:
        params = {
            'q': arama_kelimesi,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'tr'
        }
        response = requests.get("http://api.openweathermap.org/data/2.5/find", params=params)
        if response.status_code == 200:
            data = response.json()
            sehirler = [city['name'] for city in data['list']]
            return jsonify(sehirler)
    return jsonify([])

@app.route("/sehir/<sehir>")
def sehir_hava_durumu(sehir):
   
    params = {
        'q': sehir,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'tr'
    }

    
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather", params=params)
    if response.status_code == 200:
        data = response.json()
        hava_durumu = {
            "sehir": sehir,
            "sicaklik": f"{data['main']['temp']}°C",
            "durum": data['weather'][0]['description'],
            "nem": f"{data['main']['humidity']}%",
            "ruzgar": f"{data['wind']['speed']} m/s"
        }

        
        db = get_db()
        cursor = db.execute('SELECT * FROM sehirler WHERE sehir_adı = ?', (sehir,))
        existing_city = cursor.fetchone()

        
        if not existing_city:
            db.execute('INSERT INTO sehirler (sehir_adı) VALUES (?)', (sehir,))
            db.commit()

    else:
        hava_durumu = {
            "sehir": sehir,
            "sicaklik": "Veri alınamadı",
            "durum": "Hata oluştu",
            "nem": "Veri alınamadı",
            "ruzgar": "Veri alınamadı"
        }

   

    
    forecast_params = {
        'q': sehir,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'tr'
    }

    forecast_response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=forecast_params)

    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        gunluk_tahminler = []

       
        current_day = None
        daily_data = {}

        for forecast in forecast_data['list']:
            
            tarih = datetime.utcfromtimestamp(forecast['dt']).strftime('%d %b %Y')

           
            aylar = {
                'Jan': 'Oca', 'Feb': 'Şub', 'Mar': 'Mar', 'Apr': 'Nis', 'May': 'May', 'Jun': 'Haz',
                'Jul': 'Tem', 'Aug': 'Ağu', 'Sep': 'Eyl', 'Oct': 'Eki', 'Nov': 'Kas', 'Dec': 'Ara'
            }

            
            for ingilizce_ay, turkce_ay in aylar.items():
                if ingilizce_ay in tarih:
                    tarih = tarih.replace(ingilizce_ay, turkce_ay)

            if current_day != tarih:
                if current_day:
                    
                    gunluk_tahminler.append(daily_data)
                
                current_day = tarih
                daily_data = {
                    "tarih": current_day,
                    "sicaklik_min": float(forecast['main']['temp_min']),
                    "sicaklik_max": float(forecast['main']['temp_max']),
                    "durum": forecast['weather'][0]['description']
                }
            else:
               
                daily_data["sicaklik_min"] = min(daily_data["sicaklik_min"], float(forecast['main']['temp_min']))
                daily_data["sicaklik_max"] = max(daily_data["sicaklik_max"], float(forecast['main']['temp_max']))

        
        if daily_data:
            gunluk_tahminler.append(daily_data)

    else:
        gunluk_tahminler = []

    return render_template("sehir.html", hava_durumu=hava_durumu, gunluk_tahminler=gunluk_tahminler)

if __name__ == "__main__":
    init_db() 
    app.run(host="0.0.0.0", port=6000, debug=True)
