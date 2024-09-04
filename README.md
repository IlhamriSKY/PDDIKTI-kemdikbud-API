# Python 3 API wrapper to retrieve data from [PDDIKTI](https://pddikti.kemdikbud.go.id/) Kemdikbud.

[![License](https://img.shields.io/github/license/IlhamriSKY/PDDIKTI-kemdikbud-API.svg)](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/blob/master/LICENSE)
[![BuildStatus](https://travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API.svg?branch=main)](https://app.travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API)
[![Version 2.0.0](https://img.shields.io/badge/stable-2.0.0-brightgreen.svg "Version 2.0.0")](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API)
[![python3.x](https://img.shields.io/badge/3.8%20%7C%203.9-blue.svg?&logo=python&label=Python)](https://www.python.org/downloads/release/python-391/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/39e00a8c8c1c4007a68d1ae3f53c03e7)](https://app.codacy.com/gh/IlhamriSKY/PDDIKTI-kemdikbud-API/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

## Change Log

*   V 1.0.0 "First Release"
*   V 2.0.0 "Latest Stable Version"

## Requirements

*   Python 3.\*
*   requests

## Installation

```sh
$ pip install pddiktipy
```

## Pengenalan

Kelas `api` dari modul `pddiktipy` adalah sebuah antarmuka yang dirancang untuk mengakses berbagai data melalui API. Kelas ini menyediakan berbagai metode untuk melakukan pencarian dan pengambilan informasi terkait mahasiswa, dosen, program studi, universitas, dan berbagai data pendidikan lainnya.

## Cara Menggunakan

### 1\. Mengimpor Kelas dan Membuat Instance

``` python
from pddiktipy import api
from pprint import pprint as p
a = api()

p(a.search_all('ilham riski'))
```

Kode di atas mengimpor kelas `api` dari modul `pddiktipy` dan membuat sebuah instance dari kelas tersebut. Objek `a` sekarang dapat digunakan untuk memanggil berbagai metode yang tersedia dalam kelas `api`.

### 2\. Menggunakan Metode `search_all`

``` python
p(a.search_all('ilham riski'))
```

Kode ini menggunakan metode `search_all` untuk melakukan pencarian dengan kata kunci `'ilham riski'`. Hasil pencarian akan dicetak dengan rapi menggunakan fungsi `pprint`.

## Penjelasan Setiap Fungsi

### 1\. `search_all(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk melakukan pencarian di semua kategori berdasarkan kata kunci yang diberikan.

**Parameter**:  
`keyword (str)`: Kata kunci untuk pencarian.

**Contoh Penggunaan**:  

``` python
result = a.search_all('ilham riski')
```

**Return**:  
Mengembalikan hasil pencarian dalam bentuk JSON yang mencakup data dari berbagai kategori seperti mahasiswa, dosen, universitas, dan program studi.

### 2\. `search_mahasiswa(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mencari mahasiswa berdasarkan kata kunci yang diberikan.

**Parameter**:  
`keyword (str)`: Nama mahasiswa untuk pencarian.

**Contoh Penggunaan**:  

``` python
result = a.search_mahasiswa('Ilham')
```

**Return**:  
Mengembalikan data mahasiswa yang sesuai dengan kata kunci yang diberikan.

### 3\. `search_dosen(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mencari dosen berdasarkan kata kunci yang diberikan.

**Parameter**:  
`keyword (str)`: Nama dosen untuk pencarian.

**Contoh Penggunaan**:  

``` python
result = a.search_dosen('Ilham')
```

**Return**:  
Mengembalikan data dosen yang sesuai dengan kata kunci yang diberikan.

### 4\. `search_pt(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mencari universitas berdasarkan kata kunci yang diberikan.

**Parameter**:  
`keyword (str)`: Nama universitas untuk pencarian.

**Contoh Penggunaan**:  

``` python
result = a.search_pt('Unika')
```

**Return**:  
Mengembalikan data universitas yang sesuai dengan kata kunci yang diberikan.

### 5\. `search_prodi(keyword: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mencari program studi berdasarkan kata kunci yang diberikan.

**Parameter**:  
`keyword (str)`: Nama program studi untuk pencarian.

**Contoh Penggunaan**:  

``` python
result = a.search_prodi('Sistem Informasi')
```

**Return**:  
Mengembalikan data program studi yang sesuai dengan kata kunci yang diberikan.

### 6\. `get_detail_mhs(mahasiswa_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan detail mahasiswa berdasarkan ID.

**Parameter**:  
`mahasiswa_id (str)`: ID mahasiswa.

**Contoh Penggunaan**:  

``` python
result = a.get_detail_mhs('D0vgDgXXWzsaQdswAEPqHinsUH_5DUERcHgYt2c5eVXcKoWovccnVqzuxA_lRhZ-L8VPiA==')
```

**Return**:  
Mengembalikan detail mahasiswa yang sesuai dengan ID yang diberikan.

### 7\. `get_dosen_profile(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan profil dosen berdasarkan ID.

**Parameter**:  
`dosen_id (str)`: ID dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_profile('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan profil dosen yang sesuai dengan ID yang diberikan.

### 8\. `get_dosen_penelitian(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data penelitian dosen berdasarkan ID.

**Parameter**:  
`dosen_id (str)`: ID dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_penelitian('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data penelitian dosen yang sesuai dengan ID yang diberikan.

### 9\. `get_dosen_pengabdian(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data pengabdian dosen berdasarkan ID.

**Parameter**:  
`dosen_id (str)`: ID dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_pengabdian('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data pengabdian dosen yang sesuai dengan ID yang diberikan.

### 10\. `get_dosen_karya(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data karya dosen berdasarkan ID.

**Parameter**:  
`dosen_id (str)`: ID dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_karya('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data karya dosen yang sesuai dengan ID yang diberikan.

### 11\. `get_dosen_paten(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data paten dosen berdasarkan ID.

**Parameter**:  
`dosen_id (str)`: ID dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_paten('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data paten dosen yang sesuai dengan ID yang diberikan.

### 12\. `get_dosen_study_history(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data riwayat studi dosen berdasarkan ID.

**Parameter**:  
`dosen_id (str)`: ID dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_study_history('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data riwayat studi dosen yang sesuai dengan ID yang diberikan.

### 13\. `get_dosen_teaching_history(dosen_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data riwayat mengajar dosen berdasarkan ID.

**Parameter**:  
`dosen_id (str)`: ID dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_teaching_history('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data riwayat mengajar dosen yang sesuai dengan ID yang diberikan.

### 14\. `get_detail_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan detail universitas berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_detail_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan detail universitas yang sesuai dengan ID yang diberikan.

### 15\. `get_prodi_pt(pt_id: str, tahun: int) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data program studi di universitas tertentu berdasarkan ID dan tahun akademik.

**Parameter**:  
`pt_id (str)`: ID universitas.  
`tahun (int)`: Tahun akademik.

**Contoh Penggunaan**:  

``` python
result = a.get_prodi_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==', 20241)
```

**Return**:  
Mengembalikan data program studi yang sesuai dengan ID universitas dan tahun akademik yang diberikan.

### 16\. `get_logo_pt(pt_id: str) -> Optional[str]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan logo universitas berdasarkan ID dan mengembalikannya sebagai string yang telah di-encode dengan base64.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
logo_base64 = a.get_logo_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan logo universitas dalam format base64.

### 17\. `get_rasio_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan rasio mahasiswa terhadap dosen di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_rasio_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan rasio mahasiswa terhadap dosen di universitas yang sesuai dengan ID yang diberikan.

### 18\. `get_mahasiswa_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data mahasiswa di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_mahasiswa_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data mahasiswa di universitas yang sesuai dengan ID yang diberikan.

### 19\. `get_waktu_studi_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data waktu studi rata-rata mahasiswa di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_waktu_studi_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data waktu studi rata-rata mahasiswa di universitas yang sesuai dengan ID yang diberikan.

### 20\. `get_name_histories_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan sejarah nama universitas berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_name_histories_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan sejarah nama universitas yang sesuai dengan ID yang diberikan.

### 21\. `get_cost_range_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan kisaran biaya kuliah di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_cost_range_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan kisaran biaya kuliah di universitas yang sesuai dengan ID yang diberikan.

### 22\. `get_graduation_rate_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan tingkat kelulusan di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_graduation_rate_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan tingkat kelulusan di universitas yang sesuai dengan ID yang diberikan.

### 23\. `get_jumlah_prodi_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah program studi di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_jumlah_prodi_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan jumlah program studi di universitas yang sesuai dengan ID yang diberikan.

### 24\. `get_jumlah_mahasiswa_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah mahasiswa di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_jumlah_mahasiswa_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan jumlah mahasiswa di universitas yang sesuai dengan ID yang diberikan.

### 25\. `get_jumlah_dosen_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah dosen di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_jumlah_dosen_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan jumlah dosen di universitas yang sesuai dengan ID yang diberikan.

### 26\. `get_sarpras_file_name_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan nama file sarana dan prasarana di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_sarpras_file_name_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan nama file sarana dan prasarana di universitas yang sesuai dengan ID yang diberikan.

### 27\. `get_sarpras_blob_pt(pt_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan data blob sarana dan prasarana di universitas tertentu berdasarkan ID.

**Parameter**:  
`pt_id (str)`: ID universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_sarpras_blob_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')
```

**Return**:  
Mengembalikan data blob sarana dan prasarana di universitas yang sesuai dengan ID yang diberikan.

### 28\. `get_detail_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan detail program studi berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_detail_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan detail program studi yang sesuai dengan ID yang diberikan.

### 29\. `get_desc_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan deskripsi program studi berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_desc_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan deskripsi program studi yang sesuai dengan ID yang diberikan.

### 30\. `get_name_histories_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan sejarah nama program studi berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_name_histories_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan sejarah nama program studi yang sesuai dengan ID yang diberikan.

### 31\. `get_num_students_lecturers_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah mahasiswa dan dosen di program studi tertentu berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_num_students_lecturers_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan jumlah mahasiswa dan dosen di program studi yang sesuai dengan ID yang diberikan.

### 32\. `get_cost_range_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan kisaran biaya kuliah di program studi tertentu berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_cost_range_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan kisaran biaya kuliah di program studi yang sesuai dengan ID yang diberikan.

### 33\. `get_daya_tampung_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan kapasitas (daya tampung) program studi berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_daya_tampung_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan data kapasitas program studi yang sesuai dengan ID yang diberikan.

### 34\. `get_rasio_dosen_mahasiswa_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan rasio dosen terhadap mahasiswa di program studi tertentu berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_rasio_dosen_mahasiswa_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan rasio dosen terhadap mahasiswa di program studi yang sesuai dengan ID yang diberikan.

### 35\. `get_graduation_rate_prodi(prodi_id: str) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan tingkat kelulusan di program studi tertentu berdasarkan ID.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_graduation_rate_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan tingkat kelulusan di program studi yang sesuai dengan ID yang diberikan.

### 36\. `get_logo_prodi(prodi_id: str) -> Optional[str]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan logo program studi berdasarkan ID dan mengembalikannya sebagai string yang telah di-encode dengan base64.

**Parameter**:  
`prodi_id (str)`: ID program studi.

**Contoh Penggunaan**:  

``` python
logo_base64 = a.get_logo_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')
```

**Return**:  
Mengembalikan logo program studi dalam format base64.

### 37\. `get_homebase_prodi(prodi_id: str, tahun: int) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan rasio homebase program studi berdasarkan ID dan tahun akademik.

**Parameter**:  
`prodi_id (str)`: ID program studi.  
`tahun (int)`: Tahun akademik.

**Contoh Penggunaan**:  

``` python
result = a.get_homebase_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==', 20241)
```

**Return**:  
Mengembalikan rasio homebase program studi yang sesuai dengan ID dan tahun akademik yang diberikan.

### 38\. `get_penghitung_ratio_prodi(prodi_id: str, tahun: int) -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan penghitung rasio program studi berdasarkan ID dan tahun akademik.

**Parameter**:  
`prodi_id (str)`: ID program studi.  
`tahun (int)`: Tahun akademik.

**Contoh Penggunaan**:  

``` python
result = a.get_penghitung_ratio_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==', 20241)
```

**Return**:  
Mengembalikan penghitung rasio program studi yang sesuai dengan ID dan tahun akademik yang diberikan.

### 39\. `get_dosen_count_active() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah dosen aktif.

**Contoh Penggunaan**:  

``` python
result = a.get_dosen_count_active()
```

**Return**:  
Mengembalikan jumlah dosen aktif.

### 40\. `get_mahasiswa_count_active() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah mahasiswa aktif.

**Contoh Penggunaan**:  

``` python
result = a.get_mahasiswa_count_active()
```

**Return**:  
Mengembalikan jumlah mahasiswa aktif.

### 41\. `get_prodi_count() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah program studi.

**Contoh Penggunaan**:  

``` python
result = a.get_prodi_count()
```

**Return**:  
Mengembalikan jumlah program studi.

### 42\. `get_pt_count() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan jumlah universitas.

**Contoh Penggunaan**:  

``` python
result = a.get_pt_count()
```

**Return**:  
Mengembalikan jumlah universitas.

### 43\. `get_data_dosen_keaktifan() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data keaktifan dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_data_dosen_keaktifan()
```

**Return**:  
Mengembalikan visualisasi data keaktifan dosen.

### 44\. `get_data_dosen_bidang() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data bidang studi dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_data_dosen_bidang()
```

**Return**:  
Mengembalikan visualisasi data bidang studi dosen.

### 45\. `get_data_dosen_jenis_kelamin() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data distribusi jenis kelamin dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_data_dosen_jenis_kelamin()
```

**Return**:  
Mengembalikan visualisasi data distribusi jenis kelamin dosen.

### 46\. `get_data_dosen_jenjang() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data jenjang akademik dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_data_dosen_jenjang()
```

**Return**:  
Mengembalikan visualisasi data jenjang akademik dosen.

### 47\. `get_data_dosen_ikatan() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data ikatan kerja dosen.

**Contoh Penggunaan**:  

``` python
result = a.get_data_dosen_ikatan()
```

**Return**:  
Mengembalikan visualisasi data ikatan kerja dosen.

### 48\. `get_data_mahasiswa_bidang() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan bidang studi.

**Contoh Penggunaan**:  

``` python
result = a.get_data_mahasiswa_bidang()
```

**Return**:  
Mengembalikan visualisasi data mahasiswa berdasarkan bidang studi.

### 49\. `get_data_mahasiswa_jenis_kelamin() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data distribusi jenis kelamin mahasiswa.

**Contoh Penggunaan**:  

``` python
result = a.get_data_mahasiswa_jenis_kelamin()
```

**Return**:  
Mengembalikan visualisasi data distribusi jenis kelamin mahasiswa.

### 50\. `get_data_mahasiswa_jenjang() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan jenjang pendidikan.

**Contoh Penggunaan**:  

``` python
result = a.get_data_mahasiswa_jenjang()
```

**Return**:  
Mengembalikan visualisasi data mahasiswa berdasarkan jenjang pendidikan.

### 51\. `get_data_mahasiswa_kelompok_lembaga() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan kelompok lembaga.

**Contoh Penggunaan**:  

``` python
result = a.get_data_mahasiswa_kelompok_lembaga()
```

**Return**:  
Mengembalikan visualisasi data mahasiswa berdasarkan kelompok lembaga.

### 52\. `get_data_mahasiswa_status() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan status (aktif, tidak aktif).

**Contoh Penggunaan**:  

``` python
result = a.get_data_mahasiswa_status()
```

**Return**:  
Mengembalikan visualisasi data mahasiswa berdasarkan status.

### 53\. `get_data_pt_bentuk() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data bentuk perguruan tinggi.

**Contoh Penggunaan**:  

``` python
result = a.get_data_pt_bentuk()
```

**Return**:  
Mengembalikan visualisasi data bentuk perguruan tinggi.

### 54\. `get_data_pt_akreditasi() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data akreditasi perguruan tinggi.

**Contoh Penggunaan**:  

``` python
result = a.get_data_pt_akreditasi()
```

**Return**:  
Mengembalikan visualisasi data akreditasi perguruan tinggi.

### 55\. `get_data_pt_kelompok_pembina() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data perguruan tinggi berdasarkan kelompok pembina.

**Contoh Penggunaan**:  

``` python
result = a.get_data_pt_kelompok_pembina()
```

**Return**:  
Mengembalikan visualisasi data perguruan tinggi berdasarkan kelompok pembina.

### 56\. `get_data_pt_provinsi() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data perguruan tinggi berdasarkan provinsi.

**Contoh Penggunaan**:  

``` python
result = a.get_data_pt_provinsi()
```

**Return**:  
Mengembalikan visualisasi data perguruan tinggi berdasarkan provinsi.

### 57\. `get_data_prodi_jenjang() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan jenjang pendidikan.

**Contoh Penggunaan**:  

``` python
result = a.get_data_prodi_jenjang()
```

**Return**:  
Mengembalikan visualisasi data program studi berdasarkan jenjang pendidikan.

### 58\. `get_data_prodi_akreditasi() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan akreditasi.

**Contoh Penggunaan**:  

``` python
result = a.get_data_prodi_akreditasi()
```

**Return**:  
Mengembalikan visualisasi data program studi berdasarkan akreditasi.

### 59\. `get_data_prodi_bidang_ilmu() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan bidang ilmu.

**Contoh Penggunaan**:  

``` python
result = a.get_data_prodi_bidang_ilmu()
```

**Return**:  
Mengembalikan visualisasi data program studi berdasarkan bidang ilmu.

### 60\. `get_data_prodi_kelompok_pembina() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan kelompok pembina.

**Contoh Penggunaan**:  

``` python
result = a.get_data_prodi_kelompok_pembina()
```

**Return**:  
Mengembalikan visualisasi data program studi berdasarkan kelompok pembina.

### 61\. `get_contributor() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan daftar kontributor.

**Contoh Penggunaan**:  

``` python
result = a.get_contributor()
```

**Return**:  
Mengembalikan daftar kontributor.

### 62\. `get_news() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan daftar berita.

**Contoh Penggunaan**:  

``` python
result = a.get_news()
```

**Return**:  
Mengembalikan daftar berita.

### 63\. `get_bidang_ilmu_prodi() -> Optional[Dict[str, Any]]`

**Deskripsi**:  
Metode ini digunakan untuk mendapatkan bidang ilmu.

**Contoh Penggunaan**:  

``` python
result = a.get_bidang_ilmu_prodi()
```

**Return**:  
Mengembalikan bidang ilmu.

## Catatan Tambahan

*   Semua metode yang ada di dalam kelas `api` menggunakan decorator `@handle_errors` yang menangani kesalahan yang terjadi selama pemanggilan API. Jika ada kesalahan, maka akan dicatat ke log dan metode tersebut akan mengembalikan `None`.
*   Beberapa metode mengembalikan data dalam format JSON, dan untuk memudahkan pemahaman dan analisis data tersebut, Anda dapat menggunakan modul `pprint` seperti yang telah dicontohkan.

Dokumentasi ini bertujuan untuk mempermudah Anda dalam menggunakan kelas `api` dan memanfaatkan berbagai fungsi yang disediakannya. Jangan ragu untuk mencoba dan menyesuaikan contoh penggunaan sesuai dengan kebutuhan Anda.