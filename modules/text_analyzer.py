import re
from typing import Dict, Iterator

# Pre-compile regex for efficiency.
# This pattern finds a line starting with a number and captures everything
# until the next line that starts with a number. It's used for streaming.
# The lookahead `(?=\n\d+\s)` is key. We don't include `|\Z` here because
# in a streaming context, `\Z` (end of string) is premature.
STREAM_PATTERN = re.compile(
    r'^(?P<number>\d+)\s+(?P<problem>.*?)\n(?P<explanation>.*?)(?=\n\d+\s)', 
    re.MULTILINE | re.DOTALL
)

# This pattern is for the final part of the text, which might not be 
# followed by another problem number. It's used on the remainder buffer.
FINAL_PATTERN = re.compile(
    r'^(?P<number>\d+)\s+(?P<problem>.*?)\n(?P<explanation>.*?)(?=\n\d+\s|\Z)', 
    re.MULTILINE | re.DOTALL
)


def analyze_text(text_iterator: Iterator[str]) -> Iterator[Dict[str, str]]:
    """
    Analyzes a stream of text page by page to extract problems and their explanations.
    An item consists of a number, a title on the same line, and the
    content that follows until the next numbered title.
    Handles items that may span across page breaks in a memory-efficient way.

    Args:
        text_iterator: An iterator that yields text for each page.

    Yields:
        A dictionary for each found item, containing 'number', 'problem', and 'explanation'.
    """
    buffer = ""
    for page_text in text_iterator:
        buffer += page_text
        
        last_match_end = 0
        # Find all problems in the buffer that are guaranteed to be complete
        # because they are followed by another problem number.
        for match in STREAM_PATTERN.finditer(buffer):
            data = match.groupdict()
            yield {
                "number": data['number'].strip(),
                "problem": data['problem'].strip(),
                "explanation": data['explanation'].strip()
            }
            last_match_end = match.end()

        # Trim the buffer, keeping only the part that hasn't been processed.
        # This part might contain an incomplete problem.
        if last_match_end > 0:
            buffer = buffer[last_match_end:]

    # After processing all pages, parse the remaining buffer.
    # This will catch the very last item in the document.
    if buffer:
        for match in FINAL_PATTERN.finditer(buffer):
            data = match.groupdict()
            yield {
                "number": data['number'].strip(),
                "problem": data['problem'].strip(),
                "explanation": data['explanation'].strip()
            }

if __name__ == '__main__':
    sample_text = """
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
    
    items = analyze_text(iter([sample_text]))
    print(f"Found {len(list(items))} items.") # Re-listing consumes the iterator, so we need to be careful
    
    # To print items, we need to re-create the iterator
    items_to_print = analyze_text(iter([sample_text]))
    for item in items_to_print:
        print("--- ITEM ---")
        print(f"번호: {item['number']}")
        print(f"문제(제목): {item['problem']}")
        print(f"해설(내용):\n{item['explanation']}\n") 