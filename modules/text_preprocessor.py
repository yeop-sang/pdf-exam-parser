import re

def normalize_whitespace(text: str) -> str:
    """
    Normalizes whitespace in a string by processing it line by line.
    - Strips leading/trailing whitespace from the entire text.
    - Replaces multiple horizontal whitespace characters (space, tab) with a single space.
    - Collapses multiple consecutive blank lines into a single blank line.
    """
    # Split the text into lines, process each line, and filter out empty lines
    # that result from stripping whitespace-only lines.
    lines = (re.sub(r'[ \t]+', ' ', line).strip() for line in text.strip().split('\n'))

    # Reconstruct the text, ensuring that multiple blank lines are collapsed
    normalized_lines = []
    last_line_was_blank = False
    for line in lines:
        if line:
            normalized_lines.append(line)
            last_line_was_blank = False
        elif not last_line_was_blank:
            normalized_lines.append("") # Add a single blank line
            last_line_was_blank = True
            
    # Join the lines back, and handle the case where the text might end with newlines
    result = '\n'.join(normalized_lines)
    if text.endswith('\n\n'):
        # If the original text ended with a double newline, preserve one blank line
        if not result.endswith('\n\n'):
             result += '\n'
    return result

def clean_text(text: str) -> str:
    """
    Performs a series of cleaning operations on a string.
    - Replaces common ligatures.
    - Normalizes whitespace in a structure-preserving way.
    """
    # Ligature replacements
    ligatures = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
    }
    for lig, ascii_equiv in ligatures.items():
        text = text.replace(lig, ascii_equiv)
        
    # Normalize whitespace
    text = normalize_whitespace(text)
    
    return text 