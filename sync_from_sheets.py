#!/usr/bin/env python3
"""
sync_from_sheets.py — Fetch the parallel-algorithms Google Sheet and
compare against the local JSON data files.

Usage:
    python3 sync_from_sheets.py            # report only (no files changed)
    python3 sync_from_sheets.py --update   # also download CSVs for converter

Spreadsheet: https://docs.google.com/spreadsheets/d/1c6HTfHQfp7MIg1LFo6_wFOzKLIHA1rzVpDxXIPosRQ0/edit

Sheet GIDs:
  gid=867359064   → "Parallel Algos"        (792 rows, the correct parallel sheet)
  gid=0           → "Sheet1"                (sequential algorithms, ~998 rows)
  gid=1737371097  → "New Entries to Sheet 1" (additional sequential, ~274 rows)
"""

import csv, io, json, os, re, sys, urllib.request
from collections import Counter
from datetime import date

# ── configuration ──────────────────────────────────────────────────────────────
SHEET_ID = "1c6HTfHQfp7MIg1LFo6_wFOzKLIHA1rzVpDxXIPosRQ0"
PAR_GID      = "867359064"    # "Parallel Algos"
SEQ_GID      = "0"            # "Sheet1"
SEQ_NEW_GID  = "1737371097"   # "New Entries to Sheet 1"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# ── Parallel Algos (gid=867359064) column names ────────────────────────────────
# 3 debugging columns inserted at positions 3-5 vs JAN23 CSV, but DictReader
# uses names so they are irrelevant for the column-name-based fields below.
# These are the exact column names as they appear in the sheet header.
PAR_FAMILY    = "Old Family #"
PAR_LOOKED    = "Looked at?"
PAR_SUB       = "Subproblem"
PAR_VAR       = "Variation"
PAR_ID        = "Algo ID"
PAR_AUTH      = "Algorithm Name"
PAR_YEAR      = "Year"
PAR_SPAN_ENC  = "Span Encoding (T_1)"   # matches converter.py PARALLEL_ALGO_FIELDS
PAR_WORK_ENC  = "Work Encoding (T_inf)" # matches converter.py PARALLEL_ALGO_FIELDS
PAR_MODEL_ENC = "Model Encoding"
PAR_RAND      = "Randomized?"
PAR_APPROX    = "Approximate?"
PAR_HEUR      = "Heuristic-based?"
PAR_PARALLEL  = "Parallel?"
PAR_PROC_ENC  = "# of\nProcessors"    # NOTE: column is actually "# of Proc Encoding" in some versions
PAR_PROC_ENC2 = "# of Proc Encoding"  # fallback
PAR_QUANTUM   = "Quantum?"
PAR_GPU       = "GPU-based?"
PAR_DOMAIN    = "Domains"

# ── Sequential Algos column names (shared between Sheet1 and New Entries) ──────
SEQ_FAMILY  = "Family Name"
SEQ_LOOKED  = "Looked at?"
SEQ_VAR     = "Variation"
SEQ_ID      = "Algo ID"
SEQ_AUTH    = "Algorithm Name"
SEQ_YEAR    = "Year"
SEQ_TIME_ENC= "Time Encoding"
SEQ_RAND    = "Randomized?"
SEQ_APPROX  = "Approximate?"
SEQ_HEUR    = "Heuristic-based?"
SEQ_PAR     = "Parallel?"
SEQ_QUANTUM = "Quantum?"
SEQ_GPU     = "GPU-based?"
SEQ_DOMAIN  = "Domains"

BAD_ENC = {"", "xxxx", "xxx", "yy", " ", "-"}
# ───────────────────────────────────────────────────────────────────────────────


def fetch_csv(gid: str) -> list[dict]:
    """Return rows as list-of-dicts using DictReader (column-name-based)."""
    url = (f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
           f"/export?format=csv&gid={gid}")
    with urllib.request.urlopen(url, timeout=30) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(text)))


def fetch_raw_csv(gid: str) -> str:
    """Return raw CSV text for saving to disk."""
    url = (f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
           f"/export?format=csv&gid={gid}")
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def s(row: dict, *keys) -> str:
    """Get first non-empty value from row by trying each key in order."""
    for k in keys:
        v = row.get(k, "").strip()
        if v:
            return v
    return ""


def norm_auth(a: str) -> str:
    """Normalize author/algorithm name for comparison."""
    a = str(a).strip().lower()
    a = re.sub(r"\s*\(\d+\)\s*$", "", a)  # remove trailing "(1)", "(2)"
    return a.strip()


# ── load local JSON files ──────────────────────────────────────────────────────
def load_latest_json(prefix: str) -> list[dict]:
    candidates = sorted(
        [f for f in os.listdir(DATA_DIR) if re.match(rf"{prefix}.*\.json$", f)],
        reverse=True,
    )
    if not candidates:
        return []
    path = os.path.join(DATA_DIR, candidates[0])
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    print(f"  Loaded {path} ({len(data)} entries)")
    return data


