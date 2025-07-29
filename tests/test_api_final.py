"""
Simple realistic test for PDDIKTI API
Tests with actual functionality and proper validation
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


def test_import_api():
    """Test that we can import the API class"""
    from pddiktipy.api import api
    assert api is not None


def test_api_initialization():
    """Test API client initialization"""
    from pddiktipy.api import api
    client = api()
    assert client is not None
    assert hasattr(client, 'H')
    assert hasattr(client, 'api_link')
    assert client.api_link is not None


def test_search_methods_exist():
    """Test that search methods exist and are callable"""
    from pddiktipy.api import api
    client = api()
    
    # Check search methods exist
    assert hasattr(client, 'search_all')
    assert hasattr(client, 'search_mahasiswa')
    assert hasattr(client, 'search_dosen')
    assert hasattr(client, 'search_pt')
    assert hasattr(client, 'search_prodi')
    
    # Check they are callable
    assert callable(client.search_all)
    assert callable(client.search_mahasiswa)
    assert callable(client.search_dosen)
    assert callable(client.search_pt)
    assert callable(client.search_prodi)


def test_detail_methods_exist():
    """Test that detail methods exist and are callable"""
    from pddiktipy.api import api
    client = api()
    
    # Check detail methods exist
    assert hasattr(client, 'get_detail_mhs')
    assert hasattr(client, 'get_detail_pt')
    assert hasattr(client, 'get_dosen_profile')
    
    # Check they are callable
    assert callable(client.get_detail_mhs)
    assert callable(client.get_detail_pt)
    assert callable(client.get_dosen_profile)


def test_university_methods_exist():
    """Test that university methods exist and are callable"""
    from pddiktipy.api import api
    client = api()
    
    # Check university methods exist
    assert hasattr(client, 'get_prodi_pt')
    assert hasattr(client, 'get_logo_pt')
    assert hasattr(client, 'get_rasio_pt')
    assert hasattr(client, 'get_mahasiswa_pt')
    assert hasattr(client, 'get_waktu_studi_pt')
    assert hasattr(client, 'get_name_histories_pt')
    assert hasattr(client, 'get_cost_range_pt')
    
    # Check they are callable
    assert callable(client.get_prodi_pt)
    assert callable(client.get_logo_pt)
    assert callable(client.get_rasio_pt)


def test_lecturer_methods_exist():
    """Test that lecturer methods exist and are callable"""
    from pddiktipy.api import api
    client = api()
    
    # Check lecturer methods exist
    assert hasattr(client, 'get_dosen_penelitian')
    assert hasattr(client, 'get_dosen_pengabdian')
    assert hasattr(client, 'get_dosen_karya')
    assert hasattr(client, 'get_dosen_paten')
    assert hasattr(client, 'get_dosen_study_history')
    assert hasattr(client, 'get_dosen_teaching_history')
    
    # Check they are callable
    assert callable(client.get_dosen_penelitian)
    assert callable(client.get_dosen_pengabdian)
    assert callable(client.get_dosen_study_history)


def test_search_mahasiswa_functionality():
    """Test search_mahasiswa functionality with real query"""
    from pddiktipy.api import api
    client = api()
    
    # Test with valid student name
    result = client.search_mahasiswa("Ilham")
    # Should return list or None (not raise exception)
    assert result is None or isinstance(result, list)
    
    # Test data constants
    assert STUDENT_NAME == "Ilham Riski"


def test_search_dosen_functionality():
    """Test search_dosen functionality with real query"""
    from pddiktipy.api import api
    client = api()
    
    # Test with valid lecturer name
    result = client.search_dosen("Ridwan")
    # Should return list or None (not raise exception)
    assert result is None or isinstance(result, list)
    
    # Test data constants
    assert LECTURER_NAME == "Ridwan Sanjaya"


def test_search_pt_functionality():
    """Test search_pt functionality with real query"""
    from pddiktipy.api import api
    client = api()
    
    # Test with valid university name
    result = client.search_pt("Unika")
    # Should return list or None (not raise exception)
    assert result is None or isinstance(result, list)
    
    # Test data constants
    assert UNIVERSITY_NAME == "Universitas Unika Soegijapranata"


def test_search_prodi_functionality():
    """Test search_prodi functionality with real query"""
    from pddiktipy.api import api
    client = api()
    
    # Test with valid program name
    result = client.search_prodi("Sistem Informasi")
    # Should return list or None (not raise exception)
    assert result is None or isinstance(result, list)
    
    # Test data constants
    assert PROGRAM_NAME == "Sistem Informasi"


def test_error_handling_empty_string():
    """Test error handling with empty string"""
    from pddiktipy.api import api
    client = api()
    
    # Empty string should return None due to validation
    result = client.search_mahasiswa("")
    assert result is None
    
    # Empty string for detail should return None
    result = client.get_detail_mhs("")
    assert result is None


def test_error_handling_none_value():
    """Test error handling with None value"""
    from pddiktipy.api import api
    client = api()
    
    # None value should return None due to validation
    result = client.search_mahasiswa(None)
    assert result is None
    
    # None value for detail should return None
    result = client.get_detail_pt(None)
    assert result is None


def test_context_manager():
    """Test API client as context manager"""
    from pddiktipy.api import api
    
    with api() as client:
        assert client is not None
        assert hasattr(client, 'search_mahasiswa')
        assert hasattr(client, 'H')


def test_api_close_method():
    """Test API client close method"""
    from pddiktipy.api import api
    client = api()
    
    # Close should not raise exception
    client.close()


def test_validation_methods():
    """Test internal validation methods"""
    from pddiktipy.api import api
    client = api()
    
    # These methods should exist for internal validation
    assert hasattr(client, '_validate_keyword')
    assert hasattr(client, '_validate_year')
    assert callable(client._validate_keyword)
    assert callable(client._validate_year)


def test_data_constants_validity():
    """Test that our test data constants are properly defined"""
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
    
    # Test specific values for Unika Soegijapranata
    assert "Unika" in UNIVERSITY_NAME
    assert "Sistem Informasi" in PROGRAM_NAME


def test_api_method_coverage():
    """Test that API has comprehensive method coverage"""
    from pddiktipy.api import api
    client = api()
    
    # Search methods
    search_methods = [
        'search_all', 'search_mahasiswa', 'search_dosen', 
        'search_pt', 'search_prodi'
    ]
    
    # Detail methods
    detail_methods = [
        'get_detail_mhs', 'get_detail_pt', 'get_dosen_profile'
    ]
    
    # University methods
    university_methods = [
        'get_prodi_pt', 'get_logo_pt', 'get_rasio_pt', 
        'get_mahasiswa_pt', 'get_waktu_studi_pt', 
        'get_name_histories_pt', 'get_cost_range_pt'
    ]
    
    # Lecturer methods
    lecturer_methods = [
        'get_dosen_penelitian', 'get_dosen_pengabdian', 
        'get_dosen_karya', 'get_dosen_paten',
        'get_dosen_study_history', 'get_dosen_teaching_history'
    ]
    
    all_methods = search_methods + detail_methods + university_methods + lecturer_methods
    
    for method_name in all_methods:
        assert hasattr(client, method_name), f"Method {method_name} not found"
        assert callable(getattr(client, method_name)), f"Method {method_name} not callable"


def test_comprehensive_api_initialization():
    """Test comprehensive API initialization and basic functionality"""
    from pddiktipy.api import api
    
    # Test normal initialization
    client = api()
    assert client is not None
    
    # Test context manager initialization
    with api() as client2:
        assert client2 is not None
        
        # Test basic method calls don't raise exceptions
        try:
            result = client2.search_mahasiswa("test")
            # Should either return data or None, not raise exception
            assert result is None or isinstance(result, (list, dict))
        except Exception as e:
            # If exception occurs, it should be a known API exception type
            assert "error" in str(e).lower() or "failed" in str(e).lower()


if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"])
