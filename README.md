<h1>Python 3 API wrapper to retrieve data from <a href="https://pddikti.kemdikbud.go.id/">PDDIKTI</a> Kemdikbud.</h1>

<p align="center">
    <a href="https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/IlhamriSKY/PDDIKTI-kemdikbud-API.svg" alt="License">
    </a>
    <a href="https://app.travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API">
        <img src="https://app.travis-ci.com/IlhamriSKY/PDDIKTI-kemdikbud-API.svg?token=3ssapyanyNraGyM8m5yz&branch=main" alt="BuildStatus">
    </a>
    <a href="https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API">
        <img src="https://img.shields.io/badge/stable-2.0.0-brightgreen.svg" alt="Version 2.0.0">
    </a>
    <a href="https://www.python.org/downloads/release/python-3.12.1/">
        <img src="https://img.shields.io/badge/3.12-blue.svg?logo=python&label=Python" alt="python3.x">
    </a>
    <a href="https://www.codacy.com/gh/IlhamriSKY/PDDIKTI-kemdikbud-API/dashboard?utm_source=github.com&utm_medium=referral&utm_content=IlhamriSKY/PDDIKTI-kemdikbud-API&utm_campaign=Badge_Grade">
        <img src="https://app.codacy.com/project/badge/Grade/39e00a8c8c1c4007a68d1ae3f53c03e7" alt="Codacy Badge">
    </a>
    <a href="https://github.com/IlhamriSKY">
        <img src="https://img.shields.io/badge/Author-Ilham%20Riski-blue.svg?style=flat" alt="Author">
    </a>
</p>

<h2>Change Log</h2>
<ul>
    <li>V 1.0.0 "First Release"</li>
    <li>V 2.0.0 "Latest Stable Version"</li>
</ul>

<h2>Requirements</h2>
<ul>
    <li>Python 3.*</li>
    <li>requests</li>
</ul>

<h2>Installation</h2>
<pre><code>$ pip install pddiktipy</code></pre>

<h2>Pengenalan</h2>
<p>Kelas <code>api</code> dari modul <code>pddiktipy</code> adalah sebuah antarmuka yang dirancang untuk mengakses berbagai data melalui API. Kelas ini menyediakan berbagai metode untuk melakukan pencarian dan pengambilan informasi terkait mahasiswa, dosen, program studi, universitas, dan berbagai data pendidikan lainnya.</p>

<h2>Cara Menggunakan</h2>

<h3>1. Mengimpor Kelas dan Membuat Instance</h3>
<pre><code>from pddiktipy import api
from pprint import pprint as p
a = api()

p(a.search_all('ilham riski'))
</code></pre>
<p>Kode di atas mengimpor kelas <code>api</code> dari modul <code>pddiktipy</code> dan membuat sebuah instance dari kelas tersebut. Objek <code>a</code> sekarang dapat digunakan untuk memanggil berbagai metode yang tersedia dalam kelas <code>api</code>.</p>

<h3>2. Menggunakan Metode <code>search_all</code></h3>
<pre><code>p(a.search_all('ilham riski'))
</code></pre>
<p>Kode ini menggunakan metode <code>search_all</code> untuk melakukan pencarian dengan kata kunci <code>'ilham riski'</code>. Hasil pencarian akan dicetak dengan rapi menggunakan fungsi <code>pprint</code>.</p>

<h2>Penjelasan Setiap Fungsi</h2>

