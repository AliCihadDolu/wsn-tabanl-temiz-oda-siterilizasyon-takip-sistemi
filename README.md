# Akıllı Hastane Temiz Oda KAA Simülatörü

Bu proje, Kablosuz Ağ Algılayıcıları (WSN) dersi kapsamında geliştirilmiştir. Ameliyathane ve yoğun bakım gibi sterilizasyonun kritik olduğu alanlarda ESP32 ağ geçidi (Gateway) ve bağlı sensörlerin (Sıcaklık, Nem, Basınç, Partikül) çalışmasını görsel olarak simüle eder.

## Özellikler
- **Sol Panel:** ESP32 tabanlı KAA donanım şeması ve kablosuz veri akış diyagramı (Kod ile çizilmiştir).
- **Sağ Panel:** Anlık veri takibi yapan dinamik SCADA/Monitor ekranı.
- **Alarm Sistemi:** Değerler kritik eşikleri geçtiğinde (örn: pozitif basınç düştüğünde) kartlar kırmızıya dönerek görsel alarm üretir.
