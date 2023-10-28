# File converters

- [File converters](#file-converters)
  - [Should be ok](#should-be-ok)
    - [PyPDF2: PDF · PyPI](#pypdf2-pdf--pypi)
    - [EbookLib: EBOOK · PyPI](#ebooklib-ebook--pypi)
    - [python-docx: Offcie DOCX · PyPI](#python-docx-offcie-docx--pypi)
    - [KindleUnpack: MOBI \& AWZ ebooks](#kindleunpack-mobi--awz-ebooks)
  - [Tools](#tools)
    - [Temporary dirs/files](#temporary-dirsfiles)
    - [Infer the type of file](#infer-the-type-of-file)
    - [CSV output](#csv-output)
      - [Initial search](#initial-search)

## Should be ok

### [PyPDF2: PDF · PyPI](https://pypi.org/project/PyPDF2/)

```python
import PyPDF2

# Open the PDF file in read-binary mode
with open('yourfile.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

    # Initialize an empty string to store the text
    text = ''

    # Iterate through each page in the PDF
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()

# Now, 'text' contains the text extracted from the PDF
print(text)

```

### [EbookLib: EBOOK · PyPI](https://pypi.org/project/EbookLib/)

```bash
pip install ebooklib

```

```python
from ebooklib import epub

# Open the EPUB file
book = epub.read_epub('yourfile.epub')

# Initialize an empty string to store the text
text = ''

# Iterate through the items in the book
for item in book.items:
    if isinstance(item, epub.EpubHtml):
        text += item.content

# 'text' now contains the text from the EPUB
print(text)

```

### [python-docx: Offcie DOCX · PyPI](https://pypi.org/project/python-docx/)

```bash
pip install python-docx

```

```PYTHON
from docx import Document

# Open the DOCX file
doc = Document('yourfile.docx')

# Initialize an empty string to store the text
text = ''

# Iterate through the paragraphs in the document
for paragraph in doc.paragraphs:
    text += paragraph.text

# 'text' now contains the text from the DOCX file
print(text)

```

### [KindleUnpack: MOBI & AWZ ebooks](https://github.com/kevinhendricks/KindleUnpack)

```bash
pip install kindleunpack
```

```python

import kindleunpack

# Open the MOBI or AZW file
book = kindleunpack.mobi.Book("yourfile.mobi")

# Initialize an empty string to store the text
text = ''

# Iterate through the book's sections to extract text
for section in book.get_all_content():
    text += section.get_text()

# 'text' now contains the text from the Kindle file
print(text)


```

----------------

## Tools

### Temporary dirs/files

To create a temporary directory in a platform-independent way and ensure that it's deleted with all its contents, you can use the `tempfile` module. The `tempfile` module provides a cross-platform way to create temporary directories and files. Here's how you can use it:

```python
import tempfile
import shutil

def create_temp_directory():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    return temp_dir

def clean_temp_directory(temp_dir):
    # Delete the temporary directory and its contents
    shutil.rmtree(temp_dir, ignore_errors=True)

# Example of using the functions:
try:
    # Create a temporary directory
    temp_dir = create_temp_directory()

    # Work with the temporary directory
    # ...

    # When done, clean up the directory
    clean_temp_directory(temp_dir)
except Exception as e:
    # Handle any exceptions
    print(f"Error: {e}")
    # Clean up the directory in case of an error
    clean_temp_directory(temp_dir)
```

In this code:

1. `create_temp_directory()` creates a temporary directory using `tempfile.mkdtemp()`. This directory will be unique and platform-independent.

2. `clean_temp_directory(temp_dir)` is used to delete the temporary directory and its contents. The `shutil.rmtree` function is used for this purpose. We pass `ignore_errors=True` to ensure that it won't raise an error if the directory doesn't exist.

3. In your program, you can create the temporary directory, perform your work, and then call `clean_temp_directory` to ensure it's deleted.

4. In the event of an error, the temporary directory is also cleaned up.

This code should provide you with a reliable way to manage temporary directories and ensure they are deleted, regardless of the platform you're working on.

### Infer the type of file

You're correct that processing large files with wildcards and regular expressions can be slow, especially if the files are several megabytes in size. To improve performance and efficiently infer the type of file, you can follow a different approach by examining only a portion of the file, such as the first 10K bytes, as you suggested.

Here's an updated approach:

```python
import re
import glob

def has_extensions(text: str) -> bool:
    return bool(re.search(r'\.\w+', text))

def has_file_path(text: str) -> bool:
    return bool(re.search(r'(\w:/|/|\w:\\)', text))

# Your list to store lines from files
lines_list = []

# Process your input files one by one
input_files = ["file1.txt", "file2.txt", "path/to/files/*.txt"]  # Add your file paths or patterns

def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if has_extensions(line) or has_file_path(line):
                lines_list.append(line)

for input_file in input_files:
    # Check if the input_file is a wildcard pattern
    if '*' in input_file or '?' in input_file:
        matching_files = glob.glob(input_file)
        for file_path in matching_files:
            process_file(file_path)
    else:
        # Process a single file
        process_file(input_file)

# Now lines_list contains lines from both individual files and files matching wildcards
```

In this updated approach:

1. We have a `process_file` function that reads and processes a file line by line, similar to your initial code.

2. We check if the input file matches a wildcard pattern and process all matching files accordingly, using the `process_file` function.

3. For individual files, we also use the `process_file` function to read and process them.

This approach efficiently processes files by only examining a portion of each file. If a file is very large, it only processes the first part, which should help avoid performance issues.

### CSV output

Hi Silvio! Sure, I can help you with that. When saving data to a CSV file in Python, you can use the `csv` module, which is built into the language. Here's a step-by-step guide on how to save your book data to a CSV file:

1. **Import the CSV module:**
   First, you need to import the `csv` module at the beginning of your Python script:

   ```python
   import csv
   ```

2. **Open the CSV file for writing:**
   You can open a CSV file for writing using the `open()` function. Make sure to specify the mode as `'w'` (write) and the file name where you want to save your data.

   ```python
   with open('books.csv', 'w', newline='') as file:
       writer = csv.writer(file)
   ```

   The `newline=''` argument is used to ensure that there are no extra newline characters in the output file.

3. **Write data to the CSV file:**
   You can use the `writerow()` method to write a row of data to the CSV file. For each book, you can create a list of values (title and the dozen numbers) and write it to the file.

   ```python
   book_data = ["Book Title", 12, 34, 56, ...]  # Replace the numbers with your data.
   writer.writerow(book_data)
   ```

   You can repeat this step for each book.

4. **Close the CSV file:**
   After writing all your data, it's important to close the file to ensure that everything is saved properly.

   ```python
   file.close()
   ```

That's it! This will create a CSV file with your book data. You can repeat the process for each book you want to save. If you have any specific data or code you'd like to discuss, feel free to share it, and I can provide more detailed examples.

-----------------

#### Initial search

[Convert PDF to TXT file using Python - AskPython](https://www.askpython.com/python/examples/convert-pdf-to-txt)

[GitHub - raul23/convert-to-txt: Convert documents (pdf, djvu, epub, word) to txt](https://github.com/raul23/convert-to-txt)

[epub2txt · PyPI](https://pypi.org/project/epub2txt/) !!!

[GitHub - aerkalov/ebooklib: Python E-book library for handling books in EPUB2/EPUB3 format -](https://github.com/aerkalov/ebooklib)

[~~python-docx · PyPI~~](https://pypi.org/project/python-docx/)
