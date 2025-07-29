# 🎓 PDDIKTI API Python Wrapper

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/39e00a8c8c1c4007a68d1ae3f53c03e7)](https://app.codacy.com/gh/IlhamriSKY/PDDIKTI-kemdikbud-API/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![BuildStatus](https://api.travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API.svg?branch=main)](https://app.travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API)
[![python3.x](https://img.shields.io/badge/3.12.1-blue.svg?&logo=python&label=Python)](https://www.python.org/downloads/release/python-3121/)
[![Version 2.0.5](https://img.shields.io/pypi/v/pddiktipy?logo=Python&logoColor=white&label=PyPI&color=c125ff)](https://pypi.org/project/pddiktipy/2.0.5/)
[![Downloads](https://img.shields.io/pepy/dt/pddiktipy?logo=PyPI&logoColor=white&label=Downloads&color=c125ff)](https://www.pepy.tech/projects/pddiktipy)
[![Author](https://img.shields.io/badge/Author-Ilham%20Riski-blue.svg?style=flat)](https://github.com/IlhamriSKY)
[![License](https://img.shields.io/github/license/IlhamriSKY/PDDIKTI-kemdikbud-API.svg)](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/blob/master/LICENSE)

> **Library Python untuk mengakses data PDDIKTI Kemdikbud dengan mudah, aman, dan terdokumentasi lengkap**

Wrapper API Python yang powerful dan user-friendly untuk mengambil data dari [PDDIKTI](https://pddikti.kemdikbud.go.id/) Kemdikbud. Library ini menyediakan interface yang mudah digunakan untuk mengakses data mahasiswa, dosen, perguruan tinggi, dan program studi di Indonesia dengan dukungan type hints, error handling yang komprehensif, dan dokumentasi lengkap.

## 📋 Daftar Isi

- [🚀 Fitur Utama](#-fitur-utama)
- [📦 Instalasi](#-instalasi)
- [⚡ Quick Start](#-quick-start)
- [📚 Penggunaan Lengkap](#-penggunaan-lengkap)
- [🔧 Fitur Lanjutan](#-fitur-lanjutan)
- [⚠️ Error Handling](#️-error-handling)
- [📊 Struktur Data Response](#-struktur-data-response)
- [📖 Dokumentasi API Lengkap](#-dokumentasi-api-lengkap)
- [🔄 Changelog](#-changelog)
- [📋 Requirements](#-requirements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🚀 Fitur Utama

- ✅ **Type Hints Lengkap**: Full type annotations untuk better IDE support
- ✅ **Error Handling Komprehensif**: Custom exceptions dan validation
- ✅ **Context Manager Support**: Resource management yang aman
- ✅ **Dokumentasi Lengkap**: Google-style docstrings dengan 63 API methods
- ✅ **Performance Optimized**: Connection pooling dan retry strategy
- ✅ **Indonesian Context**: Field explanations dalam konteks pendidikan Indonesia
- ✅ **Flexible Parameters**: Support untuk integer dan string parameters
- ✅ **Production Ready**: Enhanced validation dan logging

## 📦 Instalasi

```bash
pip install pddiktipy
```

**Requirements:**
- Python 3.7+
- requests
- urllib3

## ⚡ Quick Start

```python
from pddiktipy import api
from pprint import pprint

# Menggunakan context manager (recommended)
with api() as client:
    # Cari semua data dengan keyword
    hasil = client.search_all('Universitas Indonesia')
    pprint(hasil)
    
    # Cari mahasiswa spesifik
    mahasiswa = client.search_mahasiswa('Ahmad Rizki')
    pprint(mahasiswa)
```

## 📚 Penggunaan Lengkap

### Context Manager

**Direkomendasikan** untuk menggunakan context manager untuk resource management yang aman:

```python
from pddiktipy import api

# Context manager otomatis handle resource cleanup
with api() as client:
    hasil = client.search_all('data yang dicari')
    print(hasil)
# Resource otomatis dibersihkan di sini
```

### Contoh Pencarian Data

#### 1. Pencarian Mahasiswa

```python
with api() as client:
    mahasiswa = client.search_mahasiswa('Ahmad Rizki')
    
    if mahasiswa and mahasiswa.get('data'):
        for mhs in mahasiswa['data']:
            print(f"Nama: {mhs['nama']}")
            print(f"NIM: {mhs['nim']}")
            print(f"Universitas: {mhs['nama_pt']}")
            print(f"Prodi: {mhs['nama_prodi']}")
            print("-" * 30)
```

#### 2. Pencarian Dosen

```python
with api() as client:
    dosen = client.search_dosen('Prof. Dr.')
    
    if dosen and dosen.get('data'):
        for dsn in dosen['data']:
            print(f"Nama: {dsn['nama']}")
            print(f"NIDN: {dsn['nidn']}")
            print(f"Universitas: {dsn['nama_pt']}")
```

#### 3. Detail Perguruan Tinggi

```python
with api() as client:
    # Cari universitas
    pt_search = client.search_pt('Universitas Indonesia')
    if pt_search and pt_search.get('data'):
        pt_id = pt_search['data'][0]['id']
        
        # Detail universitas
        detail_pt = client.get_detail_pt(pt_id)
        if detail_pt:
            print(f"Nama: {detail_pt['nama_pt']}")
            print(f"Alamat: {detail_pt['alamat']}")
            print(f"Website: {detail_pt['website']}")
            print(f"Akreditasi: {detail_pt['akreditasi_pt']}")
```

## 🔧 Fitur Lanjutan

### Flexible Year Parameter

```python
with api() as client:
    pt_id = "some_university_id"
    
    # Kedua format ini didukung (bug integer parsing telah diperbaiki)
    prodi_int = client.get_prodi_pt(pt_id, 20241)      # Integer
    prodi_str = client.get_prodi_pt(pt_id, "20241")    # String
```

### Batch Processing

```python
with api() as client:
    keywords = ['Universitas Indonesia', 'ITB', 'UGM']
    
    results = {}
    for keyword in keywords:
        results[keyword] = client.search_pt(keyword)
        
    for keyword, result in results.items():
        if result and result.get('data'):
            print(f"{keyword}: {len(result['data'])} hasil")
```

## ⚠️ Error Handling

Library ini menyediakan error handling yang komprehensif:

```python
from pddiktipy import api
from pddiktipy.exceptions import (
    ValidationError, 
    APIConnectionError, 
    APITimeoutError,
    PDDIKTIError
)

try:
    with api() as client:
        # Ini akan raise ValidationError karena keyword kosong
        result = client.search_mahasiswa("")
        
except ValidationError as e:
    print(f"Error validasi: {e}")
except APIConnectionError as e:
    print(f"Error koneksi: {e}")
except APITimeoutError as e:
    print(f"Request timeout: {e}")
except PDDIKTIError as e:
    print(f"Error PDDIKTI API: {e}")
```

### Custom Exceptions

- **`PDDIKTIError`**: Base exception untuk semua error
- **`ValidationError`**: Error validasi parameter
- **`APIConnectionError`**: Error koneksi network
- **`APITimeoutError`**: Request timeout
- **`APIRateLimitError`**: Rate limit exceeded
- **`APIResponseError`**: Error response dari API

## 📊 Struktur Data Response

### Data Mahasiswa
```python
{
    'id': 'unique_identifier',
    'nama': 'Nama Lengkap',
    'nim': '123456789',
    'nama_pt': 'Nama Universitas',
    'singkatan_pt': 'UNIV',
    'nama_prodi': 'Program Studi',
    'jenis_kelamin': 'L/P',
    'jenjang': 'S1/S2/S3/D3/D4',
    'status_saat_ini': 'Status Akademik',
    'tahun_masuk': '2020'
}
```

### Data Dosen
```python
{
    'id': 'unique_identifier',
    'nama': 'Nama Lengkap',
    'nidn': '1234567890',
    'nama_pt': 'Nama Universitas',
    'singkatan_pt': 'UNIV',
    'nama_prodi': 'Program Studi',
    'jabatan_akademik': 'Jabatan',
    'pendidikan_tertinggi': 'S3/S2/S1',
    'status_ikatan_kerja': 'Status',
    'status_aktivitas': 'Aktif/Tidak Aktif'
}
```

## 📖 Dokumentasi API Lengkap

Untuk dokumentasi API yang komprehensif dengan semua method dan parameter yang tersedia, silakan lihat:

**➡️ [API Documentation](API_DOCUMENTATION.md)**

Dokumentasi ini mencakup:
- 🔍 **63 Method API** dengan penjelasan detail
- 📝 **Parameter & Return Values** untuk setiap method
- 💡 **Contoh penggunaan** yang praktis
- 📊 **Struktur data response** yang lengkap
- 🛠️ **Best practices** dan tips penggunaan

### Quick Links ke Dokumentasi API:
- [Method Pencarian](API_DOCUMENTATION.md#-method-pencarian) - Search mahasiswa, dosen, PT, prodi
- [Data Mahasiswa](API_DOCUMENTATION.md#-data-mahasiswa) - Detail dan statistik mahasiswa
- [Data Dosen](API_DOCUMENTATION.md#-data-dosen) - Profil, penelitian, pengabdian dosen
- [Data Perguruan Tinggi](API_DOCUMENTATION.md#️-data-perguruan-tinggi) - Detail PT dan statistik
- [Data Program Studi](API_DOCUMENTATION.md#-data-program-studi) - Detail prodi dan metrics
- [Data Statistik](API_DOCUMENTATION.md#-data-statistik--visualisasi) - Visualisasi dan analytics

## 🔄 Changelog

### V 2.0.5 (Versi Terbaru Stabil) ⭐
- ✅ **Dokumentasi API Lengkap**: 63 method terdokumentasi komprehensif
- ✅ **Lokalisasi Indonesia**: Dokumentasi penuh dalam bahasa Indonesia
- ✅ **Enhanced Error Handling**: Custom exception hierarchy yang ditingkatkan
- ✅ **Full Type Hints Support**: 100% coverage untuk better IDE experience
- ✅ **Comprehensive Documentation**: Google-style docstrings di semua method
- ✅ **Context Manager Support**: Resource management yang aman
- ✅ **Performance Improvements**: Connection pooling dan retry strategy
- ✅ **Bug Fixes**: Integer parsing di `get_prodi_pt()` dan validasi parameter

### Versi Sebelumnya
- **V 2.0.4**: Enhanced error handling dan documentation improvements
- **V 2.0.3**: Fix code bugs dan stability improvements
- **V 2.0.0**: Major refactor untuk align dengan updated API
- **V 1.0.0**: First release dengan basic functionality

**📋 [Lihat Changelog Lengkap](CHANGELOG.md)** untuk detail semua perubahan dan roadmap versi mendatang.

## 📋 Requirements

- **Python**: 3.7+
- **Dependencies**:
  - `requests`: HTTP library
  - `urllib3`: HTTP client
  - `typing`: Type hints (built-in untuk Python 3.7+)

## 🤝 Contributing

Kontribusi sangat diterima! Kami menyambut berbagai jenis kontribusi dari community.

### Quick Contribution Guide

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### 📚 Detailed Contributing Guide

**➡️ [CONTRIBUTING.md](CONTRIBUTING.md)**

Untuk panduan lengkap tentang:
- 🐛 **Melaporkan bug** dengan template yang tepat
- 💡 **Mengusulkan fitur baru** dan feature requests
- 🔧 **Development setup** dan environment configuration
- 📝 **Code guidelines** dan best practices
- 🧪 **Testing procedures** dan coverage requirements
- 📖 **Documentation standards** dan formatting
- 🔄 **Pull request process** step-by-step

### Development Setup (Quick)

```bash
# Clone repository
git clone https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API.git
cd PDDIKTI-kemdikbud-API

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python run_tests.py
```

**📖 [Lihat Contributing Guide Lengkap](CONTRIBUTING.md)** untuk detail setup dan guidelines.

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 📞 Support & Contact

- **Author**: [Ilham Riski](https://github.com/IlhamriSKY)
- **Issues**: [GitHub Issues](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/issues)
- **PyPI**: [pddiktipy](https://pypi.org/project/pddiktipy/)
- **📖 API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### 📚 Dokumentasi Lengkap
- **[README.md](README.md)**: Panduan penggunaan dan contoh dasar
- **[API Documentation](API_DOCUMENTATION.md)**: Dokumentasi lengkap semua method API
- **[Changelog](CHANGELOG.md)**: Version history dan roadmap
- **[Contributing](CONTRIBUTING.md)**: Panduan untuk berkontribusi
- **Code Comments**: Inline documentation dalam source code

---

**⭐ Jika library ini membantu proyek Anda, jangan lupa untuk memberikan star di GitHub!**
