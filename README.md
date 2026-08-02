# 🎓 PDDIKTI API Python Library

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/39e00a8c8c1c4007a68d1ae3f53c03e7)](https://app.codacy.com/gh/IlhamriSKY/PDDIKTI-kemdikbud-API/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![python3.x](https://img.shields.io/badge/3.12.1-blue.svg?&logo=python&label=Python)](https://www.python.org/downloads/release/python-3121/)
[![Version](https://img.shields.io/pypi/v/pddiktipy?logo=pypi&logoColor=white&label=PyPI&color=c125ff&cacheSeconds=3600)](https://pypi.org/project/pddiktipy/)
[![Downloads](https://img.shields.io/pepy/dt/pddiktipy?logo=PyPI&logoColor=white&label=Downloads&color=c125ff)](https://www.pepy.tech/projects/pddiktipy)
[![Author](https://img.shields.io/badge/Author-Ilham%20Riski-blue.svg?style=flat)](https://github.com/IlhamriSKY)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/blob/master/LICENSE)

> **An unofficial Python wrapper for the Indonesian Higher Education Database (PDDIKTI, Kemdiktisaintek).**

`pddiktipy` gives you a clean, typed interface to student, lecturer, university,
and study-program data from [PDDIKTI](https://pddikti.kemdiktisaintek.go.id/),
with connection pooling, retries, validation, and comprehensive error handling.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Cloudflare access (read this first)](#-cloudflare-access-read-this-first)
- [Quick Start](#-quick-start)
- [Error Handling](#-error-handling)
- [Documentation](#-documentation)
- [Requirements](#-requirements)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Features

- ✅ **70+ endpoints**: search, details, statistics, and visualizations
- ✅ **Full type hints** for good editor support
- ✅ **Robust error handling** with custom exceptions and input validation
- ✅ **Context manager** support for clean resource management
- ✅ **Connection pooling & retries** out of the box
- ✅ **Transparent AES-256 decryption** for the encrypted search endpoint

## 📦 Installation

```bash
pip install pddiktipy
```

To let the client read the Cloudflare clearance cookie from your local browser
automatically (see below), install the optional extra:

```bash
pip install "pddiktipy[auto]"
```

## 🚨 Cloudflare access (read this first)

The upstream API (`https://pddikti.kemdiktisaintek.go.id/api`) is protected by a
**Cloudflare Turnstile** challenge. A plain HTTP client always receives `403`, so
**`api()` with no arguments will not work on its own.** Only a real browser can
pass the challenge. Even automated browsers (Selenium/Playwright) are blocked.

You therefore need to supply Cloudflare *clearance* in one of three ways.

### Option A: auto cookie (easiest, on your own machine)

```bash
pip install "pddiktipy[auto]"
```

1. Open `https://pddikti.kemdiktisaintek.go.id` in Chrome or Edge and complete
   the **"Verify you are human"** check once.
2. Run your code. The client reads the `cf_clearance` cookie for you:

```python
from pddiktipy import api

with api(auto_cookie=True) as client:
    print(client.get_pt_count())   # {'status': 'success', 'data': {'jumlah': 4416}}
```

### Option B: paste the cookie manually (works on servers or other machines)

1. Open the site in your browser and pass the check.
2. Open DevTools (`F12`) → **Application → Cookies** → select the site → copy the
   value of **`cf_clearance`**.
3. In DevTools → **Network**, click any request → **Headers** → copy the
   **`User-Agent`** (the cookie is bound to it).

```python
from pddiktipy import api

client = api(
    cf_clearance="PASTE_CF_CLEARANCE_HERE",
    user_agent="PASTE_YOUR_BROWSER_USER_AGENT_HERE",
)
print(client.get_pt_count())
```

### Option C: run your own solver proxy (most stable for production)

Point `base_url` at a service that solves Cloudflare for you (for example a
[FlareSolverr](https://github.com/FlareSolverr/FlareSolverr)-backed proxy that
forwards to the PDDIKTI upstream):

```python
from pddiktipy import api

client = api(base_url="http://localhost:8080/api")
print(client.get_pt_count())
```

> **Note:** `cf_clearance` is bound to your IP and User-Agent and expires after
> ~30 minutes. For long-running, unattended use, prefer **Option C**.

## ⚡ Quick Start

```python
from pddiktipy import api
from pprint import pprint

# See "Cloudflare access" above for how to provide clearance.
with api(auto_cookie=True) as client:
    # Search across all categories (payload is decrypted for you)
    results = client.search_all("Universitas Diponegoro")
    pprint(results)

    # Search a specific category
    students = client.search_mahasiswa("Ilham Riski Wibowo")
    pprint(students)

    # Aggregate statistics
    print(client.get_pt_count())          # number of universities
    print(client.get_mahasiswa_count())   # number of students
```

A runnable example lives in [`examples/quickstart.py`](examples/quickstart.py).

## ⚠️ Error Handling

By default, API methods **log and return `None`** on failure rather than raising,
so everyday calls stay simple:

```python
with api(auto_cookie=True) as client:
    result = client.search_mahasiswa("")   # invalid keyword -> logs and returns None
    if result is None:
        print("No result / request failed")
```

The lower-level exceptions are still available if you build on top of the helper:

```python
from pddiktipy.exceptions import (
    ValidationError, APIConnectionError, APITimeoutError,
    APIRateLimitError, APIResponseError, PDDIKTIError,
)
```

If the upstream returns a Cloudflare challenge, the client raises an
`APIResponseError` whose message explains exactly how to supply clearance.

## 📚 Documentation

**➡️ [API Documentation](documentation/API_DOCUMENTATION.md)**: every method, with
parameters, examples, and response field descriptions.

## 📋 Requirements

- **Python 3.7+**
- **requests**
- **cryptography**
- **browser_cookie3** *(optional, only for `auto_cookie=True`)*

## 🧪 Testing

**🧪 [Testing Guide](documentation/TESTING.md)**: how to run the test suite.

Offline tests (no network) can be run directly:

```bash
python -m pytest tests/test_crypto_and_endpoints.py -q
```

## 🤝 Contributing

**🤝 [Contributing Guide](documentation/CONTRIBUTING.md)**: how to contribute.

## 📄 License

Distributed under the [MIT License](LICENSE).

---

## 📞 Support & Contact

- **Author**: [Ilham Riski Wibowo](https://github.com/IlhamriSKY)
- **Issues**: [GitHub Issues](https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/issues)
- **PyPI**: [pddiktipy](https://pypi.org/project/pddiktipy/)

**⭐ If this library helps your project, please consider starring it on GitHub!**