# ── parallel filtering (mirrors PARALLEL_DISCARABLE_FIELD_VALUES) ──────────────
def par_is_complete(row: dict) -> bool:
    proc_enc = s(row, PAR_PROC_ENC, PAR_PROC_ENC2)
    return (
        s(row, PAR_SUB) not in ("", "#N/A")
        and s(row, PAR_AUTH)
        and s(row, PAR_YEAR)
        and s(row, PAR_SPAN_ENC) not in BAD_ENC
        and s(row, PAR_WORK_ENC) not in BAD_ENC
        and s(row, PAR_MODEL_ENC) not in ("", " ")
        and s(row, PAR_PARALLEL) not in ("0", "", " ")
        and proc_enc not in ("", " ")
        and s(row, PAR_APPROX)  != "1"
        and s(row, PAR_HEUR)    != "1"
        and s(row, PAR_QUANTUM) != "1"
        and s(row, PAR_GPU)     != "1"
    )


# ── sequential filtering (mirrors SEQUENTIAL_DISCARABLE_FIELD_VALUES) ──────────
def seq_is_complete(row: dict) -> bool:
    return (
        s(row, SEQ_AUTH)
        and s(row, SEQ_YEAR)
        and s(row, SEQ_TIME_ENC) not in BAD_ENC
        and s(row, SEQ_PAR)     != "1"
        and s(row, SEQ_APPROX)  != "1"
        and s(row, SEQ_HEUR)    != "1"
        and s(row, SEQ_QUANTUM) != "1"
        and s(row, SEQ_GPU)     != "1"
    )


# ── main report ────────────────────────────────────────────────────────────────
def run_report(par_rows, seq_rows, seq_new_rows,
               par_json: list[dict], seq_json: list[dict]):

    # Build JSON key sets for matching
    par_json_keys = {(norm_auth(e["auth"]), str(e["year"])) for e in par_json}
    seq_json_keys = {(str(e["auth"]).strip().lower(), str(e["year"])) for e in seq_json}

    # ── Parallel ──────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("PARALLEL ALGORITHMS — Parallel Algos sheet vs local MAY1 JSON")
    print("=" * 70)

    par_complete = [r for r in par_rows if par_is_complete(r)]
    par_new = [r for r in par_complete
               if (norm_auth(s(r, PAR_AUTH)), s(r, PAR_YEAR)) not in par_json_keys]
    par_in_json = [r for r in par_complete
                   if (norm_auth(s(r, PAR_AUTH)), s(r, PAR_YEAR)) in par_json_keys]

    # Entries in JSON not found in sheet
    sheet_par_keys = {(norm_auth(s(r, PAR_AUTH)), s(r, PAR_YEAR)) for r in par_rows}
    json_missing = [(norm_auth(e["auth"]), str(e["year"]), e["auth"])
                    for e in par_json
                    if (norm_auth(e["auth"]), str(e["year"])) not in sheet_par_keys]

    print(f"\nParallel Algos sheet:                 {len(par_rows)} rows")
    print(f"  Complete (all encodings filled):    {len(par_complete)}")
    print(f"  Matching MAY1 JSON:                 {len(par_in_json)}")
    print(f"  NEW — complete & not in MAY1 JSON:  {len(par_new)}")
    print(f"  MAY1 JSON entries not in sheet:     {len(json_missing)}")

    # Rows with span encoding but still incomplete (needs proc encoding, subproblem, etc.)
    has_span = [r for r in par_rows
                if s(r, PAR_SPAN_ENC) not in BAD_ENC
                and s(r, PAR_WORK_ENC) not in BAD_ENC]
    print(f"\nWith span+work encoding (any completeness): {len(has_span)}")
    missing_span = [r for r in par_rows
                    if s(r, PAR_SPAN_ENC) in BAD_ENC or s(r, PAR_WORK_ENC) in BAD_ENC]
    fam_dist = Counter(s(r, "Family Name") for r in missing_span)
    print(f"Without span/work encoding (needs data entry): {len(missing_span)}")
    print("  Top families needing encoding:")
    for fam, cnt in fam_dist.most_common(10):
        print(f"    {cnt:3d}  {fam}")

    if par_new:
        print(f"\n{'─'*60}")
        print(f"NEW COMPLETE PARALLEL ENTRIES ({len(par_new)}) — ready to add:")
        print(f"{'─'*60}")
        for r in sorted(par_new, key=lambda r: s(r, PAR_YEAR)):
            print(f"  [{s(r,PAR_YEAR)}] {s(r,'Family Name')} / {s(r,PAR_SUB)}"
                  f" — {s(r,PAR_AUTH)}"
                  f"  span={s(r,PAR_SPAN_ENC)} work={s(r,PAR_WORK_ENC)}"
                  f" model={s(r,PAR_MODEL_ENC)}")

    if json_missing:
        print(f"\n{'─'*60}")
        print(f"MAY1 JSON ENTRIES NOT FOUND IN SHEET ({len(json_missing)}):")
        print(f"{'─'*60}")
        for _,year,auth in sorted(json_missing, key=lambda x: x[1]):
            print(f"  [{year}] {auth}")

    # ── Sequential ────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SEQUENTIAL ALGORITHMS — Sheet1 + New Entries vs local MAY1 JSON")
    print("=" * 70)

    seq1_complete = [r for r in seq_rows if seq_is_complete(r)]
    seq2_complete = [r for r in seq_new_rows if seq_is_complete(r)]

    seq1_new = [r for r in seq1_complete
                if (s(r, SEQ_AUTH).lower(), s(r, SEQ_YEAR)) not in seq_json_keys]
    seq2_new = [r for r in seq2_complete
                if (s(r, SEQ_AUTH).lower(), s(r, SEQ_YEAR)) not in seq_json_keys]

    print(f"\nSheet1 (gid=0):                       {len(seq_rows)} rows")
    print(f"  Complete after filter:              {len(seq1_complete)}")
    print(f"  Matching MAY1 seq JSON:             {len(seq1_complete)-len(seq1_new)}")
    print(f"  NEW — not in MAY1 seq JSON:         {len(seq1_new)}")

    print(f"\nNew Entries to Sheet 1 (gid=1737371097): {len(seq_new_rows)} rows")
    print(f"  Complete after filter:              {len(seq2_complete)}")
    print(f"  Matching MAY1 seq JSON:             {len(seq2_complete)-len(seq2_new)}")
    print(f"  NEW — not in MAY1 seq JSON:         {len(seq2_new)}")

    print(f"\nMAY1 seq JSON:                        {len(seq_json)} entries")
    total_new_seq = len(set(
        (s(r, SEQ_AUTH).lower(), s(r, SEQ_YEAR)) for r in seq1_new + seq2_new
    ))
    print(f"Total NEW seq entries (combined):     {total_new_seq}")

    return par_new, seq1_new, seq2_new


