import logging
from typing import Any, Dict, Optional, Callable, Union, List
from functools import wraps
from .helper import helper
from .exceptions import (
    PDDIKTIError, APIConnectionError, APITimeoutError,
    APIRateLimitError, APIResponseError, ValidationError
)

APIResponse = Optional[Union[Dict[str, Any], str]]
APIMethod = Callable[..., APIResponse]

# Library code should not configure the root logger; leave that to the app.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def handle_errors(func: APIMethod) -> APIMethod:
    """Wrap an API method so it logs and returns None instead of raising."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> APIResponse:
        func_name = getattr(func, '__name__', 'unknown_function')
        try:
            # Reject blank string arguments early.
            for i, arg in enumerate(args[1:], 1):
                if isinstance(arg, str) and not arg.strip():
                    raise ValidationError(f"Parameter {i} cannot be empty string")

            response = func(*args, **kwargs)
            if response is None:
                logger.warning(f"{func_name}: received None response")
                return None
            if isinstance(response, dict) and response.get("error"):
                raise APIResponseError(f"API error: {response.get('error')}")
            return response

        except ValidationError as e:
            logger.error(f"{func_name}: validation error - {e.message}")
        except APITimeoutError as e:
            logger.error(f"{func_name}: timeout error - {e.message}")
        except APIConnectionError as e:
            logger.error(f"{func_name}: connection error - {e.message}")
        except APIRateLimitError as e:
            logger.warning(f"{func_name}: rate limit error - {e.message}")
        except APIResponseError as e:
            logger.error(f"{func_name}: response error - {e.message}")
        except PDDIKTIError as e:
            logger.error(f"{func_name}: PDDIKTI error - {e.message}")
        except Exception as e:
            logger.error(f"{func_name}: unexpected error - {e}", exc_info=True)
        return None

    return wrapper


class api:
    def __init__(
        self,
        base_url: Optional[str] = None,
        session: Optional[Any] = None,
        cf_clearance: Optional[str] = None,
        user_agent: Optional[str] = None,
        auto_cookie: bool = False,
    ) -> None:
        """Create a PDDIKTI API client.

        The official upstream (https://pddikti.kemdiktisaintek.go.id/api) is
        protected by a Cloudflare challenge, so supply clearance one of three ways:

        - ``auto_cookie=True`` reads ``cf_clearance`` from a local browser
          (needs ``pip install pddiktipy[auto]`` and having opened the site once).
        - ``cf_clearance`` + ``user_agent`` copied from a browser that solved
          the challenge (the cookie is bound to that exact User-Agent).
        - ``base_url`` pointing at your own Cloudflare-solving proxy.

        Args:
            base_url: Override the upstream base URL (e.g. a local solver proxy).
            session: Pre-configured ``requests.Session``.
            cf_clearance: ``cf_clearance`` cookie from a solved browser session.
            user_agent: User-Agent that produced ``cf_clearance``.
            auto_cookie: Load ``cf_clearance`` from an installed browser.
        """
        try:
            self.H: helper = helper(
                base_url=base_url,
                session=session,
                cf_clearance=cf_clearance,
                user_agent=user_agent,
                auto_cookie=auto_cookie,
            )
            self.api_link: str = self.H.endpoint()
            self.logger: logging.Logger = logging.getLogger(__name__)
            self.logger.info("PDDIKTI API client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize API client: {e}")
            raise PDDIKTIError(f"Initialization failed: {str(e)}")

    def __enter__(self) -> 'api':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
        if exc_type is not None:
            self.logger.error(f"Exception in context: {exc_type.__name__}: {exc_val}")

    def close(self) -> None:
        """Release the underlying HTTP session."""
        try:
            if hasattr(self.H, 'close'):
                self.H.close()
        except Exception as e:
            self.logger.error(f"Error closing API client: {e}")

    def _validate_keyword(self, keyword: str, max_length: int = 100) -> None:
        """Ensure a search keyword is a non-empty string within max_length."""
        if not isinstance(keyword, str):
            raise ValidationError("Keyword must be a string")
        if not keyword.strip():
            raise ValidationError("Keyword cannot be empty")
        if len(keyword) > max_length:
            raise ValidationError(f"Keyword too long (max {max_length} characters)")

    def _validate_year(self, year: Union[int, str], field_name: str = "Year") -> None:
        """Ensure a year is a number within 1900-2100."""
        if year is None:
            raise ValidationError(f"{field_name} cannot be None")
        year_str = str(year)
        if not year_str.strip():
            raise ValidationError(f"{field_name} cannot be empty")
        try:
            year_int = int(year_str)
            if year_int < 1900 or year_int > 2100:
                raise ValidationError(f"{field_name} must be between 1900 and 2100")
        except ValueError:
            raise ValidationError(f"{field_name} must be a valid year number")

    def _validate_semester(self, semester: Union[int, str], field_name: str = "Semester") -> None:
        """Ensure a semester is in YYYYS format (year 1900-2100, semester 1-2)."""
        if semester is None:
            raise ValidationError(f"{field_name} cannot be None")
        semester_str = str(semester)
        if not semester_str.strip():
            raise ValidationError(f"{field_name} cannot be empty")
        try:
            semester_int = int(semester_str)
            if len(semester_str) != 5:
                raise ValidationError(f"{field_name} must be in YYYYS format (5 digits), e.g., 20241 or 20242")
            year = semester_int // 10
            sem = semester_int % 10
            if year < 1900 or year > 2100:
                raise ValidationError(f"Year in {field_name} must be between 1900 and 2100")
            if sem < 1 or sem > 2:
                raise ValidationError(f"Semester digit in {field_name} must be 1 or 2 (got {sem})")
        except ValueError:
            raise ValidationError(f"{field_name} must be a valid semester number in YYYYS format")

    def _validate_id(self, id_value: str, field_name: str = "ID") -> None:
        """Ensure an entity ID is a non-empty string of plausible length."""
        if not isinstance(id_value, str):
            raise ValidationError(f"{field_name} must be a string")
        if not id_value.strip():
            raise ValidationError(f"{field_name} cannot be empty")
        if len(id_value) < 10:
            raise ValidationError(f"{field_name} appears to be too short")

    def _build_endpoint(self, path: str, *args: Union[str, int]) -> str:
        """Join the base URL, a path, and URL-encoded positional arguments."""
        if not path:
            raise ValidationError("API path cannot be empty")
        try:
            parsed_args: List[str] = [self.H.parse(arg) for arg in args if arg is not None]
            full_path = f"{path}/{'/'.join(parsed_args)}" if parsed_args else path
            return f"{self.api_link}/{full_path}"
        except Exception as e:
            raise ValidationError(f"Error building endpoint: {str(e)}")

    # -- Search ---------------------------------------------------------------
    @handle_errors
    def search_all(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search students, lecturers, universities and study programs at once.

        The upstream returns this payload AES-256-CBC encrypted under ``data``;
        it is decrypted transparently before being returned.
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/enc/all", keyword)
        result = self.H.response(endpoint)
        if isinstance(result, dict) and isinstance(result.get("data"), str):
            result = {**result, "data": self.H.decrypt(result["data"])}
        return result

    @handle_errors
    def search_mahasiswa(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search students by name.

        Data: ['id', 'nama', 'nim', 'nama_pt', 'singkatan_pt', 'nama_prodi']
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/mhs", keyword)
        return self.H.response(endpoint)

    @handle_errors
    def search_dosen(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search lecturers by name.

        Data: ['id', 'nama', 'nidn', 'nama_pt', 'singkatan_pt', 'nama_prodi']
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/dosen", keyword)
        return self.H.response(endpoint)

    @handle_errors
    def search_pt(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search universities by name.

        Data: ['id', 'kode', 'nama_singkat', 'nama']
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/pt", keyword)
        return self.H.response(endpoint)

    @handle_errors
    def search_prodi(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search study programs by name.

        Data: ['id', 'nama', 'jenjang', 'pt', 'pt_singkat']
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/prodi", keyword)
        return self.H.response(endpoint)

    def _filter_query(self, limit: int, offset: int, filters: Dict[str, Any]) -> str:
        """Build a ``limit/offset`` query string plus any extra filter params."""
        query = f"limit={self.H.parse(limit)}&offset={self.H.parse(offset)}"
        for key, value in filters.items():
            if value is not None:
                query += f"&{key}={self.H.parse(value)}"
        return query

    @handle_errors
    def search_pt_filter(self, limit: int = 10, offset: int = 0, **filters: Any) -> Optional[Dict[str, Any]]:
        """Filtered, paginated university search.

        Args:
            limit: Maximum number of results.
            offset: Number of results to skip.
            **filters: Any extra upstream filter parameters, passed as query args.
        """
        endpoint = f"{self.api_link}/v2/pt/search/filter?{self._filter_query(limit, offset, filters)}"
        return self.H.response(endpoint)

    @handle_errors
    def search_prodi_filter(self, limit: int = 10, offset: int = 0, **filters: Any) -> Optional[Dict[str, Any]]:
        """Filtered, paginated study-program search.

        Args:
            limit: Maximum number of results.
            offset: Number of results to skip.
            **filters: Any extra upstream filter parameters, passed as query args.
        """
        endpoint = f"{self.api_link}/v2/prodi/search/filter?{self._filter_query(limit, offset, filters)}"
        return self.H.response(endpoint)

    # -- Students -------------------------------------------------------------
    @handle_errors
    def get_detail_mhs(self, mahasiswa_id: str) -> Optional[Dict[str, Any]]:
        """Get student details by ID.

        Data: ['id', 'nama_pt', 'kode_pt', 'kode_prodi', 'prodi', 'nama', 'nim',
        'jenis_daftar', 'id_pt', 'id_sms', 'jenis_kelamin', 'jenjang',
        'status_saat_ini', 'tahun_masuk']
        """
        self._validate_id(mahasiswa_id, "Mahasiswa ID")
        endpoint = self._build_endpoint("detail/mhs", mahasiswa_id)
        return self.H.response(endpoint)

    # -- Lecturers ------------------------------------------------------------
    @handle_errors
    def get_dosen_profile(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get a lecturer's profile by ID.

        Data: ['id_sdm', 'nama_dosen', 'nama_pt', 'nama_prodi', 'jenis_kelamin',
        'jabatan_akademik', 'pendidikan_tertinggi', 'status_ikatan_kerja',
        'status_aktivitas']
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/profile", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_penelitian(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get a lecturer's research activities by ID.

        Data: ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/penelitian", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_pengabdian(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get a lecturer's community service activities by ID.

        Data: ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/pengabdian", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_karya(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get a lecturer's creative works by ID.

        Data: ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/karya", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_paten(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get a lecturer's patents by ID.

        Data: ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/paten", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_study_history(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get a lecturer's study history by ID."""
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/study-history", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_teaching_history(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get a lecturer's teaching history by ID.

        Data: ['id_sdm', 'nama_semester', 'kode_matkul', 'nama_matkul',
        'nama_kelas', 'nama_pt']
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/teaching-history", dosen_id)
        return self.H.response(endpoint)

    # -- Universities ---------------------------------------------------------
    @handle_errors
    def get_detail_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get university details by ID.

        Data: ['kelompok', 'pembina', 'id_sp', 'kode_pt', 'email', 'no_tel',
        'no_fax', 'website', 'alamat', 'nama_pt', 'nm_singkat', 'kode_pos',
        'provinsi_pt', 'kab_kota_pt', 'kecamatan_pt', 'lintang_pt', 'bujur_pt',
        'tgl_berdiri_pt', 'tgl_sk_pendirian_sp', 'sk_pendirian_sp', 'status_pt',
        'akreditasi_pt', 'status_akreditasi']
        """
        self._validate_id(pt_id, "PT ID")
        endpoint: str = self._build_endpoint("pt/detail", pt_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_prodi_pt(self, pt_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get study programs of a university for an academic semester.

        Args:
            pt_id: University ID.
            tahun: Academic semester in YYYYS format, e.g. 20241 (2024, sem 1).

        Data: ['id_sms', 'kode_prodi', 'nama_prodi', 'akreditasi', 'jenjang_prodi',
        'status_prodi', 'jumlah_dosen_nidn', 'jumlah_dosen_nidk', 'jumlah_dosen',
        'jumlah_dosen_ajar', 'jumlah_mahasiswa', 'rasio', 'indikator_kelengkapan_data']
        """
        self._validate_id(pt_id, "PT ID")
        self._validate_semester(tahun, "Academic semester")
        endpoint: str = self._build_endpoint("pt/prodi", pt_id, tahun)
        return self.H.response(endpoint)

    @handle_errors
    def get_logo_pt(self, pt_id: str) -> Optional[str]:
        """Get a university's logo by ID as a base64-encoded string."""
        self._validate_id(pt_id, "PT ID")
        url: str = f"{self.H.endpoint()}/pt/logo/{self.H.parse(pt_id)}"
        return self.H.fetch_image_as_base64(url)

    @handle_errors
    def get_rasio_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's student-to-lecturer ratio by ID.

        Data: ['rasio']
        """
        self._validate_id(pt_id, "PT ID")
        endpoint: str = self._build_endpoint("pt/rasio", pt_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_mahasiswa_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's student intake/graduation means by ID.

        Data: ['id_sp', 'kode_pt', 'mean_jumlah_lulus', 'mean_jumlah_baru']
        """
        self._validate_id(pt_id, "PT ID")
        endpoint: str = self._build_endpoint("pt/mahasiswa", pt_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_waktu_studi_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's mean study time by ID.

        Data: ['id_sp', 'jenjang', 'mean_masa_studi']
        """
        endpoint = f"{self.api_link}/pt/waktu-studi/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_name_histories_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's name-change history by ID."""
        endpoint = f"{self.api_link}/pt/name-histories/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_cost_range_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's tuition cost range by ID.

        Data: ['id_sp', 'nama_pt', 'range_biaya_kuliah']
        """
        endpoint = f"{self.api_link}/pt/cost-range/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_graduation_rate_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's graduation rate by ID.

        Data: ['id_sp', 'graduation_rate']
        """
        endpoint = f"{self.api_link}/pt/graduation-rate/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_jumlah_prodi_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get the number of study programs of a university by ID.

        Data: ['id_sp', 'jumlah_prodi']
        """
        endpoint = f"{self.api_link}/pt/jumlah-prodi/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_jumlah_mahasiswa_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get the number of students of a university by ID.

        Data: ['id_sp', 'jumlah_mahasiswa']
        """
        endpoint = f"{self.api_link}/pt/jumlah-mahasiswa/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_jumlah_dosen_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get the number of lecturers of a university by ID.

        Data: ['id_sp', 'jumlah_dosen']
        """
        endpoint = f"{self.api_link}/pt/jumlah-dosen/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_sarpras_file_name_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's facility (sarpras) file names by ID."""
        endpoint = f"{self.api_link}/pt/sarpras-file-name/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_sarpras_blob_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """Get a university's facility (sarpras) blob data by ID."""
        endpoint = f"{self.api_link}/pt/sarpras-blob/{self.H.parse(pt_id)}"
        return self.H.response(endpoint)

    # -- Study programs -------------------------------------------------------
    @handle_errors
    def get_detail_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get study program details by ID.

        Data: ['id_sp', 'id_sms', 'nama_pt', 'kode_pt', 'nama_prodi', 'kode_prodi',
        'kel_bidang', 'jenj_didik', 'tgl_berdiri', 'tgl_sk_selenggara',
        'sk_selenggara', 'no_tel', 'no_fax', 'website', 'email', 'alamat',
        'provinsi', 'kab_kota', 'kecamatan', 'lintang', 'bujur', 'status',
        'akreditasi', 'akreditasi_internasional', 'status_akreditasi']
        """
        endpoint = f"{self.api_link}/prodi/detail/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_desc_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get a study program's description by ID.

        Data: ['id_sms', 'kode_prodi', 'jumlah_dosen', 'jumlah_mahasiswa',
        'jumlah_dosen_ajar', 'rasio', 'rasio_terima_daftar', 'akreditasi',
        'jumlah_pendaftar', 'jumlah_diterima', 'persentase', 'deskripsi_singkat',
        'visi', 'misi', 'kompetensi', 'capaian_belajar', 'rata_masa_studi']
        """
        endpoint = f"{self.api_link}/prodi/desc/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_name_histories_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get a study program's name-change history by ID."""
        endpoint = f"{self.api_link}/prodi/name-histories/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_num_students_lecturers_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get a study program's student and lecturer counts by ID.

        Data: ['jumlah_mahasiswa', 'jumlah_dosen', 'jumlah_dosen_ajar', 'semester']
        """
        endpoint = f"{self.api_link}/prodi/num-students-lecturers/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_cost_range_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get a study program's tuition cost range by ID.

        Data: ['id_sms', 'nama_prodi', 'range_biaya_kuliah']
        """
        endpoint = f"{self.api_link}/prodi/cost-range/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_daya_tampung_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get a study program's capacity (quota) by ID.

        Data: ['id_sms', 'nama_pt', 'nama_prodi', 'kuota']
        """
        endpoint = f"{self.api_link}/prodi/daya-tampung/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_rasio_dosen_mahasiswa_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get a study program's lecturer-to-student ratio by ID.

        Data: ['rasio_dosen_mahasiswa']
        """
        endpoint = f"{self.api_link}/prodi/rasio-dosen-mahasiswa/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_graduation_rate_prodi(self, prodi_id: str) -> Optional[Dict[str, Any]]:
        """Get a study program's graduation rate by ID.

        Data: ['id_sms', 'graduation_rate']
        """
        endpoint = f"{self.api_link}/prodi/graduation-rate/{self.H.parse(prodi_id)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_logo_prodi(self, pt_id: str) -> Optional[str]:
        """Get a study program's university logo by ID as a base64 string."""
        url = f"{self.H.endpoint()}/prodi/logo-pt/{self.H.parse(pt_id)}"
        return self.H.fetch_image_as_base64(url)

    @handle_errors
    def get_homebase_prodi(self, prodi_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get a study program's homebase ratio for an academic semester.

        Args:
            prodi_id: Study program ID.
            tahun: Academic semester in YYYYS format, e.g. 20241.
        """
        self._validate_id(prodi_id, "Prodi ID")
        self._validate_semester(tahun, "Academic semester")
        endpoint = f"{self.api_link}/dosen/homebase/{self.H.parse(prodi_id)}?semester={self.H.parse(tahun)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_penghitung_ratio_prodi(self, prodi_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get a study program's ratio counter for an academic semester.

        Args:
            prodi_id: Study program ID.
            tahun: Academic semester in YYYYS format, e.g. 20241.
        """
        self._validate_id(prodi_id, "Prodi ID")
        self._validate_semester(tahun, "Academic semester")
        endpoint = f"{self.api_link}/dosen/penghitung-ratio/{self.H.parse(prodi_id)}?semester={self.H.parse(tahun)}"
        return self.H.response(endpoint)

    # -- Aggregate counts -----------------------------------------------------
    @handle_errors
    def get_dosen_count_active(self) -> Optional[Dict[str, Any]]:
        """Get the number of active lecturers.

        Data: ['jumlah_dosen']
        """
        endpoint = f"{self.api_link}/dosen/count-active"
        return self.H.response(endpoint)

    @handle_errors
    def get_mahasiswa_count_active(self) -> Optional[Dict[str, Any]]:
        """Get the number of active students.

        Data: ['jumlah_mahasiswa']
        """
        endpoint = f"{self.api_link}/mahasiswa/count-active"
        return self.H.response(endpoint)

    @handle_errors
    def get_prodi_count(self) -> Optional[Dict[str, Any]]:
        """Get the total number of study programs.

        Data: ['jumlah']
        """
        endpoint = f"{self.api_link}/prodi/count"
        return self.H.response(endpoint)

    @handle_errors
    def get_pt_count(self) -> Optional[Dict[str, Any]]:
        """Get the total number of universities.

        Data: ['jumlah']
        """
        endpoint = f"{self.api_link}/pt/count"
        return self.H.response(endpoint)

    # -- Visualizations -------------------------------------------------------
    @handle_errors
    def get_data_dosen_keaktifan(self) -> Optional[Dict[str, Any]]:
        """Lecturer activeness distribution.

        Data: ['status_keaktifan', 'jumlah_dosen']
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-keaktifan"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_bidang(self) -> Optional[Dict[str, Any]]:
        """Lecturer distribution by field of study.

        Data: ['bidang', 'jumlah_dosen']
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-bidang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_jenis_kelamin(self) -> Optional[Dict[str, Any]]:
        """Lecturer distribution by gender.

        Data: ['jenis_kelamin', 'jumlah']
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-jenis-kelamin"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_jenjang(self) -> Optional[Dict[str, Any]]:
        """Lecturer distribution by academic level.

        Data: ['jenjang_dosen', 'jumlah_dosen']
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-jenjang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_dosen_ikatan(self) -> Optional[Dict[str, Any]]:
        """Lecturer distribution by employment binding.

        Data: ['ikatan_dosen', 'jumlah']
        """
        endpoint = f"{self.api_link}/visualisasi/dosen-ikatan"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_bidang(self) -> Optional[Dict[str, Any]]:
        """Student distribution by field of study.

        Data: ['bidang', 'jumlah_mhs']
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-bidang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_jenis_kelamin(self) -> Optional[Dict[str, Any]]:
        """Student distribution by gender.

        Data: ['jenis_kelamin', 'jumlah_mhs']
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-jenis-kelamin"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_jenjang(self) -> Optional[Dict[str, Any]]:
        """Student distribution by educational level.

        Data: ['nama_jenjang', 'jumlah_mhs']
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-jenjang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_kelompok_lembaga(self) -> Optional[Dict[str, Any]]:
        """Student distribution by institutional group.

        Data: ['kelompok_lembaga', 'jumlah_mhs']
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-kelompok-lembaga"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_mahasiswa_status(self) -> Optional[Dict[str, Any]]:
        """Student distribution by status (active/inactive).

        Data: ['status_mahasiswa', 'jumlah']
        """
        endpoint = f"{self.api_link}/visualisasi/mahasiswa-status"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_bentuk(self) -> Optional[Dict[str, Any]]:
        """University distribution by institution type.

        Data: ['bentuk_pt', 'jumlah_pt']
        """
        endpoint = f"{self.api_link}/visualisasi/pt-bentuk"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_akreditasi(self) -> Optional[Dict[str, Any]]:
        """University distribution by accreditation.

        Data: ['akreditasi', 'jumlah_pt']
        """
        endpoint = f"{self.api_link}/visualisasi/pt-akreditasi"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_kelompok_pembina(self) -> Optional[Dict[str, Any]]:
        """University distribution by administrative overseer.

        Data: ['kelompok_pembina', 'jumlah_pt']
        """
        endpoint = f"{self.api_link}/visualisasi/pt-kelompok-pembina"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_pt_provinsi(self) -> Optional[Dict[str, Any]]:
        """University distribution by province.

        Data: ['provinsi', 'jumlah_pt']
        """
        endpoint = f"{self.api_link}/visualisasi/pt-provinsi"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_jenjang(self) -> Optional[Dict[str, Any]]:
        """Study program distribution by level.

        Data: ['jenjang_prodi', 'jumlah_prodi']
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-jenjang"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_akreditasi(self) -> Optional[Dict[str, Any]]:
        """Study program distribution by accreditation.

        Data: ['akreditasi_prodi', 'jumlah_prodi']
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-akreditasi"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_bidang_ilmu(self) -> Optional[Dict[str, Any]]:
        """Study program distribution by field of study.

        Data: ['bidang_ilmu', 'jumlah_prodi']
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-bidang-ilmu"
        return self.H.response(endpoint)

    @handle_errors
    def get_data_prodi_kelompok_pembina(self) -> Optional[Dict[str, Any]]:
        """Study program distribution by administrative overseer.

        Data: ['kelompok_pembina', 'jumlah_prodi']
        """
        endpoint = f"{self.api_link}/visualisasi/prodi-kelompok-pembina"
        return self.H.response(endpoint)

    # -- Misc -----------------------------------------------------------------
    @handle_errors
    def get_beranda(self, content_limit: int = 4) -> Optional[Dict[str, Any]]:
        """Get the homepage summary (latest content and aggregate stats).

        Args:
            content_limit: Number of content items to include.
        """
        endpoint = f"{self.api_link}/beranda?content_limit={self.H.parse(content_limit)}"
        return self.H.response(endpoint)

    @handle_errors
    def get_contributor(self) -> Optional[Dict[str, Any]]:
        """Get the list of project contributors.

        Data: ['id', 'name', 'role', 'universitas', 'image_data', 'batch', 'linkedin']
        """
        endpoint = f"{self.api_link}/contributor/contributor"
        return self.H.response(endpoint)

    def _content(self, kind: str, page: int, page_size: int, search: str) -> str:
        """Build a paginated ``content/*`` endpoint URL."""
        return (
            f"{self.api_link}/content/{kind}"
            f"?page_size={self.H.parse(page_size)}"
            f"&page={self.H.parse(page)}"
            f"&search={self.H.parse(search) if search else ''}"
        )

    @handle_errors
    def get_news(self, page: int = 1, page_size: int = 10, search: str = "") -> Optional[Dict[str, Any]]:
        """Get news. Alias of get_announcements(); upstream replaced news/list."""
        return self.H.response(self._content("announcements", page, page_size, search))

    @handle_errors
    def get_announcements(self, page: int = 1, page_size: int = 10, search: str = "") -> Optional[Dict[str, Any]]:
        """Get paginated announcements."""
        return self.H.response(self._content("announcements", page, page_size, search))

    @handle_errors
    def get_publications(self, page: int = 1, page_size: int = 10, search: str = "") -> Optional[Dict[str, Any]]:
        """Get paginated publications."""
        return self.H.response(self._content("publications", page, page_size, search))

    @handle_errors
    def get_activities(self, page: int = 1, page_size: int = 10, search: str = "") -> Optional[Dict[str, Any]]:
        """Get paginated activities."""
        return self.H.response(self._content("activities", page, page_size, search))

    @handle_errors
    def get_activity_detail(self, activity_id: str) -> Optional[Dict[str, Any]]:
        """Get a single activity by ID."""
        self._validate_id(activity_id, "Activity ID")
        return self.H.response(self._build_endpoint("content/activities", activity_id))

    @handle_errors
    def get_pt_locations(self) -> Optional[Dict[str, Any]]:
        """Get the list of university locations."""
        endpoint = f"{self.api_link}/pt/locations"
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_count(self) -> Optional[Dict[str, Any]]:
        """Get the total number of lecturers (active and inactive)."""
        endpoint = f"{self.api_link}/dosen/count"
        return self.H.response(endpoint)

    @handle_errors
    def get_mahasiswa_count(self) -> Optional[Dict[str, Any]]:
        """Get the total number of students (active and inactive)."""
        endpoint = f"{self.api_link}/mahasiswa/count"
        return self.H.response(endpoint)

    @handle_errors
    def get_bidang_ilmu_prodi(self) -> Optional[Dict[str, Any]]:
        """Get the list of study-program fields of science."""
        endpoint = f"{self.api_link}/prodi/bidang-ilmu"
        return self.H.response(endpoint)
