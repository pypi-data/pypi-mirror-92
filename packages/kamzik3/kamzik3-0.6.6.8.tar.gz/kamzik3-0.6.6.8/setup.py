import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kamzik3",
    version="0.6.6.8",
    author="Martin Domaracky",
    author_email="martin.domaracky@desy.de",
    description="Device controlling framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stash.desy.de/projects/KAM/repos/kamzik3",
    packages=setuptools.find_packages(),
    package_data={'kamzik3': ['*.yml'], 'kamzik3.examples': ['*.yml', "*.att"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
        "numpy>=1.16",
        "pyzmq>=18.0",
        "pint>=0.16.0",
        "bidict>=0.18",
        "pyqt5>=5.15.0",
        "pyqtgraph>=0.11.0",
        "pyserial>=3.4",
        "oyaml>=0.9",
        "psutil>=5.6.0",
        "natsort>=7.0.1",
        "reportlab>=3.5.42",
        "pandas>=1.0.4"
    ],
    extras_requires={
        "pytango": [],
        "pyopengl": [],
        "sysutil": [],
        "pydaqmx": [],
        "pypiwin32": [],
        "rocketchat-API": [],
    },
    python_requires='>=3.6',
)
