Project Summary 
Filtering and Extacting required data (ALL units from various departments in the academic catalogue) from locally stored document
Purpose: Collected and normalized course information by scraping program pages and course listings to produce machine-readable datasets and human-readable reports.
What's Included
Scripts: simple_extract.py, extract_units.py, extract_with_names.py, extract_final.py, detailed_courses.py, explore_units.py, debug_pdf.py
Outputs: courses_report.csv, courses_report.md, courses_with_names.md, courses_by_program.md, Courses.md, programs_courses.json, programs_data.json
Dependencies: requirements.txt
Quick Start
Install: pip install -r requirements.txt
Run extraction: python simple_extract.py (or python extract_with_names.py to include course names)
Result location: check the generated CSV/MD/JSON files in the repository root
Notes & Next Steps
Validation: review courses_report.csv for missing fields and run debug_pdf.py for problematic PDFs.
Enhancements: add retry/backoff, parallel requests, and a small CLI to select programs or output formats.
