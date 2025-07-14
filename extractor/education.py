from .section_segmenter import segment_sections
import re
from config import _DEGREE_KEYWORDS

_CONTEXT_CLUES = [
    "university", "college", "school","Higher" "institute", "academy",
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
    Returns the highest-ranked degree actually present in the Education section.
    Filters out 'seeking master', 'aspiring', 'mastering', etc.
    Picks the highest rank: Master > Bachelor > Diploma > Intermediate > Matric.
    """
    secs = segment_sections(text)
    edu_block = secs.get("education", "").strip()

    if not edu_block:
        # Fallback: scan certs/experience for stray degree lines
        for sec in ["certifications", "experience"]:
            edu_block += "\n" + secs.get(sec, "")
        if not edu_block.strip():
            edu_block = text

    best_rank = -1
    best_line = ""

    lines = [line.strip() for line in edu_block.splitlines() if line.strip()]

    for line in lines:
        low = line.lower()

        # 🚫 Ignore suspicious lines
        if re.search(r"\b(seeking|aspiring|pursuing|master-to-master|mastering)\b", low):
            continue

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


        # 🔍 Phrase fallback for common patterns
        if re.search(r"bachelor\s+of", low) and best_rank < 2:
            best_rank = 2
            best_line = line.strip()
        elif re.search(r"master\s+of", low) and best_rank < 3:
            best_rank = 3
            best_line = line.strip()
        elif re.search(r"diploma\s+in", low) and best_rank < 1:
            best_rank = 1
            best_line = line.strip()
         
            
    if best_rank < 0 and "university" in edu_block.lower():
        return "Bachelor / No major degree found but there is a university mention"
    
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

