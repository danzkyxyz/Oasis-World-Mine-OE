# 🐉 OasisWorld Telegram Bot Automation

Bot Python ini digunakan untuk **mengotomatiskan aktivitas di OasisWorld MiniApp Telegram**, seperti:
- Autologin via token atau query string
- Auto claim `feed` setiap 12 jam
- Auto submit & finish misi (social + daily)
- Multi akun support (data.txt / token.txt)

---

## 🔧 Fitur Utama

- ✅ **Login otomatis** dengan `init_data` (query) atau `jwt` (token)
- 🍖 **Feed otomatis** (setiap 12 jam)
- 🧹 **Pembersih misi** otomatis (social + daily)
- 🔁 **Loop otomatis** setiap 1 menit
- 👥 **Multi akun support** (multi-threaded)

---

## 📁 Struktur File

```bash
.
├── main.py              # File utama bot
├── data.txt             # List akun berbasis `init_data` (auth via query)
├── token.txt            # List akun berbasis JWT token
```

## 📥 Cara Pakai
1. Clone Repository
```bash
git clone https://github.com/yourusername/oasisworld-bot.git
cd oasisworld-bot
```
2. Install Library Python
```bash
pip install requests
```

## Masukkan Akun

Jika login pakai init_data:
- Edit file data.txt
- Tambahkan 1 baris per akun (hasil dari query login Telegram MiniApp)

Jika login pakai JWT token langsung:

- Edit file token.txt
- Tambahkan 1 token per baris

## Cara cari token dan query

- Buka miniapp
- F12 atau Inspect
- Application
- Local storage > Token
- Session storage > Query

## Jalankan Bot

```bash
python bot.py
```
atau
```bash
python3 main.py
```

## 📌 Catatan
Bot akan:
- Cek power, balance, dan address
- Feed otomatis tiap 12 jam
- Clear misi (submit dan finish jika perlu)
- Akun login akan dieksekusi paralel via threading

## 🧾 Contoh Isi data.txt
```bash
query_id=AAFX72hBxxxxx
```

## 🧾 Contoh Isi data.txt
```bash
EyJxxx
```

# ⚠️ Disclaimer
- Gunakan script ini dengan bijak.
- Kami tidak bertanggung jawab atas pemblokiran akun akibat penyalahgunaan script.
