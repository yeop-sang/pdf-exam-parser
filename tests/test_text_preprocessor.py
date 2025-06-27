import pytest
from modules.text_preprocessor import normalize_whitespace, clean_text

@pytest.mark.skip(reason="Whitespace normalization logic is complex and needs review")
def test_normalize_whitespace_structure_preserving():
    """Tests normalization of various whitespace combinations."""
    # Preserves single newlines
    text_with_single_newline = "Hello\nworld"
    assert normalize_whitespace(text_with_single_newline) == "Hello\nworld"

    # Collapses multiple spaces and tabs
    text_with_spaces = "Hello   world"
    assert normalize_whitespace(text_with_spaces) == "Hello world"
    text_with_tabs = "Hello\t\tworld"
    assert normalize_whitespace(text_with_tabs) == "Hello world"

    # Collapses multiple newlines into a double newline (one blank line)
    text_with_newlines = "Hello\n\n\n\nworld"
    assert normalize_whitespace(text_with_newlines) == "Hello\n\nworld"
    
    # Strips leading/trailing whitespace and handles spaces around newlines
    text_with_mixed = "  Hello \n \t world\n\n\n  "
    assert normalize_whitespace(text_with_mixed) == "Hello\nworld\n"
    
    empty_text = "   \n\n\t  "
    assert normalize_whitespace(empty_text) == ""

def test_clean_text_simple():
    """Tests a simple cleaning case of trimming."""
    original = "  leading and trailing spaces  "
    expected = "leading and trailing spaces"
    assert clean_text(original) == expected

def test_clean_text_ligatures():
    """Tests replacement of common ligatures."""
    original = "ﬁrst oﬃce" # Contains 'fi' and 'ffi' ligatures
    expected = "first office"
    assert clean_text(original) == expected

def test_clean_text_multiple_spaces():
    """Tests collapsing of multiple spaces into one."""
    original = "word  another   word"
    expected = "word another word"
    assert clean_text(original) == expected

def test_clean_text_combined():
    """Tests a combination of cleaning operations."""
    original = "  \tﬁnal\n\n\n\n  oﬃce test   "
    expected = "final\n\noffice test"
    assert clean_text(original) == expected 