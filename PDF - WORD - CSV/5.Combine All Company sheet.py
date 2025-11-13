#!/usr/bin/env python3
import os
import sys
import re
import time
import argparse
import logging
import logging.handlers
from typing import List
import pandas as pd
import numpy as np

# =================== EDIT THESE TWO LINES ===================
INPUT_FOLDER = r"C:\RA work\SEC Rule 606 Datasets\1_Final_Kavin\Final\Combined"
OUTPUT_FOLDER = r"C:\RA work\SEC Rule 606 Datasets\1_Final_Kavin\Final\Combined"
OUTPUT_FILENAME = "Combined.xlsx"
SHEET_NAME = "Combined"
# ============================================================


def natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def list_csvs(folder: str):
    files = [f for f in os.listdir(folder) if f.lower().endswith(".csv")]
    files.sort(key=natural_key)
    return files


def read_csv_robust(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path, dtype=str, keep_default_na=True)
    except Exception:
        return pd.read_csv(path, dtype=str, keep_default_na=True, engine="python")


def trim_at_first_blank_row(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    # blank = all cells NA or whitespace
    is_na = df.isna()
    stripped_empty = df.astype(str).apply(
        lambda c: c.str.strip().eq(""), axis=0)
    row_blank = (is_na | stripped_empty).all(axis=1)
    if row_blank.any():
        pos = np.argmax(row_blank.to_numpy())
        return df.iloc[:pos]
    return df


def setup_logger(out_path: str) -> logging.Logger:
    log_dir = os.path.dirname(out_path) or "."
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(
        log_dir, f"combine_{time.strftime('%Y%m%d-%H%M%S')}.log")

    logger = logging.getLogger("combiner")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "[%(asctime)s] %(message)s", datefmt="%H:%M:%S"))

    fh = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=5_000_000, backupCount=2, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s - %(message)s"))

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.info(f"Log file: {log_path}")
    return logger


def combine(folder: str, output_xlsx: str, sheet_name: str, logger: logging.Logger):
    t0 = time.perf_counter()
    if not os.path.isdir(folder):
        logger.error(f"Folder not found: {folder}")
        sys.exit(1)

    csvs = list_csvs(folder)
    if not csvs:
        logger.error("No CSV files found in the folder.")
        sys.exit(1)

    logger.info(f"Folder: {folder}")
    logger.info(f"Found {len(csvs)} CSV file(s).")
    base_path = os.path.join(folder, csvs[0])
    logger.info(f"Base file (kept as-is): {csvs[0]}")

    t = time.perf_counter()
    base = read_csv_robust(base_path)
    logger.info(
        f"Read base: {len(base):,} row(s) in {time.perf_counter()-t:.2f}s")

    append_parts: List[pd.DataFrame] = []
    total_to_append = len(csvs) - 1
    total_appended_rows = 0

    for i, name in enumerate(csvs[1:], start=1):
        path = os.path.join(folder, name)
        start = time.perf_counter()
        try:
            df = read_csv_robust(path)
        except Exception as e:
            logger.warning(
                f"[{i}/{total_to_append}] SKIP {name}: read error -> {e}")
            continue

        rows_before = len(df)
        df = trim_at_first_blank_row(df)     # “till before null”
        rows_after = len(df)

        # Align columns to base schema (drop extras, add missing)
        df = df.reindex(columns=base.columns, fill_value=pd.NA)

        if not df.empty:
            append_parts.append(df)
            total_appended_rows += len(df)

        elapsed = time.perf_counter() - start
        logger.info(
            f"[{i}/{total_to_append}] {name} | read={rows_before:,} -> trimmed={rows_after:,} -> appended={len(df):,} | {elapsed:.2f}s")

    combined = pd.concat([base] + append_parts,
                         ignore_index=True) if append_parts else base

    os.makedirs(os.path.dirname(output_xlsx) or ".", exist_ok=True)
    logger.info(f"Writing Excel → {output_xlsx} (sheet='{sheet_name}')")
    t = time.perf_counter()
    with pd.ExcelWriter(output_xlsx, engine="openpyxl") as xw:
        combined.to_excel(xw, index=False, sheet_name=sheet_name)
    logger.info(f"Wrote Excel in {time.perf_counter()-t:.2f}s")

    logger.info("----- Summary -----")
    logger.info(f"Files processed: {len(csvs)} (appended {total_to_append})")
    logger.info(f"Rows appended: {total_appended_rows:,}")
    logger.info(f"Final total rows: {len(combined):,}")
    logger.info(f"Total time: {time.perf_counter()-t0:.2f}s")


def parse_args(default_input: str, default_output: str, default_sheet: str):
    p = argparse.ArgumentParser(
        description="Combine CSVs: keep first as-is, append data rows from others."
    )
    p.add_argument("-i", "--input", default=default_input,
                   help="Folder containing CSV files")
    p.add_argument("-o", "--output", default=default_output,
                   help="Output Excel path (e.g., combined.xlsx)")
    p.add_argument("-s", "--sheet", default=default_sheet,
                   help="Sheet name (default: Combined)")
    return p.parse_args()


if __name__ == "__main__":
    # Build default output path from OUTPUT_FOLDER + OUTPUT_FILENAME
    default_out_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
    args = parse_args(INPUT_FOLDER, default_out_path, SHEET_NAME)

    logger = setup_logger(args.output)
    try:
        combine(args.input, args.output, args.sheet, logger)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
