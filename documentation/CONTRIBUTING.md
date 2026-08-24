# 🤝 Panduan Kontribusi

Terima kasih atas minat Anda untuk berkontribusi! Panduan ini akan membantu Anda
memulai.

## 🎯 Cara Berkontribusi

- **🐛 Laporkan Bug**: Buat issue dengan detail lengkap
- **💡 Usulkan Fitur**: Diskusikan ide baru via issue
- **📖 Perbaiki Docs**: Tingkatkan dokumentasi
- **🔧 Kirim PR**: Fix bug atau implement fitur
- **🧪 Tambah Test**: Tingkatkan test coverage

## 🔧 Setup Pengembangan

```bash
# 1. Fork & Clone
git clone https://github.com/your-username/PDDIKTI-kemdikbud-API.git
cd PDDIKTI-kemdikbud-API

# 2. Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install Dependensi
pip install -r requirements.txt
pip install -e .

# 4. Verifikasi Setup
python -c "from pddiktipy import api; print('Setup OK!')"
```

## 📝 Panduan Kode

### Standar

- Ikuti panduan style **PEP 8**
- Gunakan **Type Hints** untuk semua functions
- Tulis **Google-style docstrings**
- Jaga functions tetap **kecil** dan terfokus

### Contoh

```python
def search_mahasiswa(self, keyword: str) -> Optional[Dict[str, Any]]:
    """Mencari mahasiswa berdasarkan nama atau NIM.
    
    Args:
        keyword: Nama mahasiswa atau NIM untuk pencarian.
        
    Returns:
        Dictionary berisi data mahasiswa atau None jika error.
    """
    if not keyword.strip():
        raise ValidationError("Keyword tidak boleh kosong")
    return self._make_request('search', {'keyword': keyword})
```

## 🧪 Testing

### Jalankan Test

```bash
# Jalankan semua test (rekomendasi)
python run_tests.py

# Jalankan dengan pytest langsung
pytest tests/ -v
```

### Persyaratan Test

- ✅ **Semua test harus lulus** sebelum submit PR
- ✅ **Test coverage**: Tambahkan test untuk fungsi baru
- ✅ **Data test**: Gunakan data terpusat di `tests/test_data.py`
- ✅ **Tanpa mocking**: Test menggunakan API call nyata untuk validasi

📖 **[Lihat TESTING.md](TESTING.md)** untuk panduan testing lengkap.

## 🔄 Proses Pull Request

1. **Buat branch**: `git checkout -b feature/nama-fitur`
2. **Buat perubahan** sesuai panduan
3. **Tambah test** untuk perubahan baru
4. **Jalankan test**: `python run_tests.py` - **WAJIB LULUS**
5. **Commit**: `git commit -m "Add: deskripsi singkat"`
6. **Push & buat PR**

### Checklist PR

- [ ] **Test lulus** (`python run_tests.py`)
- [ ] **Tambah test** untuk functionality baru
- [ ] Kode mengikuti panduan style
- [ ] Dokumentasi diupdate
- [ ] Pesan commit deskriptif

⚠️ **PENTING**: PR akan ditolak jika test tidak lulus!

## 🐛 Template Laporan Bug

```markdown
**Deskripsi Bug**
Penjelasan singkat tentang bug.

**Cara Mereproduksi**
1. Langkah 1
2. Langkah 2
3. Error terjadi

**Lingkungan**
- OS: Windows 10 / Ubuntu 20.04
- Python: 3.9.7
- pddiktipy: 2.0.4
```

## ➡️ Template Permintaan Fitur

```markdown
**Masalah**
Jelaskan masalah yang akan dipecahkan oleh fitur ini.

**Solusi**
Jelaskan solusi yang Anda usulkan.

**Kasus Penggunaan**
Kapan fitur ini akan berguna?
```

## 📖 Dokumentasi

Update dokumentasi jika:

- Menambah method baru
- Mengubah perilaku API
- Menambah dependensi

File yang perlu diupdate:

- `README.md`: Panduan quick start
- `API_DOCUMENTATION.md`: Referensi API detail
- Code docstrings: Dokumentasi inline

---
