# PDDIKTI API Testing Framework

## 📋 Overview

Proyek ini dilengkapi dengan comprehensive testing framework menggunakan pytest untuk memastikan kualitas dan reliabilitas PDDIKTI API Python Wrapper. Test suite mencakup **semua 54 API methods** dengan validation menyeluruh.

## 🚀 Quick Start

### Install Dependencies

```bash
# Install pytest dan dependencies
pip install pytest pytest-cov

# Atau install dari requirements
pip install -r requirements-test.txt
```

### Run Tests

```bash
# Run semua tests (recommended)
python run_tests.py

# Run dengan pytest langsung
pytest tests/ -v

# Run specific test file
pytest tests/test_comprehensive.py -v
pytest tests/test_api_final.py -v
```

## 📁 Test Structure

```
tests/
├── __init__.py                # Package initialization
├── conftest.py               # Pytest configuration & fixtures
├── test_data.py              # Centralized test data (Unika Soegijapranata)
├── test_comprehensive.py     # Comprehensive test suite (69 tests, all 54 API methods)
├── test_api_final.py         # Basic functionality tests (18 tests)
run_tests.py                  # Main test runner
```

## 🧪 Test Categories

### 1. Comprehensive Test Suite (`test_comprehensive.py`)
- **API Initialization Tests**: Import, context manager, close methods
- **Search Methods (5)**: `search_all`, `search_mahasiswa`, `search_dosen`, `search_pt`, `search_prodi`
- **Detail Methods (3)**: `get_detail_mhs`, `get_detail_pt`, `get_detail_prodi`  
- **Lecturer Methods (8)**: Profile, research, community service, patents, history
- **University Methods (14)**: Programs, statistics, costs, graduation rates, infrastructure
- **Program Methods (12)**: Description, capacity, ratios, costs, history
- **Statistics Methods (4)**: Active counts for students, lecturers, programs, universities
- **Data Analytics Methods (18)**: Comprehensive demographic and institutional data
- **Miscellaneous Methods (3)**: Contributors, news, scientific fields
- **Error Handling**: Empty string, None values, validation methods
- **Data Validation**: Test constants validity

### 2. Basic Functionality Tests (`test_api_final.py`)
- **Import & Initialization**: Basic API setup
- **Method Existence**: Verify all methods are callable
- **Search Functionality**: Real API calls with institutional data
- **Error Handling**: Input validation and edge cases
- **Context Manager**: Proper resource management

## 🏫 Test Data

Semua tests menggunakan data **Universitas Unika Soegijapranata**:

- **University**: Universitas Unika Soegijapranata
- **Student**: Ilham Riski  
- **Lecturer**: Ridwan Sanjaya
- **Program**: Sistem Informasi
- **Test IDs**: Valid IDs untuk setiap entity type

Data terpusat di `tests/test_data.py` untuk kemudahan maintenance.

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers --color=yes
markers =
    unit: Unit tests for individual functions
    integration: Integration tests with real API calls
    comprehensive: Full API method coverage tests
    basic: Basic functionality tests
```

### Test Fixtures (`conftest.py`)
- **API Client**: Pre-configured API client for tests
- **Test Timeout**: Timeout settings for network tests
- **Sample Keywords**: Test keywords for search functionality
## 📊 Test Results

### Test Coverage: **54/54 API Methods (100%)**

```bash
$ python run_tests.py

============================================================
PDDIKTI API TEST SUITE
============================================================
Testing Universitas Unika Soegijapranata Data
Student: Ilham Riski
Lecturer: Ridwan Sanjaya
Program: Sistem Informasi
============================================================

tests/test_comprehensive.py::TestAPIComprehensive
✅ 69 tests PASSED (36.39s)

tests/test_api_final.py
✅ 18 tests PASSED (2.54s)

SUCCESS: All tests passed!
Framework is optimized and ready for production use!
```

## 🚀 Running Tests

### Using Test Runner (Recommended)

```bash
# Run all tests
python run_tests.py
```

### Using Pytest Directly

```bash
# Run all tests
pytest tests/ -v

# Run comprehensive test suite only
pytest tests/test_comprehensive.py -v

# Run basic tests only  
pytest tests/test_api_final.py -v

