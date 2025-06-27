import pytest
from modules.text_analyzer import analyze_text, ExtractedItem

@pytest.fixture
def realistic_sample_text():
    return """
    01 생물의 특성
    석회 동굴에서 발견되는 석순, 석주, 종유석은 탄산 칼슘 성분이
    쌓여 만들어진 지형이므로 생물이 아니다.
    ㄱ. 물질대사는 생물이 갖는 특성이므로 종유석이 만들어질 때는
    물질대사가 일어나지 않는다.
    ㄴ. 식물은 빛에너지를 이용한 광합성을 통해 필요한 양분을 만든
    다. 따라서 '광합성을 통해 양분을 합성한다.'는 튤립이 갖는 특징
    이다.
    ㄷ. 튤립의 싹이 자라는 것은 생물의 특성인 생장에 해당하지만,
    석순이 자라는 것은 생장에 해당하지 않는다.

    02 다음은 어떤 물질에 대한 설명이다.
    이것은 세포의 주성분이며, 생명 활동에 필수적이다.
    비열이 커서 체온 유지에 유리하다.
    """

def test_analyze_text_with_realistic_format(realistic_sample_text):
    """Tests analysis with the new, realistic format provided by the user."""
    items = analyze_text(realistic_sample_text)
    
    assert len(items) == 2

    # Check item 1
    assert items[0].problem_number == 1
    assert items[0].problem_text == "생물의 특성"
    assert "석회 동굴에서" in items[0].explanation_text
    assert "석순이 자라는 것은 생장에 해당하지 않는다." in items[0].explanation_text
    assert "02 다음은" not in items[0].explanation_text

    # Check item 2
    assert items[1].problem_number == 2
    assert items[1].problem_text == "다음은 어떤 물질에 대한 설명이다."
    assert "이것은 세포의 주성분이며" in items[1].explanation_text
    assert "체온 유지에 유리하다." in items[1].explanation_text

def test_analyze_text_empty_input():
    """Tests the function with an empty string."""
    items = analyze_text("")
    assert len(items) == 0

def test_analyze_text_no_matches():
    """Tests text that does not contain any matching problem formats."""
    text = "This text has no numbered items at the start of its lines."
    items = analyze_text(text)
    assert len(items) == 0

def test_analyze_text_single_item():
    """Tests parsing of a text with only one item."""
    text = "99 마지막 문제\n이것이 내용의 전부입니다."
    items = analyze_text(text)
    assert len(items) == 1
    assert items[0].problem_number == 99
    assert items[0].problem_text == "마지막 문제"
    assert items[0].explanation_text == "이것이 내용의 전부입니다." 