<h3>1. <code>search_all(keyword: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk melakukan pencarian di semua kategori berdasarkan kata kunci yang diberikan.</p>

<p><strong>Parameter</strong>:<br>
<code>keyword (str)</code>: Kata kunci untuk pencarian.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.search_all('ilham riski')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan hasil pencarian dalam bentuk JSON yang mencakup data dari berbagai kategori seperti mahasiswa, dosen, universitas, dan program studi.</p>

<h3>2. <code>search_mahasiswa(keyword: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mencari mahasiswa berdasarkan kata kunci yang diberikan.</p>

<p><strong>Parameter</strong>:<br>
<code>keyword (str)</code>: Nama mahasiswa untuk pencarian.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.search_mahasiswa('Ilham')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data mahasiswa yang sesuai dengan kata kunci yang diberikan.</p>

<h3>3. <code>search_dosen(keyword: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mencari dosen berdasarkan kata kunci yang diberikan.</p>

<p><strong>Parameter</strong>:<br>
<code>keyword (str)</code>: Nama dosen untuk pencarian.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.search_dosen('Ilham')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data dosen yang sesuai dengan kata kunci yang diberikan.</p>

<h3>4. <code>search_pt(keyword: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mencari universitas berdasarkan kata kunci yang diberikan.</p>

<p><strong>Parameter</strong>:<br>
<code>keyword (str)</code>: Nama universitas untuk pencarian.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.search_pt('Unika')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data universitas yang sesuai dengan kata kunci yang diberikan.</p>

<h3>5. <code>search_prodi(keyword: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mencari program studi berdasarkan kata kunci yang diberikan.</p>

<p><strong>Parameter</strong>:<br>
<code>keyword (str)</code>: Nama program studi untuk pencarian.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.search_prodi('Sistem Informasi')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data program studi yang sesuai dengan kata kunci yang diberikan.</p>

<h3>6. <code>get_detail_mhs(mahasiswa_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan detail mahasiswa berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>mahasiswa_id (str)</code>: ID mahasiswa.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_detail_mhs('D0vgDgXXWzsaQdswAEPqHinsUH_5DUERcHgYt2c5eVXcKoWovccnVqzuxA_lRhZ-L8VPiA==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan detail mahasiswa yang sesuai dengan ID yang diberikan.</p>

<h3>7. <code>get_dosen_profile(dosen_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan profil dosen berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>dosen_id (str)</code>: ID dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_profile('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan profil dosen yang sesuai dengan ID yang diberikan.</p>

<h3>8. <code>get_dosen_penelitian(dosen_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data penelitian dosen berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>dosen_id (str)</code>: ID dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_penelitian('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data penelitian dosen yang sesuai dengan ID yang diberikan.</p>

<h3>9. <code>get_dosen_pengabdian(dosen_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data pengabdian dosen berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>dosen_id (str)</code>: ID dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_pengabdian('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data pengabdian dosen yang sesuai dengan ID yang diberikan.</p>

<h3>10. <code>get_dosen_karya(dosen_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data karya dosen berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>dosen_id (str)</code>: ID dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_karya('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data karya dosen yang sesuai dengan ID yang diberikan.</p>

<h3>11. <code>get_dosen_paten(dosen_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data paten dosen berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>dosen_id (str)</code>: ID dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_paten('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data paten dosen yang sesuai dengan ID yang diberikan.</p>

<h3>12. <code>get_dosen_study_history(dosen_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data riwayat studi dosen berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>dosen_id (str)</code>: ID dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_study_history('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data riwayat studi dosen yang sesuai dengan ID yang diberikan.</p>

<h3>13. <code>get_dosen_teaching_history(dosen_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data riwayat mengajar dosen berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>dosen_id (str)</code>: ID dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_teaching_history('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data riwayat mengajar dosen yang sesuai dengan ID yang diberikan.</p>

<h3>14. <code>get_detail_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan detail universitas berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_detail_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan detail universitas yang sesuai dengan ID yang diberikan.</p>

<h3>15. <code>get_prodi_pt(pt_id: str, tahun: int) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data program studi di universitas tertentu berdasarkan ID dan tahun akademik.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.<br>
<code>tahun (int)</code>: Tahun akademik.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_prodi_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==', 20241)</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data program studi yang sesuai dengan ID universitas dan tahun akademik yang diberikan.</p>

<h3>16. <code>get_logo_pt(pt_id: str) -> Optional[str]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan logo universitas berdasarkan ID dan mengembalikannya sebagai string yang telah di-encode dengan base64.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>logo_base64 = a.get_logo_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan logo universitas dalam format base64.</p>

<h3>17. <code>get_rasio_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan rasio mahasiswa terhadap dosen di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_rasio_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan rasio mahasiswa terhadap dosen di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>18. <code>get_mahasiswa_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data mahasiswa di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_mahasiswa_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data mahasiswa di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>19. <code>get_waktu_studi_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data waktu studi rata-rata mahasiswa di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_waktu_studi_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data waktu studi rata-rata mahasiswa di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>20. <code>get_name_histories_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan sejarah nama universitas berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_name_histories_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan sejarah nama universitas yang sesuai dengan ID yang diberikan.</p>

<h3>21. <code>get_cost_range_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan kisaran biaya kuliah di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_cost_range_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan kisaran biaya kuliah di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>22. <code>get_graduation_rate_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan tingkat kelulusan di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_graduation_rate_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan tingkat kelulusan di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>23. <code>get_jumlah_prodi_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah program studi di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_jumlah_prodi_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah program studi di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>24. <code>get_jumlah_mahasiswa_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah mahasiswa di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_jumlah_mahasiswa_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah mahasiswa di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>25. <code>get_jumlah_dosen_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah dosen di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_jumlah_dosen_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah dosen di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>26. <code>get_sarpras_file_name_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan nama file sarana dan prasarana di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_sarpras_file_name_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan nama file sarana dan prasarana di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>27. <code>get_sarpras_blob_pt(pt_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan data blob sarana dan prasarana di universitas tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>pt_id (str)</code>: ID universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_sarpras_blob_pt('790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data blob sarana dan prasarana di universitas yang sesuai dengan ID yang diberikan.</p>

<h3>28. <code>get_detail_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan detail program studi berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_detail_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan detail program studi yang sesuai dengan ID yang diberikan.</p>

<h3>29. <code>get_desc_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan deskripsi program studi berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_desc_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan deskripsi program studi yang sesuai dengan ID yang diberikan.</p>

<h3>30. <code>get_name_histories_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan sejarah nama program studi berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_name_histories_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan sejarah nama program studi yang sesuai dengan ID yang diberikan.</p>

<h3>31. <code>get_num_students_lecturers_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah mahasiswa dan dosen di program studi tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_num_students_lecturers_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah mahasiswa dan dosen di program studi yang sesuai dengan ID yang diberikan.</p>

<h3>32. <code>get_cost_range_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan kisaran biaya kuliah di program studi tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_cost_range_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan kisaran biaya kuliah di program studi yang sesuai dengan ID yang diberikan.</p>

<h3>33. <code>get_daya_tampung_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan kapasitas (daya tampung) program studi berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_daya_tampung_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan data kapasitas program studi yang sesuai dengan ID yang diberikan.</p>

<h3>34. <code>get_rasio_dosen_mahasiswa_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan rasio dosen terhadap mahasiswa di program studi tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_rasio_dosen_mahasiswa_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan rasio dosen terhadap mahasiswa di program studi yang sesuai dengan ID yang diberikan.</p>

<h3>35. <code>get_graduation_rate_prodi(prodi_id: str) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan tingkat kelulusan di program studi tertentu berdasarkan ID.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_graduation_rate_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan tingkat kelulusan di program studi yang sesuai dengan ID yang diberikan.</p>

<h3>36. <code>get_logo_prodi(prodi_id: str) -> Optional[str]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan logo program studi berdasarkan ID dan mengembalikannya sebagai string yang telah di-encode dengan base64.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>logo_base64 = a.get_logo_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==')</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan logo program studi dalam format base64.</p>

<h3>37. <code>get_homebase_prodi(prodi_id: str, tahun: int) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan rasio homebase program studi berdasarkan ID dan tahun akademik.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.<br>
<code>tahun (int)</code>: Tahun akademik.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_homebase_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==', 20241)</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan rasio homebase program studi yang sesuai dengan ID dan tahun akademik yang diberikan.</p>

<h3>38. <code>get_penghitung_ratio_prodi(prodi_id: str, tahun: int) -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan penghitung rasio program studi berdasarkan ID dan tahun akademik.</p>

<p><strong>Parameter</strong>:<br>
<code>prodi_id (str)</code>: ID program studi.<br>
<code>tahun (int)</code>: Tahun akademik.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_penghitung_ratio_prodi('lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg==', 20241)</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan penghitung rasio program studi yang sesuai dengan ID dan tahun akademik yang diberikan.</p>

<h3>39. <code>get_dosen_count_active() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah dosen aktif.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_dosen_count_active()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah dosen aktif.</p>

<h3>40. <code>get_mahasiswa_count_active() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah mahasiswa aktif.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_mahasiswa_count_active()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah mahasiswa aktif.</p>

<h3>41. <code>get_prodi_count() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah program studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_prodi_count()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah program studi.</p>

<h3>42. <code>get_pt_count() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan jumlah universitas.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_pt_count()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan jumlah universitas.</p>

<h3>43. <code>get_data_dosen_keaktifan() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data keaktifan dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_dosen_keaktifan()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data keaktifan dosen.</p>

<h3>44. <code>get_data_dosen_bidang() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data bidang studi dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_dosen_bidang()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data bidang studi dosen.</p>

<h3>45. <code>get_data_dosen_jenis_kelamin() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data distribusi jenis kelamin dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_dosen_jenis_kelamin()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data distribusi jenis kelamin dosen.</p>

<h3>46. <code>get_data_dosen_jenjang() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data jenjang akademik dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_dosen_jenjang()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data jenjang akademik dosen.</p>

<h3>47. <code>get_data_dosen_ikatan() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data ikatan kerja dosen.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_dosen_ikatan()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data ikatan kerja dosen.</p>

<h3>48. <code>get_data_mahasiswa_bidang() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan bidang studi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_mahasiswa_bidang()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data mahasiswa berdasarkan bidang studi.</p>

<h3>49. <code>get_data_mahasiswa_jenis_kelamin() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data distribusi jenis kelamin mahasiswa.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_mahasiswa_jenis_kelamin()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data distribusi jenis kelamin mahasiswa.</p>

<h3>50. <code>get_data_mahasiswa_jenjang() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan jenjang pendidikan.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_mahasiswa_jenjang()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data mahasiswa berdasarkan jenjang pendidikan.</p>

<h3>51. <code>get_data_mahasiswa_kelompok_lembaga() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan kelompok lembaga.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_mahasiswa_kelompok_lembaga()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data mahasiswa berdasarkan kelompok lembaga.</p>

<h3>52. <code>get_data_mahasiswa_status() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data mahasiswa berdasarkan status (aktif, tidak aktif).</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_mahasiswa_status()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data mahasiswa berdasarkan status.</p>

<h3>53. <code>get_data_pt_bentuk() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data bentuk perguruan tinggi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_pt_bentuk()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data bentuk perguruan tinggi.</p>

<h3>54. <code>get_data_pt_akreditasi() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data akreditasi perguruan tinggi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_pt_akreditasi()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data akreditasi perguruan tinggi.</p>

<h3>55. <code>get_data_pt_kelompok_pembina() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data perguruan tinggi berdasarkan kelompok pembina.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_pt_kelompok_pembina()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data perguruan tinggi berdasarkan kelompok pembina.</p>

<h3>56. <code>get_data_pt_provinsi() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data perguruan tinggi berdasarkan provinsi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_pt_provinsi()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data perguruan tinggi berdasarkan provinsi.</p>

<h3>57. <code>get_data_prodi_jenjang() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan jenjang pendidikan.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_prodi_jenjang()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data program studi berdasarkan jenjang pendidikan.</p>

<h3>58. <code>get_data_prodi_akreditasi() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan akreditasi.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_prodi_akreditasi()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data program studi berdasarkan akreditasi.</p>

<h3>59. <code>get_data_prodi_bidang_ilmu() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan bidang ilmu.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_prodi_bidang_ilmu()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data program studi berdasarkan bidang ilmu.</p>

<h3>60. <code>get_data_prodi_kelompok_pembina() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan visualisasi data program studi berdasarkan kelompok pembina.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_data_prodi_kelompok_pembina()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan visualisasi data program studi berdasarkan kelompok pembina.</p>

<h3>61. <code>get_contributor() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan daftar kontributor.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_contributor()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan daftar kontributor.</p>

<h3>62. <code>get_news() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan daftar berita.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_news()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan daftar berita.</p>

<h3>63. <code>get_bidang_ilmu_prodi() -> Optional[Dict[str, Any]]</code></h3>
<p><strong>Deskripsi</strong>:<br>
Metode ini digunakan untuk mendapatkan bidang ilmu.</p>

<p><strong>Contoh Penggunaan</strong>:<br>
<pre><code>result = a.get_bidang_ilmu_prodi()</code></pre></p>

<p><strong>Pengembalian</strong>:<br>
Mengembalikan bidang ilmu.</p>

<h2>Catatan Tambahan</h2>
<ul>
<li>Semua metode yang ada di dalam kelas <code>api</code> menggunakan decorator <code>@handle_errors</code> yang menangani kesalahan yang terjadi selama pemanggilan API. Jika ada kesalahan, maka akan dicatat ke log dan metode tersebut akan mengembalikan <code>None</code>.</li>
<li>Beberapa metode mengembalikan data dalam format JSON, dan untuk memudahkan pemahaman dan analisis data tersebut, Anda dapat menggunakan modul <code>pprint</code> seperti yang telah dicontohkan.</li>
</ul>

<p>Dokumentasi ini bertujuan untuk mempermudah Anda dalam menggunakan kelas <code>api</code> dan memanfaatkan berbagai fungsi yang disediakannya. Jangan ragu untuk mencoba dan menyesuaikan contoh penggunaan sesuai dengan kebutuhan Anda.</p>
