import tkinter as tk
from tkinter import ttk
import random
import sys
import io

# Terminal kodlama sorununu önleme
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- KRİTİK EŞİK DEĞERLERİ ---
THRESHOLDS = {
    "Sıcaklık": {"min": 20.0, "max": 24.0, "unit": "°C"},
    "Nem": {"min": 30.0, "max": 60.0, "unit": "%"},
    "Basınç": {"min": 15.0, "max": 30.0, "unit": "Pa"},
    "Partikül": {"min": 0.0, "max": 10.0, "unit": "µg/m³"}
}

class WSNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KAA - Akıllı Hastane Temiz Oda Simülatörü")
        self.root.geometry("850x550")
        self.root.configure(bg="#f0f4f8")

        # Başlık ve Üst Panel
        title_frame = tk.Frame(self.root, bg="#1a365d", height=70)
        title_frame.pack(fill="x")
        title_label = tk.Label(title_frame, text="HASTANE TEMİZ ODA SENSÖR AĞI (WSN) MONITORÜ", 
                               fg="white", bg="#1a365d", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=15)

        # Odalar Paneli (Merkezi Alan)
        self.main_frame = tk.Frame(self.root, bg="#f0f4f8", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Sensör Kartları Sözlüğü (Arayüz elemanlarını tutmak için)
        self.sensor_cards = {}
        
        # Sensörleri Ekrana Yerleştirme (2x2 Grid Düzeni)
        sensors_info = [
            ("Sıcaklık", "N1_TEMP", "🌡️"),
            ("Nem", "N2_HUMID", "💧"),
            ("Basınç", "N3_PRESS", "💨"),
            ("Partikül", "N4_PART", "🎛️")
        ]

        for i, (s_type, n_id, icon) in enumerate(sensors_info):
            row = i // 2
            col = i % 2
            
            # Kart Çerçevesi
            card = tk.Frame(self.main_frame, bg="white", bd=2, relief="groove", padx=15, pady=15)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Kart Başlığı (İkon + İsim)
            lbl_title = tk.Label(card, text=f"{icon} {s_type} Sensörü ({n_id})", 
                                 font=("Helvetica", 12, "bold"), bg="white", fg="#2d3748")
            lbl_title.pack(anchor="w")
            
            # Değer Göstergesi
            lbl_val = tk.Label(card, text="--", font=("Helvetica", 24, "bold"), bg="white", fg="#4a5568")
            lbl_val.pack(pady=10)
            
            # Durum Yazısı
            lbl_status = tk.Label(card, text="Sistem Başlatılıyor...", font=("Helvetica", 10, "italic"), bg="white", fg="#718096")
            lbl_status.pack(anchor="w")

            # Referansları sakla
            self.sensor_cards[s_type] = {
                "frame": card,
                "value_label": lbl_val,
                "status_label": lbl_status,
                "node_id": n_id
            }

        # Grid genişleme ayarları
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Alt Bilgi Paneli / Log Alanı
        self.status_bar = tk.Label(self.root, text="Kablosuz ağ algılayıcıları aktif. Veriler Gateway üzerinden okunuyor...", 
                                   bd=1, relief="sunken", anchor="w", bg="#e2e8f0", padx=10, font=("Helvetica", 9))
        self.status_bar.pack(side="bottom", fill="x")

        # Simülasyonu Başlat (Her 2 saniyede bir tetiklenecek)
        self.update_simulation()

    def generate_simulated_data(self, s_type):
        """Sensör tipine göre anomali ihtimalli veri üretir."""
        anomaly = random.random() < 0.15 # %15 ihtimalle hata/kriz durumu
        
        if s_type == "Sıcaklık":
            return round(random.uniform(25.0, 29.0) if anomaly else random.uniform(21.0, 23.5), 2)
        elif s_type == "Nem":
            return round(random.uniform(62.0, 75.0) if anomaly else random.uniform(35.0, 52.0), 2)
        elif s_type == "Basınç":
            return round(random.uniform(0.0, 12.0) if anomaly else random.uniform(18.0, 26.0), 2)
        elif s_type == "Partikül":
            return round(random.uniform(12.0, 45.0) if anomaly else random.uniform(2.0, 5.5), 2)

    def update_simulation(self):
        """Her sensörün verisini yeniler ve görsel alarm durumunu kontrol eder."""
        for s_type, card_elements in self.sensor_cards.items():
            val = self.generate_simulated_data(s_type)
            limits = THRESHOLDS[s_type]
            unit = limits["unit"]
            
            # Değer etiketini güncelle
            card_elements["value_label"].config(text=f"{val} {unit}")
            
            # Eşik Kontrolü ve Renklendirme (Görsel Alarm)
            if val < limits["min"] or val > limits["max"]:
                # KRİTİK DURUM: Kartı kırmızı yap
                card_elements["frame"].config(bg="#fed7d7", highlightbackground="red", highlightcolor="red", highlightthickness=2)
                card_elements["value_label"].config(bg="#fed7d7", fg="#9b2c2c")
                card_elements["status_label"].config(
                    text=f"🚨 ALARM: Değer Sınır Dışı! ({limits['min']}-{limits['max']} olmalı)", 
                    bg="#fed7d7", fg="#9b2c2c", font=("Helvetica", 10, "bold")
                )
            else:
                # NORMAL DURUM: Kartı yeşil/beyaz yap
                card_elements["frame"].config(bg="#f0fff4", highlightbackground="green", highlightcolor="green", highlightthickness=1)
                card_elements["value_label"].config(bg="#f0fff4", fg="#22543d")
                card_elements["status_label"].config(
                    text="✅ Durum: Güvenli / Normal", 
                    bg="#f0fff4", fg="#22543d", font=("Helvetica", 10, "normal")
                )

        # 2000 milisaniye (2 saniye) sonra bu fonksiyonu tekrar çalıştır
        self.root.after(2000, self.update_simulation)

# Uygulamayı Çalıştır
if __name__ == "__main__":
    root = tk.Tk()
    app = WSNApp(root)
    root.mainloop()