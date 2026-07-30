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


# Web Tools


## web_search()


Search the public web (ddgs / DuckDuckGo backends).


## fetch_url()


Fetch a URL and return extracted readable text.


## current_weather()


Current conditions via Open-Meteo (no API key).


## timezone_now()


Local time for a city via Open-Meteo geocoding.


# Utility Tools


## exchange_rate()


Currency conversion via Frankfurter (ECB rates).


## unit_convert()


Length, mass, and temperature conversion.


# Calendar


## calendar_events()


Read-only upcoming events from `CALENDAR_ICS_URL` (private ICS feed).


# Automation


## schedule_reminder()


## list_scheduled_tasks()


## cancel_task()


## run_allowed_script()


Runs scripts listed in `config/settings.yaml` → `automation.allowed_scripts`.


# Rules


Every tool must:

- Have documentation
- Validate inputs
- Handle errors
- Produce logs