# ── main ───────────────────────────────────────────────────────────────────────
def main():
    update_mode = "--update" in sys.argv

    print("Fetching Parallel Algos sheet (gid=867359064)...")
    par_rows = fetch_csv(PAR_GID)
    print(f"  {len(par_rows)} rows")

    print("Fetching Sheet1 / sequential (gid=0)...")
    seq_rows = fetch_csv(SEQ_GID)
    print(f"  {len(seq_rows)} rows")

    print("Fetching New Entries to Sheet 1 (gid=1737371097)...")
    seq_new_rows = fetch_csv(SEQ_NEW_GID)
    print(f"  {len(seq_new_rows)} rows")

    print("\nLoading local JSON files...")
    par_json = load_latest_json(r"par_algos_original")
    seq_json = load_latest_json(r"seq_data")

    par_new, seq1_new, seq2_new = run_report(
        par_rows, seq_rows, seq_new_rows, par_json, seq_json
    )

    if update_mode:
        today = date.today().strftime("%b%d").upper()   # e.g. "MAR21"
        print("\n" + "=" * 70)
        print(f"UPDATE MODE — Saving CSVs with date tag '{today}'")
        print("=" * 70)

        raw_par = fetch_raw_csv(PAR_GID)
        raw_seq = fetch_raw_csv(SEQ_GID)
        raw_new = fetch_raw_csv(SEQ_NEW_GID)

        par_csv_path = os.path.join(DATA_DIR, f"Parallel_Algos_{today}.csv")
        seq_csv_path = os.path.join(DATA_DIR, f"Sheet1_{today}.csv")
        new_csv_path = os.path.join(DATA_DIR, f"Sheet1_New_Entries_{today}.csv")

        for path, content in [(par_csv_path, raw_par),
                               (seq_csv_path, raw_seq),
                               (new_csv_path, raw_new)]:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(content)
            print(f"  Saved: {path}")

        print(f"\nNext steps:")
        print(f"  1. Update VERSION = '_{today}' in src/processed_data.py")
        print(f"  2. Update SAVE_LOC = 'Plots/{today} data/' in header.py")
        print(f"  3. Create the output directory:")
        print(f"       mkdir -p 'Plots/{today} data/'")
        print(f"  4. Run the converter:")
        print(f"       python3 -c \"")
        print(f"         from converter import create_par_data, create_seq_data")
        print(f"         create_par_data('data/Parallel_Algos_{today}')")
        print(f"         create_seq_data('data/Sheet1_{today}', 'data/Sheet1_New_Entries_{today}')\"")
        print(f"  5. Run: python3 main.py")

    print("\nDone.")


if __name__ == "__main__":
    main()
