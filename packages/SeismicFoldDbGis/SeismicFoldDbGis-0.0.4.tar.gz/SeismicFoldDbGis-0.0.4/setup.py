"""
    SETUP
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SeismicFoldDbGis",
    version="0.0.4",
    author="Piotr Synowiec",
    author_email="psynowiec@gmail.com",
    description="Loads calculated fold from CSV file to GIS database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mysiar/seismic-fold_db_gis-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
