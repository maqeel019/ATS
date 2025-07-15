# extractor/info_extractor.py
import re
from typing import Tuple, List
import os
from datetime import datetime
from config import _MONTH_MAP
from dateutil.relativedelta import relativedelta
from extractor.section_segmenter import segment_sections  # make sure this is imported


def extract_years_months(exp_str):
    parts = exp_str.strip().split()
    years = int(parts[0]) if "year" in parts[1] else 0
    months = int(parts[2]) if len(parts) > 2 and "month" in parts[3] else 0
    return years, months


def extract_experience_from_text(text: str) -> Tuple[int, int, str]:
    text = text.lower()
    # Common patterns for experience or work‑years
    patterns = [
        # 4+ years of (optional work) experience
        re.compile(
            r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)"
            r"(?:\s*of\s*(?:work\s*)?)?"
            r"(?:experience)?",
            re.IGNORECASE
        ),
        re.compile(
            r"have\s*(\d+(?:\.\d+)?)\s*\+?\s*years?(?:\s*of\s*work)?", re.IGNORECASE),
    ]

    for pattern in patterns:
        match = pattern.search(text)
        if match:
            years = float(match.group(1))
            y_int = int(years)
            months = round((years - y_int) * 12)
            return y_int, months, "summary"

    return 0, 0, "none"


