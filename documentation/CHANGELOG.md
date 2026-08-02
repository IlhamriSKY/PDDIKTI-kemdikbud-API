# 📋 Changelog

All notable changes to this project are documented in this file.

## [2.1.0] - 2026-08-02 (Upstream Migration + Cloudflare) 🚨

### 💥 Breaking
- **Old host retired**: `api-pddikti.kemdiktisaintek.go.id` now refuses connections.
  The base URL moved to same-origin `https://pddikti.kemdiktisaintek.go.id/api`.
- **Cloudflare Turnstile**: the upstream now requires browser-solved clearance.
  `api()` with no arguments is no longer sufficient — see the README
  "Cloudflare access" section.

### ✨ Added
- New constructor: `api(base_url=..., session=..., cf_clearance=..., user_agent=..., auto_cookie=...)`.
  - `auto_cookie=True` reads `cf_clearance` from a local browser (`pip install "pddiktipy[auto]"`).
- Transparent AES-256-CBC decryption for `search_all()` (endpoint is now `pencarian/enc/all`).
- New helpers: `encrypt_id()`, `decrypt_id()`, `decrypt()`.
- New methods: `get_announcements`, `get_publications`, `get_activities`,
  `get_activity_detail`, `get_pt_locations`, `get_dosen_count`, `get_mahasiswa_count`.
- Full endpoint coverage — added the remaining upstream endpoints:
  `search_pt_filter`, `search_prodi_filter` (`/v2/*/search/filter`), and
  `get_beranda` (`/beranda`).
- Actionable 403 error message explaining how to supply clearance.

### 🔀 Changed
- `detail/pt` → `pt/detail` (`get_detail_pt`).
- `news/list` → `content/announcements`; `get_news()` is kept as a paginated alias
  of `get_announcements()`.
- New dependency: `cryptography`. Optional: `browser_cookie3` (extra `[auto]`).
- Trimmed verbose docstrings and switched to a library `NullHandler` logger.

### ✅ Verified live (2026-08-02)
- `pt/count` → `{"status":"success","data":{"jumlah":4416}}`.
- `pencarian/enc/all/undip` → encrypted blob decrypted to valid UNDIP student data
  using the AES key/IV in `helper.py`.
- Verified through a browser session that had passed the Cloudflare Turnstile check.

## [2.0.6] - 2025-07-30 (Bug Fix Release) 🐛

### 🐛 Diperbaiki
- **Critical Fix**: Memperbaiki method `get_prodi_pt()` yang gagal dengan semester codes (Issue GitHub)
  - **Root Cause**: Method menggunakan endpoint yang salah `"pt/detail"` → **Fixed**: `"pt/prodi"`  
  - **Impact**: Method sekarang berhasil mengembalikan data program studi untuk semester 20241, 20242, dll
  - **Validation**: Semester validation tetap berfungsi dengan benar (format YYYYS)
  - **Testing**: Method telah diverifikasi dengan 308 programs dari Universitas Indonesia

### ✅ Testing & Verification  
- **New Test Suite**: Menambahkan `test_fix_verification.py` dengan 4 comprehensive tests
  - Test valid semester 20241 & 20242
  - Test invalid semester format validation  
  - Test dengan real university data
- **Test Results**: 72 total tests (68 original + 4 new) - **ALL PASSED** ✅
- **Backward Compatibility**: Semua existing tests masih berjalan sempurna

### 🛠️ Technical Details
- **File Changed**: `pddiktipy/api.py` line 888
- **Error Handling**: Tetap mengembalikan `None` untuk input tidak valid
- **API Endpoint**: Menggunakan official PDDIKTI API `kemdiktisaintek.go.id`
- **Performance**: Tidak ada perubahan performa, hanya perbaikan endpoint

### 📊 Impact
- **Breaking Changes**: ❌ TIDAK ADA - Full backward compatibility
- **Method Signature**: Tidak berubah
- **Production Ready**: ✅ Siap untuk production use

## [2.0.5.post1] - 2025-07-29 (Patch Release) 🔧

### 🔧 Diperbaiki
- **Build System**: Optimasi konfigurasi packaging untuk PyPI
  - Perbaikan format metadata license di `setup.py`
  - Exclusion folder `tests/` dari distribution package
  - Optimasi `MANIFEST.in` untuk package yang lebih clean
  - Validasi PyPI compatibility (PASSED twine check)

### 📦 Package Improvements
- **Package Size**: Reduced package size dengan menghapus development files
- **Distribution**: Hanya include file utama (`pddiktipy/` + essentials)
- **Metadata**: Format license yang kompatibel dengan PyPI standards

