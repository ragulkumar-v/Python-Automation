#!/usr/bin/env python3
"""
Batch-create and populate CSVs based on PDF filenames.

1. Scan INPUT_FOLDER for all PDFs.
2. Ensure OUTPUT_FOLDER exists.
3. For each PDF:
   a. Create an empty CSV named <pdf_stem>.csv in OUTPUT_FOLDER.
   b. Extract YEAR and QUARTER from the filename stem.
      - Matches patterns like '2021Q2', '2024_Q3', '..._2021_Q4_...'
      - Q1→start_month=1, Q2→4, Q3→7, Q4→10
   c. Prompt user once for:
      - Broker
      - Header row values (space-separated)
   d. Populate CSV:
      - Row 1: header values
      - Rows 2–73 (72 data rows):
          Col1: broker
          Col2: YEAR
          Col3: month blocks: 24× start_month, 24× start_month+1, 24× start_month+2
          Col4: SP500 flag pattern [1×12,0×12] repeated 3× → total 72 flags
          Remaining columns blank
"""

import csv
import re
from pathlib import Path
import re
from typing import Tuple, Optional
# === Configuration ===
INPUT_FOLDER = Path(r"C:\RA work\SEC Rule 606 Datasets\UBSS\pdf")
OUTPUT_FOLDER = Path(r"C:\RA work\SEC Rule 606 Datasets\UBSS\base_csv_12")
# =====================


def extract_year_quarter(stem: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract (year, quarter) from a filename stem.

    Matches any of:
      • 2021Q2, 2021-Q2, 2021_Q2, 2021 Q2
      • Q1 2022, q1_2022, q12022
      • ..._2021_Q4_..., ...-2021Q2, etc.

    Returns (year, quarter) or (None, None) if no match.
    """
    # 1) Year before Q:  YYYY [non-digits] Q?[-]?<1-4>
    m = re.search(r"(\d{4})\D*[Qq]\s*[-]?\s*([1-4])", stem)
    if m:
        year = int(m.group(1))
        quarter = int(m.group(2))
        return year, quarter

    # 2) Quarter before Year: Q?[-]?<1-4> [non-digits] YYYY
    m = re.search(r"[Qq]\s*([1-4])\D*(\d{4})", stem)
    if m:
        quarter = int(m.group(1))
        year = int(m.group(2))
        return year, quarter

    return None, None


def main():
    # Gather PDFs
    pdfs = sorted(INPUT_FOLDER.glob("*.pdf"))
    if not pdfs:
        print(f"❗ Caution: No PDFs in {INPUT_FOLDER}")
        return

    # Ensure output folder exists
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Prompt once for broker and header row
    broker = input("Broker: ").strip()
    header = input("Enter header values separated by space: ").strip().split()
    num_cols = len(header)

    # SP500 flag pattern: [1×12,0×12] ×3 → length 72
    base_pattern = [1]*12 + [0]*12
    spflags = base_pattern * 3  # 72 entries

    # Process each PDF
    for pdf in pdfs:
        stem = pdf.stem
        csv_path = OUTPUT_FOLDER / f"{stem}.csv"
        # Create or clear file
        csv_path.write_text("")

        year, q = extract_year_quarter(stem)
        if year is None:
            print(
                f"⚠️ Warning: Couldn't parse year/quarter from '{stem}'. Skipping.")
            continue
        # Determine start month mapping
        start_month = {1: 1, 2: 4, 3: 7, 4: 10}[q]

        # Build month list (72 entries): 24 of each quarter month
        months = [start_month]*24 + [start_month+1]*24 + [start_month+2]*24

        # Write CSV
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Header row
            writer.writerow(header)
            # 72 data rows
            for i in range(72):
                row = [
                    broker,       # column 1
                    year,         # column 2
                    months[i],    # column 3
                    spflags[i],   # column 4
                ]
                # fill remaining columns blank
                row += [""] * (num_cols - 4)
                writer.writerow(row)

        print(f"✅ Created and populated '{csv_path.name}' (Year={year}, Q{q})")


if __name__ == "__main__":
    main()
