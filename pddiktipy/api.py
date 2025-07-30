import logging
from typing import Any, Dict, Optional, Callable, Union, List, Tuple, TypeVar
from functools import wraps
from .helper import helper
from .exceptions import (
    PDDIKTIError, APIConnectionError, APITimeoutError, 
    APIRateLimitError, APIResponseError, ValidationError
)

# Type variables for better type hinting
T = TypeVar('T')
APIResponse = Optional[Union[Dict[str, Any], str]]
APIMethod = Callable[..., APIResponse]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_errors(func: APIMethod) -> APIMethod:
    """Decorator to handle errors for API calls with comprehensive error categorization.
    
    This decorator provides enhanced error handling for API methods by:
    - Validating input parameters
    - Catching and categorizing different types of exceptions
    - Providing meaningful error messages
    - Logging errors for debugging purposes
    
    Args:
        func: The API method function to wrap with error handling.
        
    Returns:
        APIMethod: The wrapped function with comprehensive error handling.
        
    Note:
        This decorator automatically validates string parameters to ensure 
        they are not empty and handles various API-specific exceptions.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> APIResponse:
        func_name = getattr(func, '__name__', 'unknown_function')
        
        try:
            # Input validation for common parameters
            if len(args) > 1:  # Has parameters beyond self
                for i, arg in enumerate(args[1:], 1):  # Skip self
                    if isinstance(arg, str) and not arg.strip():
                        raise ValidationError(f"Parameter {i} cannot be empty string")
            
            response = func(*args, **kwargs)
            
            # Additional response validation
            if response is None:
                logger.warning(f"{func_name}: Received None response")
                return None
                
            if isinstance(response, dict) and response.get("error"):
                error_msg = response.get("error", "Unknown API error")
                logger.error(f"{func_name}: API returned error - {error_msg}")
                raise APIResponseError(f"API error: {error_msg}")
                
            return response
            
        except ValidationError as e:
            logger.error(f"{func_name}: Validation error - {e.message}")
            return None
            
        except APITimeoutError as e:
            logger.error(f"{func_name}: Timeout error - {e.message}")
            return None
            
        except APIConnectionError as e:
            logger.error(f"{func_name}: Connection error - {e.message}")
            return None
            
        except APIRateLimitError as e:
            logger.warning(f"{func_name}: Rate limit error - {e.message}")
            return None
            
        except APIResponseError as e:
            logger.error(f"{func_name}: Response error - {e.message}")
            return None
            
        except PDDIKTIError as e:
            logger.error(f"{func_name}: PDDIKTI API error - {e.message}")
            return None
            
        except Exception as e:
            logger.error(f"{func_name}: Unexpected error - {str(e)}", exc_info=True)
            return None
            
    return wrapper

class api:
    def __init__(self) -> None:
        """Initialize the PDDIKTI API client.
        
        Creates a new instance of the PDDIKTI API client with all necessary
        components including the helper class for HTTP operations, API endpoint
        configuration, and logging setup.
        
        Raises:
            PDDIKTIError: If the API client initialization fails due to 
                         configuration issues or network problems.
                         
        Example:
            >>> api_client = api()
            >>> # or using context manager
            >>> with api() as client:
            ...     result = client.search_mahasiswa("John")
        """
        try:
            self.H: helper = helper()
            self.api_link: str = self.H.endpoint()
            self.logger: logging.Logger = logging.getLogger(__name__)
            self.logger.info("PDDIKTI API client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize API client: {e}")
            raise PDDIKTIError(f"Initialization failed: {str(e)}")
    
    def __enter__(self) -> 'api':
        """Enter the context manager.
        
        Returns:
            api: The API client instance for use within the context.
        """
        return self
    
    def __exit__(self, 
                 exc_type: Optional[type], 
                 exc_val: Optional[BaseException], 
                 exc_tb: Optional[Any]) -> None:
        """Exit the context manager and perform cleanup.
        
        Args:
            exc_type: The exception type if an exception occurred.
            exc_val: The exception value if an exception occurred.
            exc_tb: The exception traceback if an exception occurred.
        """
        self.close()
        
        # Log any exceptions that occurred
        if exc_type is not None:
            self.logger.error(f"Exception in context: {exc_type.__name__}: {exc_val}")
    
    def close(self) -> None:
        """Close the API client and release resources.
        
        Properly closes the helper class and releases any network resources
        that were allocated during the API client's lifetime.
        
        Note:
            This method is automatically called when using the context manager,
            but can be called manually if needed.
        """
        try:
            if hasattr(self.H, 'close'):
                self.H.close()
                self.logger.debug("API client closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing API client: {e}")
    
    def _validate_keyword(self, keyword: str, max_length: int = 100) -> None:
        """Validate search keyword parameters.
        
        Ensures that the provided keyword is a valid string that meets
        the requirements for API search operations.
        
        Args:
            keyword: The search keyword to validate.
            max_length: Maximum allowed length for the keyword. Defaults to 100.
            
        Raises:
            ValidationError: If the keyword is not a string, is empty, 
                           or exceeds the maximum length.
                           
        Example:
            >>> self._validate_keyword("John Doe")  # Valid
            >>> self._validate_keyword("")  # Raises ValidationError
        """
        if not isinstance(keyword, str):
            raise ValidationError("Keyword must be a string")
            
        if not keyword or not keyword.strip():
            raise ValidationError("Keyword cannot be empty")
            
        if len(keyword) > max_length:
            raise ValidationError(f"Keyword too long (max {max_length} characters)")
    
    def _validate_year(self, year: Union[int, str], field_name: str = "Year") -> None:
        """Validate year parameter for API calls.
        
        Ensures the year parameter is valid and within reasonable bounds.
        Accepts both integer and string representations of years.
        
        Args:
            year: The year to validate (accepts int or str).
            field_name: Name of the field for error messages. Defaults to "Year".
            
        Raises:
            ValidationError: If the year is None, empty, not a valid number,
                           or outside the range 1900-2100.
                           
        Example:
            >>> self._validate_year(2024)     # Valid
            >>> self._validate_year("2024")   # Valid  
            >>> self._validate_year(1800)     # Raises ValidationError
        """
        if year is None:
            raise ValidationError(f"{field_name} cannot be None")
        
        # Convert to string if it's an integer
        year_str = str(year)
        
        if not year_str.strip():
            raise ValidationError(f"{field_name} cannot be empty")
        
        # Basic year validation (should be reasonable year)
        try:
            year_int = int(year_str)
            if year_int < 1900 or year_int > 2100:
                raise ValidationError(f"{field_name} must be between 1900 and 2100")
        except ValueError:
            raise ValidationError(f"{field_name} must be a valid year number")
    
    def _validate_semester(self, semester: Union[int, str], field_name: str = "Semester") -> None:
        """Validate semester parameter for API calls.
        
        Ensures the semester parameter is valid for PDDIKTI API which expects
        format YYYYS where YYYY is year (1900-2100) and S is semester (1-2).
        
        Args:
            semester: The semester to validate in YYYYS format (accepts int or str).
            field_name: Name of the field for error messages. Defaults to "Semester".
            
        Raises:
            ValidationError: If the semester is None, empty, not a valid number,
                           wrong format, or year/semester out of range.
                           
        Example:
            >>> self._validate_semester(20241)     # Valid (year 2024, semester 1)
            >>> self._validate_semester("20242")   # Valid (year 2024, semester 2)  
            >>> self._validate_semester(18001)     # Raises ValidationError (year too old)
            >>> self._validate_semester(20243)     # Raises ValidationError (invalid semester)
        """
        if semester is None:
            raise ValidationError(f"{field_name} cannot be None")
        
        # Convert to string if it's an integer
        semester_str = str(semester)
        
        if not semester_str.strip():
            raise ValidationError(f"{field_name} cannot be empty")
        
        # Validate semester format (YYYYS - 5 digits)
        try:
            semester_int = int(semester_str)
            
            # Check if it's 5 digits
            if len(semester_str) != 5:
                raise ValidationError(f"{field_name} must be in YYYYS format (5 digits), e.g., 20241 or 20242")
            
            # Extract year and semester parts
            year = semester_int // 10  # First 4 digits
            sem = semester_int % 10    # Last digit
            
            # Validate year range
            if year < 1900 or year > 2100:
                raise ValidationError(f"Year in {field_name} must be between 1900 and 2100")
            
            # Validate semester (usually 1 or 2, but allow up to 9 for flexibility)
            if sem < 1 or sem > 2:
                raise ValidationError(f"Semester digit in {field_name} must be 1 or 2 (got {sem})")
                
        except ValueError:
            raise ValidationError(f"{field_name} must be a valid semester number in YYYYS format")
    
    def _validate_id(self, id_value: str, field_name: str = "ID") -> None:
        """Validate ID parameters for API calls.
        
        Ensures that ID parameters meet the basic format requirements for
        PDDIKTI API calls. IDs are typically base64-encoded strings.
        
        Args:
            id_value: The ID string to validate.
            field_name: Type of ID for error messages. Defaults to "ID".
            
        Raises:
            ValidationError: If the ID is not a string, is empty, or appears
                           to be too short (less than 10 characters).
                           
        Example:
            >>> self._validate_id("f1c3b0ea-c239-45dd-841f...")  # Valid
            >>> self._validate_id("123")  # Raises ValidationError (too short)
        """
        if not isinstance(id_value, str):
            raise ValidationError(f"{field_name} must be a string")
            
        if not id_value or not id_value.strip():
            raise ValidationError(f"{field_name} cannot be empty")
            
        # Basic format validation for base64-like IDs
        if len(id_value) < 10:
            raise ValidationError(f"{field_name} appears to be too short")
    
    def _build_endpoint(self, path: str, *args: Union[str, int]) -> str:
        """Build complete API endpoint URL with parameters.
        
        Constructs a properly formatted API endpoint URL by combining the base
        API link with the specified path and encoded parameters.
        
        Args:
            path: The API endpoint path (e.g., "pencarian/mhs").
            *args: Variable number of parameters to append to the URL.
                  Each parameter will be URL-encoded automatically.
                  
        Returns:
            str: Complete formatted API endpoint URL.
            
        Example:
            >>> self._build_endpoint("pencarian/mhs", "John Doe")
            'https://api.pddikti.kemdikbud.go.id/pencarian/mhs/John%20Doe'
        """
        if not path:
            raise ValidationError("API path cannot be empty")
            
        try:
            parsed_args: List[str] = [self.H.parse(arg) for arg in args if arg is not None]
            if parsed_args:
                full_path: str = f"{path}/{'/'.join(parsed_args)}"
            else:
                full_path = path
                
            endpoint: str = f"{self.api_link}/{full_path}"
            self.logger.debug(f"Built endpoint: {endpoint}")
            return endpoint
            
        except Exception as e:
            raise ValidationError(f"Error building endpoint: {str(e)}")

    # Search
    @handle_errors
    def search_all(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search across all categories in the PDDIKTI database.
        
        Performs a comprehensive search across students (mahasiswa), lecturers (dosen),
        universities (perguruan tinggi), and study programs (program studi) using a
        single keyword.
        
        Args:
            keyword: The search term to query across all categories. Should be a
                    non-empty string with meaningful content.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing search results organized
                by category, or None if the search fails or no results are found.
                
        Raises:
            ValidationError: If the keyword is invalid (empty, too long, or wrong type).
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     results = client.search_all("Universitas Indonesia")
            ...     if results:
            ...         print(f"Found {len(results)} categories")

        Data Structure:
            Returns data in format:
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
        
        Note:
            The API may return "sinkatan_pt" instead of "singkatan_pt" in some
            responses due to a typo in the original API endpoint.
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/all", keyword)
        return self.H.response(endpoint)

    @handle_errors
    def search_mahasiswa(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search for students (mahasiswa) in the PDDIKTI database.
        
        Searches for student records matching the provided keyword. The search
        can match against student names and returns comprehensive information
        about each matching student.
        
        Args:
            keyword: The search term for student names. Should be a meaningful
                    search term (e.g., student's first name, last name, or full name).

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing matching student records,
                or None if no students are found or the search fails.
                
        Raises:
            ValidationError: If the keyword is invalid (empty, too long, or wrong type).
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     students = client.search_mahasiswa("Ahmad")
            ...     for student in students.get('data', []):
            ...         print(f"Student: {student['nama']} - NIM: {student['nim']}")

        Data Structure:
            Each student record contains:
            ['id', 'nama', 'nim', 'nama_pt', 'singkatan_pt', 'nama_prodi']
            
            Where:
            - id: Unique student identifier
            - nama: Student's full name
            - nim: Student identification number (Nomor Induk Mahasiswa)
            - nama_pt: Full university name
            - singkatan_pt: University abbreviation
            - nama_prodi: Study program name
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/mhs", keyword)
        return self.H.response(endpoint)

    @handle_errors
    def search_dosen(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search for lecturers (dosen) in the PDDIKTI database.
        
        Searches for lecturer records matching the provided keyword. The search
        can match against lecturer names and returns comprehensive information
        about each matching lecturer.
        
        Args:
            keyword: The search term for lecturer names. Should be a meaningful
                    search term (e.g., lecturer's first name, last name, or full name).

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing matching lecturer records,
                or None if no lecturers are found or the search fails.
                
        Raises:
            ValidationError: If the keyword is invalid (empty, too long, or wrong type).
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     lecturers = client.search_dosen("Prof. Dr.")
            ...     for lecturer in lecturers.get('data', []):
            ...         print(f"Lecturer: {lecturer['nama']} - NIDN: {lecturer['nidn']}")

        Data Structure:
            Each lecturer record contains:
            ['id', 'nama', 'nidn', 'nama_pt', 'singkatan_pt', 'nama_prodi']
            
            Where:
            - id: Unique lecturer identifier
            - nama: Lecturer's full name
            - nidn: National lecturer identification number (NIDN)
            - nama_pt: Full university name
            - singkatan_pt: University abbreviation
            - nama_prodi: Study program name
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/dosen", keyword)
        return self.H.response(endpoint)

    @handle_errors
    def search_pt(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search for universities (perguruan tinggi) in the PDDIKTI database.
        
        Searches for university records matching the provided keyword. The search
        can match against university names and returns comprehensive information
        about each matching institution.
        
        Args:
            keyword: The search term for university names. Can be a full name,
                    abbreviation, or partial name of the institution.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing matching university records,
                or None if no universities are found or the search fails.
                
        Raises:
            ValidationError: If the keyword is invalid (empty, too long, or wrong type).
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     universities = client.search_pt("Universitas Indonesia")
            ...     for uni in universities.get('data', []):
            ...         print(f"University: {uni['nama']} - Code: {uni['kode']}")

        Data Structure:
            Each university record contains:
            ['id', 'kode', 'nama_singkat', 'nama']
            
            Where:
            - id: Unique university identifier
            - kode: Official university code
            - nama_singkat: University abbreviation/short name
            - nama: Full university name
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/pt", keyword)
        return self.H.response(endpoint)

    @handle_errors
    def search_prodi(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Search for study programs (program studi) in the PDDIKTI database.
        
        Searches for study program records matching the provided keyword. The search
        can match against program names and returns information about each matching
        program including the associated university.
        
        Args:
            keyword: The search term for study program names. Can be a full program
                    name or partial name (e.g., "Sistem Informasi", "Teknik").

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing matching study program records,
                or None if no programs are found or the search fails.
                
        Raises:
            ValidationError: If the keyword is invalid (empty, too long, or wrong type).
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     programs = client.search_prodi("Teknik Informatika")
            ...     for program in programs.get('data', []):
            ...         print(f"Program: {program['nama']} at {program['pt']}")

        Data Structure:
            Each study program record contains:
            ['id', 'nama', 'jenjang', 'pt', 'pt_singkat']
            
            Where:
            - id: Unique program identifier
            - nama: Full study program name
            - jenjang: Education level (S1, S2, S3, D3, D4, etc.)
            - pt: Full university name offering the program
            - pt_singkat: University abbreviation
        """
        self._validate_keyword(keyword)
        endpoint: str = self._build_endpoint("pencarian/prodi", keyword)
        return self.H.response(endpoint)

    # Data Mahasiswa
    @handle_errors
    def get_detail_mhs(self, mahasiswa_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific student.
        
        Retrieves comprehensive details about a student including their academic
        information, university affiliation, and current status using the student's
        unique identifier.
        
        Args:
            mahasiswa_id: The unique identifier for the student. This is typically
                         a base64-encoded string obtained from search results.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the student's detailed
                information, or None if the student is not found or the request fails.
                
        Raises:
            ValidationError: If the mahasiswa_id is invalid (empty, too short, or wrong type).
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     # First search for a student
            ...     search_results = client.search_mahasiswa("Ahmad")
            ...     if search_results and search_results.get('data'):
            ...         student_id = search_results['data'][0]['id']
            ...         details = client.get_detail_mhs(student_id)
            ...         print(f"Student: {details['nama']} - NIM: {details['nim']}")

        Data Structure:
            The returned data contains:
            ['id', 'nama_pt', 'kode_pt', 'kode_prodi', 'prodi', 'nama', 'nim', 
             'jenis_daftar', 'id_pt', 'id_sms', 'jenis_kelamin', 'jenjang', 
             'status_saat_ini', 'tahun_masuk']
            
            Where:
            - id: Unique student identifier
            - nama: Student's full name
            - nim: Student identification number
            - nama_pt: Full university name
            - kode_pt: University code
            - prodi: Study program name
            - kode_prodi: Study program code
            - jenis_kelamin: Gender (L/P)
            - jenjang: Education level (S1, S2, etc.)
            - status_saat_ini: Current academic status
            - tahun_masuk: Year of enrollment
        """
        self._validate_id(mahasiswa_id, "Mahasiswa ID")
        endpoint = self._build_endpoint("detail/mhs", mahasiswa_id)
        return self.H.response(endpoint)

    # Data Dosen
    @handle_errors
    def get_dosen_profile(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive profile information of a lecturer.
        
        Retrieves detailed profile information about a specific lecturer including
        their academic credentials, current position, and institutional affiliation
        using the lecturer's unique identifier.
        
        Args:
            dosen_id: The unique identifier for the lecturer. This is typically
                     a base64-encoded string obtained from lecturer search results.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the lecturer's profile
                information, or None if the lecturer is not found or request fails.
                
        Raises:
            ValidationError: If dosen_id is invalid (empty, too short, or wrong type).
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     # First search for a lecturer
            ...     search_results = client.search_dosen("Prof. Ahmad")
            ...     if search_results and search_results.get('data'):
            ...         lecturer_id = search_results['data'][0]['id']
            ...         profile = client.get_dosen_profile(lecturer_id)
            ...         print(f"Lecturer: {profile['nama_dosen']}")
            ...         print(f"Position: {profile['jabatan_akademik']}")

        Data Structure:
            The returned profile contains:
            ['id_sdm', 'nama_dosen', 'nama_pt', 'nama_prodi', 'jenis_kelamin', 
             'jabatan_akademik', 'pendidikan_tertinggi', 'status_ikatan_kerja', 
             'status_aktivitas']
            
            Where:
            - id_sdm: Human resources system ID
            - nama_dosen: Lecturer's full name
            - nama_pt: Full university name
            - nama_prodi: Study program name
            - jenis_kelamin: Gender (L/P)
            - jabatan_akademik: Academic position/rank
            - pendidikan_tertinggi: Highest education level
            - status_ikatan_kerja: Employment status
            - status_aktivitas: Current activity status
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/profile", dosen_id)
        return self.H.response(endpoint)
    
    @handle_errors
    def get_dosen_penelitian(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get research of a lecturer by ID with enhanced validation.

        Args:
            dosen_id: The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If dosen_id is invalid
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/penelitian", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_pengabdian(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get dedication of a lecturer by ID with enhanced validation.

        Args:
            dosen_id: The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If dosen_id is invalid
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/pengabdian", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_karya(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get creation of a lecturer by ID with enhanced validation.

        Args:
            dosen_id: The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If dosen_id is invalid
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/karya", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_paten(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get patent of a lecturer by ID with enhanced validation.

        Args:
            dosen_id: The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'jenis_kegiatan', 'judul_kegiatan', 'tahun_kegiatan']
        
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If dosen_id is invalid
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/portofolio/paten", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_study_history(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get study history of a lecturer by ID with enhanced validation.

        Args:
            dosen_id: The lecturer's ID.

        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If dosen_id is invalid
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/study-history", dosen_id)
        return self.H.response(endpoint)

    @handle_errors
    def get_dosen_teaching_history(self, dosen_id: str) -> Optional[Dict[str, Any]]:
        """
        Get teaching history of a lecturer by ID with enhanced validation.

        Args:
            dosen_id: The lecturer's ID.

        Example:
            dosen_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sdm', 'nama_semester', 'kode_matkul', 'nama_matkul', 'nama_kelas', 'nama_pt']
        
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If dosen_id is invalid
        """
        self._validate_id(dosen_id, "Dosen ID")
        endpoint: str = self._build_endpoint("dosen/teaching-history", dosen_id)
        return self.H.response(endpoint)

    # Data Universities
    @handle_errors
    def get_detail_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detail of a universities by ID with enhanced validation.

        Args:
            pt_id: The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['kelompok', 'pembina', 'id_sp', 'kode_pt', 'email', 'no_tel', 'no_fax', 'website', 'alamat', 'nama_pt', 'nm_singkat', 'kode_pos', 'provinsi_pt', 'kab_kota_pt', 'kecamatan_pt', 'lintang_pt', 'bujur_pt', 'tgl_berdiri_pt', 'tgl_sk_pendirian_sp', 'sk_pendirian_sp', 'status_pt', 'akreditasi_pt', 'status_akreditasi']
        
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If pt_id is invalid
        """
        self._validate_id(pt_id, "PT ID")
        endpoint: str = self._build_endpoint("detail/pt", pt_id)
        return self.H.response(endpoint)
    
    @handle_errors
    def get_prodi_pt(self, pt_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get study programs offered by a specific university for a given academic year.
        
        Retrieves detailed information about all study programs available at a specific
        university during a particular academic year, including statistics about
        students, lecturers, and accreditation status.
        
        Args:
            pt_id: The unique identifier for the university. This is typically
                  a base64-encoded string obtained from university search results.
            tahun: The academic semester in YYYYS format where YYYY is the year and S
                  is the semester number (e.g., 20241 for first semester 2024,
                  20242 for second semester 2024). Accepts both integer and string.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing study program information
                for the specified university and semester, or None if not found or request fails.
                
        Raises:
            ValidationError: If pt_id is invalid or tahun is not in valid YYYYS format.
            APIConnectionError: If there's a network connectivity issue.
            APITimeoutError: If the request times out.
            
        Example:
            >>> with api() as client:
            ...     # Search for a university first
            ...     universities = client.search_pt("Universitas Indonesia")
            ...     if universities and universities.get('data'):
            ...         uni_id = universities['data'][0]['id']
            ...         # Get programs for first semester 2024
            ...         programs = client.get_prodi_pt(uni_id, 20241)
            ...         for program in programs.get('data', []):
            ...             print(f"Program: {program['nama_prodi']} - Accreditation: {program['akreditasi']}")

        Data Structure:
            Each study program record contains:
            ['id_sms', 'kode_prodi', 'nama_prodi', 'akreditasi', 'jenjang_prodi', 
             'status_prodi', 'jumlah_dosen_nidn', 'jumlah_dosen_nidk', 'jumlah_dosen', 
             'jumlah_dosen_ajar', 'jumlah_mahasiswa', 'rasio', 'indikator_kelengkapan_data']
            
            Where:
            - id_sms: Study management system ID
            - kode_prodi: Official study program code
            - nama_prodi: Full study program name
            - akreditasi: Accreditation grade (A, B, C, etc.)
            - jenjang_prodi: Education level (S1, S2, S3, D3, D4)
            - status_prodi: Program status (Active, Inactive, etc.)
            - jumlah_dosen_*: Various lecturer counts
            - jumlah_mahasiswa: Number of students
            - rasio: Student-to-lecturer ratio
            - indikator_kelengkapan_data: Data completeness indicator
            
        Note:
            This method was enhanced to handle semester codes (YYYYS format) instead of
            just year codes, fixing the validation issue that prevented valid semester
            codes like 20241 from being accepted.
        """
        self._validate_id(pt_id, "PT ID")
        self._validate_semester(tahun, "Academic semester")
        endpoint: str = self._build_endpoint("pt/prodi", pt_id, tahun)
        return self.H.response(endpoint)

    @handle_errors
    def get_logo_pt(self, pt_id: str) -> Optional[str]:
        """
        Get the logo of a university by ID and return it as a base64-encoded string with enhanced validation.

        Args:
            pt_id: The university's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Returns:
            Base64-encoded image or None if an error occurs.
            
        Raises:
            ValidationError: If pt_id is invalid
        """
        self._validate_id(pt_id, "PT ID")
        url: str = f"{self.H.endpoint()}/pt/logo/{self.H.parse(pt_id)}"
        return self.H.fetch_image_as_base64(url)

    @handle_errors
    def get_rasio_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get ratio of a universities by ID with enhanced validation.

        Args:
            pt_id: The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['rasio']
            
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If pt_id is invalid
        """
        self._validate_id(pt_id, "PT ID")
        endpoint: str = self._build_endpoint("pt/rasio", pt_id)
        return self.H.response(endpoint)
    
    @handle_errors
    def get_mahasiswa_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student of a universities by ID with enhanced validation.

        Args:
            pt_id: The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            ['id_sp', 'kode_pt', 'mean_jumlah_lulus', 'mean_jumlah_baru']
        
        Returns:
            JSON response or None if an error occurs.
            
        Raises:
            ValidationError: If pt_id is invalid
        """
        self._validate_id(pt_id, "PT ID")
        endpoint: str = self._build_endpoint("pt/mahasiswa", pt_id)
        return self.H.response(endpoint)
    
    @handle_errors
    def get_waktu_studi_pt(self, pt_id: str) -> Optional[Dict[str, Any]]:
        """
        Get study time of a universities by ID.

        Args:
            pt_id: The universities's ID.

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
            pt_id: The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            The response structure contains university name change history.
            Fields may include previous names, dates of changes, and official documentation.
        
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
            pt_id: The universities's ID.

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
            pt_id: The universities's ID.

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
            pt_id: The universities's ID.

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
            pt_id: The universities's ID.

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
            pt_id: The universities's ID.

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
            pt_id: The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            The response structure depends on the specific API endpoint. Refer to PDDIKTI API documentation for detailed field descriptions.
        
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
            pt_id: The universities's ID.

        Example:
            pt_id = "790W6QZ49VIBAks-T2pSPlFh4URK9dTZioFjEqeUDCj6L0X6iSaPHxbDgu8pz6FFAha58w=="

        Data:
            The response structure depends on the specific API endpoint. Refer to PDDIKTI API documentation for detailed field descriptions.
        
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
            prodi_id: The study programs's ID.

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
            prodi_id: The study programs's ID.

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
            prodi_id: The study programs's ID.

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Data:
            The response structure depends on the specific API endpoint. Refer to PDDIKTI API documentation for detailed field descriptions.
        
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
            prodi_id: The study programs's ID.

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
            prodi_id: The study programs's ID.

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
            prodi_id: The study programs's ID.

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
            prodi_id: The study programs's ID.

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
            prodi_id: The study programs's ID.

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
            pt_id: The university's ID.

        Example:
            pt_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="

        Returns:
            Optional[str]: Base64-encoded image or None if an error occurs.
        """
        url = f"{self.H.endpoint()}/prodi/logo-pt/{self.H.parse(pt_id)}"
        return self.H.fetch_image_as_base64(url)

    @handle_errors
    def get_homebase_prodi(self, prodi_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Get homebase ratio of a study programs by ID.

        Args:
            prodi_id: The study programs's ID.
            tahun: Academic semester in YYYYS format (accepts both integer and string).

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="
            tahun = 20241 or "20241" (year 2024, semester 1)

        Data:
            The response structure depends on the specific API endpoint. Refer to PDDIKTI API documentation for detailed field descriptions.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        self._validate_id(prodi_id, "Prodi ID")
        self._validate_semester(tahun, "Academic semester")
        endpoint = f"{self.api_link}/dosen/homebase/{self.H.parse(prodi_id)}?semester={self.H.parse(tahun)}"
        return self.H.response(endpoint)
    
    @handle_errors
    def get_penghitung_ratio_prodi(self, prodi_id: str, tahun: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Get ratio counter of a study programs by ID.

        Args:
            prodi_id: The study programs's ID.
            tahun: Academic semester in YYYYS format (accepts both integer and string).

        Example:
            prodi_id = "lCOatIX_hCe2RQSG1Rghn5kO81hHLJdYawJxkqiblUu6ZPeJ9OkBwbb5tnuvQqb-WcMSAg=="
            tahun = 20241 or "20241" (year 2024, semester 1)

        Data:
            The response structure depends on the specific API endpoint. Refer to PDDIKTI API documentation for detailed field descriptions.
        
        Returns:
            Optional[Dict[str, Any]]: JSON response or None if an error occurs.
        """
        self._validate_id(prodi_id, "Prodi ID")
        self._validate_semester(tahun, "Academic semester")
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
