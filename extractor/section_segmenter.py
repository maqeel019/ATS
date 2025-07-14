# extractor/section_segmenter.py
import re
from datetime import datetime


headers = {
    "professional summary": "summary",
    "summary": "summary",
    "technical experience": "experience",
    "work experience": "experience",
    "employment history": "experience",
    "professional experience": "experience",
    "experience": "experience",
    "work history": "experience",
    "industry experience": "experience",
    "qualifications": "education",
    "qualifications and training": "education",
    "academic qualifications": "education",
    "academic background": "education",
    "education": "education",
    "education and training": "education",
    "education and experience": "education",
    "skills": "skills",
    "projects": "projects",
    "certifications": "certifications",
}

REASSIGN_RULES = {
    "education": {
        "move_to": "experience",
        "keywords": [
            "developed", "designed", "built", "implemented", "managed",
            "frontend developer", "backend developer", "software engineer",
            "company", "pvt ltd", "intern"
        ],
        "date_pattern": r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s*\d{4}\b|\b\d{4}\b"
    },
"experience": {
    "move_to": "education",
    "keywords": ["cgpa", "gpa", "university", "degree", "bachelor", "master of", "masters", "master's"]

},

}


def preprocess_text(text):
    text = text.lower().replace('\xa0', ' ').replace('\r\n', '\n').replace('\r', '\n')
    return re.sub(r'\n+', '\n', text.strip())


def detect_section_starts(lines):
    section_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip(": ").lower()
        for section, variants in headers.items():
            if any(v in stripped for v in variants):
                section_starts.append((i, section))
                break
    return section_starts


def extract_sections_from_starts(lines, section_starts):
    sections = {}
    for i, (start_idx, section) in enumerate(section_starts):
        end_idx = section_starts[i + 1][0] if i + \
            1 < len(section_starts) else len(lines)
        content = "\n".join(lines[start_idx + 1:end_idx]).strip()
        if section not in sections:
            sections[section] = content
        else:
            sections[section] += "\n" + content
    return sections


def heuristic_segment_sections(text):
    text = preprocess_text(text)
    lines = text.split("\n")
    section_starts = detect_section_starts(lines)
    if not section_starts:
        return {}
    return extract_sections_from_starts(lines, section_starts)


def classify_line(line):
    """
    Classify a single line into one of:
    'contact', 'portfolio', 'experience', 'education', 'skills', 'projects', 'certifications'
    based on entity patterns, keywords, and verbs.
    """
    line_lower = line.lower().strip()

    # 1) Direct entity checks
    if "@" in line:
        return "contact"
    if re.search(r"\+?[\d\-\s()]{7,}\d", line):
        return "contact"
    if re.search(r"linkedin\.com", line):
        return "contact"
    if re.search(r"github\.com|vercel\.app|\.netlify\.app|\.portfolio", line):
        return "portfolio"
    if re.search(r"https?://", line) and "linkedin.com" not in line:
        return "portfolio"

    # 2) Verb/action checks → likely project or experience
    verbs = ["developed", "built", "designed", "implemented",
        "created", "led", "managed", "deployed"]
    if any(v in line_lower for v in verbs):
        return "experience"

    # 3) Title & date check → Front-end Developer near date
    if "developer" in line_lower or "engineer" in line_lower:
        if re.search(r"\b\d{4}\b", line):
            return "experience"

    # 4) Keywords fallback (keep your old logic)
    scores = {sec: 0 for sec in headers}
    for section, keywords in headers.items():
        if isinstance(keywords, str):
            keywords = [keywords]
        for kw in keywords:
            if kw in line_lower:
                scores[section] += 1

    best_section = max(scores, key=scores.get)
    return best_section if scores[best_section] > 0 else None


