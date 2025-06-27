import re
from dataclasses import dataclass
from typing import List

@dataclass
class ExtractedItem:
    problem_number: int
    problem_text: str  # This will hold the title, e.g., "생물의 특성"
    explanation_text: str # This will hold the content block

def analyze_text(text: str) -> List[ExtractedItem]:
    """
    Analyzes text to extract items based on a numbered title format.
    An item consists of a number, a title on the same line, and the
    content that follows until the next numbered title.
    """
    # Regex to find lines starting with a number, capturing the number and the rest of the line as the title.
    # e.g., "01 생물의 특성"
    problem_pattern = re.compile(r"^\s*(\d+)\s+(.+)", re.MULTILINE)
    
    extracted_items: List[ExtractedItem] = []
    matches = list(problem_pattern.finditer(text))

    for i, match in enumerate(matches):
        problem_number = int(match.group(1))
        title = match.group(2).strip()
        
        # The content starts right after the full match of the current problem marker
        content_start = match.end()
        # The content ends at the start of the next problem marker, or at the end of the text
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        
        content = text[content_start:content_end].strip()
        
        extracted_items.append(
            ExtractedItem(
                problem_number=problem_number,
                problem_text=title,
                explanation_text=content
            )
        )
        
    return extracted_items

if __name__ == '__main__':
    sample_text = """
    01 생물의 특성
    석회 동굴에서 발견되는 석순, 석주, 종유석은 탄산 칼슘 성분이
    쌓여 만들어진 지형이므로 생물이 아니다.
    ㄱ. 물질대사는 생물이 갖는 특성이므로 종유석이 만들어질 때는
    물질대사가 일어나지 않는다.

    02 다음은 어떤 물질에 대한 설명이다.
    이것은 세포의 주성분이며, 생명 활동에 필수적이다.
    """
    
    items = analyze_text(sample_text)
    for item in items:
        print(f"번호: {item.problem_number}")
        print(f"문제(제목): {item.problem_text}")
        print(f"해설(내용):\n{item.explanation_text}\n") 