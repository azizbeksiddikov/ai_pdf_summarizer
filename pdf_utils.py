import pdfplumber
import re

DEFAULT_NEXT_SECTIONS = ["Introduction", "Methods", "Results", "Discussion", "Conclusion", "References"]

# Add variants for sections, as needed.
# For example, "Methods" can appear as "Methodology" or "Materials and Methods".
# Similarly, you can add variants for Abstract, Results, etc.
SECTION_VARIANTS = {
    "Abstract": ["Abstract", "Summary", "Executive Summary"],
    "Methods": ["Methods", "Methodology", "Materials and Methods", "Research Methods", "Methodology"],
    "Results": ["Results", "Findings", "Observations", "Outcomes"]
}

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber and return the concatenated text.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def find_section(text: str, section_name: str, next_sections=None) -> str:
    """
    Extracts a given section by looking for any of the known variants for that section 
    and returns text until the next known section is encountered.

    For example, if section_name = "Methods", 
    it will look for "Methods", "Methodology", "Materials and Methods", etc.
    """
    if next_sections is None:
        next_sections = DEFAULT_NEXT_SECTIONS

    # Get the variants for the target section (if any). If none defined, just use the original name.
    variants = SECTION_VARIANTS.get(section_name, [section_name])

    # Build a regex pattern that matches any of the variants as a heading
    # For example, if variants = ["Methods", "Methodology"], the pattern will be:
    # ^(Methods|Methodology)\b
    # (case-insensitive, multiline, DOTALL)
    variants_pattern = "|".join([re.escape(v) for v in variants])
    section_pattern = rf"(?i)^(?:{variants_pattern})\b.*?(?=^({'|'.join(next_sections)})\b|\Z)"

    match = re.search(section_pattern, text, flags=re.MULTILINE | re.DOTALL)
    if match:
        return match.group(0).strip()
    else:
        # Fallback: If no direct multiline section match, try to find any variant line and extract from there
        fallback_variants_pattern = rf"(?i)^(?:{variants_pattern})\b"
        fallback_match = re.search(fallback_variants_pattern, text, flags=re.MULTILINE)
        if fallback_match:
            start_idx = fallback_match.start()
            subsequent_text = text[start_idx:]
            next_sections_pattern = rf"(?i)^(?:{'|'.join(next_sections)})\b"
            subsequent_match = re.search(next_sections_pattern, subsequent_text, flags=re.MULTILINE)
            if subsequent_match:
                end_idx = subsequent_match.start()
                return subsequent_text[:end_idx].strip()
            else:
                return subsequent_text.strip()
    return ""
