"""Shared readers for ad-platform exports.

Every compute script used to re-derive the same parsing rules. They live here once:

  * Google Ads exports: UTF-16 with a BOM, tab-delimited. Row 1 is the report name,
    row 2 the embedded date range, row 3 the header. Use `read_google_tsv`, and trust
    the embedded range over the filename (it can disagree).
  * LinkedIn Campaign Manager exports: UTF-16 (sometimes UTF-8), tab-delimited, with
    about 5 preamble rows before the header. Use `read_linkedin`.
  * XLSX exports: loaded WITHOUT openpyxl's read_only mode, because some platforms
    declare a bogus `<dimension ref="A1">` that read_only trusts, which truncates the
    sheet to one row. Use `read_xlsx`.
  * Metric cells: "1,234", "$5.00", "12.3%", "--", "-" and blanks. Use `num`.

Footer rows ("Total", "Total of N results", "-" aggregates) are NOT dropped here,
because what counts as a footer differs by platform. Filter them in the caller;
`is_total_row` covers the Google/Bing `Month == "Total..."` case.
"""

from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

BLANK_CELLS = frozenset({"", "-", "--", "—", " --"})


def num(value) -> float:
    """Parse a metric cell to float. Blank, dash and unparseable cells become 0.0."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").replace("$", "").replace("%", "")
    if text in BLANK_CELLS:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def sniff_encoding(path: Path) -> str:
    """"utf-16" when the file starts with a UTF-16 BOM, else "utf-8-sig"."""
    with open(path, "rb") as probe:
        return "utf-16" if probe.read(2) in (b"\xff\xfe", b"\xfe\xff") else "utf-8-sig"


def _decode(path: Path) -> str:
    """Decode by BOM: UTF-16 when present, else UTF-8 (BOM stripped)."""
    return Path(path).read_bytes().decode(sniff_encoding(path))


def google_tsv_range(path: Path) -> str:
    """The date range embedded in row 2 of a Google Ads export."""
    return _decode(path).splitlines()[1].strip().strip('"')


def read_google_tsv(path: Path, expected_range: str | None = None) -> list[dict]:
    """Rows of a Google Ads UTF-16 TSV export (report name and range rows skipped).

    With `expected_range`, raise SystemExit when the embedded range differs, so a
    mislabelled file cannot flow into a report.
    """
    lines = _decode(path).splitlines()
    header_range = lines[1].strip().strip('"')
    if expected_range and header_range != expected_range:
        raise SystemExit(f"{Path(path).name}: embedded range {header_range!r} != {expected_range!r}")
    return list(csv.DictReader(io.StringIO("\n".join(lines[2:])), delimiter="\t"))


def is_total_row(row: dict, key: str = "Month") -> bool:
    """True for a footer/blank row: the period cell is empty, not a label, or "Total..."."""
    value = str(row.get(key) or "").strip()
    return not value or not value[0].isalpha() or value.startswith("Total")


def read_linkedin(path: Path) -> list[dict]:
    """Rows of a LinkedIn Campaign Manager export, preamble skipped.

    The header is the first tab-delimited line naming `Campaign Name`. Rows that are
    entirely blank (tabs only) are kept, so row counts match the file; they parse to
    empty cells, which `num` reads as zero.
    """
    rows, _, _ = read_linkedin_with_layout(path)
    return rows


def read_linkedin_with_layout(path: Path) -> tuple[list[dict], str, int]:
    """`read_linkedin` plus the detected encoding and header line index."""
    lines = _decode(path).splitlines()
    header_idx = next(
        (i for i, line in enumerate(lines) if "Campaign Name" in line and "\t" in line),
        0,
    )
    rows = list(csv.DictReader(io.StringIO("\n".join(lines[header_idx:])), delimiter="\t"))
    return rows, sniff_encoding(path), header_idx


def read_csv(path: Path, *, encoding: str = "utf-8-sig", delimiter: str = ",",
             skip_rows: int = 0) -> list[dict]:
    """Rows of a delimited export, optionally skipping preamble lines."""
    with open(path, encoding=encoding, newline="") as handle:
        stream = io.StringIO(handle.read())
    for _ in range(skip_rows):
        stream.readline()
    return list(csv.DictReader(stream, delimiter=delimiter))


def read_xlsx(path: Path, *, drop_empty: bool = True) -> list[dict]:
    """First worksheet as dicts (header row stripped of whitespace).

    Never uses read_only mode (see module docstring). `drop_empty` removes rows whose
    every cell is None or "".
    """
    import openpyxl

    sheet = openpyxl.load_workbook(path, read_only=False, data_only=True).worksheets[0]
    rows = sheet.iter_rows(values_only=True)
    try:
        header = [str(cell).strip() if cell is not None else "" for cell in next(rows)]
    except StopIteration:
        return []
    out = []
    for row in rows:
        if drop_empty and not any(v not in (None, "") for v in row):
            continue
        out.append(dict(zip(header, row)))
    return out


STDOUT_TARGETS = ("-", "/dev/stdout")


def log_stream(out):
    """Where a CLI prints its summary: stderr when `-o` sends the JSON to stdout."""
    return sys.stderr if out in STDOUT_TARGETS else sys.stdout


def write_json(obj, out) -> Path | None:
    """Write metrics JSON for a CLI's `-o`: stdout for `-`, else a file (parents made).

    Returns the path written, or None when nothing was written or it went to stdout.
    """
    if not out:
        return None
    if out in STDOUT_TARGETS:
        sys.stdout.write(json.dumps(obj, indent=2) + "\n")
        return None
    path = Path(out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))
    return path


def read_tabular(path: Path, *, encoding: str = "utf-8-sig", delimiter: str = ",",
                 drop_empty: bool = True) -> list[dict]:
    """CSV or XLSX by extension; platforms switch formats between pulls."""
    if Path(path).suffix.lower() in (".xlsx", ".xlsm"):
        return read_xlsx(path, drop_empty=drop_empty)
    return read_csv(path, encoding=encoding, delimiter=delimiter)