### 🛠️ Technical Changes
- Update build system dari `pyproject.toml` ke `setup.py` untuk compatibility
- Perbaikan exclude configuration untuk test files
- Clean distribution tanpa folder development/testing

## [2.0.5] - 2025-07-29 (Versi Terbaru Stabil) 🔥 [🚨 Breaking Changes]

### ✅ Ditambahkan
- **Dokumentasi API Lengkap**: `API_DOCUMENTATION.md` yang komprehensif
  - 📖 **63 Method API** terdokumentasi lengkap dengan contoh
  - 🔍 **Method Pencarian**: `search_all`, `search_mahasiswa`, `search_dosen`, `search_pt`, `search_prodi`
  - 👨‍🎓 **Data Mahasiswa**: `get_detail_mhs` dengan informasi profil lengkap

- **Sistem Dokumentasi yang Ditingkatkan**:
  - 🏠 **README.md**: Penulisan ulang lengkap dalam bahasa Indonesia
  - 📋 **CHANGELOG.md**: Riwayat versi detail dengan roadmap
  - 🤝 **CONTRIBUTING.md**: Panduan kontribusi yang diperkecil

- **Docstring Gaya Google**: Semua method utama didokumentasikan dengan:
  - Deskripsi parameter dengan type hints
  - Spesifikasi nilai return
  - Contoh penggunaan dengan skenario dunia nyata
  - Penjelasan penanganan error
  - Contoh struktur response

### 🔄 Diubah
- **Bahasa Dokumentasi**: Lokalisasi penuh bahasa Indonesia
- **Struktur Proyek**: Organisasi dan aksesibilitas yang lebih baik
- **Pengalaman Pengguna**: Setup dan proses kontribusi yang disederhanakan

### 📚 Cakupan Dokumentasi
- **100% Cakupan API**: Semua 63 method dari `api.py` terdokumentasi
- **Mobile-Friendly**: Format dokumentasi responsif
- **Siap IDE**: Dukungan IntelliSense yang ditingkatkan

### 🛠️ Peningkatan Teknis
- **Type Safety**: Cakupan type hint penuh tetap dipertahankan
- **Penanganan Error**: Hierarki exception kustom terdokumentasi
- **Performa**: Connection pooling dan strategi retry
- **Kualitas Kode**: Keterbacaan dan maintainability yang ditingkatkan

## [2.0.4] - 2024-Rilis Sebelumnya

### ✅ Ditambahkan
- **Penanganan Error yang Ditingkatkan**: Hierarki exception kustom yang komprehensif
  - `PDDIKTIError`: Base exception untuk semua error
  - `ValidationError`: Error validasi parameter  
  - `APIConnectionError`: Error koneksi network
  - `APITimeoutError`: Request timeout
  - `APIRateLimitError`: Rate limit exceeded
  - `APIResponseError`: Error response dari API

- **Dukungan Type Hints Penuh**: 100% cakupan type di seluruh codebase
  - Dukungan `Union`, `Optional`, `TypeVar`, `Dict`, `List`
  - Alias type kustom: `APIResponse`, `APIMethod`
  - Dukungan IDE dan autocompletion yang ditingkatkan

- **Dukungan Context Manager**: Manajemen resource yang aman
  ```python
  with api() as client:
      result = client.search_all('keyword')
  # Resource otomatis dibersihkan
  ```

- **Dokumentasi Komprehensif**: 
  - Docstring gaya Google untuk semua method utama
  - Penjelasan field dalam konteks pendidikan Indonesia
  - Contoh penggunaan dunia nyata

- **Peningkatan Performa**:
  - Connection pooling dan strategi retry
  - Manajemen session yang ditingkatkan
  - Request HTTP yang dioptimalkan

### 🐛 Diperbaiki
- **Bug Integer Parsing**: Memperbaiki bug di fungsi `get_prodi_pt()`
  - Method `parse()` yang ditingkatkan dengan dukungan `Union[int, str]`
  - Kedua format sekarang didukung: `get_prodi_pt(pt_id, 20241)` dan `get_prodi_pt(pt_id, "20241")`

- **Validasi Parameter**: Validasi yang ditingkatkan dengan pesan error informatif
- **Penanganan Response**: Peningkatan penanganan error untuk response API yang tidak valid
- **Manajemen Memori**: Memperbaiki potensi memory leak dalam HTTP session

### 🔄 Diubah
- **Signature Method**: Diperbarui dengan type hints yang tepat
- **Pesan Error**: Lebih deskriptif dan user-friendly
- **Format Dokumentasi**: Distandarisasi ke docstring gaya Google
- **Struktur Kode**: Peningkatan modularitas dan maintainability

