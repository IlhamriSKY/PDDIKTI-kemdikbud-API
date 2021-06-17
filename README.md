Unofficial Python 3 API wrapper to get data at [PDDIKTI](https://pddikti.kemdikbud.go.id/) Kemdikbud
====================================================================================================

[![License](https://img.shields.io/github/license/IlhamriSKY/PDDIKTI-kemdikbud-API.svg)](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/blob/master/LICENSE)
[![BuildStatus](https://travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API.svg?branch=main)](https://travis-ci.org/IlhamriSKY/PDDIKTI-kemdikbud-API)
[![Version 0.0.1](https://img.shields.io/badge/stable-1.0.0-brightgreen.svg "Version 1.0.0")](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API)
[![python3.x](https://img.shields.io/badge/3.8%20%7C%203.9-blue.svg?&logo=python&label=Python)](https://www.python.org/downloads/release/python-391/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8c2abcf7e3f648f281936af0c328c4d6)](https://www.codacy.com/gh/IlhamriSKY/PDDIKTI-kemdikbud-API/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=IlhamriSKY/PDDIKTI-kemdikbud-API&amp;utm_campaign=Badge_Grade)

Introduction
------------
Python API wrapper makes it easy for you to get data from the web [pddikti.kemdikbud.go.id](https://pddikti.kemdikbud.go.id/)

Change Log
------------
- V 1.0.0 "First Release"

Requirements
------------
- Python 3.*
- requests

Installation
------------

    $ pip install pddiktipy

Synopsis
--------
Usage:
```python
from pddiktipy import api

a = api()

print(a.search_all('ilham riski'))
```

# API
### 🔎 Get
Fetch the whole data from api 
###  Get All Data
```python
a.search_all('ilham riski')
```
### Get University only
#### Data [text, Nama PT, NPSN, Singkatan, Alamat, website-link]
```python
a.search_pt('University Name')
```
### Get Lecturer only 
#### Data [text, NIDN, PT, Prodi, website-link]
```python
a.search_dosen('Lecturer Name')
```
### Get study program only
#### Data [text, Nama Prodi, Jenjang Prodi, Nama Lembaga, website-link]
```python
a.search_prodi('Sistem Informasi')
```
### Get student only
#### Data [text(NIM), PT, Prodi, website-link]
```python
a.search_mahasiswa('Ilham Riski Wibowo')
```
### Get Data By Category
```python
# mahasiswa, pt, dosen, prodi
a.search_by_category('mahasiswa', 'Ilham Riski Wibowo')
```

### 🔎 Specific Data Search
Specific data search, more return data 
### Search University
#### Data [current_page, max_page, pt [akreditasi, bujur, id, jln, jumlah_prodi, lintang, logo, nama, no_tel, npsn, provinsi, rasio, singkatan, website]]
```python
specific_search_pt(self, keyword = '', provinsi = '',akreditas = '',jenis = '',status = '',koordinasi = '',tipe = '',page = '0')
```
### Search Lecturer
#### Data [id, jenjang, nama, nip, prodi, pt]
```python
specific_search_dosen(self, nama = '', nip = '', pt = '', prodi = '')
```
### Search Study Program
#### Data [akreditas, id, jenjang, lembaga, nama]
```python
specific_search_prodi(self, prodi = '', pt = '', wilayah = '', akreditas = '', jenjang = '')
```
### Search Student
#### Data [id, nama, nipd, prodi, pt]
```python
specific_search_mhs(self, nama = '', nipd = '', pt = '', prodi = '')
```

### 🔎 Dump
Dump data, this data is usually used for auto fill 
### Dump All Univ
#### Data [id_sp, kode_pt, nama_pt]
```python
a.dump_all_univ()
```
### Dump All Provinsi
#### Data [id, nama]
```python
a.dump_all_provinsi()
```
### Dump all Study Program
#### Data [id_sms, id_sp, kode_prodi, nama_prodi]
```python
a.dump_all_prodi()
```

### 🔎 In Script Search
Don't use this, because search fuction hardcoded on the client side instead of the server
### Get Univ By Name
#### Data [id_sp, kode_pt, nama_pt]
```python
a.get_univ_by_name('University Name')
```
### Get id_sp or uuid Univ V1
```python
a.get_uuid_univ_by_name_v1('University Name')
```
### Get id_sp or uuid Univ V2
```python
a.get_uuid_univ_by_name_v2('University Name')
```
### Get Endpoint / Web University
```python
a.get_univ_website_by_name('University Name')
```
### Get id_sp or uuid Lecturer
```python
a.get_uuid_dosen_by_name('Lecturer Name')
```
### Get Endpoint / Web Lecturer
```python
a.get_dosen_website_by_name('Lecturer Name')
```
### Get id_sp or uuid Student
```python
a.get_uuid_mahasiswa_by_name('Ilham Riski Wibowo')
```
### Get Endpoint / Web Mahasiswa
```python
a.get_mahasiswa_website_by_name('Ilham Riski Wibowo')
```

### 🔎 Detail Pages
### Get page detail data on University
#### Data [akreditas_list [akreditas, tgl_akreditasi, tgl_berlaku], bujur, email, id_sp, internet, jln, kode_pos, laboratorium, lintag, listrik luas_tanah, nama_rektor, nama_wil, nm_lamb, no_fax, no_tel, npsn, perpustakaan, ruang_kelas, sk_pendirian_sp, stat_sp, tgl_berdiri, tgl_sk_pendirian_sp, website]
```python
a.detail_data_univ_by_name('University Name')
```
### Get page detail data on University (Study Program)
#### Data [akreditas, id_sms, jenjang, kode_prodi, nm_lamb, rasio_list [dosen, mahasiswa],  stat_prodi]
```python
a.detail_data_univ_prodi_by_name('University Name')
```
### Get page detail data on University (Amount)
#### Data [jumlah_bidangilmu, jumlah_fakultas, jumlah_prodi, jumlah_prodi_akreditasi, rasio_list [dosen, mahasiswa]]
```python
a.detail_univ_jumlah_by_name('University Name')
```
### Get page detail data on University (Lecturer)
#### Data [jumlah_dosen_jabatan [categories, series [data, nama]] jumlah_dosen_jenis_kelamin]
```python
a.detail_univ_dosen_by_name('University Name')
```

### Get page detail data on Lecturer
```python
a.detail_dosen_by_name('University Name')
```

### 🔎 Images / Logo
Data Raw Image
### Logo Univesity
```python
a.detail_univ_logo_by_name('University Name')
```


TODO
------------
- [x] Detail Page Program Study
- [x] Detail Page Student
- [x] Statistik chart
- [x] News
- [x] Data Pages
- [x] Report
- [x] Etc.