def classify_lines_by_section(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    section_map = {}

    for line in lines:
        label = classify_line(line)
        if label:
            section_map.setdefault(label, []).append(line)
        else:
            section_map.setdefault("unknown", []).append(line)

    return section_map


def combined_segment_sections(text):
    heuristic = heuristic_segment_sections(text)
    if not heuristic.get("experience"):
        classified = classify_lines_by_section(text)
        for section, lines in classified.items():
            if section not in heuristic or not heuristic[section]:
                heuristic[section] = "\n".join(lines)
    return heuristic


def reassign_misplaced_lines(sections):
    updated_sections = {k: [] for k in sections}

    # Convert content into line lists
    for sec, content in list(sections.items()):
        lines = []
        for chunk in content.splitlines():
            for sub in re.split(r'[•\-–—;]', chunk):
                lines.append(sub.strip())

        for line in lines:
            line_lower = line.lower()
            moved = False
            # Apply section-specific rules
            if sec in REASSIGN_RULES:
                rule = REASSIGN_RULES[sec]
                for kw in rule["keywords"]:
                    if kw in line_lower:
                        updated_sections.setdefault(
                            rule["move_to"], []).append(line)
                        moved = True
                        break

            if not moved:
                updated_sections[sec].append(line)

    # Join back lines into text
    return {k: "\n".join(v).strip() for k, v in updated_sections.items() if v}

<<<<<<< HEAD

=======
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
def segment_sections(text: str) -> dict:
    sections = {}
    current_section = None
    buffer = []

    def flush_buffer():
        nonlocal buffer, current_section
        if current_section and buffer:
            content = "\n".join(buffer).strip()
            if current_section not in sections or len(sections[current_section]) < len(content):
                sections[current_section] = content
            buffer = []

    lines = text.splitlines()

    for line in lines:
        stripped = line.strip().lower().rstrip(":")
        match_found = None
        for h in headers:
            if re.fullmatch(h, stripped) or stripped.startswith(h):
                match_found = headers[h]
                break

        if match_found:
            flush_buffer()
            current_section = match_found
            continue

        if current_section:
            buffer.append(line)

    flush_buffer()

<<<<<<< HEAD
=======
    # Fallback: detect experience chunk if missing
    if "experience" not in sections:
        clean_text = text.lower().replace("\n", " ")
        tokens = clean_text.split()
        chunks = [" ".join(tokens[i:i + 200]) for i in range(0, len(tokens), 100)]

        date_pattern = re.compile(
            r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s*\d{4}\b"
            r"|\b\d{1,2}/\d{4}\b"
            r"|\b\d{4}\b"
        )
        job_keywords = [
            "developer", "engineer", "intern", "manager", "consultant", "company",
            "experience", "worked", "employer", "responsibilities", "job", "role",
            "joined", "organization", "team", "senior", "junior", "supervisor", "project"
        ]

        fallback = ""
        for chunk in chunks:
            if len(date_pattern.findall(chunk)) >= 1 and any(kw in chunk for kw in job_keywords):
                fallback += chunk + "\n"
            if len(fallback) > 1500:
                break

        if fallback:
            sections["experience"] = fallback.strip()

    updated_sections = {k: [] for k in sections}
    updated_sections.setdefault("contact", [])
    updated_sections.setdefault("portfolio", [])
    updated_sections.setdefault("unknown", [])

    for sec, content in list(sections.items()):
        sec_lines = content.splitlines()
        for i, line in enumerate(sec_lines):
            moved = False
            line_lower = line.lower().strip()

            if any(x in line_lower for x in ["@", "+92", "linkedin.com/", "github.com/", "vercel.app"]):
                if "@" in line_lower or "+92" in line_lower or "linkedin.com" in line_lower:
                    updated_sections.setdefault("contact", []).append(line.strip())
                    moved = True
                elif "github.com" in line_lower or "vercel.app" in line_lower:
                    updated_sections.setdefault("portfolio", []).append(line.strip())
                    moved = True

            elif any(job in line_lower for job in [
                "front-end developer", "frontend developer", "backend developer",
                "software engineer", "developer", "intern", "manager"
            ]):
                updated_sections.setdefault("experience", []).append(line.strip())
                moved = True

            elif any(verb in line_lower for verb in ["developed", "built", "implemented", "designed", "worked"]):
                updated_sections.setdefault("experience", []).append(line.strip())
                moved = True

            elif sec in REASSIGN_RULES:
                rule = REASSIGN_RULES[sec]
                keyword_hit = any(kw in line_lower for kw in rule["keywords"])
                date_hit = bool(re.search(rule.get("date_pattern", ""), line_lower))
                prev_line = sec_lines[i - 1].lower() if i > 0 else ""
                next_line = sec_lines[i + 1].lower() if i + 1 < len(sec_lines) else ""
                window_hit = any(kw in prev_line or kw in next_line for kw in ["pvt ltd", "company", "inc", "llc"]) or \
                             bool(re.search(rule.get("date_pattern", ""), prev_line + " " + next_line))
                if keyword_hit and (date_hit or window_hit):
                    updated_sections.setdefault(rule["move_to"], []).append(line.strip())
                    moved = True

            if not moved:
                updated_sections[sec].append(line.strip())

    # Remove duplicate education date lines from experience
    edu_dates = []
    if "education" in updated_sections:
        for line in updated_sections["education"]:
            if re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s*\d{4}\b"
                         r"|\b\d{1,2}/\d{4}\b"
                         r"|\b\d{4}\b", line, re.IGNORECASE):
                edu_dates.append(line.strip())

    if "experience" in updated_sections:
        filtered_exp = []
        for line in updated_sections["experience"]:
            if line.strip() not in edu_dates:
                filtered_exp.append(line)
        updated_sections["experience"] = filtered_exp

    # Context window for stray education lines
    if "experience" in updated_sections:
        exp_lines = updated_sections["experience"]
        keep_exp = []
        moved_idx = set()
        edu_keywords = ["school", "college", "university", "degree", "intermediate", "matriculation"]

        for i, line in enumerate(exp_lines):
            if re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s*\d{4}\b"
                         r"|\b\d{1,2}/\d{4}\b"
                         r"|\b\d{4}\b", line, re.IGNORECASE):
                prev_line = exp_lines[i - 1].lower() if i > 0 else ""
                next_line = exp_lines[i + 1].lower() if i + 1 < len(exp_lines) else ""
                if any(kw in prev_line for kw in edu_keywords):
                    updated_sections.setdefault("education", []).append(exp_lines[i - 1].strip())
                    updated_sections.setdefault("education", []).append(line.strip())
                    moved_idx.add(i)
                    moved_idx.add(i - 1)
                elif any(kw in next_line for kw in edu_keywords):
                    updated_sections.setdefault("education", []).append(line.strip())
                    updated_sections.setdefault("education", []).append(exp_lines[i + 1].strip())
                    moved_idx.add(i)
                    moved_idx.add(i + 1)

        for j, line in enumerate(exp_lines):
            if j not in moved_idx:
                keep_exp.append(line)
        updated_sections["experience"] = keep_exp

    degree_pattern = re.compile(
        r"\b("
        r"(bachelor|master)\s+(of|in)\s+[a-z][a-z\s&/().\-]+"
        r"|b\.?\s?s\.?c?\.?\s+[a-z][a-z\s&/().\-]+"
        r"|m\.?\s?s\.?c?\.?\s+[a-z][a-z\s&/().\-]+"
        r")\b",
        re.IGNORECASE
    )

    updated_sections.setdefault("education", [])

    for sec, sec_lines in updated_sections.items():
        if sec == "education":
            continue
        keep = []
        for line in sec_lines:
            if degree_pattern.search(line):
                updated_sections["education"].append(line)
            else:
                keep.append(line)
        updated_sections[sec] = keep

    # ✅ Sweep for truly stray lines → unknown
    placed = {l.strip() for sec_lines in updated_sections.values() for l in sec_lines}

    for line in lines:
        line_clean = line.strip()
        if line_clean and line_clean not in placed:
            if len(line_clean) > 3:
                updated_sections["unknown"].append(line_clean)

    updated_sections["unknown"] = list(dict.fromkeys(updated_sections["unknown"]))

    final_sections = {}
    for sec, sec_lines in updated_sections.items():
        joined = "\n".join(sec_lines).strip()
        if len(joined) >= 10:
            final_sections[sec] = joined

    return final_sections

    sections = {}
    current_section = None
    buffer = []

    def flush_buffer():
        nonlocal buffer, current_section
        if current_section and buffer:
            content = "\n".join(buffer).strip()
            if current_section not in sections or len(sections[current_section]) < len(content):
                sections[current_section] = content
            buffer = []

    lines = text.splitlines()

    for line in lines:
        stripped = line.strip().lower().rstrip(":")
        match_found = None
        for h in headers:
            if re.fullmatch(h, stripped) or stripped.startswith(h):
                match_found = headers[h]
                break

        if match_found:
            flush_buffer()
            current_section = match_found
            continue

        if current_section:
            buffer.append(line)

    flush_buffer()

