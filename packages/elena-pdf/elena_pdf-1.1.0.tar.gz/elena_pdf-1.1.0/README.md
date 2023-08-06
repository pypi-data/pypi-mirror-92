# Elena Pdf
Manage pdf files fast and easy
Merge, split, convert pdf to image and convert images to pdf

# Install 
```bash
$ pip install elena-pdf
```

# How to use

## Import module
``` python
from elena_pdf import elena
```

## Merge pdf files

List of files to merge
``` python
files_to_merge = [
    "c:\\my_folder\\01.pdf",
    "c:\\my_folder\\02.pdf",
    "c:\\my_folder\\03.pdf"
]
```

Instance of the class
``` python
my_elena = elena.PdfManager (files_to_merge, replace=True, debug=True)

# replace: replace destination file if exist
# debug: print program status during execution
```

Merge file and save in specific output file
``` python
my_elena.merge("c:\\output_folder\\output_file.pdf")
```

Merge file and save in specific folder, with default output file name
``` python
my_elena.merge("c:\\output_folder")
```

## Split pdf files

List of files to merge
``` python
files_to_split = [
    "c:\\my_folder\\01.pdf",
    "c:\\my_folder\\02.pdf",
    "c:\\my_folder\\03.pdf"
]
```

Instance of the class
``` python
my_elena = elena.PdfManager (files_to_split, replace=True, debug=True)

# replace: replace destination file if exist
# debug: print program status during execution
```

Split files with default base name
``` python
my_elena.split("c:\\output_folder")
```

Split files with specific base name
``` python
my_elena.split("c:\\output_folder", " page ")
```

Split files with empty base name
``` python
my_elena.split("c:\\output_folder", "")
```

## Convert pdf to image

List of files to merge
``` python
files_to_convert = [
    "c:\\my_folder\\01.pdf",
    "c:\\my_folder\\02.pdf",
    "c:\\my_folder\\03.pdf"
]
```

Instance of the class
``` python
my_elena = elena.PdfManager (files_to_convert, replace=True, debug=True)

# replace: replace destination file if exist
# debug: print program status during execution
```

Convert files to images with default base name
``` python
my_elena.pdf_to_img("c:\\output_folder")
```

Convert files to images specific base name
``` python
my_elena.pdf_to_img("c:\\output_folder", " page ")
```

Convert files to images with empty base name
``` python
my_elena.pdf_to_img("c:\\output_folder", "")
```

## Convert image to pdf

List of files to merge
``` python
files_to_convert = [
    "c:\\my_folder\\01.jpg",
    "c:\\my_folder\\02.jpg",
    "c:\\my_folder\\03.jpg"
]
```

Instance of the class
``` python
my_elena = elena.PdfManager (files_to_convert, replace=True, debug=True)

# replace: replace destination file if exist
# debug: print program status during execution
```

Convert imges to pdf files, and generate one file for image
``` python
my_elena.pdf_to_img("c:\\output_folder")
```

Convert imges to pdf files, and merge in one oputput file
``` python
my_elena.pdf_to_img("c:\\output_folder", "c:\\output_folder\\images_converted.pdf")
```