# def extract_experience_from_logs(logs_dir: str) -> dict:
#     """
#     Loop through all .txt log files in the specified directory,
#     extract experience from each, and return a mapping of filename to experience.
#     """
#     experience_map = {}
#     for filename in os.listdir(logs_dir):
#         if filename.endswith(".txt"):
#             log_path = os.path.join(logs_dir, filename)
#             with open(log_path, "r", encoding="utf-8") as f:
#                 content = f.read()
#                 years, months, method = extract_experience_from_text(content)
#                 experience_map[filename] = (years, months, method)
#     return experience_map


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\[\(]{1}\s*(.*?)\s*[\]\)]", r"\1", text)
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"-{2,}", "-", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def merge_date_ranges(ranges: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    if not ranges:
        return []
    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    merged = [sorted_ranges[0]]
    for current in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        curr_start, curr_end = current
        if curr_start <= last_end or curr_start <= last_end + relativedelta(months=1):
            merged[-1] = (last_start, max(last_end, curr_end))
        else:
            merged.append(current)
    return merged


def filter_education_like_ranges(
    work_ranges: List[Tuple[datetime, datetime]],
    edu_ranges: List[Tuple[datetime, datetime]]
) -> List[Tuple[datetime, datetime]]:
    """
    Filters work date ranges:
    - Removes overlap with any education range.
    - Removes if span is exactly 4 years.
    - Removes if exact month/year pair exists in education.
    """
    result = []

    def same_month_year(d1, d2):
        return d1.year == d2.year and d1.month == d2.month

    for ws, we in work_ranges:
        keep = True

        for es, ee in edu_ranges:
            # 1) Drop if overlaps
            if max(ws, es) <= min(we, ee):
                keep = False
                break

            # 2) Drop if start & end month/year match
            if same_month_year(ws, es) and same_month_year(we, ee):
                keep = False
                break

        # 3) Drop if exactly 4 years long
        if (we.year - ws.year) == 4:
            keep = False

        if keep:
            result.append((ws, we))

    return result


def extract_experience_ranges(
    text: str,
    education_date_ranges: List[Tuple[datetime, datetime]] = []
) -> Tuple[Tuple[int, int], str]:
    now = datetime.now()
    text = normalize_text(text)
    date_ranges: List[Tuple[datetime, datetime]] = []
    used_patterns = set()

    patterns = [
        # Month-name + year
        (re.compile(
            rf"({'|'.join(_MONTH_MAP.keys())})\.?\s*(\d{{4}})\s*[-–—]\s*"
            rf"(present|now|current|continue|({'|'.join(_MONTH_MAP.keys())})\.?\s*(\d{{4}}))",
            re.IGNORECASE
        ), "month-name + year-only"),

        # Year first: 2024 April - Present
        (re.compile(
            rf"(\d{{4}})\s+({'|'.join(_MONTH_MAP.keys())})\s*[-–—]\s*"
            rf"(present|now|current|continue|\d{{4}}\s+({'|'.join(_MONTH_MAP.keys())}))",
            re.IGNORECASE
        ), "reverse-order"),

        # MM/YYYY
        (re.compile(
            r"(\d{1,2})/(\d{4})\s*[-–—]\s*(present|now|current|continue|(\d{1,2})/(\d{4}))",
            re.IGNORECASE
        ), "mm/yyyy"),

        # Month–Month Year
        (re.compile(
            rf"({'|'.join(_MONTH_MAP.keys())})\s*[-–—]\s*({'|'.join(_MONTH_MAP.keys())})\s+(\d{{4}})",
            re.IGNORECASE
        ), "month-only + year"),

        # Fuzzy (Mar 2023 – Mar ... 2024)
        (re.compile(
            rf"({'|'.join(_MONTH_MAP.keys())})\s+(\d{{4}})\s*[-–—]\s*"
            rf"({'|'.join(_MONTH_MAP.keys())})[^\d]*(\d{{4}})",
            re.IGNORECASE
        ), "fuzzy-month"),

        # Year-only: 2020 – 2024
        (re.compile(
            r"(\d{4})\s*[-–—]\s*(present|now|current|continue|\d{4})",
            re.IGNORECASE
        ), "year-only"),
    ]

    for pattern, tag in patterns:
        for match in pattern.finditer(text):
            try:
                if tag == "month-name + year-only":
                    sm, sy, pres, em, ey = match.groups()
                    start = datetime(int(sy), _MONTH_MAP[sm.lower()], 1)
                    end = (
                        datetime(now.year, now.month, 1)
                        if pres.lower() in ("present", "now", "current", "continue")
                        else datetime(int(ey), _MONTH_MAP[em.lower()], 1)
                    )
                elif tag == "reverse-order":
                    sy, sm, end_token, _ = match.groups()
                    start = datetime(int(sy), _MONTH_MAP[sm.lower()], 1)
                    if end_token.lower() in ("present", "now", "current", "continue"):
                        end = datetime(now.year, now.month, 1)
                    else:
                        ey, em = end_token.split()
                        end = datetime(int(ey), _MONTH_MAP[em.lower()], 1)
                elif tag == "mm/yyyy":
                    m1, y1, end_token, m2, y2 = match.groups()
                    start = datetime(int(y1), int(m1), 1)
                    if end_token.lower() in ("present", "now", "current", "continue"):
                        end = datetime(now.year, now.month, 1)
                    else:
                        end = datetime(int(y2), int(m2), 1)
                elif tag == "month-only + year":
                    sm, em, year = match.groups()
                    start = datetime(int(year), _MONTH_MAP[sm.lower()], 1)
                    end = datetime(int(year), _MONTH_MAP[em.lower()], 1)
                elif tag == "fuzzy-month":
                    sm, sy, em, ey = match.groups()
                    start = datetime(int(sy), _MONTH_MAP[sm.lower()], 1)
                    end = datetime(int(ey), _MONTH_MAP[em.lower()], 1)
                else:  # year-only
                    sy, end_token = match.groups()
                    start = datetime(int(sy), 1, 1)
                    if end_token.lower() in ("present", "now", "current", "continue"):
                        end = datetime(now.year, now.month, 1)
                    else:
                        end = datetime(int(end_token), 1, 1)

                if end > start:
                    date_ranges.append((start, end))
                    used_patterns.add(tag)

            except Exception:
                continue

    if not date_ranges:
        return (0, 0), "none"

    # 🗑️ Clean overlaps with education & long gaps
    cleaned = filter_education_like_ranges(date_ranges, education_date_ranges)

    merged = merge_date_ranges(cleaned)
    total_months = sum(
        (end.year - start.year) * 12 + (end.month - start.month)
        for start, end in merged
    )
    return divmod(total_months, 12), " + ".join(sorted(used_patterns))


def extract_experience(text: str, log_path: str = None) -> Tuple[int, int, str, str]:
    # 1) Try explicit statement in text
    years, months, summary_method = extract_experience_from_text(text)
    if years > 0 or months > 0:
        return years, months, "summary", summary_method

    # 2) Try explicit statement in log file (optional)
    if log_path and os.path.exists(log_path):
        for filename in os.listdir(log_path):
            if filename.endswith(".txt"):
                with open(os.path.join(log_path, filename), "r", encoding="utf-8") as f:
                    log_content = f.read()
                y, m, log_method = extract_experience_from_text(log_content)
                if y > 0 or m > 0:
                    return y, m, "logs", log_method

    # 3) Extract date range ONLY from experience section
    sections = segment_sections(text)
    experience_text = sections.get("experience", "")
    if experience_text:
        (y2, m2), range_method = extract_experience_ranges(experience_text)
        if y2 > 0 or m2 > 0:
            return y2, m2, "date_range", range_method

    # 4) Nothing found
    return 0, 0, "none", "none"
