# 📖 Dokumentasi API PDDIKTI Python Wrapper

Dokumentasi lengkap untuk semua method dan endpoint yang tersedia dalam library `pddiktipy`.

## 📋 Daftar Isi

- [🔍 Method Pencarian](#-method-pencarian)
- [👨‍🎓 Data Mahasiswa](#-data-mahasiswa)
- [👨‍🏫 Data Dosen](#-data-dosen)
- [🏛️ Data Perguruan Tinggi](#️-data-perguruan-tinggi)
- [📚 Data Program Studi](#-data-program-studi)
- [📊 Data Statistik & Visualisasi](#-data-statistik--visualisasi)
- [📰 Data Umum](#-data-umum)
- [🔧 Utility Methods](#-utility-methods)

---

## 🔍 Method Pencarian

### `search_all(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Melakukan pencarian di semua kategori (mahasiswa, dosen, PT, prodi) berdasarkan kata kunci.

**Parameter**:
- `keyword` (str): Kata kunci untuk pencarian

**Return**: Dictionary berisi hasil pencarian dari semua kategori

**Contoh Penggunaan**:
```python
from pddiktipy import api

with api() as client:
    hasil = client.search_all('Unika Soegijapranata')
    print(hasil)
```

**Response Structure**:
```python
[
    'mahasiswa', 
    ['id', 'nama', 'nim', 'nama_pt', 'singkatan_pt', 'nama_prodi'], 
    'dosen', 
    ['id', 'nama', 'nidn', 'nama_pt', 'singkatan_pt', 'nama_prodi'], 
    'pt', 
    ['id', 'kode', 'nama_singkat', 'nama'], 
    'prodi', 
    ['id', 'nama', 'jenjang', 'pt', 'pt_singkat']
]
```

---

### `search_mahasiswa(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mencari mahasiswa berdasarkan nama atau NIM.

**Parameter**:
- `keyword` (str): Nama mahasiswa atau NIM untuk pencarian

**Return**: Dictionary berisi data mahasiswa yang ditemukan

**Contoh Penggunaan**:
```python
with api() as client:
    mahasiswa = client.search_mahasiswa('Ilham Riski')
    if mahasiswa and mahasiswa.get('data'):
        for mhs in mahasiswa['data']:
            print(f"Nama: {mhs['nama']}")
            print(f"NIM: {mhs['nim']}")
            print(f"Universitas: {mhs['nama_pt']}")
```

**Response Fields**:
- `id`: ID unik mahasiswa
- `nama`: Nama lengkap mahasiswa
- `nim`: Nomor Induk Mahasiswa
- `nama_pt`: Nama perguruan tinggi
- `singkatan_pt`: Singkatan perguruan tinggi
- `nama_prodi`: Nama program studi

---

### `search_dosen(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mencari dosen berdasarkan nama atau NIDN.

**Parameter**:
- `keyword` (str): Nama dosen atau NIDN untuk pencarian

**Return**: Dictionary berisi data dosen yang ditemukan

**Contoh Penggunaan**:
```python
with api() as client:
    dosen = client.search_dosen('Prof. Dr. Ilham')
    if dosen and dosen.get('data'):
        for dsn in dosen['data']:
            print(f"Nama: {dsn['nama']}")
            print(f"NIDN: {dsn['nidn']}")
```

**Response Fields**:
- `id`: ID unik dosen
- `nama`: Nama lengkap dosen
- `nidn`: Nomor Induk Dosen Nasional
- `nama_pt`: Nama perguruan tinggi
- `singkatan_pt`: Singkatan perguruan tinggi
- `nama_prodi`: Nama program studi

---

### `search_pt(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mencari perguruan tinggi berdasarkan nama atau singkatan.

**Parameter**:
- `keyword` (str): Nama atau singkatan perguruan tinggi

**Return**: Dictionary berisi data perguruan tinggi yang ditemukan

**Contoh Penggunaan**:
```python
with api() as client:
    pt = client.search_pt('Unika Soegijapranata')
    if pt and pt.get('data'):
        for universitas in pt['data']:
            print(f"Nama: {universitas['nama']}")
            print(f"Kode: {universitas['kode']}")
```

**Response Fields**:
- `id`: ID unik perguruan tinggi
- `kode`: Kode perguruan tinggi
- `nama`: Nama lengkap perguruan tinggi
- `nama_singkat`: Nama singkat/akronim

---

### `search_prodi(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mencari program studi berdasarkan nama.

**Parameter**:
- `keyword` (str): Nama program studi

**Return**: Dictionary berisi data program studi yang ditemukan

**Contoh Penggunaan**:
```python
with api() as client:
    prodi = client.search_prodi('Teknik Informatika')
    if prodi and prodi.get('data'):
        for program in prodi['data']:
            print(f"Nama Prodi: {program['nama']}")
            print(f"Jenjang: {program['jenjang']}")
```

**Response Fields**:
- `id`: ID unik program studi
- `nama`: Nama program studi
- `jenjang`: Jenjang pendidikan (S1, S2, S3, D3, D4)
- `pt`: Nama perguruan tinggi
- `pt_singkat`: Singkatan perguruan tinggi

---

## 👨‍🎓 Data Mahasiswa

### `get_detail_mhs(mahasiswa_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan detail lengkap mahasiswa berdasarkan ID.

**Parameter**:
- `mahasiswa_id` (str): ID mahasiswa dari hasil pencarian

**Return**: Dictionary berisi detail lengkap mahasiswa

**Contoh Penggunaan**:
```python
with api() as client:
    # Dapatkan ID dari pencarian terlebih dahulu
    search_result = client.search_mahasiswa('Ilham')
    if search_result and search_result.get('data'):
        student_id = search_result['data'][0]['id']
        detail = client.get_detail_mhs(student_id)
        if detail:
            print(f"Nama: {detail['nama']}")
            print(f"NIM: {detail['nim']}")
            print(f"Status: {detail['status_saat_ini']}")
```

**Response Fields**:
- `nama`: Nama lengkap mahasiswa
- `nim`: Nomor Induk Mahasiswa
- `jenis_kelamin`: Jenis kelamin (L/P)
- `tempat_lahir`: Tempat lahir
- `tanggal_lahir`: Tanggal lahir
- `nama_pt`: Nama perguruan tinggi
- `nama_prodi`: Nama program studi
- `jenjang`: Jenjang pendidikan
- `tahun_masuk`: Tahun masuk kuliah
- `status_saat_ini`: Status akademik saat ini
- `nama_ibu`: Nama ibu kandung

---

## 👨‍🏫 Data Dosen

### `get_dosen_profile(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan profil lengkap dosen.

**Parameter**:
- `dosen_id` (str): ID dosen dari hasil pencarian

**Return**: Dictionary berisi profil dosen

**Contoh Penggunaan**:
```python
with api() as client:
    profile = client.get_dosen_profile(dosen_id)
    if profile:
        print(f"Nama: {profile['nama_dosen']}")
        print(f"Jabatan: {profile['jabatan_akademik']}")
```

**Response Fields**:
- `nama_dosen`: Nama lengkap dosen
- `nidn`: Nomor Induk Dosen Nasional
- `jabatan_akademik`: Jabatan akademik
- `pendidikan_tertinggi`: Pendidikan terakhir
- `status_ikatan_kerja`: Status kepegawaian
- `status_aktivitas`: Status aktivitas dosen

---

### `get_dosen_penelitian(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan data penelitian yang dilakukan dosen.

**Parameter**:
- `dosen_id` (str): ID dosen

**Return**: Dictionary berisi daftar penelitian dosen

**Contoh Penggunaan**:
```python
with api() as client:
    penelitian = client.get_dosen_penelitian(dosen_id)
    if penelitian and penelitian.get('data'):
        for research in penelitian['data']:
            print(f"Judul: {research['judul_kegiatan']}")
            print(f"Tahun: {research['tahun_kegiatan']}")
```

**Response Fields**:
- `judul_kegiatan`: Judul penelitian
- `tahun_kegiatan`: Tahun pelaksanaan
- `jenis_kegiatan`: Jenis penelitian
- `sumber_dana`: Sumber pendanaan

---

### `get_dosen_pengabdian(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan data pengabdian masyarakat dosen.

**Parameter**:
- `dosen_id` (str): ID dosen

**Return**: Dictionary berisi daftar pengabdian masyarakat

**Contoh Penggunaan**:
```python
with api() as client:
    pengabdian = client.get_dosen_pengabdian(dosen_id)
    if pengabdian and pengabdian.get('data'):
        for service in pengabdian['data']:
            print(f"Judul: {service['judul_kegiatan']}")
            print(f"Tahun: {service['tahun_kegiatan']}")
```

---

### `get_dosen_karya(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan data karya ilmiah dosen.

**Parameter**:
- `dosen_id` (str): ID dosen

**Return**: Dictionary berisi daftar karya ilmiah

---

### `get_dosen_paten(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan data paten yang dimiliki dosen.

**Parameter**:
- `dosen_id` (str): ID dosen

**Return**: Dictionary berisi daftar paten

---

### `get_dosen_study_history(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan riwayat pendidikan dosen.

**Parameter**:
- `dosen_id` (str): ID dosen

**Return**: Dictionary berisi riwayat pendidikan

---

### `get_dosen_teaching_history(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan riwayat mengajar dosen.

**Parameter**:
- `dosen_id` (str): ID dosen

**Return**: Dictionary berisi riwayat mengajar

---

## 🏛️ Data Perguruan Tinggi

### `get_detail_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan detail lengkap perguruan tinggi.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi detail perguruan tinggi

**Contoh Penggunaan**:
```python
with api() as client:
    detail_pt = client.get_detail_pt(pt_id)
    if detail_pt:
        print(f"Nama: {detail_pt['nama_pt']}")
        print(f"Alamat: {detail_pt['alamat']}")
        print(f"Website: {detail_pt['website']}")
        print(f"Akreditasi: {detail_pt['akreditasi_pt']}")
```

**Response Fields**:
- `nama_pt`: Nama perguruan tinggi
- `alamat`: Alamat lengkap
- `website`: Website resmi
- `email`: Email resmi
- `telepon`: Nomor telepon
- `akreditasi_pt`: Status akreditasi
- `bentuk_pt`: Bentuk perguruan tinggi
- `status_pt`: Status perguruan tinggi

---

### `get_prodi_pt(pt_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan daftar program studi di perguruan tinggi untuk tahun tertentu.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi
- `tahun` (Union[int, str]): Tahun akademik (contoh: 20241 atau "20241")

**Return**: Dictionary berisi daftar program studi

**Contoh Penggunaan**:
```python
with api() as client:
    # Kedua format didukung
    prodi_pt = client.get_prodi_pt(pt_id, 20241)    # Integer
    prodi_pt = client.get_prodi_pt(pt_id, "20241")  # String
    
    if prodi_pt and prodi_pt.get('data'):
        for program in prodi_pt['data']:
            print(f"Program Studi: {program['nama_prodi']}")
            print(f"Jenjang: {program['jenjang_prodi']}")
            print(f"Akreditasi: {program['akreditasi']}")
```

**Response Fields**:
- `nama_prodi`: Nama program studi
- `jenjang_prodi`: Jenjang pendidikan
- `akreditasi`: Status akreditasi
- `jumlah_mahasiswa`: Jumlah mahasiswa aktif

---

### `get_logo_pt(pt_id: str) -> Optional[str]`

**Deskripsi**: Mendapatkan logo perguruan tinggi dalam format base64.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: String base64 logo atau None

**Contoh Penggunaan**:
```python
with api() as client:
    logo = client.get_logo_pt(pt_id)
    if logo:
        print(f"Logo tersedia (base64): {len(logo)} karakter")
        # Dapat disimpan sebagai file image
```

---

### `get_rasio_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan rasio mahasiswa terhadap dosen.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi data rasio

---

### `get_mahasiswa_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan statistik mahasiswa perguruan tinggi.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi statistik mahasiswa

---

### `get_waktu_studi_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan data rata-rata waktu studi mahasiswa.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi data waktu studi

---

### `get_name_histories_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan sejarah perubahan nama perguruan tinggi.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi sejarah nama

---

### `get_cost_range_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan kisaran biaya kuliah.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi kisaran biaya

---

### `get_graduation_rate_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan tingkat kelulusan.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi tingkat kelulusan

---

### `get_jumlah_prodi_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan jumlah program studi.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi jumlah program studi

---

### `get_jumlah_mahasiswa_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan jumlah mahasiswa.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi jumlah mahasiswa

---

### `get_jumlah_dosen_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan jumlah dosen.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi jumlah dosen

---

### `get_sarpras_file_name_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan nama file sarana dan prasarana.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi nama file sarpras

---

### `get_sarpras_blob_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan data blob sarana dan prasarana.

**Parameter**:
- `pt_id` (str): ID perguruan tinggi

**Return**: Dictionary berisi data blob sarpras

---

## 📚 Data Program Studi

### `get_detail_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan detail lengkap program studi.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi detail program studi

**Contoh Penggunaan**:
```python
with api() as client:
    detail = client.get_detail_prodi(prodi_id)
    if detail:
        print(f"Nama Prodi: {detail['nama_prodi']}")
        print(f"Jenjang: {detail['jenjang']}")
        print(f"Akreditasi: {detail['akreditasi']}")
```

---

### `get_desc_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan deskripsi program studi.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi deskripsi program studi

---

### `get_name_histories_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan sejarah perubahan nama program studi.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi sejarah nama

---

### `get_num_students_lecturers_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan jumlah mahasiswa dan dosen di program studi.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi jumlah mahasiswa dan dosen

---

### `get_cost_range_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan kisaran biaya kuliah program studi.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi kisaran biaya

---

### `get_daya_tampung_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan kapasitas daya tampung program studi.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi data daya tampung

---

### `get_rasio_dosen_mahasiswa_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan rasio dosen terhadap mahasiswa.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi data rasio

---

### `get_graduation_rate_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan tingkat kelulusan program studi.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: Dictionary berisi tingkat kelulusan

---

### `get_logo_prodi(prodi_id: str) -> Optional[str]`

**Deskripsi**: Mendapatkan logo program studi dalam format base64.

**Parameter**:
- `prodi_id` (str): ID program studi

**Return**: String base64 logo atau None

---

### `get_homebase_prodi(prodi_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan rasio homebase program studi.

**Parameter**:
- `prodi_id` (str): ID program studi
- `tahun` (Union[int, str]): Tahun akademik

**Return**: Dictionary berisi rasio homebase

---

### `get_penghitung_ratio_prodi(prodi_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan penghitung rasio program studi.

**Parameter**:
- `prodi_id` (str): ID program studi
- `tahun` (Union[int, str]): Tahun akademik

**Return**: Dictionary berisi penghitung rasio

---

## 📊 Data Statistik & Visualisasi

### Count Methods

#### `get_dosen_count_active() -> Optional[Dict[str, Any]]`
Mendapatkan jumlah dosen aktif secara nasional.

#### `get_mahasiswa_count_active() -> Optional[Dict[str, Any]]`
Mendapatkan jumlah mahasiswa aktif secara nasional.

#### `get_prodi_count() -> Optional[Dict[str, Any]]`
Mendapatkan jumlah program studi secara nasional.

#### `get_pt_count() -> Optional[Dict[str, Any]]`
Mendapatkan jumlah perguruan tinggi secara nasional.

### Visualisasi Data Dosen

#### `get_data_dosen_keaktifan() -> Optional[Dict[str, Any]]`
Visualisasi data keaktifan dosen.

#### `get_data_dosen_bidang() -> Optional[Dict[str, Any]]`
Visualisasi data dosen berdasarkan bidang studi.

#### `get_data_dosen_jenis_kelamin() -> Optional[Dict[str, Any]]`
Visualisasi distribusi jenis kelamin dosen.

#### `get_data_dosen_jenjang() -> Optional[Dict[str, Any]]`
Visualisasi data dosen berdasarkan jenjang pendidikan.

#### `get_data_dosen_ikatan() -> Optional[Dict[str, Any]]`
Visualisasi data dosen berdasarkan ikatan kerja.

### Visualisasi Data Mahasiswa

#### `get_data_mahasiswa_bidang() -> Optional[Dict[str, Any]]`
Visualisasi data mahasiswa berdasarkan bidang studi.

#### `get_data_mahasiswa_jenis_kelamin() -> Optional[Dict[str, Any]]`
Visualisasi distribusi jenis kelamin mahasiswa.

#### `get_data_mahasiswa_jenjang() -> Optional[Dict[str, Any]]`
Visualisasi data mahasiswa berdasarkan jenjang pendidikan.

#### `get_data_mahasiswa_kelompok_lembaga() -> Optional[Dict[str, Any]]`
Visualisasi data mahasiswa berdasarkan kelompok lembaga.

#### `get_data_mahasiswa_status() -> Optional[Dict[str, Any]]`
Visualisasi data mahasiswa berdasarkan status.

### Visualisasi Data Perguruan Tinggi

#### `get_data_pt_bentuk() -> Optional[Dict[str, Any]]`
Visualisasi data perguruan tinggi berdasarkan bentuk.

#### `get_data_pt_akreditasi() -> Optional[Dict[str, Any]]`
Visualisasi data perguruan tinggi berdasarkan akreditasi.

#### `get_data_pt_kelompok_pembina() -> Optional[Dict[str, Any]]`
Visualisasi data perguruan tinggi berdasarkan kelompok pembina.

#### `get_data_pt_provinsi() -> Optional[Dict[str, Any]]`
Visualisasi data perguruan tinggi berdasarkan provinsi.

### Visualisasi Data Program Studi

#### `get_data_prodi_jenjang() -> Optional[Dict[str, Any]]`
Visualisasi data program studi berdasarkan jenjang.

#### `get_data_prodi_akreditasi() -> Optional[Dict[str, Any]]`
Visualisasi data program studi berdasarkan akreditasi.

#### `get_data_prodi_bidang_ilmu() -> Optional[Dict[str, Any]]`
Visualisasi data program studi berdasarkan bidang ilmu.

#### `get_data_prodi_kelompok_pembina() -> Optional[Dict[str, Any]]`
Visualisasi data program studi berdasarkan kelompok pembina.

**Contoh Penggunaan Statistik**:
```python
with api() as client:
    # Statistik nasional
    total_dosen = client.get_dosen_count_active()
    total_mahasiswa = client.get_mahasiswa_count_active()
    
    print(f"Total Dosen Aktif: {total_dosen}")
    print(f"Total Mahasiswa Aktif: {total_mahasiswa}")
    
    # Data visualisasi
    data_gender = client.get_data_mahasiswa_jenis_kelamin()
    print("Distribusi Gender Mahasiswa:", data_gender)
```

---

## 📰 Data Umum

### `get_contributor() -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan daftar kontributor sistem PDDIKTI.

**Return**: Dictionary berisi daftar kontributor

**Contoh Penggunaan**:
```python
with api() as client:
    contributors = client.get_contributor()
    if contributors:
        print("Kontributor PDDIKTI:", contributors)
```

---

### `get_news() -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan daftar berita terkini dari PDDIKTI.

**Return**: Dictionary berisi daftar berita

**Contoh Penggunaan**:
```python
with api() as client:
    news = client.get_news()
    if news and news.get('data'):
        for article in news['data']:
            print(f"Judul: {article['title']}")
            print(f"Tanggal: {article['date']}")
```

---

### `get_bidang_ilmu_prodi() -> Optional[Dict[str, Any]]`

**Deskripsi**: Mendapatkan daftar bidang ilmu yang tersedia.

**Return**: Dictionary berisi daftar bidang ilmu

**Contoh Penggunaan**:
```python
with api() as client:
    bidang_ilmu = client.get_bidang_ilmu_prodi()
    if bidang_ilmu:
        print("Bidang Ilmu Tersedia:", bidang_ilmu)
```

---

## 🔧 Utility Methods

### Context Manager Support

**Penggunaan Recommended**:
```python
from pddiktipy import api

# Menggunakan context manager (recommended)
with api() as client:
    hasil = client.search_all('keyword')
    # Resource otomatis dibersihkan
```

### Error Handling

Semua method menggunakan decorator `@handle_errors` yang menangani:
- Network errors
- API timeouts
- Invalid responses
- Validation errors

**Contoh Error Handling**:
```python
from pddiktipy import api
from pddiktipy.exceptions import ValidationError, APIConnectionError

try:
    with api() as client:
        result = client.search_mahasiswa("")  # Akan raise ValidationError
except ValidationError as e:
    print(f"Error validasi: {e}")
except APIConnectionError as e:
    print(f"Error koneksi: {e}")
```

### Parameter Flexibility

**Support untuk Multiple Types**:
```python
with api() as client:
    # Kedua format ini didukung
    prodi_int = client.get_prodi_pt(pt_id, 20241)      # Integer
    prodi_str = client.get_prodi_pt(pt_id, "20241")    # String
    
    homebase_int = client.get_homebase_prodi(prodi_id, 20241)    # Integer
    homebase_str = client.get_homebase_prodi(prodi_id, "20241")  # String
```

---

## 📋 Best Practices

### 1. Gunakan Context Manager
```python
# ✅ Recommended
with api() as client:
    result = client.search_all('keyword')

# ❌ Tidak recommended
client = api()
result = client.search_all('keyword')
# Resource tidak otomatis dibersihkan
```

### 2. Handle Errors dengan Proper
```python
try:
    with api() as client:
        result = client.search_mahasiswa(keyword)
        if result and result.get('data'):
            # Process data
            pass
        else:
            print("Tidak ada data ditemukan")
except Exception as e:
    print(f"Error: {e}")
```

### 3. Batch Processing untuk Multiple Queries
```python
with api() as client:
    keywords = ['Unika Soegijapranata', 'ITB', 'UGM']
    results = {}
    
    for keyword in keywords:
        results[keyword] = client.search_pt(keyword)
    
    # Process all results
    for keyword, result in results.items():
        if result and result.get('data'):
            print(f"{keyword}: {len(result['data'])} hasil")
```

### 4. Validasi Data Response
```python
with api() as client:
    result = client.search_mahasiswa('Ilham')
    
    if result and isinstance(result, dict) and result.get('data'):
        for student in result['data']:
            # Validasi field yang diperlukan
            if all(key in student for key in ['nama', 'nim', 'nama_pt']):
                print(f"Valid data: {student['nama']}")
            else:
                print("Data tidak lengkap")
```

---