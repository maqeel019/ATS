# extractor/info_extractor.py
import re
from typing import Tuple, List
import os
from datetime import datetime
from config import _MONTH_MAP
from dateutil.relativedelta import relativedelta
from extractor.section_segmenter import segment_sections  # make sure this is imported

_NUM_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20,
    "half": 0.5
}


def extract_years_months(exp_str):
    parts = exp_str.strip().lower().split()
    years = 0
    months = 0

    if len(parts) >= 2:
        if "year" in parts[1]:
            years = int(parts[0])
    if len(parts) >= 4:
        if "month" in parts[3]:
            months = int(parts[2])

    # Handle cases like "6 months" (no years part)
    if len(parts) == 2 and "month" in parts[1]:
        months = int(parts[0])

    return years, months


def extract_experience_from_text(text: str):
    text = text.lower()

    patterns = [
        re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:to\s*\d+)?\s*(?:years?|yrs?)"),
        re.compile(r"over\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)"),
        re.compile(r"(\d+)\s*(?:months?)\s*(?:of\s+)?(?:[a-z\s]{0,10})\s*(?:experience|work)"),
        re.compile(r"(?:over|around|approximately|nearly|about)?\s*([a-z\- ]+)\s*(?:years?|yrs?)")
    ]


    for pattern in patterns:
        match = pattern.search(text)
        if match:
            if pattern.pattern.endswith("months?)"):
                months = int(match.group(1))
                return 0, months, "summary"

            raw = match.group(1).strip()
            if raw.replace(".", "", 1).isdigit():
                value = float(raw)
            else:
                # Try word → number conversion
                words = raw.replace("-", " ").split()
                value = 0
                for word in words:
                    word = word.strip()
                    if word in _NUM_WORDS:
                        value += _NUM_WORDS[word]
                if value == 0:
                    continue  # If no match, skip

            years = int(value)
            months = round((value - years) * 12)
            return years, months, "summary"

    return 0, 0, "none"


def normalize_text(text: str) -> str:
    text = text.lower()
    # Replace bracketed text
    text = re.sub(r"[\[\(]{1}\s*(.*?)\s*[\]\)]", r"\1", text)
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"-{2,}", "-", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)

    # 📌 NEW: replace non-breaking spaces & invisible
    text = text.replace("\xa0", " ").replace("\u200b", " ")
    text = re.sub(r"[^\S\r\n]+", " ", text)  # multiple non-breaking = space

    return text.strip()


def merge_date_ranges(ranges: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:

    if not ranges:
        return []

    # Auto-fix any inverted (start > end)
    fixed_ranges = []
    for start, end in ranges:
        if start > end:
            start, end = end, start
        fixed_ranges.append((start, end))

    sorted_ranges = sorted(fixed_ranges, key=lambda r: r[0])
    merged = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        curr_start, curr_end = current

        # If current starts before last ends, or within 1 month gap, merge
        if curr_start <= last_end or curr_start <= last_end + relativedelta(days=5):
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
        (re.compile(
            r"(\d{4})\s+(\d{4})",
            re.IGNORECASE
        ), "year-only-space"),
        # Add this pattern too:
        (re.compile(
            r"(\d{4})[^\d]{1,5}(\d{4})",
            re.IGNORECASE
        ), "year-only-fuzzy")

    ]

    for pattern, tag in patterns:
        for match in pattern.finditer(text):
            try:
                if tag == "month-name + year-only":
                    sm, sy, pres, em, ey = match.groups()
                    start = datetime(int(sy), _MONTH_MAP[sm.lower()], 1)
                    end = now if pres.lower() in ("present", "now", "current",
                                                  "continue") else datetime(int(ey), _MONTH_MAP[em.lower()], 1)
                elif tag == "reverse-order":
                    sy, sm, end_token, _ = match.groups()
                    start = datetime(int(sy), _MONTH_MAP[sm.lower()], 1)
                    end = now if end_token.lower() in ("present", "now", "current", "continue") else datetime(
                        int(end_token.split()[0]), _MONTH_MAP[end_token.split()[1].lower()], 1)
                elif tag == "mm/yyyy":
                    m1, y1, end_token, m2, y2 = match.groups()
                    start = datetime(int(y1), int(m1), 1)
                    end = now if end_token.lower() in ("present", "now", "current",
                                                       "continue") else datetime(int(y2), int(m2), 1)
                elif tag == "month-only + year":
                    sm, em, year = match.groups()
                    start = datetime(int(year), _MONTH_MAP[sm.lower()], 1)
                    end = datetime(int(year), _MONTH_MAP[em.lower()], 1)
                elif tag == "year-only-fuzzy":
                    sy, ey = match.groups()
                    start = datetime(int(sy), 1, 1)
                    end = datetime(int(ey), 1, 1)
                elif tag == "fuzzy-month":
                    sm, sy, em, ey = match.groups()
                    start = datetime(int(sy), _MONTH_MAP[sm.lower()], 1)
                    end = datetime(int(ey), _MONTH_MAP[em.lower()], 1)
                else:  # year-only
                    sy, end_token = match.groups()
                    start = datetime(int(sy), 1, 1)
                    end = now if end_token.lower() in ("present", "now", "current",
                                                       "continue") else datetime(int(end_token), 1, 1)

                # ✅ Stronger checks:
                if start > now:
                    continue
                if end > now:
                    end = now
                if end <= start:
                    continue

                months = (end.year - start.year) * \
                    12 + (end.month - start.month)
                if months > 480:  # 40 years? Unlikely!
                    continue

                date_ranges.append((start, end))
                used_patterns.add(tag)

            except Exception as e:
                print(f"⚠️ Pattern {tag} failed: {e}")
                continue

    if not date_ranges:
        return (0, 0), "none"

    cleaned = filter_education_like_ranges(date_ranges, education_date_ranges)
    merged = merge_date_ranges(cleaned)
    total_months = sum((end.year - start.year) * 12 +
                       (end.month - start.month) for start, end in merged)
    return divmod(total_months, 12), " + ".join(sorted(used_patterns))


def extract_experience(text: str) -> Tuple[int, int, str, str]:
    # 1) Try explicit summary statement
    years, months, summary_method = extract_experience_from_text(text)
    if years > 0 or months > 0:
        return years, months, "summary", summary_method

    # 2) Fallback: date ranges
    sections = segment_sections(text)
    experience_text = sections.get("experience", "")
    if experience_text:
        (y2, m2), range_method = extract_experience_ranges(experience_text)
        if y2 > 0 or m2 > 0:
            return y2, m2, "date_range", range_method

    # 3) Nothing found
    return 0, 0, "none", "none"