### 📚 Dokumentasi
- **README.md**: Penulisan ulang lengkap dalam bahasa Indonesia
  - Daftar isi yang komprehensif
  - Contoh yang ditingkatkan dengan skenario dunia nyata
  - Pengalaman pengguna yang lebih baik dengan emoji dan struktur yang jelas
- **API_DOCUMENTATION.md**: Dokumentasi lengkap untuk semua 63 method API
- **CHANGELOG.md**: Riwayat versi yang detail

### 🔧 Teknis
- **Update Dependensi**: Diperbarui ke versi terbaru yang kompatibel
- **Kualitas Kode**: Ditingkatkan dengan linting dan formatting
- **Testing**: Test suite komprehensif dengan 100% pass rate
- **CI/CD**: Proses build dan deployment yang diperbaiki

## [2.0.3] - 2024-Sebelumnya

### 🐛 Diperbaiki
- Berbagai bug kode dan peningkatan stabilitas
- Optimisasi performa minor

## [2.0.0] - 2024-Rilis Besar

### 🔄 Diubah
- **Refactor Besar**: Refactor codebase lengkap untuk diselaraskan dengan API yang diperbarui
- **Perubahan Besar**: Signature method dan format response yang diperbarui
- **Endpoint API**: Diperbarui ke endpoint PDDIKTI terbaru
- **Autentikasi**: Mekanisme autentikasi yang ditingkatkan

### ⚠️ Perubahan Besar
- Signature method berubah untuk beberapa fungsi
- Update format response untuk konsistensi
- Method yang deprecated dihapus

## [1.0.0] - 2023-Rilis Awal

### ✅ Ditambahkan
- **Rilis Pertama**: Versi awal dari PDDIKTI API wrapper
- **Fungsionalitas Dasar**: Method pencarian inti dan pengambilan data
- **Method Pencarian**: 
  - `search_all()`: Pencarian di semua kategori
  - `search_mahasiswa()`: Pencarian mahasiswa
  - `search_dosen()`: Pencarian dosen
  - `search_pt()`: Pencarian perguruan tinggi
  - `search_prodi()`: Pencarian program studi

- **Method Detail**:
  - `get_detail_mhs()`: Detail mahasiswa
  - `get_dosen_profile()`: Profil dosen
  - `get_detail_pt()`: Detail perguruan tinggi
  - `get_detail_prodi()`: Detail program studi

- **Penanganan Error Dasar**: Penanganan exception sederhana
- **HTTP Client**: Implementasi requests dasar

---

## 🎯 Roadmap

### ✅ Selesai di 2.0.5
- ✅ **Dokumentasi Lengkap**: Sistem dokumentasi API yang komprehensif
- ✅ **Lokalisasi Indonesia**: Dukungan bahasa Indonesia penuh
- ✅ **Panduan Kontribusi**: Proses kontribusi yang diperkecil
- ✅ **Referensi Silang**: Navigasi mulus antar dokumentasi

### Versi Mendatang (Direncanakan)

#### [2.1.0] - Segera Hadir
- **Enhanced Caching**: Redis/Memory caching untuk peningkatan performa
- **Dukungan Async**: Dukungan async/await untuk request bersamaan
- **Rate Limiting**: Rate limiting pintar untuk menghindari API throttling
- **Fitur Export**: Export data ke berbagai format (CSV, Excel, JSON)

#### [2.2.0] - Masa Depan
- **Tool CLI**: Command-line interface untuk query cepat
- **Visualisasi Data**: Tool plotting dan visualisasi built-in
- **Pencarian Lanjutan**: Pencarian dengan multiple filter dan sorting
- **Operasi Batch**: Kemampuan pemrosesan data massal

#### [3.0.0] - Jangka Panjang
- **Dukungan GraphQL**: Interface GraphQL alternatif
- **WebSocket**: Streaming data real-time
- **Machine Learning**: Pencarian dan rekomendasi bertenaga ML
- **REST API Server**: API server built-in untuk penyajian data

---

## 📊 Statistik Versi

| Versi | Tanggal Rilis | Method | Fitur | Perbaikan Bug | Dokumentasi |
|-------|---------------|--------|-------|---------------|-------------|
| 2.0.5 | 2025-07-29    | 63     | 18    | 8             | Lengkap ✅  |
| 2.0.4 | 2024-Current  | 63     | 15    | 8             | Sebagian    |
| 2.0.3 | 2024          | 58     | 12    | 5             | Dasar       |
| 2.0.0 | 2024          | 55     | 10    | -             | Minimal     |
| 1.0.0 | 2023          | 30     | 5     | -             | Tidak Ada   |

---