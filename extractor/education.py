from .section_segmenter import segment_sections
import re
from config import _DEGREE_KEYWORDS

_CONTEXT_CLUES = [
    "university", "college", "school","higher" ,"institute", "academy",
    "faculty", "degree", "diploma", "hssc", "matric",
    "intermediate", "certificate"
]

def extract_all_degrees(text: str) -> list:
    """
    Extract all lines containing ANY known degree keyword
    plus fallback for 'Bachelor/Master/PhD/Diploma/Intermediate' phrases.
    """
    secs = segment_sections(text)
    edu_block = secs.get("education", "")
    if not edu_block:
        edu_block = text

    found = []
    lines = [line.strip() for line in edu_block.splitlines() if line.strip()]

    # Fallback phrase pattern: Bachelor, Master, PhD, Diploma, Intermediate, Matric
    fallback_pattern = re.compile(
        r"\b("
        r"(bachelor|master|ph\.?d\.?|doctor|mba|m\.?s\.?c?|b\.?s\.?c?|b\.?tech|b\.?e\.?|m\.?tech|m\.?e\.?|diploma|polytechnic|intermediate|matric|ssc|hsc|12th|10th)"
        r")\b",
        re.IGNORECASE
    )

    for line in lines:
        low = line.lower()
        keyword_hit = any(k in low for k in _DEGREE_KEYWORDS)
        fallback_hit = fallback_pattern.search(line)

        if keyword_hit or fallback_hit:
            found.append(line)

    return found

def extract_highest_education(text: str) -> str:
    """
    Returns the highest-ranked degree actually present.
    Tries: education section → fallback in other sections → fallback in whole text.
    Picks highest: PhD > Master > Bachelor > Diploma > Intermediate > Matric.
    """
    secs = segment_sections(text)
    edu_block = secs.get("education", "").strip()

    if not edu_block:
        # 🔄 Fallback: look in other logical blocks too
        for sec in ["certifications", "experience"]:
            edu_block += "\n" + secs.get(sec, "")
        if not edu_block.strip():
            edu_block = text  # Last resort: full text

    best_rank = -1
    best_line = ""

    lines = [line.strip() for line in edu_block.splitlines() if line.strip()]

    for line in lines:
        low = line.lower()

        # 🚫 Skip suspicious lines
        if re.search(r"\b(seeking|aspiring|pursuing|mastering)\b", low):
            continue

        # ✅ Standard keyword map match
        for keyword, rank in _DEGREE_KEYWORDS.items():
            if " " in keyword:
                match = keyword in low
            else:
                match = re.search(rf"\b{re.escape(keyword)}\b", low)

            if match:
                if keyword in ["diploma", "intermediate", "matric", "high school", "higher school"]:
                    if not any(clue in low for clue in _CONTEXT_CLUES):
                        continue
                if rank > best_rank:
                    best_rank = rank
                    best_line = line.strip()

    # ✅ Smart fallback: common patterns if still no match
    degree_fallback_patterns = [
        (r"\b(ph\.?d\.?|doctor)\b", 4),
        (r"\b(master|ms\.?|m\.?sc\.?|mba|m\.?e\.?)\b", 3),
        (r"\b(bachelor|bs\.?|b\.?sc\.?|b\.?e\.?)\b", 2),
        (r"\b(diploma|polytechnic|associate degree)\b", 1),
        (r"\b(intermediate|matric|high school|hssc|ssc)\b", 0),
    ]

    for pat, rank in degree_fallback_patterns:
        if re.search(pat, low):
            if rank > best_rank:
                best_rank = rank
                best_line = line.strip()

    # SUPER fallback for "Bachelor in XYZ"
    if re.search(r"bachelor\s+.*(in|of)", low) and best_rank < 2:
        best_rank = 2
        best_line = line.strip()

    # ✅ Ultimate clue: mention of "university"
    if best_rank < 0 and "university" in text.lower():
        return "Bachelor (inferred) / No major degree found but mentions university"

    return best_line if best_rank >= 0 else ""


def map_to_standard_degree(edu_text):
    edu_text = edu_text.lower()
    best_rank = -1
    for key, rank in _DEGREE_KEYWORDS.items():
        if key in edu_text and rank > best_rank:
            best_rank = rank

    # Normalize into standard degree group
    if best_rank >= 4:
        return "phd"
    elif best_rank >= 3:
        return "master"
    elif best_rank >= 2:
        return "bachelor"
    elif best_rank >= 1:
        return "diploma"
    elif best_rank == 0:
        return "high school"
    else:
        return "none"

