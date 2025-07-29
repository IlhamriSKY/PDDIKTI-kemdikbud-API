# 🤝 Contributing Guide

Terima kasih atas minat Anda untuk berkontribusi! Panduan ini akan membantu Anda memulai.

## 🎯 Cara Berkontribusi

- **🐛 Laporkan Bug**: Buat issue dengan detail lengkap
- **💡 Usulkan Fitur**: Diskusikan ide baru via issue
- **📖 Perbaiki Docs**: Tingkatkan dokumentasi  
- **🔧 Kirim PR**: Fix bug atau implement fitur
- **🧪 Tambah Test**: Tingkatkan test coverage

## 🔧 Setup Development

```bash
# 1. Fork & Clone
git clone https://github.com/your-username/PDDIKTI-kemdikbud-API.git
cd PDDIKTI-kemdikbud-API

# 2. Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install Dependencies
pip install -r requirements.txt
pip install -e .

# 4. Verify Setup
python -c "from pddiktipy import api; print('Setup OK!')"
```

## 📝 Code Guidelines

### Standards
- Follow **PEP 8** style guide
- Use **Type Hints** untuk semua functions
- Write **Google-style docstrings**
- Keep functions **small** dan focused

### Example
```python
def search_mahasiswa(self, keyword: str) -> Optional[Dict[str, Any]]:
    """Mencari mahasiswa berdasarkan nama atau NIM.
    
    Args:
        keyword: Nama mahasiswa atau NIM untuk pencarian.
        
    Returns:
        Dictionary berisi data mahasiswa atau None jika error.
    """
    if not keyword.strip():
        raise ValidationError("Keyword tidak boleh kosong")
    return self._make_request('search', {'keyword': keyword})
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests (recommended)
python run_tests.py

# Run with pytest directly
pytest tests/ -v

# Run comprehensive tests only
pytest tests/test_comprehensive.py -v

# Run basic tests only
pytest tests/test_api_final.py -v

# Run with coverage
pytest tests/ --cov=pddiktipy --cov-report=html
```

### Test Requirements
- ✅ **All tests must pass** before submitting PR
- ✅ **Test coverage**: Add tests for new functionality
- ✅ **Test data**: Use centralized data in `tests/test_data.py`
- ✅ **No mocking**: Tests use real API calls for validation

📖 **[Lihat TESTING.md](TESTING.md)** untuk panduan testing lengkap.

## 🔄 Pull Request Process

1. **Create branch**: `git checkout -b feature/nama-fitur`
2. **Make changes** sesuai guidelines
3. **Add tests** untuk changes baru
4. **Run tests**: `python run_tests.py` - **WAJIB PASS**
5. **Commit**: `git commit -m "Add: deskripsi singkat"`
6. **Push & create PR**

### PR Checklist
- [ ] **Tests pass** (`python run_tests.py`)
- [ ] **Add tests** untuk functionality baru
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Descriptive commit messages

⚠️ **IMPORTANT**: PR akan ditolak jika tests tidak pass!

## 🐛 Bug Report Template

```markdown
**Bug Description**
Penjelasan singkat tentang bug.

**To Reproduce**
1. Step 1
2. Step 2
3. Error occurs

**Environment**
- OS: Windows 10 / Ubuntu 20.04
- Python: 3.9.7
- pddiktipy: 2.0.4
```

## ➡️ Feature Request Template

```markdown
**Problem**
Describe the problem this feature would solve.

**Solution**
Describe your proposed solution.

**Use Cases**
When would this feature be useful?
```

## 📖 Documentation

Update dokumentasi jika:
- Menambah method baru
- Mengubah API behavior
- Menambah dependencies

Files yang perlu diupdate:
- `README.md`: Quick start guide
- `API_DOCUMENTATION.md`: Detailed API reference
- Code docstrings: Inline documentation

---