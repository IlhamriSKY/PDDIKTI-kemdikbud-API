import logging
from typing import Any, Dict, Optional, Callable
from .helper import helper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class api:
    def __init__(self) -> None:
        self.H = helper()
        self.api_link = self.H.endpoint()

    def handle_errors(func: Callable) -> Callable:
        """
        Decorator to handle errors for API calls.

        Args:
            func (Callable): The function to wrap.

        Returns:
            Callable: The wrapped function.
        """
        def wrapper(*args, **kwargs) -> Optional[Dict[str, Any]]:
            try:
                response = func(*args, **kwargs)
                if response is None or (isinstance(response, dict) and response.get("error")):
                    raise ValueError("API response indicates an error")
                return response
            except Exception as e:
                logger.error(f"Error occurred in {func.__name__}: {str(e)}")
                return None
        return wrapper

    # Search
    @handle_errors
    def search_all(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Search all categories by keyword.

        Args:
            keyword (str): The search keyword.

        Example:
            keyword = "Ilham"

        Data:
            [
                'mahasiswa', 
                ['id', 'nama', 'nim', 'nama_pt', 'sinkatan_pt', 'nama_prodi'], 
                'dosen', 
                ['id', 'nama', 'nidn', 'nama_pt', 'singkatan_pt', 'nama_prodi'], 
                'pt', 
                ['id', 'kode', 'nama_singkat', 'nama'], 
                'prodi', 
                ['id', 'nama', 'jenjang', 'pt', 'pt_singkat']
            ]
        
        Note:
            "singkatan" means abbreviation in Indonesian. The term "sinkatan" was a typo and has been corrected. 
            Ask developer why :)
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pencarian/all/{self.H.parse(keyword)}"
        return self.H.response(endpoint)

    @handle_errors
    def search_mahasiswa(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Search for students by keyword.

        Args:
            keyword (str): The student name to search.

        Example:
            keyword = "Ilham"

        Data:
            ['id', 'nama', 'nim', 'nama_pt', 'singkatan_pt', 'nama_prodi']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pencarian/mhs/{self.H.parse(keyword)}"
        return self.H.response(endpoint)

    @handle_errors
    def search_dosen(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Search for lecturers by keyword.

        Args:
            keyword (str): The lecturer name to search.

        Example:
            keyword = "Ilham"

        Data:
            ['id', 'nama', 'nidn', 'nama_pt', 'singkatan_pt', 'nama_prodi']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pencarian/dosen/{self.H.parse(keyword)}"
        return self.H.response(endpoint)

    @handle_errors
    def search_pt(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Search for universities by keyword.

        Args:
            keyword (str): The university name to search.

        Example:
            keyword = "Unika"

        Data:
            ['id', 'kode', 'nama_singkat', 'nama']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pencarian/pt/{self.H.parse(keyword)}"
        return self.H.response(endpoint)

    @handle_errors
    def search_prodi(self, keyword: str) -> Optional[Dict[str, Any]]:
        """
        Search for study programs by keyword.

        Args:
            keyword (str): The study program name to search.

        Example:
            keyword = "Sistem Informasi"

        Data:
            ['id', 'nama', 'jenjang', 'pt', 'pt_singkat']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pencarian/prodi/{self.H.parse(keyword)}"
        return self.H.response(endpoint)

    # Data Mahasiswa
    @handle_errors
    def get_detail_mhs(self, mahasiswa_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detail of a students by ID.

        Args:
            mahasiswa_id (str): The students's ID.

        Example:
            mahasiswa_id = "D0vgDgXXWzsaQdswAEPqHinsUH_5DUERcHgYt2c5eVXcKoWovccnVqzuxA_lRhZ-L8VPiA=="

        Data:
            ['id', 'nama_pt', 'kode_pt', 'kode_prodi', 'prodi', 'nama', 'nim', 'jenis_daftar', 'id_pt', 'id_sms', 'jenis_kelamin', 'jenjang', 'status_saat_ini', 'tahun_masuk']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/detail/mhs/{self.H.parse(mahasiswa_id)}"
        return self.H.response(endpoint)

    # Data Dosen
    @handle_errors
    def get_dosen_profile(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get profile of a lecturer by ID.

        Args:
            dosen_id (str): The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'nama_dosen', 'nama_pt', 'nama_prodi', 'jenis_kelamin', 'jabatan_akademik', 'pendidikan_tertinggi', 'status_ikatan_kerja', 'status_aktivitas']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/profile/{self.H.parse(dosen_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_dosen_penelitian(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get research of a lecturer by ID.

        Args:
            dosen_id (str): The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/portofolio/penelitian/{self.H.parse(dosen_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_pengabdian(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get dedication of a lecturer by ID.

        Args:
            dosen_id (str): The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/portofolio/pengabdian/{self.H.parse(dosen_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_karya(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get creation of a lecturer by ID.

        Args:
            dosen_id (str): The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/portofolio/karya/{self.H.parse(dosen_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_paten(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get patent of a lecturer by ID.

        Args:
            dosen_id (str): The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/portofolio/paten/{self.H.parse(dosen_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_study_history(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get study history of a lecturer by ID.

        Args:
            dosen_id (str): The lecturer's ID.

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/study-history/{self.H.parse(dosen_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_teaching_history(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get teaching history of a lecturer by ID.

        Args:
            dosen_id (str): The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'nama_semester', 'kode_matkul', 'nama_matkul', 'nama_kelas', 'nama_pt']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/teaching-history/{self.H.parse(dosen_id)}"
        return self.H.response(endpoint)

    # Data Universities
    @handle_errors
    def get_detail_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detail of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['kelompok', 'pembina', 'id_sp', 'kode_pt', 'email', 'no_tel', 'no_fax', 'website', 'alamat', 'nama_pt', 'nm_singkat', 'kode_pos', 'provinsi_pt', 'kab_kota_pt', 'kecamatan_pt', 'lintang_pt', 'bujur_pt', 'tgl_berdiri_pt', 'tgl_sk_pendirian_sp', 'sk_pendirian_sp', 'status_pt', 'akreditasi_pt', 'status_akreditasi']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/detail/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_prodi_pt(self, pt_id: str, tahun: int) -> Optional[Dict[str, Any]]:
        """
        Get study programs of a universities by ID.

        Args:
            pt_id (str): The universities's ID.
            tahun (int): Academic year.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="
            tahun = 20241 (tahun, bulan)

        Data:
            ['id_sms', 'kode_prodi', 'nama_prodi', 'akreditasi', 'jenjang_prodi', 'status_prodi', 'jumlah_dosen_nidn', 'jumlah_dosen_nidk', 'jumlah_dosen', 'jumlah_dosen_ajar', 'jumlah_mahasiswa', 'rasio', 'indikator_kelengkapan_data']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/detail/{self.H.parse(pt_id)}/{self.H.parse(tahun)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_logo_pt(self, pt_id: str) -> Optional[str]:
        """
        Get the logo of a university by ID and return it as a base64-encoded string.

        Args:
            pt_id (str): The university's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Returns:
            Optional[str]: Base64-encoded image or None if an error occurs.
        """
        url = f"{self.H.endpoint()}/pt/logo/{self.H.parse(pt_id)}"
        return self.H.fetch_image_as_base64(url)

    @handle_errors
    def get_rasio_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get ratio of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['rasio']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/rasio/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_mahasiswa_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'kode_pt', 'mean_jumlah_lulus', 'mean_jumlah_baru']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/mahasiswa/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_waktu_studi_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get study time of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'jenjang', 'mean_masa_studi']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/waktu-studi/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_name_histories_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get study time of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            TODO: Define the structure once known.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/name-histories/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_cost_range_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cost range of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'nama_pt', 'range_biaya_kuliah']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/cost-range/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_graduation_rate_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get graduation rate of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'graduation_rate']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/graduation-rate/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_jumlah_prodi_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get prodi count of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'jumlah_prodi']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/jumlah-prodi/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_jumlah_mahasiswa_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student count of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'jumlah_mahasiswa']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/jumlah-mahasiswa/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_jumlah_dosen_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get lecturer count of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'jumlah_dosen']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/jumlah-dosen/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_sarpras_file_name_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get sarpras file name of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            TODO: Define the structure once known.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/sarpras-file-name/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_sarpras_blob_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get sarpras blob of a universities by ID.

        Args:
            pt_id (str): The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            TODO: Define the structure once known.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/sarpras-blob/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)
    
    # Data Study Programs
    @handle_errors
    def get_detail_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detail of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            ['id_sp', 'id_sms', 'nama_pt', 'kode_pt', 'nama_prodi', 'kode_prodi', 'kel_bidang', 'jenj_didik', 'tgl_berdiri', 'tgl_sk_selenggara', 'sk_selenggara', 'no_tel', 'no_fax', 'website', 'email', 'alamat', 'provinsi', 'kab_kota', 'kecamatan', 'lintang', 'bujur', 'status', 'akreditasi', 'akreditasi_internasional', 'status_akreditasi']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/detail/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_desc_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get desc of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            ['id_sms', 'kode_prodi', 'jumlah_dosen', 'jumlah_mahasiswa', 'jumlah_dosen_ajar', 'rasio', 'rasio_terima_daftar', 'akreditasi', 'jumlah_pendaftar', 'jumlah_diterima', 'persentase', 'deskripsi_singkat', 'visi', 'misi', 'kompetensi', 'capaian_belajar', 'rata_masa_studi']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/desc/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_name_histories_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get name histories of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            TODO: Define the structure once known.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/name-histories/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_num_students_lecturers_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get num students lecturers of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            ['jumlah_mahasiswa', 'jumlah_dosen', 'jumlah_dosen_ajar', 'semester']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/num-students-lecturers/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_cost_range_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cost ranges of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            ['id_sms', 'nama_prodi', 'range_biaya_kuliah']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/cost-range/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_daya_tampung_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get capacity of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            ['id_sms', 'nama_pt', 'nama_prodi', 'kuota']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/daya-tampung/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_rasio_dosen_mahasiswa_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get lecturer student ratio of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            ['rasio_dosen_mahasiswa']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/rasio-dosen-mahasiswa/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_graduation_rate_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """
        Get graduation rate of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            ['id_sms', 'graduation_rate']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/graduation-rate/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_logo_prodi(self, pt_id: str) -> Optional[str]:
        """
        Get the logo of a study programs by ID and return it as a base64-encoded string.

        Args:
            pt_id (str): The university's ID.

        Example:
            pt_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Returns:
            Optional[str]: Base64-encoded image or None if an error occurs.
        """
        url = f"{self.H.endpoint()}/prodi/logo-pt/{self.H.parse(pt_id)}"
        return self.H.fetch_image_as_base64(url)

    @handle_errors
    def get_homebase_prodi(self, prodi_id: str, tahun: int) -> Optional[Dict[str, Any]]:
        """
        Get homebase ratio of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.
            tahun (int): Academic year.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="
            tahun = 20241 (tahun, bulan)

        Data:
            TODO: Define the structure once known.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/homebase/{self.H.parse(prodi_id)}?semester={self.H.parse(tahun)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_penghitung_ratio_prodi(self, prodi_id: str, tahun: int) -> Optional[Dict[str, Any]]:
        """
        Get ratio counter of a study programs by ID.

        Args:
            prodi_id (str): The study programs's ID.
            tahun (int): Academic year.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="
            tahun = 20241 (tahun, bulan)

        Data:
            TODO: Define the structure once known.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/penghitung-ratio/{self.H.parse(prodi_id)}?semester={self.H.parse(tahun)}"
        return self.H.response(endpoint)

    # Data Count
    @handle_errors    
    def get_dosen_count_active(self) -> Optional[Dict[str, Any]]:
        """
        Get data count active of lecturer's.

        Data:
            ['jumlah_dosen']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/dosen/count-active"
        return self.H.response(endpoint)
    
    @handle_errors    
    def get_mahasiswa_count_active(self) -> Optional[Dict[str, Any]]:
        """
        Get data count active of lecturer's.

        Data:
            ['jumlah_mahasiswa']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/mahasiswa/count-active"
        return self.H.response(endpoint)
    
    @handle_errors    
    def get_prodi_count(self) -> Optional[Dict[str, Any]]:
        """
        Get data count of lecturer's.

        Data:
            ['jumlah']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/count"
        return self.H.response(endpoint)
    
    @handle_errors    
    def get_pt_count(self) -> Optional[Dict[str, Any]]:
        """
        Get data count of universities's.

        Data:
            ['jumlah']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/pt/count"
        return self.H.response(endpoint)

    # Data Visualizations
    @handle_errors
    def get_data_dosen_keaktifan(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of lecturer's activeness.

        Data:
            ['status_keaktifan', 'jumlah_dosen']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-keaktifan"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_bidang(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of lecturers' fields of study.

        Data:
            ['bidang', 'jumlah_dosen']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-bidang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_jenis_kelamin(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of lecturer's gender distribution.

        Data:
            ['jenis_kelamin', 'jumlah']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-jenis-kelamin"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_jenjang(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of lecturers' academic levels.

        Data:
            ['jenjang_dosen', 'jumlah_dosen']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-jenjang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_ikatan(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of lecturers' employment binding.

        Data:
            ['ikatan_dosen', 'jumlah']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-ikatan"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_bidang(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of students based on their fields of study.

        Data:
            ['bidang', 'jumlah_mhs']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-bidang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_jenis_kelamin(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of student gender distribution.

        Data:
            ['jenis_kelamin', 'jumlah_mhs']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-jenis-kelamin"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_jenjang(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of students by educational level.

        Data:
            ['nama_jenjang', 'jumlah_mhs']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-jenjang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_kelompok_lembaga(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of students based on institutional groups.

        Data:
            ['kelompok_lembaga', 'jumlah_mhs']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-kelompok-lembaga"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_status(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of students by their status (active, inactive).

        Data:
            ['status_mahasiswa', 'jumlah']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-status"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_bentuk(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of the types of higher education institutions.

        Data:
            ['bentuk_pt', 'jumlah_pt']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/pt-bentuk"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_akreditasi(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of university accreditation levels.

        Data:
            ['akreditasi', 'jumlah_pt']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/pt-akreditasi"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_kelompok_pembina(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of universities grouped by administrative overseer.

        Data:
            ['kelompok_pembina', 'jumlah_pt']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/pt-kelompok-pembina"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_provinsi(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of universities based on their province.

        Data:
            ['provinsi', 'jumlah_pt']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/pt-provinsi"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_jenjang(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of academic programs by level.

        Data:
            ['jenjang_prodi', 'jumlah_prodi']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-jenjang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_akreditasi(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of academic programs by accreditation.

        Data:
            ['akreditasi_prodi', 'jumlah_prodi']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-akreditasi"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_bidang_ilmu(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of academic programs by field of study.

        Data:
            ['bidang_ilmu', 'jumlah_prodi']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-bidang-ilmu"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_kelompok_pembina(self) -> Optional[Dict[str, Any]]:
        """
        Get data visualization of academic programs grouped by administrative overseer.

        Data:
            ['kelompok_pembina', 'jumlah_prodi']

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-kelompok-pembina"
        return self.H.response(endpoint)

    # Contributor Information
    @handle_errors
    def get_contributor(self) -> Optional[Dict[str, Any]]:
        """
        Get the list of contributors.

        Data:
            ['id', 'name', 'role', 'universitas', 'image_data', 'batch', 'linkedin']
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/contributor/contributor"
        return self.H.response(endpoint)

    # News
    @handle_errors
    def get_news(self) -> Optional[Dict[str, Any]]:
        """
        Get the list of news articles.

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/news/list"
        return self.H.response(endpoint)

    # Get Data
    @handle_errors
    def get_bidang_ilmu_prodi(self) -> Optional[Dict[str, Any]]:
        """
        Get the field of sciences.

        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        endpoint = f"{self.api_link}/prodi/bidang-ilmu"
        return self.H.response(endpoint)
