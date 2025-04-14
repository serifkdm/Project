document.getElementById("hava-durumu-formu").addEventListener("submit", function (e) {
    e.preventDefault();

    const sehirGirisi = document.getElementById("sehir-girisi").value.trim().toLowerCase();
    const havaDurumuSonuc = document.getElementById("hava-durumu-sonuc");

    const havaDurumlari = {
        "İstanbul": { sicaklik: 15, durum: "Parçalı Bulutlu", ikon: "🌥️" },
        "Ankara": { sicaklik: 10, durum: "Yağmurlu", ikon: "🌧️" },
        "İzmir": { sicaklik: 20, durum: "Güneşli", ikon: "☀️" },
        "Bursa": { sicaklik: 12, durum: "Rüzgarlı", ikon: "💨" },
        "Antalya": { sicaklik: 25, durum: "Güneşli", ikon: "☀️" },
        "Trabzon": { sicaklik: 8, durum: "Yağmurlu", ikon: "🌧️" },
        "Adana": { sicaklik: 28, durum: "Sıcak", ikon: "🔥" },
        "Erzurum": { sicaklik: -5, durum: "Karlı", ikon: "❄️" }
    };
    
    function havaDurumunuGoster() {
       
        const sehir = document.getElementById("sehir").value;
        
        const sonucDiv = document.getElementById("havaDurumuSonucu");
    
       
        if (havaDurumlari[sehir]) {
            const havaDurumu = havaDurumlari[sehir];
            sonucDiv.innerHTML = `
                <h2>${sehir}</h2>
                <p><strong>Sıcaklık:</strong> ${havaDurumu.sicaklik}°C</p>
                <p><strong>Durum:</strong> ${havaDurumu.durum} ${havaDurumu.ikon}</p>
            `;
           
            sonucDiv.style.border = "1px solid #ddd";
            sonucDiv.style.padding = "10px";
            sonucDiv.style.borderRadius = "5px";
            sonucDiv.style.backgroundColor = "#f9f9f9";
        } else {
            
            sonucDiv.innerHTML = "<p>Bu şehir için hava durumu bilgisi bulunamadı.</p>";
            sonucDiv.style.border = "none";
            sonucDiv.style.padding = "0";
            sonucDiv.style.backgroundColor = "transparent";
        }
    }
    
});
