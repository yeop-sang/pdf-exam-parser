import pytest
from modules.text_analyzer import analyze_text

@pytest.fixture
def realistic_data():
    """Uses realistic data provided by the user."""
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
02 세균과 바이러스
세균은 스스로 물질대사를 하지만, 바이러스는 독립적으로 물질
대사를 하지 못한다.
ㄱ. 바이러스(X)는 단백질 껍질을 갖는다.
ㄴ. 바이러스(X)는 독립적으로 물질대사를 하지 못하고, 숙주 세
포 내에서만 물질대사를 통해 증식이 가능하다.
ㄷ
.
세균과 바이러스는 모두 유전 물질인 핵산을 가지고 있으므
로, '돌연변이가 일어날 수 있다.'는 세균(A)과 바이러스(X)가 모
두 갖는 특징이다.
03 귀납적 탐구 방법
귀납적 탐구 방법은 자연 현상을 관찰하여 얻은 자료를 종합하고
분석하여 규칙성을 발견하고, 이로부터 일반적인 원리나 법칙을
이끌어내는 탐구 방법이다.
"""

def test_analyze_text_realistic_single_page(realistic_data):
    """
    Tests analysis with realistic data format on a single page.
    """
    text_iterator = iter([realistic_data])
    result = list(analyze_text(text_iterator))

    assert len(result) == 3

    # Check problem 1
    assert result[0]['number'] == '01'
    assert result[0]['problem'] == '생물의 특성'
    assert '석회 동굴에서' in result[0]['explanation']
    assert '생장에 해당하지 않는다.' in result[0]['explanation'].replace('\n', '')
    assert '02 세균과 바이러스' not in result[0]['explanation']

    # Check problem 2
    assert result[1]['number'] == '02'
    assert result[1]['problem'] == '세균과 바이러스'
    assert '독립적으로 물질' in result[1]['explanation']
    assert '모두 갖는 특징이다.' in result[1]['explanation'].replace('\n', '')
    assert '03 귀납적 탐구 방법' not in result[1]['explanation']
    
    # Check problem 3 (last one)
    assert result[2]['number'] == '03'
    assert result[2]['problem'] == '귀납적 탐구 방법'
    assert '이끌어내는 탐구 방법이다.' in result[2]['explanation'].replace('\n', '')


def test_analyze_text_realistic_multi_page(realistic_data):
    """
    Tests analysis with realistic data format split across multiple pages.
    """
    # Split the data in the middle of problem 02's explanation
    split_point = realistic_data.find("ㄴ. 바이러스(X)는 독립적으로")
    page1 = realistic_data[:split_point]
    page2 = realistic_data[split_point:]
    
    text_iterator = iter([page1, page2])
    result = list(analyze_text(text_iterator))

    # The result should be identical to the single page test
    assert len(result) == 3

    # Check problem 2, which was split across the page boundary
    assert result[1]['number'] == '02'
    assert result[1]['problem'] == '세균과 바이러스'
    assert '독립적으로 물질' in result[1]['explanation'] # From page 1 part
    assert '모두 갖는 특징이다.' in result[1]['explanation'].replace('\n', '') # From page 2 part
    assert '03 귀납적 탐구 방법' not in result[1]['explanation']


def test_analyze_text_no_items():
    """
    Tests that an empty list is returned when no items are found.
    """
    text = "This is just some random text without any numbered problems."
    text_iterator = iter([text])
    result = list(analyze_text(text_iterator))
    assert len(result) == 0

def test_analyze_text_empty_input():
    """Tests the function with empty pages."""
    text_iterator = iter(["", "   ", "\n"])
    items = list(analyze_text(text_iterator))
    assert len(items) == 0 