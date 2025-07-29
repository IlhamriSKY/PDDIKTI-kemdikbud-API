# 🎓 PDDIKTI API Python Library

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/39e00a8c8c1c4007a68d1ae3f53c03e7)](https://app.codacy.com/gh/IlhamriSKY/PDDIKTI-kemdikbud-API/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![BuildStatus](https://api.travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API.svg?branch=main)](https://app.travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API)
[![python3.x](https://img.shields.io/badge/3.12.1-blue.svg?&logo=python&label=Python)](https://www.python.org/downloads/release/python-3121/)
[![Version 2.0.5](https://img.shields.io/pypi/v/pddiktipy?logo=Python&logoColor=white&label=PyPI&color=c125ff)](https://pypi.org/project/pddiktipy/2.0.5/)
[![Downloads](https://img.shields.io/pepy/dt/pddiktipy?logo=PyPI&logoColor=white&label=Downloads&color=c125ff)](https://www.pepy.tech/projects/pddiktipy)
[![Author](https://img.shields.io/badge/Author-Ilham%20Riski-blue.svg?style=flat)](https://github.com/IlhamriSKY)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/blob/master/LICENSE)

> **Library Python untuk mengakses data PDDIKTI Kemdikbud dengan mudah, aman, dan terdokumentasi lengkap**

Wrapper API Python yang powerful dan user-friendly untuk mengambil data dari [PDDIKTI](https://pddikti.kemdikbud.go.id/) Kemdikbud. Library ini menyediakan interface yang mudah digunakan untuk mengakses data mahasiswa, dosen, perguruan tinggi, dan program studi di Indonesia dengan dukungan type hints, error handling yang komprehensif, dan dokumentasi lengkap.

## 📋 Daftar Isi

- [🚀 Fitur Utama](#-fitur-utama)
- [📦 Instalasi](#-instalasi)
- [⚡ Quick Start](#-quick-start)
- [⚠️ Error Handling](#️-error-handling)
- [📚 Dokumentasi Lengkap](#-dokumentasi-lengkap)
- [📊 Struktur Data Response](#-struktur-data-response)
- [📝 Changelog](#-changelog)
- [📋 Requirements](#-requirements)
- [🧪 Testing](#-testing)
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
    hasil = client.search_all('Unika Soegijapranata')
    pprint(hasil)
    
    # Cari mahasiswa spesifik
    mahasiswa = client.search_mahasiswa('Ilham Riski')
    pprint(mahasiswa)
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

## 📚 Dokumentasi Lengkap

**➡️ [API Documentation](documentation/API_DOCUMENTATION.md)** - 63 method API dengan dokumentasi komprehensif, contoh penggunaan, dan struktur data response

## 📊 Struktur Data Response

Semua response API menggunakan TypedDict untuk type safety dan konsistensi. Struktur data disesuaikan dengan konteks pendidikan Indonesia dan standar PDDIKTI.

## 📝 Changelog

**📝 [Changelog](documentation/CHANGELOG.md)** - Riwayat versi dan roadmap pengembangan

## 📋 Requirements

- **Python 3.7+**
- **requests**
- **urllib3**

## 🧪 Testing

**🧪 [Testing Guide](documentation/TESTING.md)** - Panduan testing dan quality assurance

## 🤝 Contributing

**🤝 [Contributing Guide](documentation/CONTRIBUTING.md)** - Panduan berkontribusi pada proyek

## 📄 License

**📄 [MIT License](LICENSE)** - Distributed under the MIT License

---

## 📞 Support & Contact

- **Author**: [Ilham Riski](https://github.com/IlhamriSKY)
- **Issues**: [GitHub Issues](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/issues)
- **PyPI**: [pddiktipy](https://pypi.org/project/pddiktipy/)

---

**⭐ Jika library ini membantu proyek Anda, jangan lupa untuk memberikan star di GitHub!**
