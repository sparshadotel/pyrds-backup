import setuptools
import os

try:
    with open('README.md') as file:
        long_description = file.read()
except IOError:
    # Handle file not found Exception.
    long_description = 'A simplified way to transfer RDS Backups to S3'


setuptools.setup(
    name="pyrdsbackup",
    version="1.1.2",
    author="Sparsha Dotel",
    author_email="sparshadotel@gmail.com",
    description="Simplify RDS Backups to S3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darmagedon/pyrds-backup.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ),
    keywords='cli',
    install_requires=(
        'pyodbc==4.0.23'
    ),
)
