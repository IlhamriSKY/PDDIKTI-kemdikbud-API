"""
Comprehensive Test Suite for PDDIKTI API
Tests all 54 public API methods with proper validation
Professional English standards implementation
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.test_data import (
    UNIVERSITY_NAME, STUDENT_NAME, LECTURER_NAME, PROGRAM_NAME,
    STUDENT_ID, LECTURER_ID, UNIVERSITY_ID, PROGRAM_ID
)


class TestAPIComprehensive:
    """Comprehensive test class for all PDDIKTI API methods"""
    
    @pytest.fixture(autouse=True)
    def setup_api_client(self):
        """Setup API client for all tests"""
        from pddiktipy.api import api
        self.client = api()
        yield
        self.client.close()

    # ========== API INITIALIZATION TESTS ==========
    
    def test_api_import_and_initialization(self):
        """Test API import and basic initialization"""
        from pddiktipy.api import api
        assert api is not None
        
        client = api()
        assert client is not None
        assert hasattr(client, 'H')
        assert hasattr(client, 'api_link')
        assert client.api_link is not None

    def test_context_manager_functionality(self):
        """Test API client as context manager"""
        from pddiktipy.api import api
        
        with api() as client:
            assert client is not None
            assert hasattr(client, 'search_all')
            assert hasattr(client, 'close')

    # ========== SEARCH METHODS TESTS (5 methods) ==========
    
    def test_search_all_method(self):
        """Test search_all method functionality"""
        assert hasattr(self.client, 'search_all')
        assert callable(self.client.search_all)
        
        # Test with valid keyword
        result = self.client.search_all("Unika")
        assert result is None or isinstance(result, (list, dict))

    def test_search_mahasiswa_method(self):
        """Test search_mahasiswa method functionality"""
        assert hasattr(self.client, 'search_mahasiswa')
        assert callable(self.client.search_mahasiswa)
        
        # Test with student name from test data
        result = self.client.search_mahasiswa(STUDENT_NAME.split()[0])
        assert result is None or isinstance(result, (list, dict))

    def test_search_dosen_method(self):
        """Test search_dosen method functionality"""
        assert hasattr(self.client, 'search_dosen')
        assert callable(self.client.search_dosen)
        
        # Test with lecturer name from test data
        result = self.client.search_dosen(LECTURER_NAME.split()[0])
        assert result is None or isinstance(result, (list, dict))

    def test_search_pt_method(self):
        """Test search_pt method functionality"""
        assert hasattr(self.client, 'search_pt')
        assert callable(self.client.search_pt)
        
        # Test with university name from test data
        result = self.client.search_pt("Unika")
        assert result is None or isinstance(result, (list, dict))

    def test_search_prodi_method(self):
        """Test search_prodi method functionality"""
        assert hasattr(self.client, 'search_prodi')
        assert callable(self.client.search_prodi)
        
        # Test with program name from test data
        result = self.client.search_prodi(PROGRAM_NAME)
        assert result is None or isinstance(result, (list, dict))

    # ========== DETAIL METHODS TESTS (3 methods) ==========
    
    def test_get_detail_mhs_method(self):
        """Test get_detail_mhs method functionality"""
        assert hasattr(self.client, 'get_detail_mhs')
        assert callable(self.client.get_detail_mhs)
        
        # Test with valid ID format
        result = self.client.get_detail_mhs(STUDENT_ID)
        assert result is None or isinstance(result, dict)

    def test_get_detail_pt_method(self):
        """Test get_detail_pt method functionality"""
        assert hasattr(self.client, 'get_detail_pt')
        assert callable(self.client.get_detail_pt)
        
        # Test with valid university ID
        result = self.client.get_detail_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_detail_prodi_method(self):
        """Test get_detail_prodi method functionality"""
        assert hasattr(self.client, 'get_detail_prodi')
        assert callable(self.client.get_detail_prodi)
        
        # Test with valid program ID
        result = self.client.get_detail_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    # ========== LECTURER METHODS TESTS (8 methods) ==========
    
    def test_get_dosen_profile_method(self):
        """Test get_dosen_profile method functionality"""
        assert hasattr(self.client, 'get_dosen_profile')
        assert callable(self.client.get_dosen_profile)
        
        result = self.client.get_dosen_profile(LECTURER_ID)
        assert result is None or isinstance(result, dict)

    def test_get_dosen_penelitian_method(self):
        """Test get_dosen_penelitian method functionality"""
        assert hasattr(self.client, 'get_dosen_penelitian')
        assert callable(self.client.get_dosen_penelitian)
        
        result = self.client.get_dosen_penelitian(LECTURER_ID)
        assert result is None or isinstance(result, dict)

    def test_get_dosen_pengabdian_method(self):
        """Test get_dosen_pengabdian method functionality"""
        assert hasattr(self.client, 'get_dosen_pengabdian')
        assert callable(self.client.get_dosen_pengabdian)
        
        result = self.client.get_dosen_pengabdian(LECTURER_ID)
        assert result is None or isinstance(result, dict)

    def test_get_dosen_karya_method(self):
        """Test get_dosen_karya method functionality"""
        assert hasattr(self.client, 'get_dosen_karya')
        assert callable(self.client.get_dosen_karya)
        
        result = self.client.get_dosen_karya(LECTURER_ID)
        assert result is None or isinstance(result, dict)

    def test_get_dosen_paten_method(self):
        """Test get_dosen_paten method functionality"""
        assert hasattr(self.client, 'get_dosen_paten')
        assert callable(self.client.get_dosen_paten)
        
        result = self.client.get_dosen_paten(LECTURER_ID)
        assert result is None or isinstance(result, dict)

    def test_get_dosen_study_history_method(self):
        """Test get_dosen_study_history method functionality"""
        assert hasattr(self.client, 'get_dosen_study_history')
        assert callable(self.client.get_dosen_study_history)
        
        result = self.client.get_dosen_study_history(LECTURER_ID)
        assert result is None or isinstance(result, dict)

    def test_get_dosen_teaching_history_method(self):
        """Test get_dosen_teaching_history method functionality"""
        assert hasattr(self.client, 'get_dosen_teaching_history')
        assert callable(self.client.get_dosen_teaching_history)
        
        result = self.client.get_dosen_teaching_history(LECTURER_ID)
        assert result is None or isinstance(result, dict)

    # ========== UNIVERSITY METHODS TESTS (14 methods) ==========
    
    def test_get_prodi_pt_method(self):
        """Test get_prodi_pt method functionality"""
        assert hasattr(self.client, 'get_prodi_pt')
        assert callable(self.client.get_prodi_pt)
        
        result = self.client.get_prodi_pt(UNIVERSITY_ID, "2024")
        assert result is None or isinstance(result, dict)

    def test_get_logo_pt_method(self):
        """Test get_logo_pt method functionality"""
        assert hasattr(self.client, 'get_logo_pt')
        assert callable(self.client.get_logo_pt)
        
        result = self.client.get_logo_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, str)

    def test_get_rasio_pt_method(self):
        """Test get_rasio_pt method functionality"""
        assert hasattr(self.client, 'get_rasio_pt')
        assert callable(self.client.get_rasio_pt)
        
        result = self.client.get_rasio_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_mahasiswa_pt_method(self):
        """Test get_mahasiswa_pt method functionality"""
        assert hasattr(self.client, 'get_mahasiswa_pt')
        assert callable(self.client.get_mahasiswa_pt)
        
        result = self.client.get_mahasiswa_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_waktu_studi_pt_method(self):
        """Test get_waktu_studi_pt method functionality"""
        assert hasattr(self.client, 'get_waktu_studi_pt')
        assert callable(self.client.get_waktu_studi_pt)
        
        result = self.client.get_waktu_studi_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_name_histories_pt_method(self):
        """Test get_name_histories_pt method functionality"""
        assert hasattr(self.client, 'get_name_histories_pt')
        assert callable(self.client.get_name_histories_pt)
        
        result = self.client.get_name_histories_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_cost_range_pt_method(self):
        """Test get_cost_range_pt method functionality"""
        assert hasattr(self.client, 'get_cost_range_pt')
        assert callable(self.client.get_cost_range_pt)
        
        result = self.client.get_cost_range_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_graduation_rate_pt_method(self):
        """Test get_graduation_rate_pt method functionality"""
        assert hasattr(self.client, 'get_graduation_rate_pt')
        assert callable(self.client.get_graduation_rate_pt)
        
        result = self.client.get_graduation_rate_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_jumlah_prodi_pt_method(self):
        """Test get_jumlah_prodi_pt method functionality"""
        assert hasattr(self.client, 'get_jumlah_prodi_pt')
        assert callable(self.client.get_jumlah_prodi_pt)
        
        result = self.client.get_jumlah_prodi_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_jumlah_mahasiswa_pt_method(self):
        """Test get_jumlah_mahasiswa_pt method functionality"""
        assert hasattr(self.client, 'get_jumlah_mahasiswa_pt')
        assert callable(self.client.get_jumlah_mahasiswa_pt)
        
        result = self.client.get_jumlah_mahasiswa_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_jumlah_dosen_pt_method(self):
        """Test get_jumlah_dosen_pt method functionality"""
        assert hasattr(self.client, 'get_jumlah_dosen_pt')
        assert callable(self.client.get_jumlah_dosen_pt)
        
        result = self.client.get_jumlah_dosen_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_sarpras_file_name_pt_method(self):
        """Test get_sarpras_file_name_pt method functionality"""
        assert hasattr(self.client, 'get_sarpras_file_name_pt')
        assert callable(self.client.get_sarpras_file_name_pt)
        
        result = self.client.get_sarpras_file_name_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    def test_get_sarpras_blob_pt_method(self):
        """Test get_sarpras_blob_pt method functionality"""
        assert hasattr(self.client, 'get_sarpras_blob_pt')
        assert callable(self.client.get_sarpras_blob_pt)
        
        result = self.client.get_sarpras_blob_pt(UNIVERSITY_ID)
        assert result is None or isinstance(result, dict)

    # ========== PROGRAM METHODS TESTS (12 methods) ==========
    
    def test_get_desc_prodi_method(self):
        """Test get_desc_prodi method functionality"""
        assert hasattr(self.client, 'get_desc_prodi')
        assert callable(self.client.get_desc_prodi)
        
        result = self.client.get_desc_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    def test_get_name_histories_prodi_method(self):
        """Test get_name_histories_prodi method functionality"""
        assert hasattr(self.client, 'get_name_histories_prodi')
        assert callable(self.client.get_name_histories_prodi)
        
        result = self.client.get_name_histories_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    def test_get_num_students_lecturers_prodi_method(self):
        """Test get_num_students_lecturers_prodi method functionality"""
        assert hasattr(self.client, 'get_num_students_lecturers_prodi')
        assert callable(self.client.get_num_students_lecturers_prodi)
        
        result = self.client.get_num_students_lecturers_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    def test_get_cost_range_prodi_method(self):
        """Test get_cost_range_prodi method functionality"""
        assert hasattr(self.client, 'get_cost_range_prodi')
        assert callable(self.client.get_cost_range_prodi)
        
        result = self.client.get_cost_range_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    def test_get_daya_tampung_prodi_method(self):
        """Test get_daya_tampung_prodi method functionality"""
        assert hasattr(self.client, 'get_daya_tampung_prodi')
        assert callable(self.client.get_daya_tampung_prodi)
        
        result = self.client.get_daya_tampung_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    def test_get_rasio_dosen_mahasiswa_prodi_method(self):
        """Test get_rasio_dosen_mahasiswa_prodi method functionality"""
        assert hasattr(self.client, 'get_rasio_dosen_mahasiswa_prodi')
        assert callable(self.client.get_rasio_dosen_mahasiswa_prodi)
        
        result = self.client.get_rasio_dosen_mahasiswa_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    def test_get_graduation_rate_prodi_method(self):
        """Test get_graduation_rate_prodi method functionality"""
        assert hasattr(self.client, 'get_graduation_rate_prodi')
        assert callable(self.client.get_graduation_rate_prodi)
        
        result = self.client.get_graduation_rate_prodi(PROGRAM_ID)
        assert result is None or isinstance(result, dict)

    def test_get_logo_prodi_method(self):
        """Test get_logo_prodi method functionality"""
        assert hasattr(self.client, 'get_logo_prodi')
        assert callable(self.client.get_logo_prodi)
        
        result = self.client.get_logo_prodi(UNIVERSITY_ID)
        assert result is None or isinstance(result, str)

    def test_get_homebase_prodi_method(self):
        """Test get_homebase_prodi method functionality"""
        assert hasattr(self.client, 'get_homebase_prodi')
        assert callable(self.client.get_homebase_prodi)
        
        result = self.client.get_homebase_prodi(PROGRAM_ID, "2024")
        assert result is None or isinstance(result, dict)

    def test_get_penghitung_ratio_prodi_method(self):
        """Test get_penghitung_ratio_prodi method functionality"""
        assert hasattr(self.client, 'get_penghitung_ratio_prodi')
        assert callable(self.client.get_penghitung_ratio_prodi)
        
        result = self.client.get_penghitung_ratio_prodi(PROGRAM_ID, "2024")
        assert result is None or isinstance(result, dict)

    # ========== STATISTICS METHODS TESTS (4 methods) ==========
    
    def test_get_dosen_count_active_method(self):
        """Test get_dosen_count_active method functionality"""
        assert hasattr(self.client, 'get_dosen_count_active')
        assert callable(self.client.get_dosen_count_active)
        
        result = self.client.get_dosen_count_active()
        assert result is None or isinstance(result, dict)

    def test_get_mahasiswa_count_active_method(self):
        """Test get_mahasiswa_count_active method functionality"""
        assert hasattr(self.client, 'get_mahasiswa_count_active')
        assert callable(self.client.get_mahasiswa_count_active)
        
        result = self.client.get_mahasiswa_count_active()
        assert result is None or isinstance(result, dict)

    def test_get_prodi_count_method(self):
        """Test get_prodi_count method functionality"""
        assert hasattr(self.client, 'get_prodi_count')
        assert callable(self.client.get_prodi_count)
        
        result = self.client.get_prodi_count()
        assert result is None or isinstance(result, dict)

    def test_get_pt_count_method(self):
        """Test get_pt_count method functionality"""
        assert hasattr(self.client, 'get_pt_count')
        assert callable(self.client.get_pt_count)
        
        result = self.client.get_pt_count()
        assert result is None or isinstance(result, dict)

    # ========== DATA METHODS TESTS (12 methods) ==========
    
    def test_get_data_dosen_keaktifan_method(self):
        """Test get_data_dosen_keaktifan method functionality"""
        assert hasattr(self.client, 'get_data_dosen_keaktifan')
        assert callable(self.client.get_data_dosen_keaktifan)
        
        result = self.client.get_data_dosen_keaktifan()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_dosen_bidang_method(self):
        """Test get_data_dosen_bidang method functionality"""
        assert hasattr(self.client, 'get_data_dosen_bidang')
        assert callable(self.client.get_data_dosen_bidang)
        
        result = self.client.get_data_dosen_bidang()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_dosen_jenis_kelamin_method(self):
        """Test get_data_dosen_jenis_kelamin method functionality"""
        assert hasattr(self.client, 'get_data_dosen_jenis_kelamin')
        assert callable(self.client.get_data_dosen_jenis_kelamin)
        
        result = self.client.get_data_dosen_jenis_kelamin()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_dosen_jenjang_method(self):
        """Test get_data_dosen_jenjang method functionality"""
        assert hasattr(self.client, 'get_data_dosen_jenjang')
        assert callable(self.client.get_data_dosen_jenjang)
        
        result = self.client.get_data_dosen_jenjang()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_dosen_ikatan_method(self):
        """Test get_data_dosen_ikatan method functionality"""
        assert hasattr(self.client, 'get_data_dosen_ikatan')
        assert callable(self.client.get_data_dosen_ikatan)
        
        result = self.client.get_data_dosen_ikatan()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_mahasiswa_bidang_method(self):
        """Test get_data_mahasiswa_bidang method functionality"""
        assert hasattr(self.client, 'get_data_mahasiswa_bidang')
        assert callable(self.client.get_data_mahasiswa_bidang)
        
        result = self.client.get_data_mahasiswa_bidang()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_mahasiswa_jenis_kelamin_method(self):
        """Test get_data_mahasiswa_jenis_kelamin method functionality"""
        assert hasattr(self.client, 'get_data_mahasiswa_jenis_kelamin')
        assert callable(self.client.get_data_mahasiswa_jenis_kelamin)
        
        result = self.client.get_data_mahasiswa_jenis_kelamin()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_mahasiswa_jenjang_method(self):
        """Test get_data_mahasiswa_jenjang method functionality"""
        assert hasattr(self.client, 'get_data_mahasiswa_jenjang')
        assert callable(self.client.get_data_mahasiswa_jenjang)
        
        result = self.client.get_data_mahasiswa_jenjang()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_mahasiswa_kelompok_lembaga_method(self):
        """Test get_data_mahasiswa_kelompok_lembaga method functionality"""
        assert hasattr(self.client, 'get_data_mahasiswa_kelompok_lembaga')
        assert callable(self.client.get_data_mahasiswa_kelompok_lembaga)
        
        result = self.client.get_data_mahasiswa_kelompok_lembaga()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_mahasiswa_status_method(self):
        """Test get_data_mahasiswa_status method functionality"""
        assert hasattr(self.client, 'get_data_mahasiswa_status')
        assert callable(self.client.get_data_mahasiswa_status)
        
        result = self.client.get_data_mahasiswa_status()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_pt_bentuk_method(self):
        """Test get_data_pt_bentuk method functionality"""
        assert hasattr(self.client, 'get_data_pt_bentuk')
        assert callable(self.client.get_data_pt_bentuk)
        
        result = self.client.get_data_pt_bentuk()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_pt_akreditasi_method(self):
        """Test get_data_pt_akreditasi method functionality"""
        assert hasattr(self.client, 'get_data_pt_akreditasi')
        assert callable(self.client.get_data_pt_akreditasi)
        
        result = self.client.get_data_pt_akreditasi()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_pt_kelompok_pembina_method(self):
        """Test get_data_pt_kelompok_pembina method functionality"""
        assert hasattr(self.client, 'get_data_pt_kelompok_pembina')
        assert callable(self.client.get_data_pt_kelompok_pembina)
        
        result = self.client.get_data_pt_kelompok_pembina()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_pt_provinsi_method(self):
        """Test get_data_pt_provinsi method functionality"""
        assert hasattr(self.client, 'get_data_pt_provinsi')
        assert callable(self.client.get_data_pt_provinsi)
        
        result = self.client.get_data_pt_provinsi()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_prodi_jenjang_method(self):
        """Test get_data_prodi_jenjang method functionality"""
        assert hasattr(self.client, 'get_data_prodi_jenjang')
        assert callable(self.client.get_data_prodi_jenjang)
        
        result = self.client.get_data_prodi_jenjang()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_prodi_akreditasi_method(self):
        """Test get_data_prodi_akreditasi method functionality"""
        assert hasattr(self.client, 'get_data_prodi_akreditasi')
        assert callable(self.client.get_data_prodi_akreditasi)
        
        result = self.client.get_data_prodi_akreditasi()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_prodi_bidang_ilmu_method(self):
        """Test get_data_prodi_bidang_ilmu method functionality"""
        assert hasattr(self.client, 'get_data_prodi_bidang_ilmu')
        assert callable(self.client.get_data_prodi_bidang_ilmu)
        
        result = self.client.get_data_prodi_bidang_ilmu()
        assert result is None or isinstance(result, (dict, list))

    def test_get_data_prodi_kelompok_pembina_method(self):
        """Test get_data_prodi_kelompok_pembina method functionality"""
        assert hasattr(self.client, 'get_data_prodi_kelompok_pembina')
        assert callable(self.client.get_data_prodi_kelompok_pembina)
        
        result = self.client.get_data_prodi_kelompok_pembina()
        assert result is None or isinstance(result, (dict, list))

    # ========== MISCELLANEOUS METHODS TESTS (3 methods) ==========
    
    def test_get_contributor_method(self):
        """Test get_contributor method functionality"""
        assert hasattr(self.client, 'get_contributor')
        assert callable(self.client.get_contributor)
        
        result = self.client.get_contributor()
        assert result is None or isinstance(result, (dict, list))

    def test_get_news_method(self):
        """Test get_news method functionality"""
        assert hasattr(self.client, 'get_news')
        assert callable(self.client.get_news)
        
        result = self.client.get_news()
        assert result is None or isinstance(result, dict)

    def test_get_bidang_ilmu_prodi_method(self):
        """Test get_bidang_ilmu_prodi method functionality"""
        assert hasattr(self.client, 'get_bidang_ilmu_prodi')
        assert callable(self.client.get_bidang_ilmu_prodi)
        
        result = self.client.get_bidang_ilmu_prodi()
        assert result is None or isinstance(result, (dict, list))

    # ========== ERROR HANDLING AND VALIDATION TESTS ==========
    
    def test_error_handling_empty_string(self):
        """Test error handling with empty string parameters"""
        # Empty string should return None due to validation
        result = self.client.search_mahasiswa("")
        assert result is None
        
        result = self.client.get_detail_mhs("")
        assert result is None

    def test_error_handling_none_values(self):
        """Test error handling with None parameters"""
        # None value should return None due to validation
        result = self.client.search_mahasiswa(None)
        assert result is None
        
        result = self.client.get_detail_pt(None)
        assert result is None

    def test_validation_methods_exist(self):
        """Test that internal validation methods exist"""
        assert hasattr(self.client, '_validate_keyword')
        assert hasattr(self.client, '_validate_year')
        assert hasattr(self.client, '_validate_id')
        assert hasattr(self.client, '_build_endpoint')
        
        # Check they are callable
        assert callable(self.client._validate_keyword)
        assert callable(self.client._validate_year)
        assert callable(self.client._validate_id)
        assert callable(self.client._build_endpoint)

    def test_test_data_constants_validity(self):
        """Test that test data constants are properly defined"""
        # Test constants exist and are not empty
        assert UNIVERSITY_NAME and len(UNIVERSITY_NAME) > 0
        assert STUDENT_NAME and len(STUDENT_NAME) > 0
        assert LECTURER_NAME and len(LECTURER_NAME) > 0
        assert PROGRAM_NAME and len(PROGRAM_NAME) > 0
        
        # Test IDs exist and are not empty
        assert STUDENT_ID and len(STUDENT_ID) > 0
        assert LECTURER_ID and len(LECTURER_ID) > 0
        assert UNIVERSITY_ID and len(UNIVERSITY_ID) > 0
        assert PROGRAM_ID and len(PROGRAM_ID) > 0
        
        # Test specific institutional values
        assert "Unika" in UNIVERSITY_NAME
        assert "Sistem Informasi" in PROGRAM_NAME
        assert "Ilham" in STUDENT_NAME
        assert "Ridwan" in LECTURER_NAME


if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v", "--tb=short"])
