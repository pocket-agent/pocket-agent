# Pocket Agent Tool Specification


Tools are deterministic functions executed by the system.


The LLM selects tools.

The runtime executes tools.


# File Tools


## search_files()

Purpose:

Search NAS files (SQLite index when available; filesystem fallback).


Input:

```
query
location
filters (extension)
```


Output:

```
file paths
metadata
```


---

## index_files()

Purpose:

Rebuild the SQLite file index by scanning allowed NAS roots.


---

## read_file()

Purpose:

Read supported files.


Supported:

- PDF
- TXT
- DOCX
- XLSX


---


# Excel Tools


## analyze_excel()

Reads workbook structure and sample rows.


## modify_excel()

Applies a single cell change via safe-edit pipeline (backup → working copy → validate → replace).


Requirements:

- Backup first
- Validate output (openpyxl structure check)


# PDF Tools


## extract_pdf_text()

Extracts text from PDF files (PyMuPDF).


## modify_pdf()

Adds a new page with text (`add_page` action). Safe-edit pipeline with PDF structure validation.


# Word Tools


## modify_docx()

Appends or replaces last paragraph. Safe-edit pipeline with docx validation.


# Communication Tools


## send_telegram()


Sends response to user.


# Rules


Every tool must:

- Have documentation
- Validate inputs
- Handle errors
- Produce logs