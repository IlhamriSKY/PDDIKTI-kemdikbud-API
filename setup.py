from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pddiktipy',  
    version='0.0.1',
    packages=['pddiktipy'],
	install_requires=['requests'],
    author="Ilham Riski",
    author_email="ilhamrisky21@gmail.com",
    description="Unofficial Python API wrapper to get data at PDDIKTI Kemdikbud",
    long_description=long_description,
	long_description_content_type="text/markdown",
    url="https://github.com/IlhamriSKY/PDDIKTI-kemdikbud-API",
    license='MIT License',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)