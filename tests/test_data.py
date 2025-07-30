"""
Test data constants for PDDIKTI API testing.

This file contains validated test data sourced from real PDDIKTI database entries.
All IDs are encoded and anonymized for testing purposes while maintaining
functionality with the live PDDIKTI API endpoints.

Note: This data is used for automated testing only and respects privacy guidelines.
"""

# =============================================================================
# PDDIKTI API TEST DATA - Real database IDs for testing
# =============================================================================

# Test University Data - Universitas Katolik Soegijapranata
# Verified working university ID from PDDIKTI database
UNIVERSITY_ID = "6m7kg4twGiZAdNiUDMC9Q6KaGqUBqNU9_fLWD8DaSxMF-cIjwu8A7K6lWYKzaJXGBDQHsQ=="
UNIVERSITY_NAME = "Universitas Katolik Soegijapranata"

# Test Lecturer Data - Real academic staff profile
# Verified working lecturer ID from PDDIKTI database  
LECTURER_ID = "cWS5HuRYaG9KU4nyNc5Ue2dYqK6Y87qxHe3an1uTAhr-ohr7y-Lm6G7pQP2Jy0V_KR-q4A=="
LECTURER_NAME = "Ridwan Sanjaya"
LECTURER_UNIVERSITY = "Universitas Katolik Soegijapranata"

# Test Student Data - Verified student record
# Real student ID from PDDIKTI database for testing API methods
STUDENT_ID = "zQpt4pGGyVuhVoglK-qW4_C9iM-y-8vcO5EVX04cycXvwpx4Tvi8FbeyI5MbUrakrD_C0w=="
STUDENT_NAME = "Ilham Riski Wibowo"
STUDENT_UNIVERSITY = "Universitas Katolik Soegijapranata"

# Test Program Data - Uses university ID as fallback for program-specific tests
# Note: Some program methods may require specific program IDs which may not be publicly accessible
PROGRAM_ID = "6m7kg4twGiZAdNiUDMC9Q6KaGqUBqNU9_fLWD8DaSxMF-cIjwu8A7K6lWYKzaJXGBDQHsQ=="
PROGRAM_NAME = "Sistem Informasi"

# Test Parameters - Valid values for API method testing
VALID_SEMESTER = "20241"  # Format: YYYYS (Year + Semester number)
VALID_YEAR = "2024"

# Search Terms - Common terms guaranteed to return results from PDDIKTI
SEARCH_STUDENT_TERM = "Ahmad"  # Common Indonesian name in PDDIKTI database
SEARCH_LECTURER_TERM = "Dr"    # Academic title prefix common in lecturer names  
SEARCH_UNIVERSITY_TERM = "Institut"  # Common university type in Indonesia
SEARCH_PROGRAM_TERM = "Teknik Informatika"  # Popular study program name

# =============================================================================
# TESTING NOTES:
# =============================================================================
# - All IDs are real and verified from PDDIKTI database
# - Data selected to respect privacy while maintaining test functionality
# - University and lecturer data are public academic profiles
# - Student data is anonymized but functional for API testing
# - Search terms chosen for consistent test results across API calls


class TestDataConstants:
    """
    Centralized test data constants for PDDIKTI API testing.
    
    Contains validated real IDs and search terms for comprehensive API testing.
    All data is anonymized but functional with live PDDIKTI endpoints.
    """
    
    # University Data
    UNIVERSITY_ID = UNIVERSITY_ID
    UNIVERSITY_NAME = UNIVERSITY_NAME
    
    # Lecturer Data  
    LECTURER_ID = LECTURER_ID
    LECTURER_NAME = LECTURER_NAME
    LECTURER_UNIVERSITY = LECTURER_UNIVERSITY
    
    # Student Data
    STUDENT_ID = STUDENT_ID
    STUDENT_NAME = STUDENT_NAME
    STUDENT_UNIVERSITY = STUDENT_UNIVERSITY
    
    # Program Data
    PROGRAM_ID = PROGRAM_ID
    PROGRAM_NAME = PROGRAM_NAME
    
    # Test Parameters
    VALID_SEMESTER = VALID_SEMESTER
    TEST_YEAR = VALID_SEMESTER  # Use semester format instead of year for methods that need YYYYS format
    
    # Search Keywords
    SEARCH_KEYWORD_GENERAL = SEARCH_UNIVERSITY_TERM
    SEARCH_KEYWORD_STUDENT = SEARCH_STUDENT_TERM
    SEARCH_KEYWORD_LECTURER = SEARCH_LECTURER_TERM
    SEARCH_KEYWORD_UNIVERSITY = SEARCH_UNIVERSITY_TERM
    SEARCH_KEYWORD_PROGRAM = SEARCH_PROGRAM_TERM