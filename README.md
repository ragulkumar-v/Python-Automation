📘 README – SEC Rule 605/606 Data Processing Pipeline

This repository contains two automated data-processing workflows used to extract, transform, and combine SEC Rule 605/606 broker-dealer disclosure data. The scripts support both ZIP/DAT-based filings and PDF-to-Word-based filings, producing clean, structured CSV/Excel files ready for analysis.

📂 Overview of Workflows
1️⃣ ZIP / DAT File Processing Workflow

Automates the full process of handling machine-readable 605/606 datasets:

Download and extract ZIP/DAT files

Unzip nested archives

Convert .dat files to .csv

Merge all CSVs into a single combined dataset

Key scripts include:

ZIP_Download_driver.py

Unzip_file.py

convert_csv.py

Merge_CSV_Files.py

This pipeline is used when brokers publish structured, machine-readable .dat files.

2️⃣ PDF → Word → CSV Extraction Workflow

Automates the processing of PDF-based 606 reports (text/table-based disclosures):

Unzip ZIP files containing PDFs

Convert PDFs → Word (.docx)

Extract Table 2 (SP500 & Non-SP500) from Word

Generate Base CSV templates for each filing

Copy venue & execution data into Base CSVs

Combine sheets per company

Merge all companies into one master file

Key scripts include:

Unzip_file.py

Pdf_to_word.py

Extract_tables.py

Base_CSV_Generation.py

Combine Each Sheet of company.py

Combine All Company sheet.py

This workflow is used when brokers publish PDF-format disclosures instead of standardized DAT files.

📦 What This Repository Provides

✔ Automated extraction and formatting pipelines for both data formats
✔ Cleaned and standardized CSV output per month, quarter, and company
✔ Consolidated master datasets across all brokers
✔ Modular scripts that can be run independently or in sequence
✔ Clear folder-level separation of raw, intermediate, and final files

🚀 Running the Workflows

Each workflow is independent. Use:

ZIP/DAT workflow:
python ZIP_Download_driver.py
python Unzip_file.py
python convert_csv.py
python Merge_CSV_Files.py

PDF-to-Word workflow:
python 1.Unzip_file.py
python 2.Pdf_to_word.py
python 3.Extract_tables.py
python 4.Base_CSV_Generation.py
# → manual step: copy venue/data into Base CSVs
python 5.Combine Each Sheet of company.py
python 6.Combine All Company sheet.py

📝 Notes

Both workflows can coexist and support different broker disclosure formats.

Output files are designed for downstream analytics or reporting.

Folder paths may need to be configured before running each script.