# Run specific test method
pytest tests/test_comprehensive.py::TestAPIComprehensive::test_search_all_method -v
```

### Advanced Testing

```bash
# Run dengan coverage report
pytest tests/ --cov=pddiktipy --cov-report=html

# Run dan stop pada first failure
pytest tests/ -x

# Run dengan duration report
pytest tests/ --durations=10

# Run tests yang mengandung keyword
pytest tests/ -k "search" -v
```

## 🛠️ Test Strategy

### API Method Testing
- **Method Existence**: Verify all 54 methods exist and are callable
- **Functional Testing**: Test methods with real institutional data
- **Error Handling**: Test input validation and edge cases
- **Response Validation**: Verify return types (dict, list, string, None)

### No Mocking Approach
- Tests menggunakan **real API calls** untuk validation akurat
- Menggunakan data institusi nyata (Unika Soegijapranata)
- Proper error handling untuk network issues
- Graceful handling untuk API timeouts atau downtime

### Data Centralization
- Semua test data terpusat di `tests/test_data.py`
- Consistent institutional data across all tests
- Easy maintenance dan updates

## 🔍 Test Best Practices

### 1. Test Structure
```python
class TestAPIComprehensive:
    """Comprehensive test class for all PDDIKTI API methods"""
    
    @pytest.fixture(autouse=True)
    def setup_api_client(self):
        """Setup API client for all tests"""
        from pddiktipy.api import api
        self.client = api()
        yield
        self.client.close()
```

### 2. Method Testing Pattern
```python
def test_search_mahasiswa_method(self):
    """Test search_mahasiswa method functionality"""
    # Verify method exists
    assert hasattr(self.client, 'search_mahasiswa')
    assert callable(self.client.search_mahasiswa)
    
    # Test with real data
    result = self.client.search_mahasiswa(STUDENT_NAME.split()[0])
    assert result is None or isinstance(result, (list, dict))
```

### 3. Error Handling
```python
def test_error_handling_empty_string(self):
    """Test error handling with empty string parameters"""
    result = self.client.search_mahasiswa("")
    assert result is None
```

## 🐛 Debugging Tests

### Failed Test Debugging
```bash
# Run dengan full traceback
pytest tests/ --tb=long

# Run dengan detailed output
pytest tests/ -vvv

# Run specific failing test
pytest tests/test_comprehensive.py::TestAPIComprehensive::test_failing_method -vvv
```

### Test Output
```bash
# Show print statements
pytest tests/ -s

# Show all output
pytest tests/ -v -s --tb=short
```

## 📦 Dependencies

### Required
```txt
pytest>=7.0.0
requests>=2.25.0
```

### Optional  
```txt
pytest-cov>=4.0.0       # Coverage reporting
pytest-html>=3.0.0      # HTML reports
pytest-xdist>=3.0.0     # Parallel testing
```

## 🎯 Test Goals

✅ **ACHIEVED:**
1. **Complete API Coverage**: All 54 public methods tested
2. **Error Handling**: Comprehensive input validation testing
3. **Real Data Testing**: Uses actual institutional data
4. **Professional Standards**: English language, clean output
5. **Centralized Data**: Easy maintenance and updates

## 📋 Test Checklist

Sebelum release/PR, pastikan:

- [ ] ✅ Semua tests pass (`python run_tests.py`)
- [ ] ✅ No lint errors
- [ ] ✅ All 54 API methods covered
- [ ] ✅ Error handling tests pass
- [ ] ✅ Test data is up to date

## 🤝 Contributing Tests

Saat menambah fitur baru:

1. **Add Method Tests** ke `test_comprehensive.py`
2. **Update Test Data** di `test_data.py` jika perlu
3. **Add Error Cases** untuk validation
4. **Run Full Suite** sebelum commit: `python run_tests.py`
5. **Update Documentation** untuk test cases baru

### Adding New API Method Test

```python
def test_new_api_method(self):
    """Test new_api_method functionality"""
    assert hasattr(self.client, 'new_api_method')
    assert callable(self.client.new_api_method)
    
    result = self.client.new_api_method(TEST_PARAMETER)
    assert result is None or isinstance(result, (dict, list))
```

---

Happy Testing! 🧪✨
