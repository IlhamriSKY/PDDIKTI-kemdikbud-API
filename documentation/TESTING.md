# 🧪 Framework Testing PDDIKTI API

## 🚀 Cara Menjalankan Testing

### 1. Setup Virtual Environment

#### Windows (PowerShell/Command Prompt)
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\activate

# Install dependensi testing
pip install -r requirements-test.txt
```

#### Linux/macOS (Terminal)
```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependensi testing
pip install -r requirements-test.txt
```

### 2. Deaktivasi Virtual Environment (Setelah Selesai)
```bash
# Deaktivasi virtual environment (Windows dan Linux)
deactivate
```

### 3. Jalankan Testing
```bash
# Metode 1: Menggunakan run_tests.py (Rekomendasi)
python run_tests.py

# Metode 2: Menggunakan pytest langsung  
pytest tests/ -v

# Metode 3: Jalankan file test tertentu
pytest tests/test_comprehensive.py -v
```

## 📊 Hasil Testing (100% PASS - 87 Test)

```bash
$ python run_tests.py

============================================================
PDDIKTI API TEST SUITE
============================================================
Testing Universitas Unika Soegijapranata Data
Student: Ilham Riski
Lecturer: Ridwan Sanjaya
Program: Sistem Informasi
============================================================

✅ tests/test_api_final.py         → 18 test PASS
✅ tests/test_comprehensive.py     → 69 test PASS  

================================================
87 PASS dalam 46.13 detik
================================================

SUKSES: Semua test berhasil!
Framework telah dioptimasi dan siap untuk digunakan di produksi!
```

## 💡 Catatan Penting

### Keunggulan Virtual Environment
- **Dependensi terisolasi** - Mencegah konflik dengan package sistem
- **Testing yang bersih** - Memastikan lingkungan test yang konsisten
- **Mudah dibersihkan** - Dapat menghapus folder venv untuk menghapus semua dependensi test
- **Kontrol versi** - Versi package spesifik dari requirements-test.txt

### Prasyarat
- Python 3.8+ terinstall di sistem Anda
- Koneksi internet untuk mendownload package
- Privilegi Administrator/sudo mungkin diperlukan untuk beberapa instalasi

## 🏃‍♂️ Referensi Cepat Perintah Testing

**⚠️ Penting: Pastikan virtual environment sudah diaktifkan sebelum menjalankan testing!**

```bash
# Jalankan semua test (87 test)
python run_tests.py

# Jalankan dengan output detail
pytest tests/ -v -s

# Jalankan hanya comprehensive test (69 test)
pytest tests/test_comprehensive.py -v

# Jalankan hanya basic test (18 test)  
pytest tests/test_api_final.py -v

# Jalankan metode test tertentu
pytest tests/test_comprehensive.py::TestAPIComprehensive::test_search_all_method -v

# Jalankan test dengan laporan coverage
pytest tests/ --cov=pddiktipy --cov-report=html

# Jalankan test secara paralel (eksekusi lebih cepat)
pytest tests/ -n auto
```

## 📋 Struktur File Testing

```
tests/
├── test_comprehensive.py    # 69 test - Semua metode API
├── test_api_final.py        # 18 test - Fungsi dasar  
├── test_data.py             # Konstanta data test
├── conftest.py              # Konfigurasi Pytest
└── __init__.py              # Inisialisasi package
```

---

**✅ Hasil: 87 test, 100% tingkat keberhasilan, waktu eksekusi 46.13 detik**

**🎯 Coverage Lengkap:** Semua metode API dari `api.py` telah ditest dan divalidasi sepenuhnya
