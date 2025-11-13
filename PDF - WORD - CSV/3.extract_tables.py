from pathlib import Path
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
import pandas as pd
import re
from collections import defaultdict

INPUT_FOLDER = Path(
    r"C:\RA work\SEC Rule 606 Datasets\PNC\word")
# <-- Change as needed
OUTPUT_PATH = Path(
    r"C:\RA work\SEC Rule 606 Datasets\1_csv\TastyWorks")
month_regex = re.compile(
    r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}$',
    re.IGNORECASE
)


def iter_block_items(doc):
    for block in doc.element.body:
        if block.tag.endswith('tbl'):
            yield Table(block, doc)
        elif block.tag.endswith('p'):
            yield Paragraph(block, doc)


def is_header_row(row):
    header_keywords = ["Venue", "Order",
                       "Net Payment", "Venue -", "Orders (%)"]
    return any(any(hk in cell.text for hk in header_keywords) for cell in row.cells)


def get_row_values(row):
    return [cell.text.strip() for cell in row.cells]


def tables_have_same_header(table1, table2):
    return get_row_values(table1.rows[0]) == get_row_values(table2.rows[0])


def merge_tables(tables):
    merged = []
    i = 0
    while i < len(tables):
        curr_table = tables[i]
        if i < len(tables) - 1:
            next_table = tables[i + 1]
            if tables_have_same_header(curr_table, next_table):
                for row in next_table.rows[1:]:
                    curr_table._tbl.append(row._tr)
                merged.append(curr_table)
                i += 2
                continue
        merged.append(curr_table)
        i += 1
    return merged


def table_to_dataframe(table):
    data = []
    for row in table.rows:
        data.append([cell.text.strip() for cell in row.cells])
    return pd.DataFrame(data)


docx_files = list(INPUT_FOLDER.glob('*.docx'))

for docx_path in docx_files:
    if docx_path.name.startswith('~$'):
        print(f"Skipping temporary file: {docx_path.name}")
        continue
    print(f"\nProcessing: {docx_path.name}")
    doc = Document(docx_path)
    # Find all month-section headings and their indices
    headings = []
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if month_regex.match(text):
            headings.append((text, i))
    # Now, walk through the doc in block order and map tables to headings
    results = []
    current_heading = None
    table_count = 0
    heading_iter = iter(headings)
    next_heading = next(heading_iter, None)
    para_index = -1

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            para_index += 1
            if next_heading and para_index == next_heading[1]:
                current_heading = {
                    'heading': next_heading[0], 'index': next_heading[1], 'tables': []}
                results.append(current_heading)
                table_count = 0
                next_heading = next(heading_iter, None)
        elif isinstance(block, Table):
            if current_heading is not None and table_count < 6:
                current_heading['tables'].append(block)
                table_count += 1

    # Now merge split tables in each section
    for section in results:
        original_tables = section['tables']
        merged_tables = merge_tables(original_tables)
        section['tables'] = merged_tables
        print(
            f"Section: {section['heading']} (para idx {section['index']}), Merged tables: {len(merged_tables)}")

    # --- NEW BLOCK: Extract Table 2 from S&P 500 and Non-S&P 500 for each month ---
    # Group sections by month (should be in order: [S&P, Non-S&P, Options])
    month_sections = defaultdict(list)
    for section in results:
        month = section['heading']
        month_sections[month].append(section)
    print(
        f"  Found {len(headings)} month headings and {len(results)} sections in {docx_path.name}")

    # Make an output subfolder for this file
    file_out_folder = OUTPUT_PATH / docx_path.stem
    file_out_folder.mkdir(parents=True, exist_ok=True)

    for month, sections in month_sections.items():
        # Defensive: check if there are at least two sections
        if len(sections) < 2:
            print(f"Warning: {month} has less than 2 sections!")
            continue
        try:
            # Table 2 from S&P 500 section (sections[0]), Non-S&P 500 section (sections[1])
            s_and_p_table2 = sections[0]['tables'][1]  # Table 2 of S&P 500
            # Table 2 of Non-S&P 500
            non_s_and_p_table2 = sections[1]['tables'][1]
            # Convert to DataFrame
            df_sp = table_to_dataframe(s_and_p_table2)
            df_nonsp = table_to_dataframe(non_s_and_p_table2)
            csv_sp = file_out_folder / \
                f"{month.replace(' ', '_')}_SP500_Table2.csv"
            csv_nonsp = file_out_folder / \
                f"{month.replace(' ', '_')}_NonSP500_Table2.csv"
            df_sp.to_csv(csv_sp, index=False, header=False)
            df_nonsp.to_csv(csv_nonsp, index=False, header=False)
            print(f"  Saved: {csv_sp.name} and {csv_nonsp.name}")
        except Exception as e:
            print(f"  Could not extract tables for {month}: {e}")

    # (Existing code remains unaffected, optional previews still available!)
