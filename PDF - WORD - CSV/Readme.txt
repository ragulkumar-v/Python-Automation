Project: SEC Rule 606 – PDF → Word → CSV Extraction & Consolidation Pipeline

This project automates the processing of SEC Rule 606 quarterly disclosure files by:

Extracting ZIP files

Converting PDFs to Word (.docx)

Extracting required tables from Word files into CSVs

Generating structured Base CSV templates

Manually copying venue & values into Base CSV files

Combining each broker’s sheets

Combining all brokers into a unified master sheet

Below is the description of each script used in the workflow.

📂 Scripts Overview
1️⃣ 1.Unzip_file.py — Extract ZIP Archives

Unzips all .zip files from a main folder and its subfolders.
Supports custom output directory and handles corrupt ZIPs gracefully.

The logic walks folders using os.walk() and extracts ZIPs using zipfile.ZipFile 

1.Unzip_file

.

2️⃣ 2.Pdf_to_word.py — PDF → DOCX Conversion

Batch-converts PDFs into Word (.docx) automatically.

✔ Uses pdf2docx.Converter
✔ Auto-creates output folder if missing
✔ Logs success/failure per file

Conversion routine: convert_pdf_to_docx() 

2.Pdf_to_word


Main loop iterates through PDFs and saves DOCX files 

2.Pdf_to_word

.

3️⃣ 3.Extract_tables.py — Extract Table 2 From Word

This script opens each .docx file and:

✔ Locates month section headings using regex
✔ Identifies tables under each month
✔ Merges split tables with identical headers
✔ Extracts Table 2 for:

S&P 500 section

Non–S&P 500 section

✔ Saves output as CSVs:

<Month>_SP500_Table2.csv
<Month>_NonSP500_Table2.csv


Internal logic:

Paragraph/table block iteration 

3.Extract_tables

Header comparison & table merging 

3.Extract_tables

Table 2 exporting per month 

3.Extract_tables

4️⃣ 4.Base_CSV_Generation.py — Generate Structured Base CSV Template

This script builds a Base CSV file for each PDF, containing:

Broker name (user input)

Year (derived automatically)

Quarter months (24× each month)

SP500 flags (pattern repeated for 72 rows)

Placeholder columns for venue & metric data

Pattern extraction logic for year/quarter: 

4. Base_CSV_Generation


CSV writing logic (72 rows): 

4. Base_CSV_Generation

📌 🔴 Manual Step (After File #4)

After base CSV files are generated:

➡ Copy the required venue names and numerical data values from Table 2 (SP500 & Non-SP500) extracted in Step 3 into the corresponding rows/columns of each Base CSV.

You will typically fill columns such as:

Venue

Order Type

Net Payment

Fill Rates

Execution Quality Metrics

Once all base CSV files are filled, continue with the combination scripts.

5️⃣ 5.Combine Each Sheet of company.py — Combine All CSV/XLSX for a Single Broker

This script merges files belonging to one broker.

✔ Supports both .csv and .xlsx
✔ First file acts as schema base
✔ Trims at first blank row (“till before null”)
✔ Aligns all columns
✔ Appends remaining sheets
✔ Outputs consolidated Excel named Combined.xlsx

File reading & trimming logic:

Robust CSV/XLSX reader 

5.Combine Each Sheet of company

Blank-row trimming & alignment 

5.Combine Each Sheet of company

6️⃣ 6.Combine All Company sheet.py — Merge All Companies Into One Master File

After each broker folder has its own combined Excel, this script merges them:

✔ Reads all CSV files
✔ Uses first CSV as base
✔ Trims at blank rows
✔ Aligns columns
✔ Appends all broker data into a single Excel output

Combination logic is similar to file #5 but focused on CSVs only.