>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
    # Fallback: try to detect experience chunk by dates & job words
    if "experience" not in sections:
        clean_text = text.lower().replace("\n", " ")
        tokens = clean_text.split()
        chunks = [" ".join(tokens[i:i + 200])
                           for i in range(0, len(tokens), 100)]

        date_pattern = re.compile(
            r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s*\d{4}\b"
            r"|\b\d{1,2}/\d{4}\b"
            r"|\b\d{4}\b"
        )
        job_keywords = [
            "developer", "engineer", "intern", "manager", "consultant", "company",
            "experience", "worked", "employer", "responsibilities", "job", "role",
            "joined", "organization", "team", "senior", "junior", "supervisor", "project"
        ]

        fallback = ""
        for chunk in chunks:
            if len(date_pattern.findall(chunk)) >= 1 and any(kw in chunk for kw in job_keywords):
                fallback += chunk + "\n"
            if len(fallback) > 1500:
                break

        if fallback:
            sections["experience"] = fallback.strip()

    updated_sections = {k: [] for k in sections}

    for sec, content in list(sections.items()):
        lines = content.splitlines()
        for i, line in enumerate(lines):
            moved = False
            line_lower = line.lower().strip()

            # === 1) Move obvious contact & links out ===
            if any(x in line_lower for x in ["@", "+92", "linkedin.com/", "github.com/", "vercel.app"]):
                if "@" in line_lower or "+92" in line_lower or "linkedin.com" in line_lower:
                    updated_sections.setdefault("contact", []).append(line.strip())
                    moved = True
                elif "github.com" in line_lower or "vercel.app" in line_lower:
                    updated_sections.setdefault("portfolio", []).append(line.strip())
                    moved = True

            # === 2) Job title direct match → always to experience ===
            elif any(job in line_lower for job in ["front-end developer", "frontend developer", "backend developer",
                                                   "software engineer", "developer", "intern", "manager"]):
                updated_sections.setdefault("experience", []).append(line.strip())
                moved = True

            # === 3) Job verb line → push to experience ===
            elif any(verb in line_lower for verb in ["developed", "built", "implemented", "designed", "worked"]):
                updated_sections.setdefault("experience", []).append(line.strip())
                moved = True

            # === 4) Context window for tricky stuff ===
            elif sec in REASSIGN_RULES:
                rule = REASSIGN_RULES[sec]
                keyword_hit = any(kw in line_lower for kw in rule["keywords"])
                date_hit = bool(re.search(rule.get("date_pattern", ""), line_lower))
                prev_line = lines[i - 1].lower() if i > 0 else ""
                next_line = lines[i + 1].lower() if i + 1 < len(lines) else ""
                window_hit = any(kw in prev_line or kw in next_line for kw in ["pvt ltd", "company", "inc", "llc"]) or \
                             bool(re.search(rule.get("date_pattern", ""), prev_line + " " + next_line))
                if keyword_hit and (date_hit or window_hit):
                    updated_sections.setdefault(rule["move_to"], []).append(line.strip())
                    moved = True

            # === 5) Degree phrase match → force to education ===
            # else:
            #     degree_pattern = re.compile(
            #         r"\b("
            #         r"(bachelor|master)\s+(of|in)\s+[a-z][a-z\s&/().-]+"
            #         r"|bs\s+[a-z][a-z\s&/().-]+"
            #         r"|ms\s+[a-z][a-z\s&/().-]+"
            #         r")\b",
            #         re.IGNORECASE
            #     )

            #     matched = False

            #     # Direct whole-line scan
            #     if degree_pattern.search(line):
            #         updated_sections.setdefault("education", []).append(line.strip())
            #         moved = True
            #         matched = True

            #     # If not, split line by common punctuations and scan chunks
            #     if not matched and len(line) > 30:
            #         parts = re.split(r"[.,;|•\-\n]", line)
            #         for part in parts:
            #             if degree_pattern.search(part):
            #                 updated_sections.setdefault("education", []).append(part.strip())
            #                 moved = True
            #                 matched = True
            #                 break

            #     # If still not, scan word pairs: force detect phrases like "Bachelor of" + next words
            #     if not matched:
            #         words = line.lower().split()
            #         for i in range(len(words) - 2):
            #             w1, w2, w3 = words[i:i+3]
            #             triple = f"{w1} {w2} {w3}"
            #             if re.match(r"(bachelor|master)\s+(of|in)\s+.*", triple):
            #                 updated_sections.setdefault("education", []).append(line.strip())
            #                 moved = True
            #                 matched = True
            #                 break
            #             elif re.match(r"(bs|ms)\s+.*", triple):
            #                 updated_sections.setdefault("education", []).append(line.strip())
            #                 moved = True
            #                 matched = True
            #                 break


            if not moved:
                updated_sections[sec].append(line.strip())

    # ✅ 1) Remove duplicate date lines from experience if they appear in education
    edu_dates = []
    if "education" in updated_sections:
        for line in updated_sections["education"]:
            if re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s*\d{4}\b"
                         r"|\b\d{1,2}/\d{4}\b"
                         r"|\b\d{4}\b", line, re.IGNORECASE):
                edu_dates.append(line.strip())

    if "experience" in updated_sections:
        filtered_exp = []
        for line in updated_sections["experience"]:
            if line.strip() not in edu_dates:
                filtered_exp.append(line)
        updated_sections["experience"] = filtered_exp

    # ✅ 2) Extra: context window — if date line has nearby edu hint → push both lines to education
    if "experience" in updated_sections:
        exp_lines = updated_sections["experience"]
        keep_exp = []
        moved_idx = set()
        edu_keywords = ["school", "college", "university", "degree", "intermediate", "matriculation"]

        for i, line in enumerate(exp_lines):
            if re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s*\d{4}\b"
                         r"|\b\d{1,2}/\d{4}\b"
                         r"|\b\d{4}\b", line, re.IGNORECASE):
                prev_line = exp_lines[i - 1].lower() if i > 0 else ""
                next_line = exp_lines[i + 1].lower() if i + 1 < len(exp_lines) else ""
                if any(kw in prev_line for kw in edu_keywords):
                    updated_sections.setdefault("education", []).append(exp_lines[i - 1].strip())
                    updated_sections.setdefault("education", []).append(line.strip())
                    moved_idx.add(i)
                    moved_idx.add(i - 1)
                elif any(kw in next_line for kw in edu_keywords):
                    updated_sections.setdefault("education", []).append(line.strip())
                    updated_sections.setdefault("education", []).append(exp_lines[i + 1].strip())
                    moved_idx.add(i)
                    moved_idx.add(i + 1)

        for j, line in enumerate(exp_lines):
            if j not in moved_idx:
                keep_exp.append(line)
        updated_sections["experience"] = keep_exp
        # --------------------------------------
        # EXTRA: scan all sections for stray degree lines

    degree_pattern = re.compile(
    r"\b("
    r"(bachelor|master)\s+(of|in)\s+[a-z][a-z\s&/().\-]+"
    r"|b\.?\s?s\.?c?\.?\s+[a-z][a-z\s&/().\-]+"
    r"|m\.?\s?s\.?c?\.?\s+[a-z][a-z\s&/().\-]+"
    r")\b",
    re.IGNORECASE
                                )

    updated_sections.setdefault("education", [])

    for sec, lines in updated_sections.items():
        if sec == "education":
            continue
        keep = []
        for line in lines:
            if degree_pattern.search(line):
                updated_sections["education"].append(line)
            else:
                keep.append(line)
        updated_sections[sec] = keep


    # Final cleanup
    final_sections = {}
    for sec, lines in updated_sections.items():
        joined = "\n".join(lines).strip()
        if len(joined) >= 10:
            final_sections[sec] = joined

<<<<<<< HEAD
    return final_sections
=======
    return final_sections
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
