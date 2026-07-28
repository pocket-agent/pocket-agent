# Pocket Agent Tool Specification


Tools are deterministic functions executed by the system.


The LLM selects tools.

The runtime executes tools.


# File Tools


## search_files()

Purpose:

Search NAS files.


Input:

```
query
location
filters
```


Output:

```
file paths
metadata
```


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


Reads workbook structure.


## modify_excel()


Applies controlled changes.


Requirements:

- Backup first
- Validate output


# PDF Tools


## extract_pdf_text()


## modify_pdf()


# Communication Tools


## send_telegram()


Sends response to user.


# Rules


Every tool must:

- Have documentation
- Validate inputs
- Handle errors
- Produce logs