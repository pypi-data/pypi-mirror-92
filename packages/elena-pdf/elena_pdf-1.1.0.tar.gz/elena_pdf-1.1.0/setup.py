#! python3
import os
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup (
	name = "elena_pdf",
	version = "1.1.0", 
	description = "Manage pdf files: merge, split, convert to image and convert images to pdf",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Dari Developer",
	author_email = "hernandezdarifrancisco@gmail.com",
	license = "MIT",
	keywords = "elena, elena pdf, pdf, merge, split, convert to image, convert to pdfo, merge pdf, split pdf, convert pdf to image, convert image to pdf, pdf files, manage pdf",
	project_urls = {
		"Documentation": "https://github.com/DariHernandez/elena_pdf/blob/master/README.md",
		"Funding": "https://www.paypal.com/paypalme/FranciscoDari",
		"Source": "https://github.com/DariHernandez/elena_pdf"
		},
	packages = find_packages(include=["elena_pdf", "elena_pdf.*"]),
	install_requires = ["PyPDF2", "pdf2image", "img2pdf", "Send2Trash", "Pillow"],
	python_requires = ">=3.7"
)
