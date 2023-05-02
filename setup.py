from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in navari_kayes/__init__.py
from navari_kayes import __version__ as version

setup(
	name="navari_kayes",
	version=version,
	description="Reports and customizations for Kayes",
	author="Navari Limited",
	author_email="info@navari.co.ke",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
