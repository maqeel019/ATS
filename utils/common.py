# utils/common.py

def clean_text(text):
    return text.replace('\xa0', ' ').replace('\n', ' ').strip()
import re
import unicodedata

def clean_unicode(text):
    return unicodedata.normalize("NFKD", text)

def remove_non_ascii(text):
    return re.sub(r"[^\x00-\x7F]+", " ", text)

def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()

def clean_punctuation(text):
    return re.sub(r"[^\w\s]", " ", text)
def split_into_sentences(text):
    # Very basic sentence splitter
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 1]

def extract_bullets(text):
    return [line.strip("•- ").strip() for line in text.splitlines() if re.match(r"^\s*[-•]", line)]

def generate_ngrams(tokens, n=2):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def clean_resume_text(text):
    text = clean_unicode(text)
    text = remove_non_ascii(text)
    text = text.replace("–", "-").replace("—", "-").replace("\xa0", " ")
    text = re.sub(r"\.{2,}", ".", text)  # e.g., "...."
    text = normalize_whitespace(text)
    return text.strip()


def get_work_experience_text(sections, full_text):
    for key in sections:
        if "experience" in key.lower():
            return sections[key]
    return full_text

def update_links(info, embedded_links):
    if not info["linkedin"]:
        for link in embedded_links:
            if "linkedin.com" in link.lower():
                info["linkedin"] = link
                break
    if not info.get("github"):
        for link in embedded_links:
            if "github.com" in link.lower():
                info["github"] = link
                break
    return info
