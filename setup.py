from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
def get_version():
    init_file = os.path.join(os.path.dirname(__file__), 'pddiktipy', '__init__.py')
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pddiktipy",
    version=get_version(),
    author="Ilham Riski Wibowo",
    author_email="ilhamrisky21@gmail.com",
    description="Unofficial Python API wrapper to get data at PDDIKTI Kemdikbud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API",
    project_urls={
        "Homepage": "https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API",
        "Repository": "https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API",
        "Issues": "https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API/issues",
        "Documentation": "https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API#readme",
    },
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords=[
        "pddikti", 
        "api", 
        "education", 
        "indonesia", 
        "kemdikbud", 
        "data"
    ],
    license="MIT",
)
