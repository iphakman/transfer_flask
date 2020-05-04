from setuptools import setup, find_packages

setup(
    # Application name:
    name="transfer_money",
    # Version number:
    version="0.9.1",
    # Application author details:
    author="Joshue Perez",
    author_email="joshuefpj@gmail.com",
    # Packages
    packages=find_packages(),
    # Include additional files into the package
    include_package_data=True,
    # Details
    url="https://github.com/iphakman/transfer_money",
    description="Umba test API",
)

